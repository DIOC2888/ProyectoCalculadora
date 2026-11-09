"""Algoritmos del modulo de metodos numericos de la calculadora."""

import ast
import math
import operator
from decimal import Decimal, localcontext

import numpy as np


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
