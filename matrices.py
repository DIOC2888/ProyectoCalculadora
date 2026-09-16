# matrices.py
# Operaciones matriciales básicas.
# Restricción: únicamente Python estándar.
#
# Este módulo contiene las operaciones solicitadas
# en el Programa 3 de Álgebra Lineal.


from validaciones import (
    validar_matriz,
    validar_mismas_dimensiones_matrices,
    validar_multiplicacion_matrices
)


def sumar_matrices(matrices):
    """
    Suma dos o más matrices.

    Todas las matrices deben tener las mismas dimensiones.
    """

    if not isinstance(matrices, list):
        raise TypeError(
            "Las matrices deben recibirse como una lista."
        )

    if len(matrices) < 2:
        raise ValueError(
            "Se necesitan al menos dos matrices."
        )

    for matriz in matrices:
        validar_matriz(matriz)

    # Todas deben tener la misma dimensión
    for matriz in matrices[1:]:
        validar_mismas_dimensiones_matrices(
            matrices[0],
            matriz
        )

    filas = len(matrices[0])
    columnas = len(matrices[0][0])

    resultado = []

    for i in range(filas):

        fila = []

        for j in range(columnas):

            suma = 0

            for matriz in matrices:

                suma += matriz[i][j]

            fila.append(suma)

        resultado.append(fila)

    return resultado

def restar_matrices(matrices):
    """
    Resta dos o más matrices.

    Realiza:

        A - B - C - ...

    Todas las matrices deben tener las mismas dimensiones.
    """

    if not isinstance(matrices, list):
        raise TypeError(
            "Las matrices deben recibirse como una lista."
        )

    if len(matrices) < 2:
        raise ValueError(
            "Se necesitan al menos dos matrices."
        )

    for matriz in matrices:
        validar_matriz(matriz)

    # Todas deben tener la misma dimensión
    for matriz in matrices[1:]:
        validar_mismas_dimensiones_matrices(
            matrices[0],
            matriz
        )

    filas = len(matrices[0])
    columnas = len(matrices[0][0])

    resultado = []

    for i in range(filas):

        fila = []

        for j in range(columnas):

            valor = matrices[0][i][j]

            for matriz in matrices[1:]:

                valor -= matriz[i][j]

            fila.append(valor)

        resultado.append(fila)

    return resultado
def multiplicar_matrices(matrices):
    """
    Multiplica dos o más matrices.

    Realiza:

        A × B × C × ...

    Las dimensiones deben ser compatibles
    en cada multiplicación consecutiva.
    """

    if not isinstance(matrices, list):
        raise TypeError(
            "Las matrices deben recibirse como una lista."
        )

    if len(matrices) < 2:
        raise ValueError(
            "Se necesitan al menos dos matrices."
        )

    for matriz in matrices:
        validar_matriz(matriz)

    # Comenzamos con la primera matriz
    resultado = matrices[0]

    # Multiplicamos progresivamente
    for matriz in matrices[1:]:

        resultado = _multiplicar_dos_matrices(
            resultado,
            matriz
        )

    return resultado
def _multiplicar_dos_matrices(A, B):
    """
    Multiplica dos matrices A y B.
    """

    validar_multiplicacion_matrices(
        A,
        B
    )

    filas_A = len(A)
    columnas_A = len(A[0])
    columnas_B = len(B[0])

    resultado = []

    for i in range(filas_A):

        fila = []

        for j in range(columnas_B):

            suma = 0

            for k in range(columnas_A):

                suma += (
                    A[i][k] * B[k][j]
                )

            fila.append(suma)

        resultado.append(fila)

    return resultado