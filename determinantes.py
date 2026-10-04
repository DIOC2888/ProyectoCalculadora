# determinantes.py
# Calculo de determinantes sin librerias externas.

from config import TOLERANCIA
from formato import formatear_numero
from validaciones import validar_matriz


def _copiar_matriz(matriz):
    """Crea una copia para no alterar la matriz recibida."""

    return [
        fila[:]
        for fila in matriz
    ]


def _formatear(valor):
    """Usa el formateo matematico comun cuando el valor es numerico."""

    if isinstance(valor, (int, float)):
        return formatear_numero(valor)

    return str(valor)


def _validar_matriz_cuadrada(A):
    """Garantiza que det(A) solo se calcule para matrices cuadradas."""

    validar_matriz(A)

    filas = len(A)
    columnas = len(A[0])

    if filas != columnas:
        raise ValueError(
            "El determinante solo se puede calcular en matrices cuadradas."
        )


def _menor(A, fila_eliminar, columna_eliminar):
    """Construye M_ij eliminando una fila y una columna."""

    return [
        [
            valor
            for j, valor in enumerate(fila)
            if j != columna_eliminar
        ]
        for i, fila in enumerate(A)
        if i != fila_eliminar
    ]


def _determinante_recursivo(A):
    """Calcula determinantes de menores sin guardar pasos de interfaz."""

    n = len(A)

    if n == 1:
        return A[0][0]

    if n == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]

    # Se elige la fila con mas ceros para reducir llamadas recursivas.
    fila_desarrollo = max(
        range(n),
        key=lambda i: sum(
            1
            for valor in A[i]
            if abs(valor) <= TOLERANCIA
        )
    )

    total = 0

    for columna, elemento in enumerate(A[fila_desarrollo]):
        if abs(elemento) <= TOLERANCIA:
            continue

        # termino = a_ij * C_ij, con C_ij = (-1)^(i+j) det(M_ij).
        signo = -1 if (fila_desarrollo + columna) % 2 else 1
        total += (
            signo
            * elemento
            * _determinante_recursivo(
                _menor(A, fila_desarrollo, columna)
            )
        )

    return 0 if abs(total) <= TOLERANCIA else total


def _determinante_sarrus(A):
    """Calcula el determinante 3x3 con la regla de Sarrus y sus pasos."""
    a, b, c = A[0]
    d, e, f = A[1]
    g, h, i = A[2]
    positivos = (a * e * i, b * f * g, c * d * h)
    negativos = (c * e * g, b * d * i, a * f * h)
    valor = sum(positivos) - sum(negativos)
    if abs(valor) <= TOLERANCIA:
        valor = 0
    detalle = (
        f"Diagonales descendentes: {_formatear(a)}·{_formatear(e)}·{_formatear(i)} "
        f"+ {_formatear(b)}·{_formatear(f)}·{_formatear(g)} "
        f"+ {_formatear(c)}·{_formatear(d)}·{_formatear(h)} "
        f"= {_formatear(sum(positivos))}\n"
        f"Diagonales ascendentes: {_formatear(c)}·{_formatear(e)}·{_formatear(g)} "
        f"+ {_formatear(b)}·{_formatear(d)}·{_formatear(i)} "
        f"+ {_formatear(a)}·{_formatear(f)}·{_formatear(h)} "
        f"= {_formatear(sum(negativos))}\n"
        f"det(A) = {_formatear(sum(positivos))} - "
        f"{_formatear(sum(negativos))} = {_formatear(valor)}"
    )
    return valor, detalle


def _determinante_triangular(A):
    """Reduce por operaciones de fila y conserva signo y pivotes."""
    matriz = _copiar_matriz(A)
    n = len(matriz)
    intercambios = 0
    proceso = []
    pivotes = []

    for columna in range(n):
        fila_pivote = max(
            range(columna, n),
            key=lambda fila: abs(matriz[fila][columna])
        )
        if abs(matriz[fila_pivote][columna]) <= TOLERANCIA:
            pivotes.append(0)
            proceso.append({
                "tipo": "formula", "titulo": "PIVOTE NULO",
                "operacion": f"Columna {columna + 1}",
                "detalle": "No hay pivote distinto de cero; det(A) = 0."
            })
            return 0, proceso, intercambios, pivotes, matriz

        if fila_pivote != columna:
            matriz[columna], matriz[fila_pivote] = matriz[fila_pivote], matriz[columna]
            intercambios += 1
            proceso.append({
                "tipo": "operacion_fila",
                "titulo": "Intercambio de filas",
                "operacion": f"F{columna + 1} ↔ F{fila_pivote + 1}; cambia el signo del determinante",
                "matriz": _copiar_matriz(matriz)
            })

        pivote = matriz[columna][columna]
        pivotes.append(pivote)
        for fila in range(columna + 1, n):
            factor = matriz[fila][columna] / pivote
            matriz[fila] = [
                matriz[fila][j] - factor * matriz[columna][j]
                for j in range(n)
            ]
            matriz[fila][columna] = 0
            proceso.append({
                "tipo": "operacion_fila",
                "titulo": "Anular entrada bajo el pivote",
                "operacion": (
                    f"F{fila + 1} ← F{fila + 1} - "
                    f"({_formatear(factor)})F{columna + 1}"
                ),
                "matriz": _copiar_matriz(matriz)
            })

    producto_diagonal = 1
    for pivote in pivotes:
        producto_diagonal *= pivote
    valor = (-1 if intercambios % 2 else 1) * producto_diagonal
    if abs(valor) <= TOLERANCIA:
        valor = 0
    proceso.append({
        "tipo": "formula",
        "titulo": "Determinante desde la forma triangular",
        "operacion": "det(A) = (-1)^s · producto de los pivotes",
        "detalle": (
            f"Intercambios s = {intercambios}; pivotes = "
            f"{' · '.join(_formatear(p) for p in pivotes)}; "
            f"det(A) = {'-1' if intercambios % 2 else '1'} · "
            f"{_formatear(producto_diagonal)} = {_formatear(valor)}"
        )
    })
    return valor, proceso, intercambios, pivotes, matriz


def calcular_determinante(A, metodo="cofactores"):
    """
    Calcula det(A) usando solo el método solicitado.

    metodo admite "cofactores", "triangular" o "sarrus" (solo 3x3).
    Devuelve el valor calculado y los pasos para mostrar en la interfaz.
    """

    _validar_matriz_cuadrada(A)

    matriz = _copiar_matriz(A)
    n = len(matriz)

    if metodo == "triangular":
        determinante, pasos, intercambios, pivotes, triangular = (
            _determinante_triangular(matriz)
        )
        proceso = [{
            "numero": 1, "tipo": "inicio", "titulo": "MATRIZ ORIGINAL",
            "operacion": "A", "matriz": _copiar_matriz(matriz)
        }, {
            "numero": 2, "tipo": "formula",
            "titulo": "REDUCCIÓN A FORMA TRIANGULAR",
            "operacion": "Usar operaciones de fila y producto diagonal"
        }]
        for paso in pasos:
            paso["numero"] = len(proceso) + 1
            proceso.append(paso)
        proceso.append({
            "numero": len(proceso) + 1, "tipo": "determinante",
            "titulo": "RESULTADO", "operacion": "det(A)",
            "detalle": f"det(A) = {_formatear(determinante)}",
            "valor": determinante
        })
        return {
            "determinante": determinante, "resultado": determinante,
            "matriz": matriz, "metodo": metodo,
            "intercambios_filas": intercambios,
            "factores_diagonales": pivotes,
            "matriz_triangular": triangular, "proceso": proceso
        }

    if metodo == "sarrus":
        if n != 3:
            raise ValueError("La regla de Sarrus solo se aplica a matrices 3x3.")
        determinante, detalle = _determinante_sarrus(matriz)
        proceso = [{
            "numero": 1, "tipo": "inicio", "titulo": "MATRIZ ORIGINAL",
            "operacion": "A", "matriz": _copiar_matriz(matriz)
        }, {
            "numero": 2, "tipo": "formula", "titulo": "REGLA DE SARRUS",
            "operacion": "Diagonales descendentes menos ascendentes",
            "detalle": detalle
        }, {
            "numero": 3, "tipo": "determinante", "titulo": "RESULTADO",
            "operacion": "det(A)",
            "detalle": f"det(A) = {_formatear(determinante)}",
            "valor": determinante
        }]
        return {
            "determinante": determinante, "resultado": determinante,
            "matriz": matriz, "metodo": metodo, "proceso": proceso
        }

    if metodo != "cofactores":
        raise ValueError("Selecciona cofactores, forma triangular o Sarrus.")

    proceso = [{
        "numero": 1,
        "tipo": "inicio",
        "titulo": "MATRIZ ORIGINAL",
        "operacion": "A",
        "matriz": _copiar_matriz(matriz)
    }]

    if n == 1:
        determinante = matriz[0][0]
        proceso.append({
            "numero": 2,
            "tipo": "formula",
            "titulo": "DETERMINANTE 1x1",
            "operacion": f"det(A) = {_formatear(determinante)}",
            "detalle": f"det(A) = {_formatear(determinante)}"
        })

        return {
            "determinante": determinante,
            "resultado": determinante,
            "matriz": matriz,
            "metodo": "cofactores",
            "fila_desarrollo": 0,
            "cofactores": [],
            "proceso": proceso
        }

    if n == 2:
        a, b = matriz[0]
        c, d = matriz[1]
        determinante = a * d - b * c
        determinante = 0 if abs(determinante) <= TOLERANCIA else determinante
        proceso.append({
            "numero": 2,
            "tipo": "formula",
            "titulo": "DETERMINANTE 2x2",
            "operacion": "det(A) = ad - bc",
            "detalle": (
                f"det(A) = {_formatear(a)}*{_formatear(d)} - "
                f"{_formatear(b)}*{_formatear(c)}\n"
                f"det(A) = {_formatear(a * d)} - "
                f"{_formatear(b * c)} = {_formatear(determinante)}"
            )
        })

        return {
            "determinante": determinante,
            "resultado": determinante,
            "matriz": matriz,
            "metodo": "cofactores",
            "fila_desarrollo": 0,
            "cofactores": [],
            "proceso": proceso
        }

    # Igual que en el calculo interno, se desarrolla por la fila mas simple.
    fila_desarrollo = max(
        range(n),
        key=lambda i: sum(
            1
            for valor in matriz[i]
            if abs(valor) <= TOLERANCIA
        )
    )
    cofactores = []
    terminos_texto = []
    total = 0

    proceso.append({
        "numero": 2,
        "tipo": "formula",
        "titulo": "FILA DE DESARROLLO",
        "operacion": f"Se desarrolla por F{fila_desarrollo + 1}",
        "detalle": (
            "Se elige la fila "
            f"{fila_desarrollo + 1} porque facilita el desarrollo "
            "por cofactores."
        )
    })

    for columna, elemento in enumerate(matriz[fila_desarrollo]):
        # Desarrollo por cofactores:
        # 1. Tomar el elemento a_ij.
        # 2. Construir el menor M_ij.
        # 3. Calcular C_ij = (-1)^(i+j) det(M_ij).
        # 4. Sumar a_ij * C_ij al determinante.
        signo = -1 if (fila_desarrollo + columna) % 2 else 1
        menor = _menor(matriz, fila_desarrollo, columna)
        det_menor = _determinante_recursivo(menor)
        cofactor = signo * det_menor
        termino = elemento * cofactor

        if abs(termino) <= TOLERANCIA:
            termino = 0

        # Se acumula la suma de todos los terminos de la fila elegida.
        total += termino

        signo_texto = "+" if signo > 0 else "-"
        detalle = (
            f"a{fila_desarrollo + 1}{columna + 1} = {_formatear(elemento)}\n"
            f"C{fila_desarrollo + 1}{columna + 1} = "
            f"({signo_texto}) det(M{fila_desarrollo + 1}{columna + 1})\n"
            f"det(M{fila_desarrollo + 1}{columna + 1}) = "
            f"{_formatear(det_menor)}\n"
            f"Termino = {_formatear(elemento)} * "
            f"{_formatear(cofactor)} = {_formatear(termino)}"
        )

        cofactores.append({
            "fila": fila_desarrollo,
            "columna": columna,
            "elemento": elemento,
            "signo": signo,
            "menor": menor,
            "determinante_menor": det_menor,
            "cofactor": cofactor,
            "termino": termino
        })

        proceso.append({
            "numero": len(proceso) + 1,
            "tipo": "formula",
            "titulo": f"COFACTOR C{fila_desarrollo + 1}{columna + 1}",
            "operacion": (
                f"a{fila_desarrollo + 1}{columna + 1}"
                f"C{fila_desarrollo + 1}{columna + 1}"
            ),
            "detalle": detalle
        })

        # Para mostrar la expresion final se omiten terminos nulos.
        if termino:
            terminos_texto.append(_formatear(termino))

    determinante = 0 if abs(total) <= TOLERANCIA else total
    expresion = " + ".join(terminos_texto) if terminos_texto else "0"

    proceso.append({
        "numero": len(proceso) + 1,
        "tipo": "determinante",
        "titulo": "RESULTADO",
        "operacion": (
            f"det(A) = {expresion} = {_formatear(determinante)}"
        ),
        "detalle": (
            f"det(A) = {expresion}\n"
            f"det(A) = {_formatear(determinante)}"
        ),
        "valor": determinante
    })

    return {
        "determinante": determinante,
        "resultado": determinante,
        "matriz": matriz,
        "metodo": "cofactores",
        "fila_desarrollo": fila_desarrollo,
        "cofactores": cofactores,
        "proceso": proceso
    }


def resolver_sistema_cramer(A, b):
    """Resuelve Ax=b por Cramer y conserva el desarrollo de cada determinante."""
    _validar_matriz_cuadrada(A)
    if not isinstance(b, (list, tuple)) or len(b) != len(A):
        raise ValueError("El vector b debe tener una entrada por cada ecuación.")
    if any(not isinstance(valor, (int, float)) for valor in b):
        raise ValueError("Las entradas del vector b deben ser numéricas.")

    matriz = _copiar_matriz(A)
    vector = list(b)
    base = calcular_determinante(matriz, "cofactores")
    proceso = [{
        "numero": 1, "tipo": "inicio", "titulo": "SISTEMA Ax = b",
        "operacion": "Aplicar la regla de Cramer",
        "matriz": [fila[:] + [vector[i]] for i, fila in enumerate(matriz)]
    }]
    proceso.append({
        "numero": 2, "tipo": "formula", "titulo": "DETERMINANTE PRINCIPAL",
        "operacion": "D = det(A)", "detalle": f"D = { _formatear(base['determinante']) }"
    })
    for paso in base["proceso"][1:]:
        paso_copia = dict(paso)
        paso_copia["numero"] = len(proceso) + 1
        paso_copia["titulo"] = f"D: {paso_copia.get('titulo', 'Paso')}"
        proceso.append(paso_copia)

    if abs(base["determinante"]) <= TOLERANCIA:
        proceso.append({
            "numero": len(proceso) + 1, "tipo": "singular",
            "titulo": "No hay solución única por Cramer",
            "operacion": "det(A) = 0"
        })
        return {
            "exito": True, "operacion": "Cramer", "solucion": None,
            "determinante": base["determinante"], "determinantes_reemplazo": [],
            "proceso": proceso,
            "mensaje": "det(A) = 0; la regla de Cramer no determina una solución única."
        }

    determinantes = []
    solucion = []
    for columna in range(len(matriz)):
        reemplazada = _copiar_matriz(matriz)
        for fila in range(len(matriz)):
            reemplazada[fila][columna] = vector[fila]
        datos = calcular_determinante(reemplazada, "cofactores")
        d_j = datos["determinante"]
        x_j = d_j / base["determinante"]
        determinantes.append(d_j)
        solucion.append(0 if isinstance(x_j, float) and abs(x_j) <= TOLERANCIA else x_j)
        proceso.append({
            "numero": len(proceso) + 1, "tipo": "inicio",
            "titulo": f"REEMPLAZAR COLUMNA {columna + 1}",
            "operacion": f"D{columna + 1} = det(A{columna + 1})",
            "matriz": reemplazada
        })
        for paso in datos["proceso"][1:]:
            paso_copia = dict(paso)
            paso_copia["numero"] = len(proceso) + 1
            paso_copia["titulo"] = f"D{columna + 1}: {paso_copia.get('titulo', 'Paso')}"
            proceso.append(paso_copia)
        proceso.append({
            "numero": len(proceso) + 1, "tipo": "formula",
            "titulo": f"CALCULAR x{columna + 1}",
            "operacion": f"x{columna + 1} = D{columna + 1} / D",
            "detalle": (
                f"x{columna + 1} = {_formatear(d_j)} / "
                f"{_formatear(base['determinante'])} = {_formatear(solucion[-1])}"
            )
        })

    proceso.append({
        "numero": len(proceso) + 1, "tipo": "resultado",
        "titulo": "SOLUCIÓN", "operacion": "x",
        "resultado": solucion
    })
    return {
        "exito": True, "operacion": "Cramer", "solucion": solucion,
        "resultado": solucion, "determinante": base["determinante"],
        "determinantes_reemplazo": determinantes,
        "proceso": proceso, "mensaje": "Solución calculada por la regla de Cramer."
    }
