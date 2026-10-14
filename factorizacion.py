"""Programa 6: factorización LU sin permutaciones y resolución de Ax=b."""

from config import TOLERANCIA
from ecuaciones import gauss_jordan
from matrices import (
    _matrices_son_iguales,
    _multiplicar_dos_matrices as producto_matricial,
)
from sistema import clasificar_sistema


MENSAJE_PIVOTEO = (
    "La matriz no admite Factorización 𝐿𝑈 sin permutación "
    "(requiere pivoteo parcial 𝑃𝐴 = 𝐿𝑈)"
)


def _texto_operacion_fila(fila_objetivo, fila_origen, factor):
    """Expresa el reemplazo de fila conservando el multiplicador utilizado."""
    if factor == 1:
        return f"F{fila_objetivo} ← F{fila_objetivo} − F{fila_origen}"
    if factor == -1:
        return f"F{fila_objetivo} ← F{fila_objetivo} + F{fila_origen}"
    return f"F{fila_objetivo} ← F{fila_objetivo} − ({factor:.12g}) · F{fila_origen}"


def _validar_vector(valores, mensaje):
    """Convierte una lista de números finitos y devuelve una copia independiente."""
    if not isinstance(valores, (list, tuple)):
        raise ValueError(mensaje)
    try:
        vector = [float(valor) for valor in valores]
    except (TypeError, ValueError, OverflowError):
        raise ValueError(mensaje) from None
    if any(not -float("inf") < valor < float("inf") for valor in vector):
        raise ValueError(mensaje)
    return vector


def _validar_matriz(A):
    """Valida una matriz rectangular no vacía y devuelve sus datos numéricos."""
    if not isinstance(A, (list, tuple)) or not A:
        raise ValueError("La matriz A no puede estar vacía.")
    if not isinstance(A[0], (list, tuple)) or not A[0]:
        raise ValueError("A debe ser una matriz rectangular no vacía.")
    columnas = len(A[0])
    if any(not isinstance(fila, (list, tuple)) or len(fila) != columnas for fila in A):
        raise ValueError("A debe ser una matriz rectangular.")
    return [
        _validar_vector(fila, "Todos los elementos de A deben ser números finitos.")
        for fila in A
    ]


def factorizar_lu(A):
    """Devuelve L, U escalonada y los reemplazos efectuados, sin intercambiar filas."""
    original = _validar_matriz(A)
    filas, columnas = len(original), len(original[0])
    U = [fila[:] for fila in original]
    L = [[1.0 if i == j else 0.0 for j in range(filas)] for i in range(filas)]
    pasos = [{
        "tipo": "inicio", "titulo": "MATRIZ ORIGINAL Y L INICIAL",
        "descripcion": "Se inicia con U = A y L = I; los multiplicadores completarán L.",
        "A": [fila[:] for fila in original], "L": [fila[:] for fila in L],
    }]
    fila_pivote = 0
    for columna in range(columnas):
        if fila_pivote == filas:
            break
        pivote = U[fila_pivote][columna]
        if abs(pivote) <= TOLERANCIA:
            if any(abs(U[i][columna]) > TOLERANCIA for i in range(fila_pivote + 1, filas)):
                raise ValueError(MENSAJE_PIVOTEO)
            # Una columna sin pivote no consume una fila de la forma escalonada.
            continue
        for i in range(fila_pivote + 1, filas):
            entrada = U[i][columna]
            if entrada == 0:
                continue
            multiplicador = entrada / pivote
            # L registra la fila usada en el reemplazo, incluso al saltar columnas nulas.
            L[i][fila_pivote] = multiplicador
            U[i] = [U[i][k] - multiplicador * U[fila_pivote][k] for k in range(columnas)]
            U[i][columna] = 0.0
            pasos.append({
                "tipo": "eliminacion", "titulo": "ELIMINACIÓN Y REGISTRO EN L",
                "descripcion": (
                    f"L({i + 1},{fila_pivote + 1}) = {entrada:.12g} / "
                    f"({pivote:.12g}) = {multiplicador:.12g}. "
                    + _texto_operacion_fila(i + 1, fila_pivote + 1, multiplicador)
                ),
                "multiplicador": multiplicador, "fila_objetivo": i,
                "fila_pivote": fila_pivote,
                "U": [fila[:] for fila in U], "L": [fila[:] for fila in L],
            })
        fila_pivote += 1
    pasos.append({
        "tipo": "factorizacion", "titulo": "MATRICES L Y U FINALES",
        "descripcion": "L contiene los multiplicadores y U es la forma escalonada de A.",
        "U": [fila[:] for fila in U], "L": [fila[:] for fila in L],
    })
    return L, U, pasos


def _reducir_a_identidad(matriz_aumentada, tipo, titulo):
    """Reduce [U|y] de abajo hacia arriba y devuelve x junto con sus operaciones."""
    matriz = [fila[:] for fila in matriz_aumentada]
    filas = len(matriz)
    pasos = [{
        "tipo": tipo + "_inicio", "titulo": titulo,
        "descripcion": "Se parte de U y del vector intermedio y.",
        "etiqueta_matriz": "MATRIZ AUMENTADA [U|y]",
        "matriz": [fila[:] for fila in matriz],
    }]
    for j in range(filas - 1, -1, -1):
        pivote = matriz[j][j]
        if abs(pivote) <= TOLERANCIA:
            raise ValueError("El sistema no tiene solución única: U tiene un pivote cero.")
        if pivote != 1:
            matriz[j] = [valor / pivote for valor in matriz[j]]
            matriz[j][j] = 1.0
            pasos.append({
                "tipo": tipo + "_normalizar", "titulo": "NORMALIZAR FILA PIVOTE",
                "descripcion": f"F{j + 1} ← (1/({pivote:.12g})) · F{j + 1}",
                "etiqueta_matriz": "REDUCCIÓN DE [U|y]",
                "matriz": [fila[:] for fila in matriz],
            })
        for i in range(j):
            factor = matriz[i][j]
            if factor == 0:
                continue
            matriz[i] = [matriz[i][k] - factor * matriz[j][k] for k in range(filas + 1)]
            matriz[i][j] = 0.0
            pasos.append({
                "tipo": tipo + "_eliminar", "titulo": "SUSTITUCIÓN HACIA ATRÁS",
                "descripcion": _texto_operacion_fila(i + 1, j + 1, factor),
                "etiqueta_matriz": "REDUCCIÓN DE [U|y]",
                "matriz": [fila[:] for fila in matriz],
            })
    solucion = [fila[-1] for fila in matriz]
    pasos.append({
        "tipo": tipo + "_final", "titulo": "VECTOR SOLUCIÓN x",
        "descripcion": "La última columna de [I|x] contiene la solución.",
        "etiqueta_matriz": "MATRIZ AUMENTADA [I|x]",
        "matriz": [fila[:] for fila in matriz],
    })
    return solucion, pasos


def _eliminar_debajo(matriz_coeficientes, b, tipo, titulo):
    """Reduce [L|b] a [I|y] y devuelve y y los reemplazos de fila realizados."""
    matriz = [fila[:] + [b[i]] for i, fila in enumerate(matriz_coeficientes)]
    pasos = [{
        "tipo": tipo + "_inicio", "titulo": titulo,
        "descripcion": "Se utiliza la L final, con los multiplicadores de A.",
        "etiqueta_matriz": "MATRIZ AUMENTADA [L|b]",
        "matriz": [fila[:] for fila in matriz],
    }]
    for j in range(len(matriz)):
        for i in range(j + 1, len(matriz)):
            factor = matriz[i][j]
            # Un factor pequeño puede tener un efecto grande sobre el término independiente.
            if factor == 0:
                continue
            matriz[i] = [valor - factor * base for valor, base in zip(matriz[i], matriz[j])]
            matriz[i][j] = 0.0
            pasos.append({
                "tipo": tipo + "_eliminar", "titulo": "SUSTITUCIÓN HACIA ADELANTE",
                "descripcion": _texto_operacion_fila(i + 1, j + 1, factor),
                "etiqueta_matriz": "REDUCCIÓN DE [L|b]",
                "matriz": [fila[:] for fila in matriz],
            })
    vector = [fila[-1] for fila in matriz]
    pasos.append({
        "tipo": tipo + "_final", "titulo": "VECTOR INTERMEDIO y",
        "descripcion": "La última columna de [I|y] contiene el vector intermedio.",
        "etiqueta_matriz": "MATRIZ AUMENTADA [I|y]",
        "matriz": [fila[:] for fila in matriz],
    })
    return vector, pasos


def _comparar_con_gauss(A, b, x):
    """Reutiliza Gauss-Jordan para comparar x; sus pasos se conservan por separado."""
    aumentada = [fila[:] + [b[i]] for i, fila in enumerate(A)]
    datos = gauss_jordan(aumentada)
    reducida = datos["matriz"]
    pasos = [{
        "tipo": "comparacion_inicio", "titulo": "COMPARACIÓN CON GAUSS-JORDAN",
        "descripcion": "Resolución independiente de [A|b].",
        "etiqueta_matriz": "MATRIZ AUMENTADA [A|b]", "matriz": aumentada,
    }]
    pasos.extend({
        "tipo": "comparacion_operacion", "titulo": "OPERACIÓN DE GAUSS-JORDAN",
        "descripcion": paso["operacion"],
        "etiqueta_matriz": "REDUCCIÓN DE [A|b]", "matriz": paso["matriz"],
    } for paso in datos["proceso"])
    solucion = [fila[-1] for fila in reducida] if len(datos["pivotes"]) == len(A) else None
    coincide = solucion is not None and _matrices_son_iguales(
        [[valor] for valor in solucion], [[valor] for valor in x]
    )
    pasos.append({
        "tipo": "comparacion_final", "titulo": "RESULTADO DE LA COMPARACIÓN",
        "descripcion": (
            "Gauss-Jordan obtiene la misma solución x que LU."
            if coincide else "La solución de Gauss-Jordan no coincide con la obtenida por LU."
        ),
        "etiqueta_matriz": "MATRIZ REDUCIDA DE [A|b]", "matriz": reducida,
    })
    return {"pasos": pasos, "matriz_final": reducida,
            "solucion": solucion, "solucion_coincide": coincide}


def factorizar_y_resolver(A, b):
    """Devuelve LU verificada y, para A cuadrada, la solución o su clasificación."""
    original = _validar_matriz(A)
    filas, columnas = len(original), len(original[0])
    vector = _validar_vector(b, "Todos los elementos de b deben ser números finitos.")
    if len(vector) != filas:
        raise ValueError("El vector b debe tener una componente por cada fila de A.")
    L, U, pasos = factorizar_lu(original)
    reconstruida = producto_matricial(L, U)
    lu_ok = _matrices_son_iguales(reconstruida, original)
    pasos.append({
        "tipo": "verificacion_lu", "titulo": "VERIFICACIÓN L · U = A",
        "descripcion": "La factorización es correcta (L · U == A)." if lu_ok else "L · U no coincide con A.",
        "LU": reconstruida, "correcta": lu_ok,
    })
    resultado = {
        "A": original, "b": vector, "L": L, "U": U, "LU": reconstruida,
        "proceso": pasos, "factorizacion_correcta": lu_ok,
        "y": None, "x": None, "verificacion_sistema": None, "residuo": None,
    }
    if not lu_ok:
        resultado["mensaje_sistema"] = "No se resolvió el sistema porque la verificación L · U = A falló."
        return resultado
    if filas != columnas:
        resultado["mensaje_sistema"] = "La resolución Ax=b mediante LU requiere una matriz cuadrada."
        return resultado
    y, pasos_y = _eliminar_debajo(L, vector, "adelante", "SUSTITUCIÓN HACIA ADELANTE: [L|b]")
    pasos.extend(pasos_y)
    resultado["y"] = y
    aumentada = [U[i][:] + [y[i]] for i in range(filas)]
    columnas_pivote = [
        next(j for j, valor in enumerate(fila) if abs(valor) > TOLERANCIA)
        for fila in U if any(abs(valor) > TOLERANCIA for valor in fila)
    ]
    tipo = clasificar_sistema(aumentada, filas, columnas, columnas_pivote)
    resultado["tipo_sistema"] = tipo
    if tipo != "determinado":
        mensaje = (
            "El sistema tiene infinitas soluciones; no hay una solución única."
            if tipo == "indeterminado" else "El sistema es incompatible: no tiene solución."
        )
        resultado["mensaje_sistema"] = mensaje
        pasos.append({
            "tipo": "diagnostico_sistema", "titulo": "CLASIFICACIÓN DEL SISTEMA",
            "descripcion": mensaje, "etiqueta_matriz": "MATRIZ AUMENTADA [U|y]",
            "matriz": aumentada,
        })
        return resultado
    x, pasos_x = _reducir_a_identidad(aumentada, "atras", "SUSTITUCIÓN HACIA ATRÁS: [U|y]")
    pasos.extend(pasos_x)
    Ax = [fila[0] for fila in producto_matricial(original, [[valor] for valor in x])]
    ok = _matrices_son_iguales([[valor] for valor in Ax], [[valor] for valor in vector])
    resultado.update(x=x, Ax=Ax, verificacion_sistema=ok,
                     residuo=[valor - esperado for valor, esperado in zip(Ax, vector)])
    pasos.append({
        "tipo": "verificacion_sistema", "titulo": "VERIFICACIÓN A · x = b",
        "descripcion": "Comprobación exitosa: A · x == b." if ok else "La comprobación A · x == b no se cumple.",
        "Ax": Ax, "b": vector, "correcta": ok,
    })
    resultado["comparacion_gauss"] = _comparar_con_gauss(original, vector, x)
    return resultado
