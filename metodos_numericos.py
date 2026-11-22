"""Algoritmos del modulo de metodos numericos de la calculadora."""

import ast
import math
import operator
from decimal import Decimal, localcontext

import numpy as np


def compilar_funcion_simbolica(expresion):
    """Valida una expresión y devuelve f, f′ simbólicas y sus evaluadores NumPy."""
    import sympy as sp

    simbolo = sp.Symbol("x", real=True)
    nombres_permitidos = {"x", "pi", "e", "E", "sin", "cos", "tan", "asin", "acos",
                          "atan", "exp", "log", "sqrt", "abs", "Abs"}
    funciones = {nombre: getattr(sp, nombre) for nombre in nombres_permitidos
                 if nombre not in {"x", "pi", "e", "E", "abs", "Abs"}}
    funciones.update({"x": simbolo, "pi": sp.pi, "e": sp.E, "E": sp.E,
                      "abs": sp.Abs, "Abs": sp.Abs})

    try:
        arbol = ast.parse(str(expresion), mode="eval")
    except (SyntaxError, ValueError) as exc:
        raise ValueError("La función tiene una sintaxis incorrecta.") from exc

    def validar(nodo):
        if isinstance(nodo, ast.Expression):
            validar(nodo.body)
        elif isinstance(nodo, ast.Constant) and isinstance(nodo.value, (int, float)):
            return
        elif isinstance(nodo, ast.Name) and nodo.id in nombres_permitidos:
            return
        elif isinstance(nodo, ast.BinOp) and type(nodo.op) in _BINARIOS:
            validar(nodo.left)
            validar(nodo.right)
        elif isinstance(nodo, ast.UnaryOp) and type(nodo.op) in _UNARIOS:
            validar(nodo.operand)
        elif (isinstance(nodo, ast.Call) and isinstance(nodo.func, ast.Name)
              and nodo.func.id in funciones and len(nodo.args) == 1 and not nodo.keywords):
            validar(nodo.args[0])
        else:
            raise ValueError("Use x, constantes y funciones matemáticas permitidas con operaciones básicas.")

    validar(arbol)
    try:
        funcion_simbolica = sp.sympify(str(expresion), locals=funciones, evaluate=True)
        if funcion_simbolica.free_symbols - {simbolo}:
            raise ValueError("La función solo puede depender de x.")
        derivada_simbolica = sp.diff(funcion_simbolica, simbolo)
        evaluar_f = sp.lambdify(simbolo, funcion_simbolica, modules=["numpy"])
        evaluar_df = sp.lambdify(simbolo, derivada_simbolica, modules=["numpy"])
    except (sp.SympifyError, TypeError, ValueError, SyntaxError) as exc:
        if isinstance(exc, ValueError):
            raise
        raise ValueError("No se pudo interpretar o derivar la función ingresada.") from exc

    return simbolo, funcion_simbolica, derivada_simbolica, evaluar_f, evaluar_df


def resolver_newton_raphson(expresion, x0, tolerancia, max_iteraciones,
                            tolerancia_residuo=1e-8, umbral_derivada=1e-12):
    """Resuelve f(x)=0 con derivada simbólica y devuelve tabla y diagnóstico."""
    import pandas as pd

    _, funcion_simbolica, derivada_simbolica, evaluar_f, evaluar_df = compilar_funcion_simbolica(expresion)
    tol, tol_residuo = float(tolerancia), float(tolerancia_residuo)
    umbral = float(umbral_derivada)
    try:
        x_actual, max_num = float(x0), float(max_iteraciones)
    except (TypeError, ValueError) as exc:
        raise ValueError("Revise el valor inicial y el máximo de iteraciones.") from exc
    if not all(map(math.isfinite, (x_actual, tol, tol_residuo, max_num, umbral))):
        raise ValueError("Todos los datos deben ser finitos.")
    if tol <= 0 or tol_residuo <= 0 or umbral < 0:
        raise ValueError("Las tolerancias deben ser positivas y el umbral de derivada no negativo.")
    if isinstance(max_iteraciones, bool) or not max_num.is_integer() or max_num < 1:
        raise ValueError("El máximo de iteraciones debe ser un entero mayor o igual que 1.")
    max_iteraciones = int(max_num)

    def evaluar(evaluador, punto):
        with np.errstate(all="ignore"):
            return float(np.asarray(evaluador(punto)))

    filas, aproximaciones = [], [x_actual]
    estado, motivo = "Se alcanzó el máximo de iteraciones.", "maximo_iteraciones"
    convergio, error_final = False, None
    try:
        f_actual = evaluar(evaluar_f, x_actual)
    except (ArithmeticError, TypeError, ValueError, OverflowError):
        f_actual = float("nan")
    if not math.isfinite(f_actual):
        estado, motivo = "La función no está definida o no es finita en el valor inicial.", "no_finito"
    elif abs(f_actual) <= tol_residuo:
        estado, motivo, convergio = "La aproximación inicial satisface la tolerancia del residuo.", "tolerancia", True

    if not convergio and motivo != "no_finito":
        for indice in range(1, max_iteraciones + 1):
            try:
                derivada_actual = evaluar(evaluar_df, x_actual)
            except (ArithmeticError, TypeError, ValueError, OverflowError):
                derivada_actual = float("nan")
            if not math.isfinite(derivada_actual):
                estado, motivo = f"La derivada dejó de ser finita en x = {x_actual:.8g}.", "derivada_no_finita"
                break
            if abs(derivada_actual) <= umbral:
                estado, motivo = f"La derivada es cero o demasiado pequeña en x = {x_actual:.8g}; no se dividió.", "derivada_pequena"
                break
            try:
                x_siguiente = x_actual - f_actual / derivada_actual
                if not math.isfinite(x_siguiente):
                    raise ArithmeticError
                f_siguiente = evaluar(evaluar_f, x_siguiente)
                if not math.isfinite(f_siguiente):
                    raise ArithmeticError
            except (ArithmeticError, TypeError, ValueError, OverflowError):
                estado, motivo = "La siguiente aproximación produjo un valor no finito o fuera del dominio.", "no_finito"
                break
            error_absoluto = abs(x_siguiente - x_actual)
            error_porcentual = (error_absoluto / abs(x_siguiente) * 100
                                if x_siguiente != 0 else None)
            error_criterio = error_porcentual if error_porcentual is not None else error_absoluto
            if not math.isfinite(error_absoluto) or not math.isfinite(error_criterio):
                estado, motivo = "El error aproximado dejó de ser finito; el proceso se detuvo.", "no_finito"
                break
            filas.append({"i": indice, "xi": x_actual, "fxi": f_actual,
                          "dfxi": derivada_actual, "x_siguiente": x_siguiente,
                          "error_absoluto": error_absoluto,
                          "error_porcentual": error_porcentual,
                          "error_criterio": error_criterio,
                          "residuo": abs(f_siguiente)})
            x_actual, f_actual, error_final = x_siguiente, f_siguiente, error_criterio
            aproximaciones.append(x_actual)
            if error_criterio <= tol and abs(f_actual) <= tol_residuo:
                estado, motivo, convergio = "Convergencia alcanzada: error aproximado y residuo dentro de tolerancia.", "tolerancia", True
                break
        else:
            estado = "No se alcanzaron simultáneamente las tolerancias antes del máximo de iteraciones."

    residuo_final = abs(f_actual) if math.isfinite(f_actual) else None
    tabla = pd.DataFrame(filas, columns=["i", "xi", "fxi", "dfxi", "x_siguiente",
                                         "error_absoluto", "error_porcentual",
                                         "error_criterio", "residuo"])
    return {"expresion": str(funcion_simbolica), "derivada": str(derivada_simbolica),
            "funcion_simbolica": funcion_simbolica, "derivada_simbolica": derivada_simbolica,
            "funcion": evaluar_f, "derivada_funcion": evaluar_df,
            "x0": float(x0), "raiz_aproximada": x_actual,
            "iteraciones": len(filas), "error_final": error_final,
            "residuo": residuo_final, "tolerancia": tol,
            "tolerancia_residuo": tol_residuo, "umbral_derivada": umbral,
            "max_iteraciones": max_iteraciones, "convergio": convergio,
            "motivo_parada": motivo, "estado": estado, "tabla": tabla,
            "aproximaciones": aproximaciones}


def resolver_secante(expresion, x_anterior, x_actual, tolerancia,
                     max_iteraciones, tolerancia_residuo=1e-8,
                     umbral_denominador=1e-12):
    """Resuelve f(x)=0 con secante y conserva cada aproximación y residuo."""
    import pandas as pd

    _, simbolica, _, evaluar_f, _ = compilar_funcion_simbolica(expresion)
    try:
        x_anterior, x_actual, tol = map(float, (x_anterior, x_actual, tolerancia))
        tol_residuo = float(tolerancia_residuo)
        max_num, umbral = float(max_iteraciones), float(umbral_denominador)
    except (TypeError, ValueError) as exc:
        raise ValueError("Revise los valores iniciales, tolerancias y máximo de iteraciones.") from exc
    if not all(map(math.isfinite, (x_anterior, x_actual, tol, tol_residuo, max_num, umbral))):
        raise ValueError("Todos los datos deben ser finitos.")
    if tol <= 0 or tol_residuo <= 0 or umbral < 0:
        raise ValueError("Las tolerancias deben ser positivas y el umbral no negativo.")
    if isinstance(max_iteraciones, bool) or not max_num.is_integer() or max_num < 1:
        raise ValueError("El máximo de iteraciones debe ser un entero mayor o igual que 1.")
    max_iteraciones = int(max_num)

    def evaluar(x):
        with np.errstate(all="ignore"):
            return float(np.asarray(evaluar_f(x)))

    try:
        f_anterior, f_actual = evaluar(x_anterior), evaluar(x_actual)
    except (ArithmeticError, TypeError, ValueError, OverflowError) as exc:
        raise ValueError("La función debe estar definida en los dos valores iniciales.") from exc
    if not math.isfinite(f_anterior) or not math.isfinite(f_actual):
        raise ValueError("La función debe producir valores finitos en los dos valores iniciales.")

    semilla_anterior, semilla_actual = x_anterior, x_actual
    filas = []
    aproximaciones = [x_anterior, x_actual]
    convergio = abs(f_actual) <= tol_residuo
    error_final = None
    estado = "La aproximación alcanzó la tolerancia del residuo." if convergio else "Se alcanzó el máximo de iteraciones."
    motivo = "tolerancia" if convergio else "maximo_iteraciones"
    if not convergio:
        for indice in range(1, max_iteraciones + 1):
            denominador = f_actual - f_anterior
            if not math.isfinite(denominador) or abs(denominador) <= umbral:
                estado, motivo = "El denominador de la secante es cero o demasiado pequeño; no se dividió.", "denominador_pequeno"
                break
            x_siguiente = x_actual - f_actual * (x_actual - x_anterior) / denominador
            if not math.isfinite(x_siguiente):
                estado, motivo = "La siguiente aproximación no fue finita.", "no_finito"
                break
            try:
                f_siguiente = evaluar(x_siguiente)
            except (ArithmeticError, TypeError, ValueError, OverflowError):
                f_siguiente = float("nan")
            if not math.isfinite(f_siguiente):
                estado, motivo = "La función no es finita en la siguiente aproximación.", "no_finito"
                break
            error_absoluto = abs(x_siguiente - x_actual)
            error_porcentual = error_absoluto / abs(x_siguiente) * 100 if x_siguiente != 0 else None
            error_criterio = error_porcentual if error_porcentual is not None else error_absoluto
            filas.append({"i": indice, "x_anterior": x_anterior, "x_actual": x_actual,
                          "f_anterior": f_anterior, "f_actual": f_actual,
                          "denominador": denominador, "x_siguiente": x_siguiente,
                          "error_absoluto": error_absoluto,
                          "error_porcentual": error_porcentual,
                          "error_criterio": error_criterio,
                          "residuo": abs(f_siguiente)})
            x_anterior, x_actual = x_actual, x_siguiente
            f_anterior, f_actual = f_actual, f_siguiente
            aproximaciones.append(x_siguiente)
            error_final = error_criterio
            if error_criterio <= tol and abs(f_actual) <= tol_residuo:
                convergio, estado, motivo = True, "Convergencia alcanzada: error y residuo dentro de tolerancia.", "tolerancia"
                break
        else:
            estado = "No se alcanzaron simultáneamente las tolerancias antes del máximo de iteraciones."
    tabla = pd.DataFrame(filas, columns=["i", "x_anterior", "x_actual", "f_anterior",
                                         "f_actual", "denominador", "x_siguiente",
                                         "error_absoluto", "error_porcentual",
                                         "error_criterio", "residuo"])
    return {"expresion": str(simbolica), "funcion": evaluar_f,
            "raiz_aproximada": x_actual, "x0": semilla_anterior,
            "x1": semilla_actual, "iteraciones": len(filas),
            "error_final": error_final, "residuo": abs(f_actual),
            "tolerancia": tol, "tolerancia_residuo": tol_residuo,
            "max_iteraciones": max_iteraciones, "convergio": convergio,
            "motivo_parada": motivo, "estado": estado, "tabla": tabla,
            "aproximaciones": aproximaciones}


def comparar_derivadas_numericas(expresion, x, h):
    """Compara diferencias hacia adelante, atrás y centrales con la derivada simbólica."""
    import pandas as pd

    _, simbolica, derivada, evaluar_f, evaluar_df = compilar_funcion_simbolica(expresion)
    try:
        x, h = float(x), float(h)
    except (TypeError, ValueError) as exc:
        raise ValueError("El punto x y el paso h deben ser numéricos.") from exc
    if not math.isfinite(x) or not math.isfinite(h) or h <= 0:
        raise ValueError("x debe ser finito y h debe ser positivo y finito.")
    with np.errstate(all="ignore"):
        f_menos, f_centro, f_mas = (float(np.asarray(evaluar_f(punto)))
                                    for punto in (x - h, x, x + h))
        derivada_exacta = float(np.asarray(evaluar_df(x)))
    valores = (f_menos, f_centro, f_mas, derivada_exacta)
    if not all(map(math.isfinite, valores)):
        raise ValueError("La función y su derivada deben estar definidas alrededor de x ± h.")
    aproximaciones = (
        ("Adelante", "[f(x+h) − f(x)]/h", (f_mas - f_centro) / h, "O(h)"),
        ("Atrás", "[f(x) − f(x−h)]/h", (f_centro - f_menos) / h, "O(h)"),
        ("Central", "[f(x+h) − f(x−h)]/(2h)", (f_mas - f_menos) / (2 * h), "O(h²)"),
    )
    filas = [{"esquema": nombre, "formula": formula, "aproximacion": valor,
              "derivada_exacta": derivada_exacta,
              "error_absoluto": abs(valor - derivada_exacta), "orden": orden}
             for nombre, formula, valor, orden in aproximaciones]
    return {"expresion": str(simbolica), "derivada": str(derivada),
            "x": x, "h": h, "fx_menos": f_menos, "fx": f_centro,
            "fx_mas": f_mas, "derivada_exacta": derivada_exacta,
            "tabla": pd.DataFrame(filas), "funcion": evaluar_f}


def evaluar_horner_y_derivada(coeficientes, x):
    """Evalúa un polinomio y su derivada con el esquema simultáneo de Horner."""
    acumulado_p = coeficientes[0]
    acumulado_dp = 0.0
    pasos = [{"paso": 0, "coeficiente": coeficientes[0],
              "b_i": acumulado_p, "c_i": acumulado_dp}]
    for indice, coeficiente in enumerate(coeficientes[1:], 1):
        acumulado_dp = acumulado_dp * x + acumulado_p
        acumulado_p = acumulado_p * x + coeficiente
        pasos.append({"paso": indice, "coeficiente": coeficiente,
                      "b_i": acumulado_p, "c_i": acumulado_dp})
    return acumulado_p, acumulado_dp, pasos


def resolver_newton_horner(coeficientes, x0, tolerancia, max_iteraciones,
                           tolerancia_residuo=1e-8, umbral_derivada=1e-12):
    """Encuentra una raíz real con Newton y Horner, y devuelve su deflación."""
    import pandas as pd

    try:
        coeficientes = [float(coef) for coef in coeficientes]
        x_actual, tol, tol_residuo = float(x0), float(tolerancia), float(tolerancia_residuo)
        max_num, umbral = float(max_iteraciones), float(umbral_derivada)
    except (TypeError, ValueError) as exc:
        raise ValueError("Ingrese coeficientes y parámetros numéricos válidos.") from exc
    if len(coeficientes) < 2 or not all(map(math.isfinite, coeficientes)) or coeficientes[0] == 0:
        raise ValueError("Ingrese al menos dos coeficientes finitos y con coeficiente principal distinto de cero.")
    if not all(map(math.isfinite, (x_actual, tol, tol_residuo, max_num, umbral))):
        raise ValueError("Todos los datos deben ser finitos.")
    if tol <= 0 or tol_residuo <= 0 or umbral < 0:
        raise ValueError("Las tolerancias deben ser positivas y el umbral no negativo.")
    if isinstance(max_iteraciones, bool) or not max_num.is_integer() or max_num < 1:
        raise ValueError("El máximo de iteraciones debe ser un entero mayor o igual que 1.")
    max_iteraciones = int(max_num)

    coeficientes_originales = coeficientes[:]
    px, dpx, horner_x0 = evaluar_horner_y_derivada(coeficientes, x_actual)
    filas, aproximaciones = [], [x_actual]
    convergio = abs(px) <= tol_residuo
    error_final = None
    estado = "La aproximación inicial satisface la tolerancia del residuo." if convergio else "Se alcanzó el máximo de iteraciones."
    motivo = "tolerancia" if convergio else "maximo_iteraciones"
    horner_final = horner_x0
    if not convergio:
        for indice in range(1, max_iteraciones + 1):
            if not math.isfinite(dpx) or abs(dpx) <= umbral:
                estado, motivo = "La derivada calculada con Horner es cero o demasiado pequeña; no se dividió.", "derivada_pequena"
                break
            x_siguiente = x_actual - px / dpx
            if not math.isfinite(x_siguiente):
                estado, motivo = "La siguiente aproximación no fue finita.", "no_finito"
                break
            px_siguiente, dpx_siguiente, horner_siguiente = evaluar_horner_y_derivada(coeficientes, x_siguiente)
            if not math.isfinite(px_siguiente) or not math.isfinite(dpx_siguiente):
                estado, motivo = "Horner produjo un valor no finito; el proceso se detuvo.", "no_finito"
                break
            error_absoluto = abs(x_siguiente - x_actual)
            error_porcentual = error_absoluto / abs(x_siguiente) * 100 if x_siguiente != 0 else None
            error_criterio = error_porcentual if error_porcentual is not None else error_absoluto
            filas.append({"i": indice, "xi": x_actual, "pxi": px, "dpxi": dpx,
                          "x_siguiente": x_siguiente, "error_absoluto": error_absoluto,
                          "error_porcentual": error_porcentual,
                          "error_criterio": error_criterio,
                          "residuo": abs(px_siguiente)})
            x_actual, px, dpx = x_siguiente, px_siguiente, dpx_siguiente
            horner_final = horner_siguiente
            aproximaciones.append(x_actual)
            error_final = error_criterio
            if error_criterio <= tol and abs(px) <= tol_residuo:
                convergio, estado, motivo = True, "Convergencia alcanzada: error y residuo dentro de tolerancia.", "tolerancia"
                break
        else:
            estado = "No se alcanzaron simultáneamente las tolerancias antes del máximo de iteraciones."

    cociente = None
    resto_deflacion = None
    deflacion = []
    if convergio:
        acumulado = coeficientes_originales[0]
        cociente = [acumulado]
        deflacion.append({"paso": 0, "coeficiente": coeficientes_originales[0],
                          "producto": None, "resultado": acumulado})
        for indice, coeficiente in enumerate(coeficientes_originales[1:], 1):
            producto = x_actual * acumulado
            acumulado = coeficiente + producto
            deflacion.append({"paso": indice, "coeficiente": coeficiente,
                              "producto": producto, "resultado": acumulado})
            if indice < len(coeficientes_originales) - 1:
                cociente.append(acumulado)
        resto_deflacion = acumulado
    return {"coeficientes": coeficientes_originales,
            "polinomio": np.poly1d(coeficientes_originales),
            "raiz_aproximada": x_actual, "iteraciones": len(filas),
            "error_final": error_final, "residuo": abs(px),
            "tolerancia": tol, "tolerancia_residuo": tol_residuo,
            "max_iteraciones": max_iteraciones, "convergio": convergio,
            "motivo_parada": motivo, "estado": estado,
            "tabla": pd.DataFrame(filas), "horner": pd.DataFrame(horner_final),
            "aproximaciones": aproximaciones,
            "cociente_deflacion": cociente,
            "deflacion": pd.DataFrame(deflacion),
            "resto_deflacion": resto_deflacion}


def analizar_orden_convergencia(aproximaciones):
    """Estima el orden observado a partir de cuatro iterados consecutivos."""
    try:
        puntos = [float(valor) for valor in aproximaciones]
    except (TypeError, ValueError) as exc:
        raise ValueError("Ingrese cuatro aproximaciones numéricas.") from exc
    if len(puntos) != 4 or not all(map(math.isfinite, puntos)):
        raise ValueError("Ingrese exactamente cuatro aproximaciones finitas.")
    diferencias = [abs(puntos[i + 1] - puntos[i]) for i in range(3)]
    if any(diferencia == 0 for diferencia in diferencias):
        raise ValueError("Las cuatro aproximaciones deben ser distintas consecutivamente.")
    q0, q1 = diferencias[1] / diferencias[0], diferencias[2] / diferencias[1]
    if not all(map(math.isfinite, (q0, q1))) or q0 <= 0 or q1 <= 0:
        raise ValueError("No se pudieron calcular razones de error finitas.")
    if math.isclose(q0, 1.0, rel_tol=1e-12, abs_tol=1e-15):
        raise ValueError("No se puede estimar el orden: las dos primeras razones de error son casi iguales a 1.")
    orden = math.log(q1) / math.log(q0)
    if not math.isfinite(orden):
        raise ValueError("Los datos no producen un orden de convergencia finito.")
    try:
        constante = diferencias[2] / (diferencias[1] ** orden)
    except (OverflowError, ZeroDivisionError):
        constante = float("inf")
    if not math.isfinite(constante):
        raise ValueError("No se pudo estimar una constante de convergencia finita con estos datos.")
    contrayendo = q0 < 1 and q1 < 1
    if not contrayendo:
        diagnostico = "Las diferencias no decrecen en ambos pasos; estos iterados no muestran convergencia sostenida."
    elif math.isclose(orden, 1.0, rel_tol=0.08, abs_tol=0.08):
        diagnostico = "El orden observado es aproximadamente 1: comportamiento lineal."
    elif orden > 1:
        diagnostico = f"El orden observado es mayor que 1 (p ≈ {orden:.5g}): comportamiento superlineal en estos iterados."
    elif orden > 0:
        diagnostico = "El orden observado está entre 0 y 1: la convergencia parece sublineal en estos iterados."
    else:
        diagnostico = "El orden estimado no indica convergencia de orden positivo."
    return {"aproximaciones": puntos, "diferencias": diferencias,
            "razon_1": q0, "razon_2": q1, "orden": orden,
            "constante": constante, "contrayendo": contrayendo,
            "diagnostico": diagnostico}


CRITERIOS_ERROR_ITERATIVO = {
    "infinito": ("Norma infinito (Tarea 8)", "‖x⁽ᵏ⁾ − x⁽ᵏ⁻¹⁾‖∞"),
    "euclideo": ("Norma euclídea (presentación)", "‖x⁽ᵏ⁾ − x⁽ᵏ⁻¹⁾‖₂"),
    "porcentual": ("Relativo porcentual máximo (Chapra)", "máx. εₐ (%)"),
}


def resolver_metodo_iterativo(matriz, vector, inicial, tolerancia, max_iteraciones, metodo,
                             reordenar=True, criterio_error="infinito"):
    """Resuelve Ax=b conservando las iteraciones sin redondear valores intermedios.

    El criterio predeterminado es el de la Tarea 8. La norma 2 permite comparar
    los ejemplos 1 y 2 de la presentación, y el porcentual, el ejemplo de Chapra.
    """
    A = np.asarray(matriz, dtype=float)
    b = np.asarray(vector, dtype=float)
    x0 = np.asarray(inicial, dtype=float)
    if A.ndim != 2 or A.shape[0] != A.shape[1] or A.shape[0] == 0:
        raise ValueError("La matriz A debe ser cuadrada y no vacía.")
    n = A.shape[0]
    if b.shape != (n,) or x0.shape != (n,):
        raise ValueError("Las dimensiones de A, b y x⁽⁰⁾ deben coincidir.")
    if not np.isfinite(A).all() or not np.isfinite(b).all() or not np.isfinite(x0).all():
        raise ValueError("Todos los valores de A, b y x⁽⁰⁾ deben ser finitos.")
    try:
        tol_num, max_num = float(tolerancia), float(max_iteraciones)
    except (TypeError, ValueError) as exc:
        raise ValueError("La tolerancia y el máximo de iteraciones deben ser numéricos.") from exc
    if not math.isfinite(tol_num) or tol_num <= 0:
        raise ValueError("La tolerancia debe ser positiva y finita.")
    if isinstance(max_iteraciones, bool) or not math.isfinite(max_num) or not max_num.is_integer() or max_num < 1:
        raise ValueError("El máximo de iteraciones debe ser un entero positivo.")
    max_iteraciones = int(max_num)
    if metodo not in {"Jacobi", "Gauss-Seidel"}:
        raise ValueError("Seleccione Jacobi o Gauss-Seidel.")
    if criterio_error not in CRITERIOS_ERROR_ITERATIVO:
        raise ValueError("Seleccione un criterio de error válido: infinito, euclideo o porcentual.")

    indices = list(range(n))
    diagonal = np.diag(A)
    dominante = bool(np.all(np.abs(diagonal) > np.sum(np.abs(A), axis=1) - np.abs(diagonal)))
    if (np.any(diagonal == 0) or (reordenar and not dominante)) and reordenar:
        # Buscar primero un orden que logre dominancia estricta; luego uno que
        # al menos deje una diagonal no nula. El retroceso evita permutar filas
        # indiscriminadamente y funciona bien para los tamaños de la interfaz.
        def buscar(exigir_dominancia):
            asignacion = []
            usados = set()
            forzadas = [i for i in indices]

            def dfs(columna):
                if columna == n:
                    return list(asignacion)
                candidatos = sorted(
                    (fila for fila in forzadas if fila not in usados
                     and A[fila, columna] != 0
                     and (not exigir_dominancia or abs(A[fila, columna]) > np.sum(np.abs(A[fila])) - abs(A[fila, columna]))),
                    key=lambda fila: -(abs(A[fila, columna]) - (np.sum(np.abs(A[fila])) - abs(A[fila, columna]))),
                )
                for fila in candidatos:
                    usados.add(fila); asignacion.append(fila)
                    resultado = dfs(columna + 1)
                    if resultado is not None:
                        return resultado
                    asignacion.pop(); usados.remove(fila)
                return None
            return dfs(0)

        permutacion = buscar(True)
        dominancia_encontrada = permutacion is not None
        if permutacion is None and np.any(diagonal == 0):
            permutacion = buscar(False)
        if permutacion is None:
            if np.any(diagonal == 0):
                raise ValueError("La diagonal contiene ceros y no se encontró un reordenamiento de filas con diagonal no nula.")
            # Tener diagonal no nula ya permite iterar. Una permutación sin
            # dominancia garantizada puede convertir un proceso convergente en
            # uno divergente: conservar el orden original en este caso.
            permutacion = indices
        A, b = A[permutacion, :], b[permutacion]
        indices = permutacion
    else:
        dominancia_encontrada = dominante
    if np.any(np.diag(A) == 0):
        raise ValueError("La diagonal principal contiene ceros; no es posible iniciar el cálculo.")
    diagonal = np.diag(A)
    dominante_final = bool(np.all(np.abs(diagonal) > np.sum(np.abs(A), axis=1) - np.abs(diagonal)))

    x = x0.copy()
    tabla = [{"k": 0, "x": x.copy(), "error": None, "error_infinito": None,
              "error_euclideo": None, "error_porcentual": None,
              "residuo": float(np.linalg.norm(A @ x - b, ord=np.inf))}]
    errores_crecen = 0
    advertencias = []
    convergio = False
    motivo_parada = "maximo_iteraciones"
    estado = "Máximo de iteraciones alcanzado; posible no convergencia."
    for k in range(1, max_iteraciones + 1):
        anterior = x.copy()
        with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
            if metodo == "Jacobi":
                x = (b - (A - np.diag(diagonal)) @ anterior) / diagonal
            else:
                for i in range(n):
                    x[i] = (b[i] - A[i, :i] @ x[:i] - A[i, i + 1:] @ anterior[i + 1:]) / diagonal[i]
        if not np.isfinite(x).all():
            estado = f"{metodo}: se detuvo porque aparecieron valores no finitos en la iteración {k}."
            motivo_parada = "no_finito"
            x = anterior
            break
        with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
            cambios = np.abs(x - anterior)
            error_infinito = float(np.max(cambios))
            # hypot evita desbordar al elevar al cuadrado componentes grandes.
            error_euclideo = math.hypot(*cambios)
            relativos = np.zeros(n)
            np.divide(cambios, np.abs(x), out=relativos, where=x != 0)
            relativos[(x == 0) & (cambios != 0)] = np.inf
            error_porcentual = float(np.max(relativos) * 100)
        error = {"infinito": error_infinito, "euclideo": error_euclideo,
                 "porcentual": error_porcentual}[criterio_error]
        with np.errstate(over="ignore", invalid="ignore"):
            residuo = float(np.linalg.norm(A @ x - b, ord=np.inf))
        tabla.append({"k": k, "x": x.copy(), "error": error,
                      "error_infinito": error_infinito, "error_euclideo": error_euclideo,
                      "error_porcentual": error_porcentual, "residuo": residuo})
        if not math.isfinite(residuo) or not math.isfinite(error_infinito) or (criterio_error == "euclideo" and not math.isfinite(error_euclideo)):
            estado = f"{metodo}: se detuvo porque el error o el residuo dejó de ser finito en la iteración {k}."
            motivo_parada = "no_finito"
            break
        if error <= tol_num:
            convergio = True
            motivo_parada = "tolerancia"
            estado = f"Convergencia alcanzada según {CRITERIOS_ERROR_ITERATIVO[criterio_error][1]} ≤ ε."
            break
        errores_crecen = errores_crecen + 1 if len(tabla) > 2 and error > tabla[-2]["error"] else 0
        if errores_crecen == 5 and not advertencias:
            # El crecimiento transitorio no prueba divergencia (por ejemplo,
            # una matriz triangular puede converger después de varios aumentos).
            advertencias.append(f"El error creció durante cinco iteraciones consecutivas de {metodo}; se continuó hasta la tolerancia o el límite indicado.")
    residuo_final = tabla[-1]["residuo"]
    try:
        referencia = np.linalg.solve(A, b)
        diferencia = float(np.linalg.norm(x - referencia, ord=np.inf))
        diferencia_euclidea = math.hypot(*(x - referencia))
    except np.linalg.LinAlgError:
        referencia = diferencia = diferencia_euclidea = None
    for fila in tabla:
        fila["error_referencia_euclideo"] = None if referencia is None else math.hypot(*(fila["x"] - referencia))
    return {"metodo": metodo, "A": A, "b": b, "x0": x0, "solucion": x,
            "tabla": tabla, "iteraciones": len(tabla) - 1, "error": tabla[-1]["error"],
            "residuo": residuo_final, "estado": estado, "tolerancia": tol_num,
            "convergio": convergio, "motivo_parada": motivo_parada, "advertencias": advertencias,
            "criterio_error": criterio_error, "formula_error": CRITERIOS_ERROR_ITERATIVO[criterio_error][1],
            "max_iteraciones": max_iteraciones, "dominante_original": dominante,
            "dominante": dominante_final, "dominancia_por_reordenamiento": dominancia_encontrada,
            "reordenada": indices != list(range(n)), "permutacion": [i + 1 for i in indices],
            "referencia": referencia, "diferencia_referencia": diferencia,
            "diferencia_referencia_euclidea": diferencia_euclidea}


_BINARIOS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
}
_UNARIOS = {ast.UAdd: operator.pos, ast.USub: operator.neg}
_SUPERSCRIPT = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")
_FUNCIONES = {
    "sin": np.sin, "cos": np.cos, "tan": np.tan,
    "asin": np.arcsin, "acos": np.arccos, "atan": np.arctan,
    "exp": np.exp, "log": np.log, "ln": np.log, "log10": np.log10,
    "sqrt": np.sqrt, "abs": np.abs,
}


class EvaluadorFuncion:
    """Evalua expresiones numericas mediante un interprete AST de lista blanca."""

    def __init__(self, expresion):
        expresion = expresion.strip()
        try:
            self.arbol = ast.parse(expresion, mode="eval").body
        except (SyntaxError, ValueError) as exc:
            raise ValueError("La funcion tiene una sintaxis incorrecta.") from exc
        self._validar(self.arbol)

    def _validar(self, nodo):
        if isinstance(nodo, ast.Constant) and isinstance(nodo.value, (int, float)):
            return
        if isinstance(nodo, ast.Name) and nodo.id in {"x", "pi", "e"} | set(_FUNCIONES):
            return
        if isinstance(nodo, ast.BinOp) and type(nodo.op) in _BINARIOS:
            self._validar(nodo.left)
            self._validar(nodo.right)
            return
        if isinstance(nodo, ast.UnaryOp) and type(nodo.op) in _UNARIOS:
            self._validar(nodo.operand)
            return
        if isinstance(nodo, ast.Call) and isinstance(nodo.func, ast.Name) and nodo.func.id in _FUNCIONES and len(nodo.args) == 1 and not nodo.keywords:
            self._validar(nodo.args[0])
            return
        raise ValueError("Funcion no permitida. Use x, pi, e, operaciones y funciones trigonométricas, exp, log, sqrt o abs.")

    def _evaluar(self, nodo, x):
        if isinstance(nodo, ast.Constant):
            return nodo.value
        if isinstance(nodo, ast.Name):
            if nodo.id == "x":
                return x
            return {"pi": np.pi, "e": np.e, **_FUNCIONES}[nodo.id]
        if isinstance(nodo, ast.BinOp):
            return _BINARIOS[type(nodo.op)](self._evaluar(nodo.left, x), self._evaluar(nodo.right, x))
        if isinstance(nodo, ast.UnaryOp):
            return _UNARIOS[type(nodo.op)](self._evaluar(nodo.operand, x))
        if isinstance(nodo, ast.Call):
            return _FUNCIONES[nodo.func.id](self._evaluar(nodo.args[0], x))
        raise ValueError("Expresion no admitida.")

    def __call__(self, x):
        try:
            with np.errstate(all="ignore"):
                valor = self._evaluar(self.arbol, x)
            return np.asarray(valor) if isinstance(x, (list, tuple, np.ndarray)) else float(valor)
        except (ArithmeticError, TypeError, ValueError, OverflowError) as exc:
            raise ValueError(f"No se pudo evaluar la funcion en x={x}: {exc}") from exc


def bisecar(expresion, a, b, tolerancia, max_iteraciones):
    """Encuentra una raiz por biseccion y devuelve tabla, diagnostico y resumen."""
    f = EvaluadorFuncion(expresion)
    a, b, tolerancia = float(a), float(b), float(tolerancia)
    if not all(map(math.isfinite, (a, b, tolerancia))) or a >= b:
        raise ValueError("Se requiere a < b y valores numericos finitos.")
    if tolerancia <= 0:
        raise ValueError("La tolerancia absoluta debe ser mayor que cero.")
    try:
        iteraciones_numero = float(max_iteraciones)
    except (TypeError, ValueError) as exc:
        raise ValueError("El maximo de iteraciones debe ser un entero mayor o igual que 1.") from exc
    if isinstance(max_iteraciones, bool) or not math.isfinite(iteraciones_numero) or not iteraciones_numero.is_integer() or iteraciones_numero < 1:
        raise ValueError("El maximo de iteraciones debe ser un entero mayor o igual que 1.")
    max_iteraciones = int(iteraciones_numero)
    datos_entrada = {"expresion": expresion, "tolerancia": tolerancia,
                     "max_iteraciones": max_iteraciones}
    fa, fb = f(a), f(b)
    if not math.isfinite(fa) or not math.isfinite(fb):
        raise ValueError("La funcion no esta definida o no es finita en los extremos.")
    ancho_inicial = b - a
    if not math.isfinite(ancho_inicial):
        raise ValueError("El ancho del intervalo debe ser finito.")
    # Restar logaritmos evita desbordar al calcular ancho/tolerancia.
    teoricas = max(0, math.ceil(math.log2(ancho_inicial) - math.log2(tolerancia))) if ancho_inicial > tolerancia else 0
    if fa == 0 or fb == 0:
        raiz = a if fa == 0 else b
        return {**datos_entrada, "raiz": raiz, "f_raiz": 0.0, "cota": 0.0, "error_relativo": "—", "iteraciones": 0,
                "teoricas": teoricas, "estado": "Raiz exacta encontrada en un extremo.", "tabla": [], "intervalo_inicial": (a, b), "funcion": f}
    if (fa > 0 and fb > 0) or (fa < 0 and fb < 0):
        raise ValueError("El intervalo no cumple la condicion de cambio de signo; puede buscar una raiz en otro intervalo.")
    # La continuidad no puede demostrarse por muestreo; detectar valores no definidos en una malla evita, entre otros, 1/x en [-1, 1].
    for punto in np.linspace(a, b, 101)[1:-1]:
        try:
            valor = f(float(punto))
        except ValueError as exc:
            raise ValueError("Se detecto una discontinuidad o un valor fuera del dominio en el intervalo. Elija un intervalo donde la funcion sea continua.") from exc
        if not math.isfinite(valor):
            raise ValueError("Se detecto una discontinuidad o un valor fuera del dominio en el intervalo. Elija un intervalo donde la funcion sea continua.")
    intervalo_inicial = (a, b)
    tabla, anterior, estado = [], None, "Se alcanzo el maximo de iteraciones sin garantizar la tolerancia solicitada."
    raiz = a + (b - a) / 2 if (a >= 0 and b >= 0) or (a <= 0 and b <= 0) else a / 2 + b / 2
    fr, cota, error_relativo = None, (b - a) / 2, "—"
    for k in range(1, max_iteraciones + 1):
        # Evita overflow al sumar extremos del mismo signo y al restarlos con signos opuestos.
        xr = a + (b - a) / 2 if (a >= 0 and b >= 0) or (a <= 0 and b <= 0) else a / 2 + b / 2
        eb = (b - a) / 2  # Cota calculada antes de actualizar el intervalo.
        fr = f(xr)
        if not math.isfinite(fr):
            raise ValueError("La funcion no esta definida dentro del intervalo; revise discontinuidades o el dominio.")
        error_abs = "—" if anterior is None else abs(xr - anterior)
        if anterior is None:
            error_rel = "—"
        elif xr == 0:
            error_rel = "No definido"
        else:
            error_rel = abs((xr - anterior) / xr)
        tabla.append({"k": k, "a": a, "b": b, "xr": xr, "fa": fa, "fb": fb,
                      "fr": fr, "eb": eb, "error_abs": error_abs, "error_relativo": error_rel})
        raiz, cota, error_relativo = xr, eb, error_rel
        if fr == 0:
            estado = "Raiz exacta encontrada en aritmetica de maquina."
            break
        if eb <= tolerancia:
            estado = "Tolerancia absoluta alcanzada."
            break
        if (fa < 0 < fr) or (fr < 0 < fa):
            b, fb = xr, fr
        else:
            a, fa = xr, fr
        anterior = xr
    return {**datos_entrada, "raiz": raiz, "f_raiz": fr, "cota": cota, "error_relativo": error_relativo,
            "iteraciones": len(tabla), "teoricas": teoricas, "estado": estado, "tabla": tabla,
            "intervalo_inicial": intervalo_inicial, "funcion": f, "intervalo_final": (a, b)}


def notacion_posicional(valor, base):
    """Descompone un entero expresado en base 10 o base 2 y devuelve ambas bases."""
    if base not in (2, 10):
        raise ValueError("La base de entrada debe ser 2 o 10.")
    try:
        if isinstance(valor, bool):
            raise ValueError
        valor = int(str(valor).strip(), base)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Ingrese un numero entero valido en base {base}.") from exc
    negativo = valor < 0
    digitos = bin(abs(valor))[2:] if base == 2 else str(abs(valor))
    digitos_valor = [int(d) for d in digitos]
    exponente_max = len(digitos_valor) - 1
    expansion = " + ".join(
        f"{d} · {base}{str(exponente_max-i).translate(_SUPERSCRIPT)}"
        for i, d in enumerate(digitos_valor)
    )
    suma = " + ".join(str(d * base ** (exponente_max-i)) for i, d in enumerate(digitos_valor))
    signo = "−" if negativo else ""
    decimal = f"{signo}{abs(valor)}"
    binario = f"{signo}{bin(abs(valor))[2:]}"
    return {"base": base, "digitos": f"{signo}{digitos}", "expansion": f"{signo}{digitos} = {expansion}",
            "suma": f"{signo}{digitos} = {signo}{suma} = {decimal}",
            "decimal": decimal, "binario": binario}


def informe_errores(valor_verdadero, valor_aproximado):
    """Calcula errores absoluto, relativo y porcentual entre dos valores."""
    xv, xa = map(float, (valor_verdadero, valor_aproximado))
    if not all(map(math.isfinite, (xv, xa))):
        raise ValueError("Los datos deben ser numeros finitos.")
    absoluto = abs(xv - xa)
    relativo = absoluto / abs(xv) if xv != 0 else None
    return {"absoluto": absoluto, "relativo": relativo, "porcentual": relativo * 100 if relativo is not None else None,
            "valor_verdadero": xv, "valor_aproximado": xa}


def propagar_error_numerico(expresion, x, delta_x):
    """Estima f'(x) por diferencias centrales y compara la propagacion lineal con la real."""
    f = EvaluadorFuncion(expresion)
    x, delta_x = float(x), float(delta_x)
    if not all(map(math.isfinite, (x, delta_x))):
        raise ValueError("x y Δx deben ser numeros finitos.")
    # h ~ eps^(1/3) equilibra el error de truncamiento y el de redondeo en diferencias centrales.
    h = np.cbrt(np.finfo(float).eps) * max(1.0, abs(x))
    valores = (f(x - h), f(x + h), f(x), f(x + delta_x))
    if not all(math.isfinite(v) for v in valores):
        raise ValueError("La funcion debe estar definida alrededor de x y x + Δx.")
    derivada = (valores[1] - valores[0]) / (2 * h)
    cambio_aproximado = derivada * delta_x
    cambio_real = valores[3] - valores[2]
    return {"h": h, "derivada": derivada, "cambio_aproximado": cambio_aproximado,
            "cambio_real": cambio_real, "diferencia": abs(cambio_aproximado - cambio_real),
            "fx": valores[2], "fx_delta": valores[3]}


def comparar_truncamiento_redondeo(x, max_terminos):
    """Simula la serie de Taylor de exp(x), separando truncamiento y redondeo por iteracion."""
    x = float(x)
    try:
        nmax_float = float(max_terminos)
    except (TypeError, ValueError) as exc:
        raise ValueError("El maximo de terminos debe ser un entero entre 2 y 200.") from exc
    if not math.isfinite(x) or abs(x) > 10:
        raise ValueError("Para esta simulacion, x debe ser finito y estar entre -10 y 10.")
    if not math.isfinite(nmax_float) or not nmax_float.is_integer() or not 2 <= nmax_float <= 200:
        raise ValueError("El maximo de terminos debe ser un entero entre 2 y 200.")
    nmax = int(nmax_float)
    with localcontext() as ctx:
        ctx.prec = 80
        xd = Decimal(str(x))
        referencia = xd.exp()
        termino = Decimal(1)
        parcial = Decimal(0)
        suma_float = 0.0
        tabla = []
        for k in range(nmax):
            parcial += termino
            suma_float += float(termino)
            error_truncamiento = abs(parcial - referencia)
            error_redondeo = abs(Decimal.from_float(suma_float) - parcial)
            tabla.append({"n": k + 1, "suma": suma_float,
                          "error_truncamiento": float(error_truncamiento),
                          "error_redondeo": float(error_redondeo)})
            termino *= xd / Decimal(k + 1)
    return {"x": x, "referencia": float(referencia), "tabla": tabla,
            "terminos": nmax, "funcion": "exp(x) = 1 + x + x²/2! + x³/3! + ···"}


def comparar_inestabilidad(x):
    """Compara sqrt(x+1)-sqrt(x) con su forma racionalizada numericamente estable."""
    x = float(x)
    if not math.isfinite(x) or x < 0:
        raise ValueError("x debe ser un numero finito mayor o igual que cero.")
    raiz_x = math.sqrt(x)
    raiz_siguiente = math.sqrt(x + 1.0)
    directo = raiz_siguiente - raiz_x
    reformulado = 1.0 / (raiz_siguiente + raiz_x)
    with localcontext() as ctx:
        ctx.prec = 80
        xd = Decimal(str(x))
        referencia = (xd + Decimal(1)).sqrt() - xd.sqrt()
        error_directo = abs(Decimal.from_float(directo) - referencia)
        error_reformulado = abs(Decimal.from_float(reformulado) - referencia)
    return {"x": x, "directo": directo, "reformulado": reformulado,
            "referencia": float(referencia), "error_directo": float(error_directo),
            "error_reformulado": float(error_reformulado),
            "formula_directa": "sqrt(x + 1) - sqrt(x)",
            "formula_reformulada": "1 / (sqrt(x + 1) + sqrt(x))"}


def graficar_funcion(expresion, x_min, x_max, ax, raiz=None, intervalo=None, titulo_intervalo=""):
    """Dibuja una funcion en un eje Matplotlib, omitiendo puntos invalidos y saltos."""
    f = EvaluadorFuncion(expresion)
    x_min, x_max = float(x_min), float(x_max)
    if not math.isfinite(x_min) or not math.isfinite(x_max) or x_min >= x_max:
        raise ValueError("Se requiere x_min < x_max y limites finitos.")
    xs = np.linspace(x_min, x_max, 1201)
    ys = np.asarray(f(xs), dtype=float)
    validos = np.isfinite(ys)
    if validos.any():
        escala = max(1.0, float(np.nanpercentile(np.abs(ys[validos]), 95)))
        validos &= np.abs(ys) <= escala * 50
        # Rompe saltos grandes entre muestras finitas: una asíntota no siempre cae en la malla.
        pares = validos[:-1] & validos[1:]
        diferencias = np.abs(np.diff(ys))
        diferencias_validas = diferencias[pares]
        if diferencias_validas.size:
            salto_tipico = float(np.median(diferencias_validas))
            umbral_salto = max(salto_tipico * 20, np.finfo(float).eps * escala * 100)
            cortes = np.flatnonzero(pares & (diferencias > umbral_salto))
            validos[cortes] = False
            validos[cortes + 1] = False
    # Los puntos no validos hacen que Matplotlib deje huecos en vez de cruzar asíntotas.
    ys = np.where(validos, ys, np.nan)
    ax.plot(xs, ys, color="#2563EB", linewidth=2, label=f"f(x) = {expresion}")
    if intervalo:
        ax.axvspan(intervalo[0], intervalo[1], color="#22C55E", alpha=0.13,
                   label=titulo_intervalo or "Intervalo inicial de biseccion")
    if raiz is not None:
        ax.scatter([raiz], [float(f(raiz))], color="#DC2626", zorder=3, label=f"Raiz aproximada: {raiz:.6g}")
    ax.set_title("Grafica de la funcion")
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.grid(True, alpha=0.3)
    ax.legend()
    return ax


def estado_punto_flotante():
    """Devuelve ejemplos reproducibles de representacion binaria, epsilon y rango float."""
    with np.errstate(over="ignore", under="ignore", invalid="ignore"):
        overflow = np.float64(1e308) * np.float64(1e308)
        underflow = np.float64(1e-300) * np.float64(1e-300)
    return {"suma": 0.1 + 0.2, "igualdad": 0.1 + 0.2 == 0.3,
            "epsilon": float(np.finfo(float).eps), "overflow": float(overflow),
            "underflow": float(underflow), "maximo": float(np.finfo(float).max),
            "minimo_subnormal": float(np.nextafter(0.0, 1.0))}


TIPOS_ERROR = (
    ("Inherente", "Limitación propia de los datos o del problema.", "Una medición física tiene precisión finita."),
    ("Redondeo", "Representación finita de números reales.", "0.1 + 0.2 puede diferir de 0.3."),
    ("Truncamiento", "Se omiten términos de un proceso numérico infinito.", "Aproximar exp(x) con una suma de Taylor finita."),
    ("Overflow", "El valor excede el máximo representable.", "Una operación puede producir infinito."),
    ("Underflow", "La magnitud es menor que el mínimo representable con precisión normal.", "Un producto muy pequeño puede redondearse a cero."),
    ("Error del modelo matemático", "El modelo no representa exactamente el fenómeno real.", "Ignorar la fricción en un modelo de movimiento."),
)
