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
# MULTIPLICACIÓN DE MATRIZ POR VECTOR
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
def verificar_independencia_columnas(A):
    """
    Verifica si las columnas de una matriz son linealmente independientes.

    Las columnas de A son linealmente independientes si el sistema
    homogéneo:

        A x = 0

    tiene únicamente la solución trivial.
    """

    # Importación local para evitar dependencias innecesarias
    from ecuaciones import resolver_sistema

    # Validar matriz
    validar_matriz(A)

    cantidad_filas = len(A)
    cantidad_columnas = len(A[0])

    # Vector cero del tamaño del número de columnas
    vector_cero = [0] * cantidad_filas

    # Resolver A*x = 0
    resultado = resolver_sistema(A, vector_cero)

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
