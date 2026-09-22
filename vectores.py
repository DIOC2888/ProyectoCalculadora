
# vectores.py
# Operaciones algebraicas con vectores en R^n.
# Restricción: únicamente Python estándar.
#
# Este módulo contiene las operaciones vectoriales solicitadas
# en el Programa 3 de Álgebra Lineal.


from config import TOLERANCIA
from validaciones import (
    validar_vector,
    validar_mismos_tamanos_vectores
)


def sumar_vectores(vectores):
    """
    Suma dos o más vectores de R^n componente por componente.

    Ejemplo:

        v1 = [2, 1]
        v2 = [3, 4]
        v3 = [5, 2]

        v1 + v2 + v3 = [10, 7]
    """

    if not isinstance(vectores, list) or len(vectores) < 2:
        raise ValueError(
            "Debe proporcionar al menos dos vectores."
        )

    # Validar todos los vectores
    for vector in vectores:
        validar_vector(vector)

    # Todos deben tener la misma dimensión
    for i in range(1, len(vectores)):
        validar_mismos_tamanos_vectores(
            vectores[0],
            vectores[i]
        )

    # Comenzamos con una copia del primer vector
    resultado = vectores[0][:]

    # Sumamos los demás vectores
    for vector in vectores[1:]:

        for i in range(len(resultado)):
            resultado[i] += vector[i]

    return resultado

def restar_vectores(vectores):
    """
    Resta dos o más vectores de R^n componente por componente.

    La operación respeta el orden:

        v1 - v2 - v3 - ...

    Ejemplo:

        v1 = [10, 8]
        v2 = [2, 3]
        v3 = [1, 2]

        v1 - v2 - v3 = [7, 3]
    """

    if not isinstance(vectores, list) or len(vectores) < 2:
        raise ValueError(
            "Debe proporcionar al menos dos vectores."
        )

    # Validar todos los vectores
    for vector in vectores:
        validar_vector(vector)

    # Todos deben tener la misma dimensión
    for i in range(1, len(vectores)):
        validar_mismos_tamanos_vectores(
            vectores[0],
            vectores[i]
        )

    # Comenzamos con una copia del primer vector
    resultado = vectores[0][:]

    # Restamos los demás vectores
    for vector in vectores[1:]:

        for i in range(len(resultado)):
            resultado[i] -= vector[i]

    return resultado


def multiplicar_vector_escalar(vector, escalar):
    """
    Multiplica un vector por un escalar.

    Procedimiento algebraico equivalente:

        v = (a1, a2, ..., an)

        k·v =
        (k·a1, k·a2, ..., k·an)

    El escalar debe ser un número.
    """

    validar_vector(vector)

    if not isinstance(escalar, (int, float)):
        raise TypeError("El escalar debe ser un número.")

    resultado = []

    for componente in vector:
        resultado.append(escalar * componente)

    return resultado


def copiar_vector(vector):
    """
    Crea una copia independiente de un vector.

    Se utiliza para evitar modificar accidentalmente
    el vector original durante algún procedimiento.
    """

    validar_vector(vector)

    return vector[:]


def combinacion_lineal(vectores, b):
    """
    Determina si el vector b es combinación lineal de un
    conjunto de vectores.

    Matemáticamente se busca determinar si existen escalares:

        c1, c2, ..., ck

    tales que:

        b = c1*v1 + c2*v2 + ... + ck*vk

    Para resolverlo se construye una matriz A colocando
    los vectores como COLUMNAS:

             |       |
        A =  | v1 v2 ... vk |
             |       |

    y se resuelve el sistema:

        A*c = b

    donde:

        c = (c1, c2, ..., ck)

    El resultado depende de la cantidad de soluciones:

        "unica"
            Existe una única combinación lineal.

        "infinitas"
            Existen infinitas combinaciones lineales que
            producen el vector b.

        "ninguna"
            b no es combinación lineal de los vectores dados.

    Esta función NO utiliza NumPy ni SciPy.
    """

    validar_vector(b)

    # Debe existir por lo menos un vector generador.
    if not isinstance(vectores, list) or len(vectores) == 0:
        raise ValueError(
            "Debe proporcionar al menos un vector generador."
        )

    # Todos los vectores generadores deben ser vectores
    # y tener la misma dimensión que b.
    for vector in vectores:

        validar_vector(vector)

        if len(vector) != len(b):
            raise ValueError(
                "Todos los vectores generadores deben tener "
                "la misma dimensión que el vector objetivo."
            )

    # Importación local para evitar una dependencia circular.
    #
    # vectores.py utiliza resolver_sistema()
    # de ecuaciones.py.
    from ecuaciones import resolver_sistema

    # ---------------------------------------------------------
    # CONSTRUCCIÓN DE LA MATRIZ A
    # ---------------------------------------------------------
    #
    # Si tenemos:
    #
    # v1 = (a,b,c)
    # v2 = (d,e,f)
    #
    # A debe ser:
    #
    #       | a d |
    # A =   | b e |
    #       | c f |
    #
    # Es decir, los vectores son COLUMNAS.
    #

    filas = len(b)
    columnas = len(vectores)

    A = []

    for i in range(filas):

        fila = []

        for j in range(columnas):
            fila.append(vectores[j][i])

        A.append(fila)

    # ---------------------------------------------------------
    # RESOLVER A*c = b
    # ---------------------------------------------------------

    sistema = resolver_sistema(A, b)

    # ---------------------------------------------------------
    # DEVOLVER INFORMACIÓN PARA EL CONTROLADOR Y LA VISTA
    # ---------------------------------------------------------
    #
    # No devolvemos solamente True/False.
    #
    # La interfaz necesitará también:
    #
    # - coeficientes
    # - rango
    # - pivotes
    # - variables libres
    # - matriz aumentada
    # - matriz reducida
    # - proceso de Gauss-Jordan
    #
    # Esto permitirá construir correctamente las tarjetas
    # de resultados de vista_vectores.
    #

    resultado = {

        # ¿Es combinación lineal?
        "es_combinacion":
            sistema["tipo"] != "ninguna",

        # Tipo de solución:
        #
        # "unica"
        # "infinitas"
        # "ninguna"
        #
        "tipo":
            sistema["tipo"],

        # Coeficientes cuando existe una única solución.
        #
        # Ejemplo:
        # [2, 3]
        #
        # significa:
        #
        # b = 2v1 + 3v2
        #
        "coeficientes":
            sistema["solucion"],

        # Información de solución paramétrica
        # cuando existen infinitas soluciones.
        "solucion_parametrica":
            sistema["solucion_parametrica"],

        # Matriz formada por los vectores generadores.
        "matriz_generadores":
            A,

        # Matriz [A | b].
        "matriz_aumentada":
            sistema["matriz_aumentada"],

        # Matriz después de Gauss-Jordan.
        "matriz_reducida":
            sistema["matriz_reducida"],

        # Operaciones realizadas durante Gauss-Jordan.
        "proceso":
            sistema["proceso"],

        # Información matemática del sistema.
        "rango_A":
            sistema["rango_A"],

        "rango_Ab":
            sistema["rango_Ab"],

        "num_variables":
            sistema["num_variables"],

        "num_ecuaciones":
            sistema["num_ecuaciones"],

        "columnas_pivote":
            sistema["columnas_pivote"],

        "variables_basicas":
            sistema["variables_basicas"],

        "variables_libres":
            sistema["variables_libres"],
    }

    return resultado
# ============================================================
# INDEPENDENCIA LINEAL
# ============================================================

def verificar_independencia_lineal(vectores):
    """
    Determina si un conjunto de vectores es linealmente
    independiente.

    Se utiliza la definición:

        c1*v1 + c2*v2 + ... + cp*vp = 0

    colocando los vectores como columnas de una matriz A:

        A = [v1 v2 ... vp]

    y resolviendo el sistema homogéneo:

        A*c = 0

    Si la única solución es:

        c1 = c2 = ... = cp = 0

    entonces los vectores son linealmente independientes.

    Si existen variables libres, existen soluciones no triviales
    y los vectores son linealmente dependientes.

    La eliminación de Gauss-Jordan NO se implementa nuevamente.
    Se reutiliza resolver_sistema() de ecuaciones.py.
    """

    # ---------------------------------------------------------
    # VALIDAR CONJUNTO
    # ---------------------------------------------------------

    if not isinstance(vectores, list):

        raise TypeError(
            "Los vectores deben proporcionarse como una lista."
        )

    if len(vectores) == 0:

        raise ValueError(
            "Debe proporcionar al menos un vector."
        )

    # Validar cada vector
    for vector in vectores:

        validar_vector(vector)

    # ---------------------------------------------------------
    # VERIFICAR QUE TODOS PERTENEZCAN AL MISMO R^n
    # ---------------------------------------------------------

    dimension = len(vectores[0])

    for vector in vectores[1:]:

        if len(vector) != dimension:

            raise ValueError(
                "Todos los vectores deben tener la misma dimensión."
            )

    cantidad_vectores = len(vectores)

    # ---------------------------------------------------------
    # CASO p > n
    # ---------------------------------------------------------
    #
    # Si existen más vectores que la dimensión:
    #
    #       p > n
    #
    # entonces el conjunto necesariamente es dependiente.
    #
    # Aun así construimos y resolvemos el sistema para
    # conservar el proceso matemático completo.
    # ---------------------------------------------------------

    p_mayor_que_n = (
        cantidad_vectores > dimension
    )

    # ---------------------------------------------------------
    # CONSTRUIR A CON LOS VECTORES COMO COLUMNAS
    # ---------------------------------------------------------

    A = []

    for i in range(dimension):

        fila = []

        for j in range(cantidad_vectores):

            fila.append(
                vectores[j][i]
            )

        A.append(fila)

    # ---------------------------------------------------------
    # SISTEMA HOMOGÉNEO
    #
    #       A*c = 0
    # ---------------------------------------------------------

    vector_cero = [
        0
        for _ in range(dimension)
    ]

    # ---------------------------------------------------------
    # RESOLVER SISTEMA UTILIZANDO EL BACKEND EXISTENTE
    # ---------------------------------------------------------

    from ecuaciones import resolver_sistema

    sistema = resolver_sistema(
        A,
        vector_cero
    )

    # ---------------------------------------------------------
    # ANALIZAR RESULTADO
    # ---------------------------------------------------------

    variables_libres = sistema[
        "variables_libres"
    ]

    es_independiente = (
        len(variables_libres) == 0
    )

    # ---------------------------------------------------------
    # SOLUCIÓN / RELACIÓN DE DEPENDENCIA
    # ---------------------------------------------------------

    relacion_dependencia = None

    if not es_independiente:

        # -----------------------------------------------------
        # Elegimos una variable libre y le damos valor 1.
        #
        # Las demás variables libres reciben 0.
        #
        # Esto produce una solución no trivial concreta.
        # -----------------------------------------------------

        solucion = [
            0
            for _ in range(cantidad_vectores)
        ]

        variable_libre = variables_libres[0]

        solucion[variable_libre] = 1

        matriz_reducida = sistema[
            "matriz_reducida"
        ]

        columnas_pivote = sistema[
            "columnas_pivote"
        ]

        # -----------------------------------------------------
        # Calcular las variables básicas utilizando
        # la matriz reducida.
        #
        # Para cada ecuación:
        #
        # xp + a1*x1 + ... + ak*xk = 0
        #
        # entonces:
        #
        # xp = -(a1*x1 + ... + ak*xk)
        # -----------------------------------------------------

        for fila in matriz_reducida:

            columna_pivote = None

            # Buscar el pivote de la fila.
            for j in range(cantidad_vectores):

                if abs(
                    fila[j]
                ) > TOLERANCIA:

                    if j in columnas_pivote:

                        columna_pivote = j

                    break

            if columna_pivote is None:

                continue

            valor = 0

            for j in variables_libres:

                valor += (
                    fila[j] * solucion[j]
                )

            solucion[columna_pivote] = -valor

        # -----------------------------------------------------
        # Construir relación de dependencia
        # -----------------------------------------------------

        relacion_terminos = []

        for i in range(cantidad_vectores):

            coeficiente = solucion[i]

            if abs(coeficiente) < TOLERANCIA:

                continue

            relacion_terminos.append({
                "vector": i,
                "coeficiente": coeficiente
            })

        relacion_dependencia = {
            "coeficientes": solucion,
            "terminos": relacion_terminos
        }

    # ---------------------------------------------------------
    # MENSAJE
    # ---------------------------------------------------------

    if es_independiente:

        mensaje = (
            "Los vectores son linealmente independientes. "
            "La ecuación homogénea Ac = 0 tiene únicamente "
            "la solución trivial."
        )

    elif p_mayor_que_n:

        mensaje = (
            "Los vectores son linealmente dependientes porque "
            "la cantidad de vectores es mayor que la dimensión: "
            "p > n."
        )

    else:

        mensaje = (
            "Los vectores son linealmente dependientes porque "
            "la ecuación homogénea Ac = 0 tiene soluciones "
            "no triviales."
        )

    # ---------------------------------------------------------
    # RETORNO
    # ---------------------------------------------------------

    return {

        "es_independiente":
            es_independiente,

        "tipo":
            "independiente"
            if es_independiente
            else "dependiente",

        "mensaje":
            mensaje,

        "vectores":
            [vector[:] for vector in vectores],

        "matriz":
            A,

        "vector_cero":
            vector_cero,

        "matriz_aumentada":
            sistema["matriz_aumentada"],

        "matriz_reducida":
            sistema["matriz_reducida"],

        "proceso":
            sistema["proceso"],

        "rango":
            sistema["rango_A"],

        "cantidad_vectores":
            cantidad_vectores,

        "dimension":
            dimension,

        "columnas_pivote":
            sistema["columnas_pivote"],

        "variables_basicas":
            sistema["variables_basicas"],

        "variables_libres":
            sistema["variables_libres"],

        "solucion_parametrica":
            sistema["solucion_parametrica"],

        "relacion_dependencia":
            relacion_dependencia,

        "p_mayor_que_n":
            p_mayor_que_n
    }
