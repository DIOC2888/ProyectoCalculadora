"""Factorizacion LU sin pivoteo y resolucion de sistemas cuadrados."""

from config import TOLERANCIA

MENSAJE_PIVOTEO = (
    "La matriz no admite Factorización 𝐿𝑈 sin permutación "
    "(requiere pivoteo parcial 𝑃𝐴 = 𝐿𝑈)"
)


def _texto_operacion_fila(fila_objetivo, fila_origen, factor):
    """Expresa F_i <- F_i - factor*F_j con el signo simplificado."""
    if abs(factor - 1.0) <= TOLERANCIA:
        return f"F{fila_objetivo} ← F{fila_objetivo} − F{fila_origen}"
    if abs(factor + 1.0) <= TOLERANCIA:
        return f"F{fila_objetivo} ← F{fila_objetivo} + F{fila_origen}"
    return f"F{fila_objetivo} ← F{fila_objetivo} − ({factor:g}) · F{fila_origen}"


def _validar_matriz(A):
    if not isinstance(A, (list, tuple)) or not A:
        raise ValueError("La matriz A no puede estar vacía.")
    n = len(A[0])
    if n == 0 or any(not isinstance(f, (list, tuple)) or len(f) != n for f in A):
        raise ValueError("A debe ser una matriz rectangular.")
    try:
        return [[float(x) for x in f] for f in A]
    except (TypeError, ValueError):
        raise ValueError("Todos los elementos de A deben ser numéricos.") from None


def producto_matricial(A, B):
    """Producto matricial local, compatible con la API de matrices."""
    if not A or not B or len(A[0]) != len(B):
        raise ValueError("Las dimensiones no permiten multiplicar las matrices.")
    return [[sum(A[i][k] * B[k][j] for k in range(len(B)))
             for j in range(len(B[0]))] for i in range(len(A))]


def factorizar_lu(A):
    """Retorna U y L por eliminación de filas, sin intercambios."""
    original = _validar_matriz(A)
    m, n = len(original), len(original[0])
    U = [fila[:] for fila in original]
    L = [[1.0 if i == j else 0.0 for j in range(m)] for i in range(m)]
    pasos = [{"tipo": "inicio", "titulo": "MATRIZ ORIGINAL", "descripcion": "Se copia A para iniciar la eliminación por filas.", "A": [f[:] for f in original], "U": [f[:] for f in U], "L": [f[:] for f in L]}]
    for j in range(min(m, n)):
        pivote = U[j][j]
        pasos.append({"tipo": "pivote", "titulo": f"PIVOTE EN LA COLUMNA {j + 1}", "descripcion": f"Pivote = {pivote:g} en la posición ({j + 1}, {j + 1}).", "U": [f[:] for f in U], "L": [f[:] for f in L]})
        if abs(pivote) <= TOLERANCIA:
            if any(abs(U[i][j]) > TOLERANCIA for i in range(j + 1, m)):
                raise ValueError(MENSAJE_PIVOTEO)
            pasos.append({"tipo": "columna_nula", "titulo": "COLUMNA SIN ELIMINACIÓN", "descripcion": "Las entradas debajo del pivote son cero; se continúa sin intercambiar filas.", "U": [f[:] for f in U], "L": [f[:] for f in L]})
            continue
        for i in range(j + 1, m):
            multiplicador = U[i][j] / pivote
            L[i][j] = multiplicador
            U[i] = [U[i][k] - multiplicador * U[j][k] for k in range(n)]
            U[i][j] = 0.0
            pasos.append({"tipo": "eliminacion", "titulo": "OPERACIÓN ELEMENTAL POR FILAS", "descripcion": _texto_operacion_fila(i + 1, j + 1, multiplicador), "multiplicador": multiplicador, "fila_objetivo": i, "fila_pivote": j, "U": [f[:] for f in U], "L": [f[:] for f in L]})
    pasos.append({"tipo": "factorizacion", "titulo": "FACTORIZACIÓN CONSTRUIDA", "descripcion": "L registra los multiplicadores y U es la forma escalonada de A.", "U": [f[:] for f in U], "L": [f[:] for f in L]})
    return L, U, pasos


def _sustitucion_inferior(L, b):
    y = []
    pasos = []
    for i, fila in enumerate(L):
        terminos = [f"({fila[j]:g})({y[j]:g})" for j in range(i)]
        numerador = f"{b[i]:g}" + (" − " + " − ".join(terminos) if terminos else "")
        y.append((b[i] - sum(fila[j] * y[j] for j in range(i))) / fila[i])
        pasos.append({"tipo": "adelante", "titulo": f"SUSTITUCIÓN HACIA ADELANTE · FILA {i + 1}", "descripcion": f"y{i + 1} = ({numerador}) / {fila[i]:g} = {y[i]:g}", "y": y[:]})
    return y, pasos


def _sustitucion_superior(U, y):
    n = len(U)
    x = [0.0] * n
    pasos = []
    for i in range(n - 1, -1, -1):
        if abs(U[i][i]) <= TOLERANCIA:
            raise ValueError("El sistema no tiene solución única: U tiene pivote cero.")
        terminos = [f"({U[i][j]:g})({x[j]:g})" for j in range(i + 1, n)]
        numerador = f"{y[i]:g}" + (" − " + " − ".join(terminos) if terminos else "")
        x[i] = (y[i] - sum(U[i][j] * x[j] for j in range(i + 1, n))) / U[i][i]
        pasos.append({"tipo": "atras", "titulo": f"SUSTITUCIÓN HACIA ATRÁS · FILA {i + 1}", "descripcion": f"x{i + 1} = ({numerador}) / {U[i][i]:g} = {x[i]:g}", "x": x[:]})
    return x, pasos


def _reduccion_ordinaria_aumentada(A, b):
    """Reducción ordinaria de [A|b], conservando cada operación elemental."""
    matriz = [fila[:] + [b[i]] for i, fila in enumerate(A)]
    pasos = [{"tipo": "comparacion_inicio", "titulo": "MATRIZ AUMENTADA [A|b]", "descripcion": "Se inicia la reducción ordinaria del sistema.", "matriz": [fila[:] for fila in matriz]}]
    n = len(A)
    for j in range(n):
        pivote = matriz[j][j]
        if abs(pivote) <= TOLERANCIA:
            raise ValueError(MENSAJE_PIVOTEO)
        for i in range(j + 1, n):
            multiplicador = matriz[i][j] / pivote
            matriz[i] = [matriz[i][k] - multiplicador * matriz[j][k] for k in range(n + 1)]
            matriz[i][j] = 0.0
            pasos.append({"tipo": "comparacion_eliminacion", "titulo": "REDUCCIÓN ORDINARIA DE [A|b]", "descripcion": _texto_operacion_fila(i + 1, j + 1, multiplicador), "matriz": [fila[:] for fila in matriz]})
    matriz_escalonada = [fila[:] for fila in matriz]
    pasos.append({"tipo": "comparacion_escalonada", "titulo": "FORMA ESCALONADA [U|y]", "descripcion": "La reducción ordinaria produce la misma matriz U y el mismo vector y.", "matriz": [fila[:] for fila in matriz]})
    solucion, pasos_atras = _reducir_a_identidad(matriz, "comparacion_atras", "RESOLUCIÓN ORDINARIA: SUSTITUCIÓN HACIA ATRÁS")
    pasos.extend(pasos_atras)
    pasos.append({"tipo": "comparacion_final", "titulo": "SOLUCIÓN POR REDUCCIÓN ORDINARIA", "descripcion": "La solución coincide con la obtenida mediante LU.", "matriz": [fila[:] for fila in matriz], "solucion": solucion[:]})
    return {"pasos": pasos, "matriz_final": matriz_escalonada, "coincide_con_LU": True, "solucion": solucion}


def _reducir_a_identidad(matriz_aumentada, tipo, titulo):
    """Aplica Gauss-Jordan sin intercambios y retorna la última columna."""
    matriz = [fila[:] for fila in matriz_aumentada]
    n = len(matriz)
    pasos = [{"tipo": tipo + "_inicio", "titulo": titulo, "descripcion": "Matriz aumentada inicial.", "matriz": [fila[:] for fila in matriz]}]
    for j in range(n):
        pivote = matriz[j][j]
        if abs(pivote) <= TOLERANCIA:
            raise ValueError(MENSAJE_PIVOTEO)
        if abs(pivote - 1.0) > TOLERANCIA:
            matriz[j] = [valor / pivote for valor in matriz[j]]
            pasos.append({"tipo": tipo + "_normalizar", "titulo": "NORMALIZAR FILA PIVOTE", "descripcion": f"F{j + 1} ← (1/({pivote:g})) · F{j + 1}", "matriz": [fila[:] for fila in matriz]})
        for i in range(n):
            if i == j or abs(matriz[i][j]) <= TOLERANCIA:
                continue
            factor = matriz[i][j]
            matriz[i] = [matriz[i][k] - factor * matriz[j][k] for k in range(n + 1)]
            matriz[i][j] = 0.0
            pasos.append({"tipo": tipo + "_eliminar", "titulo": "ELIMINAR SOBRE EL PIVOTE", "descripcion": _texto_operacion_fila(i + 1, j + 1, factor), "matriz": [fila[:] for fila in matriz]})
    solucion = [matriz[i][-1] for i in range(n)]
    pasos.append({"tipo": tipo + "_final", "titulo": "MATRIZ IDENTIDAD Y SOLUCIÓN", "descripcion": "La matriz de coeficientes quedó reducida a I.", "matriz": [fila[:] for fila in matriz]})
    return solucion, pasos


def _eliminar_debajo(matriz_coeficientes, b, tipo, titulo):
    """Resuelve un sistema triangular inferior mediante F_i <- F_i-lF_j."""
    matriz = [fila[:] + [b[i]] for i, fila in enumerate(matriz_coeficientes)]
    pasos = [{"tipo": tipo + "_inicio", "titulo": titulo, "descripcion": "Matriz aumentada inicial.", "matriz": [fila[:] for fila in matriz]}]
    n = len(matriz)
    for j in range(n):
        pivote = matriz[j][j]
        if abs(pivote) <= TOLERANCIA:
            raise ValueError("No se puede continuar la sustitución: hay un pivote cero.")
        for i in range(j + 1, n):
            factor = matriz[i][j] / pivote
            if abs(factor) <= TOLERANCIA:
                matriz[i][j] = 0.0
                continue
            matriz[i] = [matriz[i][k] - factor * matriz[j][k] for k in range(n + 1)]
            matriz[i][j] = 0.0
            pasos.append({"tipo": tipo + "_eliminar", "titulo": "SUSTITUCIÓN HACIA ADELANTE", "descripcion": _texto_operacion_fila(i + 1, j + 1, factor), "matriz": [fila[:] for fila in matriz]})
    vector = [matriz[i][-1] for i in range(n)]
    pasos.append({"tipo": tipo + "_final", "titulo": "VECTOR INTERMEDIO y", "descripcion": "La última columna de la matriz identidad es y.", "matriz": [fila[:] for fila in matriz], "y": vector[:]})
    return vector, pasos


def factorizar_y_resolver(A, b):
    """Factoriza A y, cuando A es cuadrada, resuelve Ax=b."""
    original = _validar_matriz(A)
    m, n = len(original), len(original[0])
    if len(b) != m:
        raise ValueError("El vector b debe tener una componente por cada fila de A.")
    try:
        vector = [float(v) for v in b]
    except (TypeError, ValueError):
        raise ValueError("Todos los elementos de b deben ser numéricos.") from None
    L, U, pasos = factorizar_lu(original)
    reconstruida = producto_matricial(L, U)
    lu_ok = all(abs(reconstruida[i][j] - original[i][j]) <= TOLERANCIA
                for i in range(m) for j in range(n))
    pasos.append({"tipo": "verificacion_lu", "titulo": "VERIFICACIÓN L · U = A", "descripcion": "La factorización es correcta (L · U == A)." if lu_ok else "L · U no coincide con A.", "LU": [f[:] for f in reconstruida], "correcta": lu_ok})
    resultado = {"A": original, "L": L, "U": U, "LU": reconstruida, "proceso": pasos,
                 "factorizacion_correcta": lu_ok, "y": None, "x": None,
                 "verificacion_sistema": None, "residuo": None}
    if m != n:
        resultado["mensaje_sistema"] = "La resolución Ax=b mediante LU requiere una matriz cuadrada."
        return resultado
    pasos.append({"tipo": "vector_b", "titulo": "VECTOR DE TÉRMINOS INDEPENDIENTES", "descripcion": "Resolver L y = b mediante operaciones fila.", "b": vector[:]})
    y, pasos_y = _eliminar_debajo(L, vector, "adelante", "SUSTITUCIÓN HACIA ADELANTE: [L|b]")
    pasos.extend(pasos_y)
    pasos.append({"tipo": "vector_y", "titulo": "VECTOR INTERMEDIO y", "descripcion": "Se toma la última columna al reducir [L|b] a [I|y].", "y": y[:]})
    matriz_Uy = [U[i][:] + [y[i]] for i in range(n)]
    x, pasos_x = _reducir_a_identidad(matriz_Uy, "atras", "SUSTITUCIÓN HACIA ATRÁS: [U|y]")
    pasos.extend(pasos_x)
    Ax = [sum(original[i][j] * x[j] for j in range(n)) for i in range(n)]
    ok = all(abs(Ax[i] - vector[i]) <= TOLERANCIA for i in range(n))
    resultado.update(y=y, x=x, Ax=Ax, b=vector, verificacion_sistema=ok,
                      residuo=[Ax[i] - vector[i] for i in range(n)])
    pasos.append({"tipo": "verificacion_sistema", "titulo": "VERIFICACIÓN A · x = b", "descripcion": "Comprobación exitosa: A · x == b." if ok else "La comprobación A · x == b no se cumple.", "Ax": Ax[:], "b": vector[:], "correcta": ok})
    comparacion = _reduccion_ordinaria_aumentada(original, vector)
    comparacion["coincide_con_LU"] = all(
        abs(comparacion["matriz_final"][i][j] - U[i][j]) <= TOLERANCIA
        for i in range(n) for j in range(n)
    ) and all(abs(comparacion["matriz_final"][i][-1] - y[i]) <= TOLERANCIA for i in range(n))
    comparacion["solucion_coincide"] = all(abs(comparacion["solucion"][i] - x[i]) <= TOLERANCIA for i in range(n))
    resultado["comparacion_gauss"] = comparacion
    pasos.extend(comparacion["pasos"])
    return resultado
