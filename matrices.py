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
    validar_multiplicacion_matrices,
    validar_vector
)
from formato import formatear_numero
from config import TOLERANCIA


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


def _matrices_son_iguales(A, B):
    """
    Compara dos matrices usando la tolerancia configurada.
    """

    if len(A) != len(B):
        return False

    if not A and not B:
        return True

    if len(A[0]) != len(B[0]):
        return False

    for i in range(len(A)):
        for j in range(len(A[0])):
            if abs(A[i][j] - B[i][j]) > TOLERANCIA:
                return False

    return True


def _crear_matriz_identidad(tamano):
    """
    Crea una matriz identidad de tamano n x n.
    """

    return [
        [
            1 if i == j else 0
            for j in range(tamano)
        ]
        for i in range(tamano)
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
# ============================================================
# PROPIEDADES DE LA MULTIPLICACION DE MATRICES
# ============================================================

def verificar_asociatividad_multiplicacion_matrices(A, B, C):
    """
    Verifica la propiedad:

        A(BC) = (AB)C
    """

    validar_matriz(A)
    validar_matriz(B)
    validar_matriz(C)

    proceso = []

    BC = _multiplicar_dos_matrices(B, C)
    proceso.append({
        "numero": 1,
        "tipo": "operacion",
        "titulo": "PRODUCTO BC",
        "operacion": "B x C",
        "matriz_izquierda": _copiar_matriz(B),
        "matriz_derecha": _copiar_matriz(C)
    })
    proceso.append({
        "numero": 2,
        "tipo": "resultado",
        "titulo": "RESULTADO BC",
        "matriz": _copiar_matriz(BC)
    })

    lado_izquierdo = _multiplicar_dos_matrices(A, BC)
    proceso.append({
        "numero": 3,
        "tipo": "operacion",
        "titulo": "LADO IZQUIERDO",
        "operacion": "A x (BC)",
        "matriz_izquierda": _copiar_matriz(A),
        "matriz_derecha": _copiar_matriz(BC)
    })
    proceso.append({
        "numero": 4,
        "tipo": "resultado",
        "titulo": "A(BC)",
        "matriz": _copiar_matriz(lado_izquierdo)
    })

    AB = _multiplicar_dos_matrices(A, B)
    proceso.append({
        "numero": 5,
        "tipo": "operacion",
        "titulo": "PRODUCTO AB",
        "operacion": "A x B",
        "matriz_izquierda": _copiar_matriz(A),
        "matriz_derecha": _copiar_matriz(B)
    })
    proceso.append({
        "numero": 6,
        "tipo": "resultado",
        "titulo": "RESULTADO AB",
        "matriz": _copiar_matriz(AB)
    })

    lado_derecho = _multiplicar_dos_matrices(AB, C)
    proceso.append({
        "numero": 7,
        "tipo": "operacion",
        "titulo": "LADO DERECHO",
        "operacion": "(AB) x C",
        "matriz_izquierda": _copiar_matriz(AB),
        "matriz_derecha": _copiar_matriz(C)
    })
    proceso.append({
        "numero": 8,
        "tipo": "resultado",
        "titulo": "(AB)C",
        "matriz": _copiar_matriz(lado_derecho)
    })

    igualdad = _matrices_son_iguales(lado_izquierdo, lado_derecho)

    proceso.append({
        "numero": 9,
        "tipo": "verificacion",
        "titulo": "VERIFICACION DE LA PROPIEDAD",
        "operacion": "A(BC) = (AB)C",
        "resultado": igualdad
    })

    return {
        "igualdad": igualdad,
        "expresion": "A(BC) = (AB)C",
        "matrices": [
            _copiar_matriz(A),
            _copiar_matriz(B),
            _copiar_matriz(C)
        ],
        "BC": BC,
        "AB": AB,
        "lado_izquierdo": lado_izquierdo,
        "lado_derecho": lado_derecho,
        "comparaciones": [
            ("A(BC)", lado_izquierdo),
            ("(AB)C", lado_derecho)
        ],
        "proceso": proceso
    }


def verificar_distributividad_izquierda_matrices(A, B, C):
    """
    Verifica la propiedad:

        A(B + C) = AB + AC
    """

    validar_matriz(A)
    validar_matriz(B)
    validar_matriz(C)
    validar_mismas_dimensiones_matrices(B, C)

    proceso = []

    B_mas_C = sumar_matrices([B, C])["resultado"]
    proceso.append({
        "numero": 1,
        "tipo": "operacion",
        "titulo": "SUMA B + C",
        "operacion": "B + C",
        "matrices": [
            _copiar_matriz(B),
            _copiar_matriz(C)
        ]
    })
    proceso.append({
        "numero": 2,
        "tipo": "resultado",
        "titulo": "RESULTADO B + C",
        "matriz": _copiar_matriz(B_mas_C)
    })

    lado_izquierdo = _multiplicar_dos_matrices(A, B_mas_C)
    proceso.append({
        "numero": 3,
        "tipo": "operacion",
        "titulo": "LADO IZQUIERDO",
        "operacion": "A x (B + C)",
        "matriz_izquierda": _copiar_matriz(A),
        "matriz_derecha": _copiar_matriz(B_mas_C)
    })
    proceso.append({
        "numero": 4,
        "tipo": "resultado",
        "titulo": "A(B + C)",
        "matriz": _copiar_matriz(lado_izquierdo)
    })

    AB = _multiplicar_dos_matrices(A, B)
    AC = _multiplicar_dos_matrices(A, C)
    proceso.append({
        "numero": 5,
        "tipo": "operacion",
        "titulo": "PRODUCTO AB",
        "operacion": "A x B",
        "matriz_izquierda": _copiar_matriz(A),
        "matriz_derecha": _copiar_matriz(B)
    })
    proceso.append({
        "numero": 6,
        "tipo": "resultado",
        "titulo": "RESULTADO AB",
        "matriz": _copiar_matriz(AB)
    })
    proceso.append({
        "numero": 7,
        "tipo": "operacion",
        "titulo": "PRODUCTO AC",
        "operacion": "A x C",
        "matriz_izquierda": _copiar_matriz(A),
        "matriz_derecha": _copiar_matriz(C)
    })
    proceso.append({
        "numero": 8,
        "tipo": "resultado",
        "titulo": "RESULTADO AC",
        "matriz": _copiar_matriz(AC)
    })

    lado_derecho = sumar_matrices([AB, AC])["resultado"]
    proceso.append({
        "numero": 9,
        "tipo": "operacion",
        "titulo": "LADO DERECHO",
        "operacion": "AB + AC",
        "matrices": [
            _copiar_matriz(AB),
            _copiar_matriz(AC)
        ]
    })
    proceso.append({
        "numero": 10,
        "tipo": "resultado",
        "titulo": "AB + AC",
        "matriz": _copiar_matriz(lado_derecho)
    })

    igualdad = _matrices_son_iguales(lado_izquierdo, lado_derecho)

    proceso.append({
        "numero": 11,
        "tipo": "verificacion",
        "titulo": "VERIFICACION DE LA PROPIEDAD",
        "operacion": "A(B + C) = AB + AC",
        "resultado": igualdad
    })

    return {
        "igualdad": igualdad,
        "expresion": "A(B + C) = AB + AC",
        "matrices": [
            _copiar_matriz(A),
            _copiar_matriz(B),
            _copiar_matriz(C)
        ],
        "B_mas_C": B_mas_C,
        "AB": AB,
        "AC": AC,
        "lado_izquierdo": lado_izquierdo,
        "lado_derecho": lado_derecho,
        "comparaciones": [
            ("A(B + C)", lado_izquierdo),
            ("AB + AC", lado_derecho)
        ],
        "proceso": proceso
    }


def verificar_distributividad_derecha_matrices(A, B, C):
    """
    Verifica la propiedad:

        (B + C)A = BA + CA
    """

    validar_matriz(A)
    validar_matriz(B)
    validar_matriz(C)
    validar_mismas_dimensiones_matrices(B, C)

    proceso = []

    B_mas_C = sumar_matrices([B, C])["resultado"]
    proceso.append({
        "numero": 1,
        "tipo": "operacion",
        "titulo": "SUMA B + C",
        "operacion": "B + C",
        "matrices": [
            _copiar_matriz(B),
            _copiar_matriz(C)
        ]
    })
    proceso.append({
        "numero": 2,
        "tipo": "resultado",
        "titulo": "RESULTADO B + C",
        "matriz": _copiar_matriz(B_mas_C)
    })

    lado_izquierdo = _multiplicar_dos_matrices(B_mas_C, A)
    proceso.append({
        "numero": 3,
        "tipo": "operacion",
        "titulo": "LADO IZQUIERDO",
        "operacion": "(B + C) x A",
        "matriz_izquierda": _copiar_matriz(B_mas_C),
        "matriz_derecha": _copiar_matriz(A)
    })
    proceso.append({
        "numero": 4,
        "tipo": "resultado",
        "titulo": "(B + C)A",
        "matriz": _copiar_matriz(lado_izquierdo)
    })

    BA = _multiplicar_dos_matrices(B, A)
    CA = _multiplicar_dos_matrices(C, A)
    proceso.append({
        "numero": 5,
        "tipo": "operacion",
        "titulo": "PRODUCTO BA",
        "operacion": "B x A",
        "matriz_izquierda": _copiar_matriz(B),
        "matriz_derecha": _copiar_matriz(A)
    })
    proceso.append({
        "numero": 6,
        "tipo": "resultado",
        "titulo": "RESULTADO BA",
        "matriz": _copiar_matriz(BA)
    })
    proceso.append({
        "numero": 7,
        "tipo": "operacion",
        "titulo": "PRODUCTO CA",
        "operacion": "C x A",
        "matriz_izquierda": _copiar_matriz(C),
        "matriz_derecha": _copiar_matriz(A)
    })
    proceso.append({
        "numero": 8,
        "tipo": "resultado",
        "titulo": "RESULTADO CA",
        "matriz": _copiar_matriz(CA)
    })

    lado_derecho = sumar_matrices([BA, CA])["resultado"]
    proceso.append({
        "numero": 9,
        "tipo": "operacion",
        "titulo": "LADO DERECHO",
        "operacion": "BA + CA",
        "matrices": [
            _copiar_matriz(BA),
            _copiar_matriz(CA)
        ]
    })
    proceso.append({
        "numero": 10,
        "tipo": "resultado",
        "titulo": "BA + CA",
        "matriz": _copiar_matriz(lado_derecho)
    })

    igualdad = _matrices_son_iguales(lado_izquierdo, lado_derecho)

    proceso.append({
        "numero": 11,
        "tipo": "verificacion",
        "titulo": "VERIFICACION DE LA PROPIEDAD",
        "operacion": "(B + C)A = BA + CA",
        "resultado": igualdad
    })

    return {
        "igualdad": igualdad,
        "expresion": "(B + C)A = BA + CA",
        "matrices": [
            _copiar_matriz(A),
            _copiar_matriz(B),
            _copiar_matriz(C)
        ],
        "B_mas_C": B_mas_C,
        "BA": BA,
        "CA": CA,
        "lado_izquierdo": lado_izquierdo,
        "lado_derecho": lado_derecho,
        "comparaciones": [
            ("(B + C)A", lado_izquierdo),
            ("BA + CA", lado_derecho)
        ],
        "proceso": proceso
    }


def verificar_escalar_producto_matrices(A, B, escalar):
    """
    Verifica la propiedad:

        r(AB) = (rA)B = A(rB)
    """

    validar_matriz(A)
    validar_matriz(B)

    if not isinstance(escalar, (int, float)):
        raise TypeError(
            "El escalar debe ser un numero."
        )

    proceso = []
    r_texto = _formatear_numero(escalar)

    AB = _multiplicar_dos_matrices(A, B)
    proceso.append({
        "numero": 1,
        "tipo": "operacion",
        "titulo": "PRODUCTO AB",
        "operacion": "A x B",
        "matriz_izquierda": _copiar_matriz(A),
        "matriz_derecha": _copiar_matriz(B)
    })
    proceso.append({
        "numero": 2,
        "tipo": "resultado",
        "titulo": "RESULTADO AB",
        "matriz": _copiar_matriz(AB)
    })

    lado_izquierdo = multiplicar_matriz_escalar(
        AB,
        escalar
    )["resultado"]
    proceso.append({
        "numero": 3,
        "tipo": "resultado",
        "titulo": "r(AB)",
        "operacion": f"{r_texto}(AB)",
        "matriz": _copiar_matriz(lado_izquierdo)
    })

    rA = multiplicar_matriz_escalar(A, escalar)["resultado"]
    lado_central = _multiplicar_dos_matrices(rA, B)
    proceso.append({
        "numero": 4,
        "tipo": "resultado",
        "titulo": "rA",
        "operacion": f"{r_texto}A",
        "matriz": _copiar_matriz(rA)
    })
    proceso.append({
        "numero": 5,
        "tipo": "operacion",
        "titulo": "(rA)B",
        "operacion": "(rA) x B",
        "matriz_izquierda": _copiar_matriz(rA),
        "matriz_derecha": _copiar_matriz(B)
    })
    proceso.append({
        "numero": 6,
        "tipo": "resultado",
        "titulo": "RESULTADO (rA)B",
        "matriz": _copiar_matriz(lado_central)
    })

    rB = multiplicar_matriz_escalar(B, escalar)["resultado"]
    lado_derecho = _multiplicar_dos_matrices(A, rB)
    proceso.append({
        "numero": 7,
        "tipo": "resultado",
        "titulo": "rB",
        "operacion": f"{r_texto}B",
        "matriz": _copiar_matriz(rB)
    })
    proceso.append({
        "numero": 8,
        "tipo": "operacion",
        "titulo": "A(rB)",
        "operacion": "A x (rB)",
        "matriz_izquierda": _copiar_matriz(A),
        "matriz_derecha": _copiar_matriz(rB)
    })
    proceso.append({
        "numero": 9,
        "tipo": "resultado",
        "titulo": "RESULTADO A(rB)",
        "matriz": _copiar_matriz(lado_derecho)
    })

    igualdad = (
        _matrices_son_iguales(lado_izquierdo, lado_central)
        and _matrices_son_iguales(lado_central, lado_derecho)
    )

    proceso.append({
        "numero": 10,
        "tipo": "verificacion",
        "titulo": "VERIFICACION DE LA PROPIEDAD",
        "operacion": f"{r_texto}(AB) = ({r_texto}A)B = A({r_texto}B)",
        "resultado": igualdad
    })

    return {
        "igualdad": igualdad,
        "expresion": f"{r_texto}(AB) = ({r_texto}A)B = A({r_texto}B)",
        "matrices": [
            _copiar_matriz(A),
            _copiar_matriz(B)
        ],
        "escalar": escalar,
        "AB": AB,
        "rA": rA,
        "rB": rB,
        "lado_izquierdo": lado_izquierdo,
        "lado_central": lado_central,
        "lado_derecho": lado_derecho,
        "comparaciones": [
            (f"{r_texto}(AB)", lado_izquierdo),
            (f"({r_texto}A)B", lado_central),
            (f"A({r_texto}B)", lado_derecho)
        ],
        "proceso": proceso
    }


def verificar_identidad_multiplicacion_matrices(A):
    """
    Verifica la propiedad:

        I_m A = A = A I_n
    """

    validar_matriz(A)

    filas = len(A)
    columnas = len(A[0])
    I_m = _crear_matriz_identidad(filas)
    I_n = _crear_matriz_identidad(columnas)

    proceso = []

    lado_izquierdo = _multiplicar_dos_matrices(I_m, A)
    proceso.append({
        "numero": 1,
        "tipo": "operacion",
        "titulo": "IDENTIDAD IZQUIERDA",
        "operacion": "Im x A",
        "matriz_izquierda": _copiar_matriz(I_m),
        "matriz_derecha": _copiar_matriz(A)
    })
    proceso.append({
        "numero": 2,
        "tipo": "resultado",
        "titulo": "Im A",
        "matriz": _copiar_matriz(lado_izquierdo)
    })

    lado_derecho = _multiplicar_dos_matrices(A, I_n)
    proceso.append({
        "numero": 3,
        "tipo": "operacion",
        "titulo": "IDENTIDAD DERECHA",
        "operacion": "A x In",
        "matriz_izquierda": _copiar_matriz(A),
        "matriz_derecha": _copiar_matriz(I_n)
    })
    proceso.append({
        "numero": 4,
        "tipo": "resultado",
        "titulo": "A In",
        "matriz": _copiar_matriz(lado_derecho)
    })

    igualdad = (
        _matrices_son_iguales(lado_izquierdo, A)
        and _matrices_son_iguales(A, lado_derecho)
    )

    proceso.append({
        "numero": 5,
        "tipo": "verificacion",
        "titulo": "VERIFICACION DE LA PROPIEDAD",
        "operacion": "Im A = A = A In",
        "resultado": igualdad
    })

    return {
        "igualdad": igualdad,
        "expresion": "I_m A = A = A I_n",
        "matriz": _copiar_matriz(A),
        "I_m": I_m,
        "I_n": I_n,
        "lado_izquierdo": lado_izquierdo,
        "lado_central": _copiar_matriz(A),
        "lado_derecho": lado_derecho,
        "comparaciones": [
            ("I_m A", lado_izquierdo),
            ("A", _copiar_matriz(A)),
            ("A I_n", lado_derecho)
        ],
        "proceso": proceso
    }


# ============================================================
# MULTIPLICACION DE MATRIZ POR VECTOR
# ============================================================

def multiplicar_matriz_vector(A, vector):
    """
    Multiplica una matriz A por un vector.

    Si:

        A es una matriz m x n

        vector pertenece a R^n

    entonces:

        A · vector

    produce un vector de R^m.

    Ejemplo:

        A = [[1, 2],
             [3, 4]]

        v = [5, 6]

        A·v =

        [1(5) + 2(6)]
        [3(5) + 4(6)]

        = [17, 39]

    Devuelve:
        {
            "resultado": vector_resultado,
            "proceso": [...]
        }
    """

    validar_matriz(A)
    validar_vector(vector)

    filas = len(A)
    columnas = len(A[0])

    # --------------------------------------------------------
    # VALIDAR DIMENSIONES
    # --------------------------------------------------------

    if columnas != len(vector):

        raise ValueError(
            "La cantidad de columnas de la matriz "
            "debe coincidir con la cantidad de componentes "
            "del vector."
        )

    proceso = []

    # --------------------------------------------------------
    # PASO 1: OPERACIÓN
    # --------------------------------------------------------

    proceso.append({
        "numero": 1,
        "tipo": "operacion",
        "titulo": "PRODUCTO MATRIZ POR VECTOR",
        "operacion": "A · v",
        "matriz": _copiar_matriz(A),
        "vector": vector[:]
    })

    # --------------------------------------------------------
    # PASO 2: FILA POR VECTOR
    # --------------------------------------------------------

    componentes = []

    resultado = []

    for i in range(filas):

        suma = 0

        terminos = []

        for j in range(columnas):

            producto = A[i][j] * vector[j]

            suma += producto

            terminos.append(
                f"{_formatear_numero(A[i][j])} · "
                f"{_formatear_numero(vector[j])}"
            )

        expresion = " + ".join(terminos)

        componentes.append(
            expresion
        )

        resultado.append(
            suma
        )

    proceso.append({
        "numero": 2,
        "tipo": "componentes",
        "titulo": "PRODUCTO FILA POR VECTOR",
        "operacion": componentes
    })

    # --------------------------------------------------------
    # PASO 3: RESULTADO
    # --------------------------------------------------------

    proceso.append({
        "numero": 3,
        "tipo": "resultado",
        "titulo": "RESULTADO",
        "vector": resultado[:]
    })

    return {
        "resultado": resultado,
        "proceso": proceso
    }


# ============================================================
# PROPIEDAD DISTRIBUTIVA
# A(u + v) = Au + Av
# ============================================================

def verificar_distributividad_matriz_vector(
    A,
    u,
    v
):
    """
    Verifica la propiedad distributiva:

        A(u + v) = Au + Av

    donde:

        A = matriz
        u = vector
        v = vector

    El procedimiento calcula ambos lados de la igualdad:

        Lado izquierdo:

            A(u + v)

        Lado derecho:

            Au + Av

    y comprueba que ambos resultados sean iguales.

    Devuelve:

        {
            "igualdad": True/False,
            "lado_izquierdo": [...],
            "lado_derecho": [...],
            "u_mas_v": [...],
            "Au": [...],
            "Av": [...],
            "proceso": [...]
        }
    """

    validar_matriz(A)
    validar_vector(u)
    validar_vector(v)

    columnas = len(A[0])

    # --------------------------------------------------------
    # VALIDAR DIMENSIONES
    # --------------------------------------------------------

    if len(u) != columnas:

        raise ValueError(
            "El vector u debe tener la misma cantidad "
            "de componentes que columnas tiene A."
        )

    if len(v) != columnas:

        raise ValueError(
            "El vector v debe tener la misma cantidad "
            "de componentes que columnas tiene A."
        )

    proceso = []

    # --------------------------------------------------------
    # PASO 1: SUMAR u + v
    # --------------------------------------------------------

    u_mas_v = []

    for i in range(len(u)):

        u_mas_v.append(
            u[i] + v[i]
        )

    proceso.append({
        "numero": 1,
        "tipo": "suma_vectores",
        "titulo": "SUMA DE VECTORES",
        "operacion": "u + v",
        "resultado": u_mas_v[:]
    })

    # --------------------------------------------------------
    # PASO 2: CALCULAR A(u + v)
    # --------------------------------------------------------

    resultado_izquierdo = multiplicar_matriz_vector(
        A,
        u_mas_v
    )

    lado_izquierdo = resultado_izquierdo["resultado"]

    proceso.append({
        "numero": 2,
        "tipo": "lado_izquierdo",
        "titulo": "LADO IZQUIERDO",
        "operacion": "A(u + v)",
        "resultado": lado_izquierdo[:],
        "subproceso": resultado_izquierdo["proceso"]
    })

    # --------------------------------------------------------
    # PASO 3: CALCULAR Au
    # --------------------------------------------------------

    resultado_Au = multiplicar_matriz_vector(
        A,
        u
    )

    Au = resultado_Au["resultado"]

    proceso.append({
        "numero": 3,
        "tipo": "producto_Au",
        "titulo": "PRODUCTO Au",
        "operacion": "Au",
        "resultado": Au[:],
        "subproceso": resultado_Au["proceso"]
    })

    # --------------------------------------------------------
    # PASO 4: CALCULAR Av
    # --------------------------------------------------------

    resultado_Av = multiplicar_matriz_vector(
        A,
        v
    )

    Av = resultado_Av["resultado"]

    proceso.append({
        "numero": 4,
        "tipo": "producto_Av",
        "titulo": "PRODUCTO Av",
        "operacion": "Av",
        "resultado": Av[:],
        "subproceso": resultado_Av["proceso"]
    })

    # --------------------------------------------------------
    # PASO 5: CALCULAR Au + Av
    # --------------------------------------------------------

    lado_derecho = []

    for i in range(len(Au)):

        lado_derecho.append(
            Au[i] + Av[i]
        )

    proceso.append({
        "numero": 5,
        "tipo": "lado_derecho",
        "titulo": "LADO DERECHO",
        "operacion": "Au + Av",
        "resultado": lado_derecho[:]
    })

    # --------------------------------------------------------
    # PASO 6: COMPARAR
    # --------------------------------------------------------

    igualdad = True

    if len(lado_izquierdo) != len(lado_derecho):

        igualdad = False

    else:

        for i in range(len(lado_izquierdo)):

             if abs(
                lado_izquierdo[i] - lado_derecho[i]
            ) > TOLERANCIA:

                igualdad = False

                break

    proceso.append({
        "numero": 6,
        "tipo": "verificacion",
        "titulo": "VERIFICACIÓN DE LA PROPIEDAD",
        "operacion": "A(u + v) = Au + Av",
        "resultado": igualdad
    })

    return {
        "igualdad": igualdad,

        "matriz": _copiar_matriz(A),

        "u": u[:],

        "v": v[:],

        "u_mas_v": u_mas_v,

        "Au": Au,

        "Av": Av,

        "lado_izquierdo": lado_izquierdo,

        "lado_derecho": lado_derecho,

        "proceso": proceso
    }
    # ============================================================
# PROPIEDAD HOMOGÉNEA
# A(cu) = c(Au)
# ============================================================

def verificar_homogeneidad_matriz_vector(
    A,
    u,
    escalar
):
    """
    Verifica la propiedad:

        A(cu) = c(Au)

    donde:

        A      = matriz
        u      = vector
        c      = escalar

    Se calculan ambos lados de la igualdad:

        Lado izquierdo:
            A(cu)

        Lado derecho:
            c(Au)

    La función reutiliza las operaciones existentes:

        multiplicar_matriz_vector()
        multiplicar_vector_escalar()

    Devuelve los resultados y todos los pasos necesarios
    para que la interfaz pueda mostrar el procedimiento.
    """

    validar_matriz(A)
    validar_vector(u)

    if not isinstance(escalar, (int, float)):
        raise TypeError(
            "El escalar debe ser un número."
        )

    columnas = len(A[0])

    # --------------------------------------------------------
    # VALIDAR DIMENSIONES
    # --------------------------------------------------------

    if len(u) != columnas:

        raise ValueError(
            "El vector u debe tener la misma cantidad "
            "de componentes que columnas tiene A."
        )

    proceso = []
    k_texto = _formatear_numero(escalar)

    # ========================================================
    # PASO 1: CALCULAR cu
    # ========================================================

    from vectores import (
        multiplicar_vector_escalar
    )

    resultado_cu = multiplicar_vector_escalar(
        u,
        escalar
    )

    proceso.append({
        "numero": 1,
        "tipo": "producto_escalar_vector",
        "titulo": "MULTIPLICACIÓN DEL ESCALAR POR EL VECTOR",
        "operacion": f"{k_texto}u",
        "escalar": escalar,
        "vector": u[:],
        "resultado": resultado_cu[:]
    })

    # ========================================================
    # PASO 2: CALCULAR A(cu)
    # ========================================================

    resultado_A_cu = multiplicar_matriz_vector(
        A,
        resultado_cu
    )

    A_cu = resultado_A_cu["resultado"]

    proceso.append({
        "numero": 2,
        "tipo": "lado_izquierdo",
        "titulo": "LADO IZQUIERDO",
        "operacion": f"A({k_texto}u)",
        "resultado": A_cu[:],
        "subproceso": resultado_A_cu["proceso"]
    })

    # ========================================================
    # PASO 3: CALCULAR Au
    # ========================================================

    resultado_Au = multiplicar_matriz_vector(
        A,
        u
    )

    Au = resultado_Au["resultado"]

    proceso.append({
        "numero": 3,
        "tipo": "producto_Au",
        "titulo": "PRODUCTO Au",
        "operacion": "Au",
        "resultado": Au[:],
        "subproceso": resultado_Au["proceso"]
    })

    # ========================================================
    # PASO 4: CALCULAR c(Au)
    # ========================================================

    resultado_c_Au = multiplicar_vector_escalar(
        Au,
        escalar
    )

    c_Au = resultado_c_Au[:]

    proceso.append({
        "numero": 4,
        "tipo": "lado_derecho",
        "titulo": "LADO DERECHO",
        "operacion": f"{k_texto}(Au)",
        "escalar": escalar,
        "vector": Au[:],
        "resultado": c_Au[:]
    })

    # ========================================================
    # PASO 5: COMPARAR
    # ========================================================

    igualdad = True

    if len(A_cu) != len(c_Au):

        igualdad = False

    else:

        for i in range(len(A_cu)):

            if abs(
                A_cu[i] - c_Au[i]
            ) > TOLERANCIA:

                igualdad = False

                break

    proceso.append({
        "numero": 5,
        "tipo": "verificacion",
        "titulo": "VERIFICACIÓN DE LA PROPIEDAD",
        "operacion": f"A({k_texto}u) = {k_texto}(Au)",
        "resultado": igualdad
    })

    return {
        "igualdad": igualdad,

        "matriz": _copiar_matriz(A),

        "u": u[:],

        "escalar": escalar,

        "cu": resultado_cu,

        "Au": Au,

        "lado_izquierdo": A_cu,

        "lado_derecho": c_Au,

        "proceso": proceso
    }


def resolver_sistema_no_homogeneo(A, b):
    """
    Resuelve un sistema no homogeneo:

        Ax = b

    Esta funcion deja disponible desde matrices.py el flujo de
    ecuaciones matriciales sin duplicar Gauss-Jordan; reutiliza
    ecuaciones.resolver_sistema().
    """

    from ecuaciones import resolver_sistema

    validar_matriz(A)
    validar_vector(b)

    if len(A) != len(b):
        raise ValueError(
            "A y b deben tener la misma cantidad de filas/componentes."
        )

    resultado = resolver_sistema(A, b)
    resultado["es_homogeneo"] = False

    tipo = resultado.get("tipo")

    if tipo == "unica":
        mensaje = "El sistema no homogeneo tiene solucion unica."
    elif tipo == "infinitas":
        mensaje = "El sistema no homogeneo tiene infinitas soluciones."
    elif tipo == "ninguna":
        mensaje = "El sistema no homogeneo no tiene solucion."
    else:
        mensaje = "Estado de solucion no determinado."

    resultado["mensaje_sistema"] = mensaje

    return resultado


def resolver_sistema_homogeneo(A):
    """
    Resuelve un sistema homogeneo:

        Ax = 0

    Construye automaticamente el vector cero y reutiliza el
    resolutor no homogeneo Ax = b con b = 0.
    """

    validar_matriz(A)

    vector_cero = [
        0
        for _ in range(len(A))
    ]

    resultado = resolver_sistema_no_homogeneo(
        A,
        vector_cero
    )

    tiene_soluciones_no_triviales = (
        len(resultado.get("variables_libres", [])) > 0
    )

    if tiene_soluciones_no_triviales:
        mensaje = (
            "El sistema homogeneo tiene soluciones no triviales "
            "porque tiene al menos una variable libre."
        )
    else:
        mensaje = (
            "El sistema homogeneo solo tiene la solucion trivial."
        )

    resultado["es_homogeneo"] = True
    resultado["vector_cero"] = vector_cero
    resultado["tiene_soluciones_no_triviales"] = (
        tiene_soluciones_no_triviales
    )
    resultado["mensaje_homogeneo"] = mensaje
    resultado["mensaje_sistema"] = mensaje

    return resultado


def verificar_independencia_columnas(A):
    """
    Verifica si las columnas de una matriz son linealmente independientes.

    Las columnas de A son linealmente independientes si el sistema
    homogéneo:

        A x = 0

    tiene únicamente la solución trivial.
    """

    # Validar matriz
    validar_matriz(A)

    cantidad_filas = len(A)
    cantidad_columnas = len(A[0])

    # Vector cero del tamaño del número de columnas
    vector_cero = [0] * cantidad_filas

    # Resolver A*x = 0
    resultado = resolver_sistema_homogeneo(A)

    es_independiente = resultado["tipo"] == "unica"

    if es_independiente:
        tipo = "independiente"
        mensaje = (
            "Las columnas de A son linealmente independientes "
            "porque Ax = 0 tiene únicamente la solución trivial."
        )
        relaciones_dependencia = []
    else:
        tipo = "dependiente"
        mensaje = (
            "Las columnas de A son linealmente dependientes "
            "porque Ax = 0 tiene soluciones no triviales."
        )

        # Las direcciones del conjunto solución representan
        # relaciones de dependencia entre las columnas.
        conjunto_solucion = resultado.get("conjunto_solucion")

        if conjunto_solucion:
            relaciones_dependencia = []

            parametros = conjunto_solucion.get("parametros", [])
            vectores_direccion = conjunto_solucion.get("vectores_direccion", [])

            for i, vector in enumerate(vectores_direccion):
                parametro = (
                    parametros[i]
                    if i < len(parametros)
                    else f"t{i + 1}"
                )

                relaciones_dependencia.append({
                    "parametro": parametro,
                    "coeficientes": vector
                })
        else:
            relaciones_dependencia = []

    return {
        "es_independiente": es_independiente,
        "tipo": tipo,
        "mensaje": mensaje,

        # Datos de entrada
        "matriz": A,
        "vector_cero": vector_cero,

        # Información del sistema homogéneo
        "matriz_aumentada": resultado["matriz_aumentada"],
        "matriz_reducida": resultado["matriz_reducida"],
        "proceso": resultado["proceso"],

        # Información sobre rango y pivotes
        "rango": resultado["rango_A"],
        "columnas_pivote": resultado["columnas_pivote"],
        "variables_basicas": resultado["variables_basicas"],
        "variables_libres": resultado["variables_libres"],

        # Solución del sistema homogéneo
        "solucion_parametrica": resultado["solucion_parametrica"],
        "conjunto_solucion": resultado.get("conjunto_solucion"),

        # Relaciones de dependencia
        "relaciones_dependencia": relaciones_dependencia,

        # Dimensiones
        "cantidad_filas": cantidad_filas,
        "cantidad_columnas": cantidad_columnas,

        # Si hay más columnas que filas, automáticamente
        # no pueden ser linealmente independientes.
        "columnas_mayor_que_filas": cantidad_columnas > cantidad_filas
    }


def verificar_dependencia_columna(A, indice_columna):
    """
    Verifica si una columna especifica de A depende linealmente
    de las demas columnas.

    Se toma la columna Cj como vector objetivo y se resuelve:

        Bc = Cj

    donde B es la matriz formada por todas las columnas de A,
    excepto Cj. Si el sistema tiene solucion, entonces Cj es
    combinacion lineal de las demas columnas.

    El indice de columna es base 0.
    """

    validar_matriz(A)

    if not isinstance(indice_columna, int):
        raise TypeError(
            "El indice de columna debe ser un numero entero."
        )

    cantidad_filas = len(A)
    cantidad_columnas = len(A[0])

    if indice_columna < 0 or indice_columna >= cantidad_columnas:
        raise ValueError(
            "El indice de columna esta fuera del rango de la matriz."
        )

    columna_objetivo = [
        fila[indice_columna]
        for fila in A
    ]

    indices_generadores = [
        j
        for j in range(cantidad_columnas)
        if j != indice_columna
    ]

    es_columna_cero = all(
        abs(valor) <= TOLERANCIA
        for valor in columna_objetivo
    )

    def construir_expresion(coeficientes):
        terminos = []

        for posicion, coeficiente in enumerate(coeficientes):
            if abs(coeficiente) <= TOLERANCIA:
                continue

            indice = indices_generadores[posicion]
            magnitud = abs(coeficiente)
            nombre_columna = f"C{indice + 1}"

            if abs(magnitud - 1) <= TOLERANCIA:
                termino = nombre_columna
            else:
                termino = (
                    f"{_formatear_numero(magnitud)}{nombre_columna}"
                )

            signo = "-" if coeficiente < 0 else "+"
            terminos.append((signo, termino))

        if not terminos:
            return "0"

        primer_signo, primer_termino = terminos[0]
        expresion = (
            f"- {primer_termino}"
            if primer_signo == "-"
            else primer_termino
        )

        for signo, termino in terminos[1:]:
            expresion += f" {signo} {termino}"

        return expresion

    if not indices_generadores:
        es_dependiente = es_columna_cero
        tipo = "dependiente" if es_dependiente else "independiente"

        relacion_dependencia = None
        expresion = None

        if es_dependiente:
            expresion = f"C{indice_columna + 1} = 0"
            relacion_dependencia = {
                "columna_dependiente": indice_columna,
                "coeficientes_generadores": [],
                "coeficientes_homogeneos": [1],
                "expresion": expresion
            }

        mensaje = (
            "La columna es el vector cero y forma una relacion "
            "de dependencia lineal."
            if es_dependiente
            else "La matriz solo tiene una columna no nula, por lo que "
            "no depende de otras columnas."
        )

        return {
            "es_dependiente": es_dependiente,
            "tipo": tipo,
            "mensaje": mensaje,
            "matriz": _copiar_matriz(A),
            "indice_columna": indice_columna,
            "columna": columna_objetivo,
            "indices_columnas_generadoras": indices_generadores,
            "matriz_generadora": [
                []
                for _ in range(cantidad_filas)
            ],
            "coeficientes": [],
            "coeficientes_por_columna": [],
            "relacion_dependencia": relacion_dependencia,
            "expresion": expresion,
            "tipo_solucion": None,
            "matriz_aumentada": None,
            "matriz_reducida": None,
            "proceso": [],
            "rango_A": 0,
            "rango_Ab": 0 if es_columna_cero else 1,
            "columnas_pivote": [],
            "variables_basicas": [],
            "variables_libres": [],
            "solucion_parametrica": None,
            "conjunto_solucion": None,
            "cantidad_filas": cantidad_filas,
            "cantidad_columnas": cantidad_columnas,
            "es_columna_cero": es_columna_cero
        }

    matriz_generadora = []

    for fila in A:
        matriz_generadora.append([
            fila[indice]
            for indice in indices_generadores
        ])

    resultado = resolver_sistema_no_homogeneo(
        matriz_generadora,
        columna_objetivo
    )

    es_dependiente = resultado["tipo"] != "ninguna"
    tipo = "dependiente" if es_dependiente else "independiente"

    coeficientes = []
    coeficientes_por_columna = []
    relacion_dependencia = None
    expresion = None

    if es_dependiente:
        if resultado["tipo"] == "unica":
            coeficientes = resultado.get("solucion") or []
        else:
            conjunto_solucion = resultado.get("conjunto_solucion") or {}
            coeficientes = (
                conjunto_solucion.get("solucion_particular")
                or [
                    0
                    for _ in indices_generadores
                ]
            )

        coeficientes_por_columna = [
            {
                "columna": indice,
                "coeficiente": coeficientes[posicion]
            }
            for posicion, indice in enumerate(indices_generadores)
        ]

        coeficientes_homogeneos = [
            0
            for _ in range(cantidad_columnas)
        ]

        for posicion, indice in enumerate(indices_generadores):
            coeficientes_homogeneos[indice] = coeficientes[posicion]

        coeficientes_homogeneos[indice_columna] = -1

        expresion = (
            f"C{indice_columna + 1} = "
            f"{construir_expresion(coeficientes)}"
        )

        relacion_dependencia = {
            "columna_dependiente": indice_columna,
            "coeficientes_generadores": coeficientes_por_columna,
            "coeficientes_homogeneos": coeficientes_homogeneos,
            "expresion": expresion
        }

    mensaje = (
        f"La columna C{indice_columna + 1} depende linealmente "
        "de las demas columnas."
        if es_dependiente
        else f"La columna C{indice_columna + 1} no depende "
        "linealmente de las demas columnas."
    )

    return {
        "es_dependiente": es_dependiente,
        "tipo": tipo,
        "mensaje": mensaje,
        "matriz": _copiar_matriz(A),
        "indice_columna": indice_columna,
        "columna": columna_objetivo,
        "indices_columnas_generadoras": indices_generadores,
        "matriz_generadora": matriz_generadora,
        "coeficientes": coeficientes,
        "coeficientes_por_columna": coeficientes_por_columna,
        "relacion_dependencia": relacion_dependencia,
        "expresion": expresion,
        "tipo_solucion": resultado["tipo"],
        "matriz_aumentada": resultado["matriz_aumentada"],
        "matriz_reducida": resultado["matriz_reducida"],
        "proceso": resultado["proceso"],
        "rango_A": resultado["rango_A"],
        "rango_Ab": resultado["rango_Ab"],
        "columnas_pivote": resultado["columnas_pivote"],
        "variables_basicas": resultado["variables_basicas"],
        "variables_libres": resultado["variables_libres"],
        "solucion_parametrica": resultado["solucion_parametrica"],
        "conjunto_solucion": resultado.get("conjunto_solucion"),
        "cantidad_filas": cantidad_filas,
        "cantidad_columnas": cantidad_columnas,
        "es_columna_cero": es_columna_cero
    }
