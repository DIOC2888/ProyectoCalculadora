# matrices.py
# Operaciones matriciales básicas.
# Restricción: únicamente Python estándar.
#
# Este módulo contiene las operaciones solicitadas
# en el Programa 3 de Álgebra Lineal.
#
# Las funciones devuelven:
#
#   resultado
#   proceso
#
# El proceso contiene los pasos matemáticos necesarios
# para que la interfaz pueda mostrarlos posteriormente.


from validaciones import (
    validar_matriz,
    validar_mismas_dimensiones_matrices,
    validar_multiplicacion_matrices
)
from formato import formatear_numero


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def _formatear_numero(valor):
    """
    Convierte un número a texto de forma limpia.

    Ejemplos:

        2.0  -> "2"
        2.5  -> "2.5"
        -3.0 -> "-3"
    """

    if isinstance(valor, (int, float)):
        return formatear_numero(valor)

    return str(valor)


def _copiar_matriz(matriz):
    """
    Realiza una copia de una matriz para evitar modificar
    accidentalmente la matriz original.
    """

    return [
        fila[:]
        for fila in matriz
    ]


# ============================================================
# SUMA DE MATRICES
# ============================================================

def sumar_matrices(matrices):
    """
    Suma dos o más matrices.

    Todas las matrices deben tener las mismas dimensiones.

    Ejemplo:

        A + B + C

    Devuelve:

        {
            "resultado": matriz_resultado,
            "proceso": [...]
        }
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

    # Verificar que todas tengan la misma dimensión
    for matriz in matrices[1:]:
        validar_mismas_dimensiones_matrices(
            matrices[0],
            matriz
        )

    filas = len(matrices[0])
    columnas = len(matrices[0][0])

    # --------------------------------------------------------
    # PROCESO
    # --------------------------------------------------------

    proceso = []

    # Paso 1: operación matricial
    nombres = []

    for i in range(len(matrices)):
        nombres.append(
            f"M{i + 1}"
        )

    proceso.append({
        "numero": 1,
        "tipo": "operacion",
        "titulo": "OPERACIÓN MATRICIAL",
        "operacion": " + ".join(nombres),
        "matrices": [
            _copiar_matriz(matriz)
            for matriz in matrices
        ]
    })

    # --------------------------------------------------------
    # PASO 2: componente a componente
    # --------------------------------------------------------

    componentes = []

    for i in range(filas):

        fila = []

        for j in range(columnas):

            valores = []

            for matriz in matrices:

                valores.append(
                    _formatear_numero(
                        matriz[i][j]
                    )
                )

            expresion = " + ".join(
                valores
            )

            fila.append(
                expresion
            )

        componentes.append(
            fila
        )

    proceso.append({
        "numero": 2,
        "tipo": "componentes",
        "titulo": "SUMA DE COMPONENTES",
        "operacion": componentes
    })

    # --------------------------------------------------------
    # RESULTADO
    # --------------------------------------------------------

    resultado = []

    for i in range(filas):

        fila = []

        for j in range(columnas):

            suma = 0

            for matriz in matrices:

                suma += matriz[i][j]

            fila.append(
                suma
            )

        resultado.append(
            fila
        )

    proceso.append({
        "numero": 3,
        "tipo": "resultado",
        "titulo": "RESULTADO",
        "matriz": _copiar_matriz(
            resultado
        )
    })

    return {
        "resultado": resultado,
        "proceso": proceso
    }


# ============================================================
# RESTA DE MATRICES
# ============================================================

def restar_matrices(matrices):
    """
    Resta dos o más matrices.

    Realiza:

        A - B - C - ...

    Todas las matrices deben tener las mismas dimensiones.

    Devuelve:

        {
            "resultado": matriz_resultado,
            "proceso": [...]
        }
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

    # Verificar dimensiones
    for matriz in matrices[1:]:
        validar_mismas_dimensiones_matrices(
            matrices[0],
            matriz
        )

    filas = len(matrices[0])
    columnas = len(matrices[0][0])

    proceso = []

    # --------------------------------------------------------
    # PASO 1: OPERACIÓN MATRICIAL
    # --------------------------------------------------------

    nombres = []

    for i in range(len(matrices)):
        nombres.append(
            f"M{i + 1}"
        )

    proceso.append({
        "numero": 1,
        "tipo": "operacion",
        "titulo": "OPERACIÓN MATRICIAL",
        "operacion": " − ".join(nombres),
        "matrices": [
            _copiar_matriz(matriz)
            for matriz in matrices
        ]
    })

    # --------------------------------------------------------
    # PASO 2: COMPONENTE A COMPONENTE
    # --------------------------------------------------------

    componentes = []

    for i in range(filas):

        fila = []

        for j in range(columnas):

            valores = []

            for matriz in matrices:

                valores.append(
                    _formatear_numero(
                        matriz[i][j]
                    )
                )

            expresion = " − ".join(
                valores
            )

            fila.append(
                expresion
            )

        componentes.append(
            fila
        )

    proceso.append({
        "numero": 2,
        "tipo": "componentes",
        "titulo": "RESTA DE COMPONENTES",
        "operacion": componentes
    })

    # --------------------------------------------------------
    # RESULTADO
    # --------------------------------------------------------

    resultado = []

    for i in range(filas):

        fila = []

        for j in range(columnas):

            valor = matrices[0][i][j]

            for matriz in matrices[1:]:

                valor -= matriz[i][j]

            fila.append(
                valor
            )

        resultado.append(
            fila
        )

    proceso.append({
        "numero": 3,
        "tipo": "resultado",
        "titulo": "RESULTADO",
        "matriz": _copiar_matriz(
            resultado
        )
    })

    return {
        "resultado": resultado,
        "proceso": proceso
    }


# ============================================================
# MULTIPLICACIÓN DE MATRIZ POR ESCALAR
# ============================================================

def multiplicar_matriz_escalar(
    matriz,
    escalar
):
    """
    Multiplica una matriz por un escalar.

    Realiza:

        kA

    donde:

        k = escalar
        A = matriz
    """

    validar_matriz(matriz)

    if not isinstance(
        escalar,
        (int, float)
    ):
        raise TypeError(
            "El escalar debe ser un número."
        )

    filas = len(matriz)
    columnas = len(matriz[0])

    proceso = []

    # --------------------------------------------------------
    # PASO 1: OPERACIÓN MATRICIAL
    # --------------------------------------------------------

    proceso.append({
        "numero": 1,
        "tipo": "operacion",
        "titulo": "OPERACIÓN MATRICIAL",
        "operacion": (
            f"{_formatear_numero(escalar)} · M1"
        ),
        "matriz": _copiar_matriz(
            matriz
        ),
        "escalar": escalar
    })

    # --------------------------------------------------------
    # PASO 2: COMPONENTE A COMPONENTE
    # --------------------------------------------------------

    componentes = []

    for i in range(filas):

        fila = []

        for j in range(columnas):

            expresion = (
                f"{_formatear_numero(escalar)} · "
                f"{_formatear_numero(matriz[i][j])}"
            )

            fila.append(
                expresion
            )

        componentes.append(
            fila
        )

    proceso.append({
        "numero": 2,
        "tipo": "componentes",
        "titulo": "MULTIPLICACIÓN DE COMPONENTES",
        "operacion": componentes
    })

    # --------------------------------------------------------
    # RESULTADO
    # --------------------------------------------------------

    resultado = []

    for i in range(filas):

        fila = []

        for j in range(columnas):

            fila.append(
                escalar * matriz[i][j]
            )

        resultado.append(
            fila
        )

    proceso.append({
        "numero": 3,
        "tipo": "resultado",
        "titulo": "RESULTADO",
        "matriz": _copiar_matriz(
            resultado
        )
    })

    return {
        "resultado": resultado,
        "proceso": proceso
    }


# ============================================================
# MULTIPLICACIÓN DE MATRICES
# ============================================================

def multiplicar_matrices(matrices):
    """
    Multiplica dos o más matrices.

    Realiza:

        A × B × C × ...

    Las dimensiones deben ser compatibles
    en cada multiplicación consecutiva.

    Devuelve:

        {
            "resultado": matriz_resultado,
            "proceso": [...]
        }
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

    proceso = []

    # --------------------------------------------------------
    # MULTIPLICACIONES PROGRESIVAS
    # --------------------------------------------------------

    resultado = _copiar_matriz(
        matrices[0]
    )

    for indice in range(
        1,
        len(matrices)
    ):

        siguiente = matrices[indice]

        # Verificar compatibilidad
        validar_multiplicacion_matrices(
            resultado,
            siguiente
        )

        # Nombre de las matrices
        nombre_izquierda = (
            "M1"
            if indice == 1
            else f"Resultado {indice - 1}"
        )

        nombre_derecha = (
            f"M{indice + 1}"
        )

        # ----------------------------------------------------
        # PASO DE OPERACIÓN
        # ----------------------------------------------------

        proceso.append({
            "numero": len(proceso) + 1,
            "tipo": "operacion",
            "titulo": "OPERACIÓN MATRICIAL",
            "operacion": (
                f"{nombre_izquierda} × "
                f"{nombre_derecha}"
            ),
            "matriz_izquierda":
                _copiar_matriz(resultado),
            "matriz_derecha":
                _copiar_matriz(siguiente)
        })

        # ----------------------------------------------------
        # CALCULAR PRODUCTO
        # ----------------------------------------------------

        producto, componentes = (
            _multiplicar_dos_matrices_con_proceso(
                resultado,
                siguiente
            )
        )

        # ----------------------------------------------------
        # PASO COMPONENTE A COMPONENTE
        # ----------------------------------------------------

        proceso.append({
            "numero": len(proceso) + 1,
            "tipo": "componentes",
            "titulo": "PRODUCTO FILA POR COLUMNA",
            "operacion": componentes
        })

        # ----------------------------------------------------
        # RESULTADO DE ESTA MULTIPLICACIÓN
        # ----------------------------------------------------

        proceso.append({
            "numero": len(proceso) + 1,
            "tipo": "resultado",
            "titulo": "RESULTADO",
            "matriz": _copiar_matriz(
                producto
            )
        })

        resultado = producto

    return {
        "resultado": resultado,
        "proceso": proceso
    }


# ============================================================
# MULTIPLICACIÓN DE DOS MATRICES
# ============================================================

def _multiplicar_dos_matrices(
    A,
    B
):
    """
    Multiplica dos matrices A y B.

    Esta función se conserva como función auxiliar
    para realizar únicamente el cálculo.
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

            fila.append(
                suma
            )

        resultado.append(
            fila
        )

    return resultado


# ============================================================
# MULTIPLICACIÓN DE DOS MATRICES CON PROCESO
# ============================================================

def _multiplicar_dos_matrices_con_proceso(
    A,
    B
):
    """
    Multiplica dos matrices y genera las expresiones
    fila por columna utilizadas para cada elemento.
    """

    validar_multiplicacion_matrices(
        A,
        B
    )

    filas_A = len(A)
    columnas_A = len(A[0])
    columnas_B = len(B[0])

    resultado = []
    componentes = []

    for i in range(filas_A):

        fila_resultado = []
        fila_componentes = []

        for j in range(columnas_B):

            suma = 0
            terminos = []

            for k in range(columnas_A):

                valor_A = A[i][k]
                valor_B = B[k][j]

                producto = (
                    valor_A * valor_B
                )

                suma += producto

                terminos.append(
                    f"{_formatear_numero(valor_A)} · "
                    f"{_formatear_numero(valor_B)}"
                )

            expresion = " + ".join(
                terminos
            )

            fila_componentes.append(
                expresion
            )

            fila_resultado.append(
                suma
            )

        componentes.append(
            fila_componentes
        )

        resultado.append(
            fila_resultado
        )

    return (
        resultado,
        componentes
    )
