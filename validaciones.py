
# validaciones.py
# Validaciones básicas para vectores y matrices.
# Se utiliza únicamente Python estándar.


def validar_vector(vector):
    """
    Verifica que el objeto recibido sea un vector no vacío.

    Procedimiento algebraico equivalente:
    Un vector de R^n posee n componentes.
    """
    if not isinstance(vector, list):
        raise TypeError("El vector debe estar representado como una lista.")

    if len(vector) == 0:
        raise ValueError("El vector no puede estar vacío.")

    for componente in vector:
        if not isinstance(componente, (int, float)):
            raise TypeError(
                "Todas las componentes del vector deben ser números."
            )


def validar_mismos_tamanos_vectores(v1, v2):
    """
    Verifica que dos vectores pertenezcan al mismo R^n.

    Procedimiento algebraico:
    Para sumar o restar vectores, ambos deben tener la misma dimensión.
    """
    validar_vector(v1)
    validar_vector(v2)

    if len(v1) != len(v2):
        raise ValueError(
            "Los vectores deben tener la misma cantidad de componentes."
        )


def validar_matriz(matriz):
    """
    Verifica que una matriz tenga forma rectangular m x n.

    Procedimiento algebraico:
    Una matriz debe tener filas y columnas bien definidas;
    todas sus filas deben contener la misma cantidad de elementos.
    """
    if not isinstance(matriz, list):
        raise TypeError(
            "La matriz debe estar representada como una lista."
        )

    if len(matriz) == 0:
        raise ValueError("La matriz no puede estar vacía.")

    if not isinstance(matriz[0], list) or len(matriz[0]) == 0:
        raise ValueError(
            "La matriz debe contener filas no vacías."
        )

    columnas = len(matriz[0])

    for fila in matriz:

        if not isinstance(fila, list):
            raise TypeError(
                "Todas las filas de la matriz deben ser listas."
            )

        if len(fila) != columnas:
            raise ValueError(
                "Todas las filas deben tener la misma cantidad "
                "de columnas."
            )

        for elemento in fila:

            if not isinstance(elemento, (int, float)):
                raise TypeError(
                    "Todos los elementos de la matriz deben ser números."
                )


def validar_mismas_dimensiones_matrices(A, B):
    """
    Verifica que dos matrices tengan las mismas dimensiones.

    Procedimiento algebraico:
    A + B y A - B solo están definidas cuando ambas matrices
    son m x n.
    """
    filas_A, columnas_A = dimensiones_matriz(A)
    filas_B, columnas_B = dimensiones_matriz(B)

    if filas_A != filas_B or columnas_A != columnas_B:
        raise ValueError(
            "Las matrices deben tener las mismas dimensiones."
        )


def validar_multiplicacion_matrices(A, B):
    """
    Verifica la condición de multiplicación matricial.

    Procedimiento algebraico:
    Si A es m x n y B es n x p, entonces A·B está definida.

    Por ello:

        columnas(A) = filas(B)
    """
    _, columnas_A = dimensiones_matriz(A)
    filas_B, _ = dimensiones_matriz(B)

    if columnas_A != filas_B:
        raise ValueError(
            "No se pueden multiplicar las matrices: "
            "las columnas de A deben ser iguales a las filas de B."
        )


def dimensiones_matriz(matriz):
    """
    Devuelve las dimensiones de una matriz:

        (cantidad_de_filas, cantidad_de_columnas)
    """
    validar_matriz(matriz)

    return len(matriz), len(matriz[0])
