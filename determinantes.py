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


def calcular_determinante(A):
    """
    Calcula det(A) por desarrollo de cofactores.

    Devuelve un diccionario con el valor y un proceso resumido para
    mostrar en la interfaz.
    """

    _validar_matriz_cuadrada(A)

    matriz = _copiar_matriz(A)
    n = len(matriz)

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
