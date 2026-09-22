
# ecuaciones.py
# Resolución de sistemas de ecuaciones y ecuaciones matriciales Ax = b.
#
# Restricción del Programa 3:
# No se utiliza NumPy, SciPy ni funciones avanzadas de math.
#
# El procedimiento utilizado es Gauss-Jordan mediante listas,
# ciclos y operaciones aritméticas básicas.


from validaciones import (
    validar_matriz,
    validar_vector
)

from config import TOLERANCIA
from formato import formatear_numero


def es_cero(valor):
    """
    Determina si un número puede considerarse cero.

    Se utiliza una tolerancia porque durante las operaciones
    con números decimales pueden aparecer valores muy pequeños
    como 0.00000000001 que matemáticamente representan cero.
    """

    return abs(valor) < TOLERANCIA


def copiar_matriz(matriz):
    """
    Crea una copia independiente de una matriz.

    Esto permite realizar operaciones sobre una copia sin
    modificar la matriz original proporcionada por el usuario.
    """

    validar_matriz(matriz)

    copia = []

    for fila in matriz:
        copia.append(fila[:])

    return copia


def construir_matriz_aumentada(A, b):
    """
    Construye la matriz aumentada [A | b] de la ecuación:

        Ax = b

    Si:

        A = [a11 a12]
            [a21 a22]

        b = [b1]
            [b2]

    entonces:

        [A | b] = [a11 a12 | b1]
                  [a21 a22 | b2]

    Esta matriz es la que se utiliza para aplicar
    eliminación de Gauss-Jordan.
    """

    validar_matriz(A)
    validar_vector(b)

    if len(A) != len(b):
        raise ValueError(
            "La cantidad de filas de A debe coincidir "
            "con la cantidad de componentes de b."
        )

    matriz_aumentada = []

    for i in range(len(A)):

        fila = A[i][:]

        fila.append(b[i])

        matriz_aumentada.append(fila)

    return matriz_aumentada


def intercambiar_filas(matriz, fila1, fila2):
    """
    Intercambia dos filas de una matriz.

    Operación elemental:

        Fi ↔ Fj

    Se utiliza cuando necesitamos colocar un elemento
    distinto de cero en la posición del pivote.
    """

    matriz[fila1], matriz[fila2] = matriz[fila2], matriz[fila1]


def normalizar_fila(matriz, fila, pivote):
    """
    Divide todos los elementos de una fila entre el pivote.

    Operación elemental:

        Fi ← Fi / pivote

    De esta forma el pivote se convierte en 1.
    """

    for j in range(len(matriz[0])):

        matriz[fila][j] = matriz[fila][j] / pivote


def limpiar_numero(valor):
    """
    Convierte en 0 los números suficientemente pequeños.

    Esto evita que la interfaz muestre valores como:

        1.2246467991473532e-16

    cuando matemáticamente el resultado es 0.
    """

    if es_cero(valor):
        return 0

    return valor


def gauss_jordan(matriz_aumentada):
    """
    Reduce una matriz aumentada mediante Gauss-Jordan.

    Procedimiento algebraico:

    1. Buscar un pivote.
    2. Intercambiar filas si es necesario.
    3. Convertir el pivote en 1.
    4. Hacer cero los elementos que están arriba y abajo
       del pivote.
    5. Repetir hasta obtener la forma escalonada reducida.

    Además de la matriz final, se guarda cada operación realizada
    para que posteriormente la interfaz pueda mostrar el proceso.

    Retorna:

        matriz
        pivotes
        proceso
    """

    matriz = copiar_matriz(matriz_aumentada)

    filas = len(matriz)

    columnas_totales = len(matriz[0])

    # La última columna corresponde a b.
    columnas_variables = columnas_totales - 1

    fila_pivote = 0

    columna = 0

    pivotes = []

    proceso = []

    while (
        fila_pivote < filas
        and columna < columnas_variables
    ):

        # -----------------------------------------------------
        # BUSCAR UNA FILA CON UN ELEMENTO DISTINTO DE CERO
        # -----------------------------------------------------

        fila_encontrada = -1

        for i in range(fila_pivote, filas):

            if not es_cero(matriz[i][columna]):

                fila_encontrada = i

                break

        # Si toda la columna debajo del pivote es cero,
        # pasamos a la siguiente columna.
        if fila_encontrada == -1:

            columna += 1

            continue

        # -----------------------------------------------------
        # INTERCAMBIO DE FILAS
        # -----------------------------------------------------

        if fila_encontrada != fila_pivote:

            intercambiar_filas(
                matriz,
                fila_encontrada,
                fila_pivote
            )

            proceso.append({
                "operacion":
                    f"F{fila_encontrada + 1} ↔ "
                    f"F{fila_pivote + 1}",

                "matriz":
                    copiar_matriz(matriz)
            })

        # -----------------------------------------------------
        # NORMALIZAR EL PIVOTE
        # -----------------------------------------------------

        pivote = matriz[fila_pivote][columna]

        if not es_cero(pivote - 1):

            normalizar_fila(
                matriz,
                fila_pivote,
                pivote
            )

            matriz[fila_pivote] = [
                limpiar_numero(x)
                for x in matriz[fila_pivote]
            ]

            proceso.append({
                "operacion":
                    f"F{fila_pivote + 1} ← "
                    f"F{fila_pivote + 1} / "
                    f"{formatear_numero(pivote)}",

                "matriz":
                    copiar_matriz(matriz)
            })

        # -----------------------------------------------------
        # HACER CEROS ARRIBA Y ABAJO DEL PIVOTE
        # -----------------------------------------------------

        for i in range(filas):

            if i == fila_pivote:
                continue

            factor = matriz[i][columna]

            if es_cero(factor):
                continue

            for j in range(columnas_totales):

                matriz[i][j] = (
                    matriz[i][j]
                    - factor * matriz[fila_pivote][j]
                )

            matriz[i] = [
                limpiar_numero(x)
                for x in matriz[i]
            ]

            proceso.append({
                "operacion":
                    f"F{i + 1} ← F{i + 1} - "
                    f"({formatear_numero(factor)})"
                    f"F{fila_pivote + 1}",

                "matriz":
                    copiar_matriz(matriz)
            })

        pivotes.append(columna)

        fila_pivote += 1

        columna += 1

    # Limpieza final.
    for i in range(filas):

        for j in range(columnas_totales):

            matriz[i][j] = limpiar_numero(
                matriz[i][j]
            )

    return {
        "matriz": matriz,
        "pivotes": pivotes,
        "proceso": proceso
    }


def obtener_pivotes_y_libres(
    matriz_reducida,
    cantidad_variables
):
    """
    Identifica las columnas pivote y las variables libres.

    En una matriz escalonada reducida, el pivote de cada fila
    no nula es su primer elemento distinto de cero.

    Ejemplo:

        [1  2 | 5]
        [0  0 | 0]

    La columna 1 es pivote y la variable x2 es libre.

    Retorna:

        columnas_pivote
        variables_libres
    """

    columnas_pivote = []

    # Buscar el primer elemento no nulo de cada fila.
    for fila in matriz_reducida:

        for j in range(cantidad_variables):

            if not es_cero(fila[j]):

                if j not in columnas_pivote:

                    columnas_pivote.append(j)

                break

    variables_libres = []

    for j in range(cantidad_variables):

        if j not in columnas_pivote:

            variables_libres.append(j)

    return columnas_pivote, variables_libres


def calcular_rango(
    matriz,
    cantidad_columnas=None
):
    """
    Calcula el rango de una matriz contando sus filas no nulas.

    Para el sistema:

        Ax = b

    se puede calcular:

        rango(A)

    y:

        rango([A | b])

    para comparar ambos.
    """

    if cantidad_columnas is None:

        cantidad_columnas = len(matriz[0])

    rango = 0

    for fila in matriz:

        fila_no_nula = False

        for j in range(cantidad_columnas):

            if not es_cero(fila[j]):

                fila_no_nula = True

                break

        if fila_no_nula:

            rango += 1

    return rango


def detectar_tipo_solucion(
    matriz_reducida,
    cantidad_variables
):
    """
    Determina qué tipo de solución tiene Ax=b.

    Caso 1: ninguna solución.

    Si aparece una fila:

        [0  0  ...  0 | c]

    con c diferente de cero, tenemos una contradicción:

        0 = c

    Por lo tanto, el sistema es incompatible.

    Caso 2: solución única.

    Si no existe contradicción y:

        rango(A) = número de variables

    existe una única solución.

    Caso 3: infinitas soluciones.

    Si no existe contradicción pero:

        rango(A) < número de variables

    existen variables libres y por tanto infinitas soluciones.
    """

    # Buscar contradicción.
    for fila in matriz_reducida:

        coeficientes_cero = True

        for j in range(cantidad_variables):

            if not es_cero(fila[j]):

                coeficientes_cero = False

                break

        if (
            coeficientes_cero
            and not es_cero(fila[cantidad_variables])
        ):

            return "ninguna"

    columnas_pivote, variables_libres = (
        obtener_pivotes_y_libres(
            matriz_reducida,
            cantidad_variables
        )
    )

    # Todas las variables tienen pivote.
    if len(columnas_pivote) == cantidad_variables:

        return "unica"

    # Hay variables libres.
    return "infinitas"


def obtener_solucion_unica(
    matriz_reducida,
    cantidad_variables
):
    """
    Obtiene la solución cuando el sistema tiene una única solución.

    Si la matriz reducida tiene:

        [1 0 | x]
        [0 1 | y]

    entonces:

        x1 = x
        x2 = y

    Retorna una lista:

        [x1, x2, ..., xn]
    """

    columnas_pivote, _ = (
        obtener_pivotes_y_libres(
            matriz_reducida,
            cantidad_variables
        )
    )

    solucion = [
        0
        for _ in range(cantidad_variables)
    ]

    for fila in matriz_reducida:

        for j in columnas_pivote:

            if fila[j] == 1:

                solucion[j] = fila[
                    cantidad_variables
                ]

                break

    return solucion


def nombre_parametro(posicion):
    """
    Genera nombres para las variables libres.

    Ejemplo:

        primera variable libre -> t
        segunda variable libre -> s
        tercera variable libre -> u
    """

    letras = [
        "t",
        "s",
        "u",
        "v",
        "w",
        "r",
        "q"
    ]

    if posicion < len(letras):

        return letras[posicion]

    return "t" + str(posicion + 1)


def formatear_coeficiente(coeficiente):
    """
    Convierte un coeficiente numérico a texto para
    construir expresiones paramétricas.

    Ejemplos:

        1    -> ""
        -1   -> "-"
        2    -> "2"
        -2   -> "-2"
    """

    if es_cero(coeficiente - 1):

        return ""

    if es_cero(coeficiente + 1):

        return "-"

    return formatear_numero(coeficiente)


def obtener_solucion_parametrica(
    matriz_reducida,
    cantidad_variables
):
    """
    Construye la solución paramétrica de un sistema con
    infinitas soluciones.

    Ejemplo:

        x1 + 2x3 = 5
        x2 - x3  = 3

    Si x3 es libre:

        x3 = t

        x1 = 5 - 2t

        x2 = 3 + t

    La función devuelve tanto las variables libres como
    las expresiones de las variables básicas.
    """

    columnas_pivote, variables_libres = (
        obtener_pivotes_y_libres(
            matriz_reducida,
            cantidad_variables
        )
    )

    parametros = {}

    for posicion, variable in enumerate(
        variables_libres
    ):

        parametros[variable] = nombre_parametro(
            posicion
        )

    soluciones = []

    # Recorrer cada variable.
    for variable in range(cantidad_variables):

        # -----------------------------------------------------
        # VARIABLE LIBRE
        # -----------------------------------------------------

        if variable in variables_libres:

            parametro = parametros[variable]

            soluciones.append({
                "variable": variable,
                "expresion": parametro,
                "libre": True,
                "parametro": parametro
            })

            continue

        # -----------------------------------------------------
        # BUSCAR FILA DEL PIVOTE
        # -----------------------------------------------------

        fila_pivote = -1

        for i in range(
            len(matriz_reducida)
        ):

            if (
                matriz_reducida[i][variable]
                == 1
            ):

                es_pivote = True

                # Comprobar que sea realmente el
                # primer elemento no nulo de la fila.
                for j in range(variable):

                    if not es_cero(
                        matriz_reducida[i][j]
                    ):

                        es_pivote = False

                        break

                if es_pivote:

                    fila_pivote = i

                    break

        if fila_pivote == -1:

            continue

        # -----------------------------------------------------
        # CONSTRUIR LA EXPRESIÓN
        # -----------------------------------------------------

        termino_independiente = (
            matriz_reducida[
                fila_pivote
            ][cantidad_variables]
        )

        expresion = formatear_numero(
            termino_independiente
        )

        for variable_libre in variables_libres:

            coeficiente = (
                matriz_reducida[
                    fila_pivote
                ][variable_libre]
            )

            if es_cero(coeficiente):

                continue

            # Al despejar:
            #
            # xp + a*t = b
            #
            # xp = b - a*t
            #
            coeficiente = -coeficiente

            parametro = parametros[
                variable_libre
            ]

            if es_cero(coeficiente - 1):

                termino = parametro

                if expresion == "0":

                    expresion = termino

                else:

                    expresion += (
                        " + " + termino
                    )

            elif es_cero(coeficiente + 1):

                termino = parametro

                if expresion == "0":

                    expresion = "-" + termino

                else:

                    expresion += (
                        " - " + termino
                    )

            elif coeficiente > 0:

                termino = (
                    formatear_numero(coeficiente)
                    + parametro
                )

                if expresion == "0":

                    expresion = termino

                else:

                    expresion += (
                        " + " + termino
                    )

            else:

                termino = (
                    formatear_numero(abs(coeficiente))
                    + parametro
                )

                if expresion == "0":

                    expresion = "-" + termino

                else:

                    expresion += (
                        " - " + termino
                    )

        soluciones.append({
            "variable": variable,
            "expresion": expresion,
            "libre": False,
            "parametro": None
        })

    return {
        "columnas_pivote": columnas_pivote,
        "variables_libres": variables_libres,
        "parametros": parametros,
        "soluciones": soluciones
    }
def obtener_conjunto_solucion(
    matriz_reducida,
    cantidad_variables,
    tipo,
    solucion=None
):
    """
    Construye el conjunto solución en forma vectorial.

    Para un sistema homogéneo:

        Ax = 0

    devuelve:

        x = t1*v1 + t2*v2 + ... + tk*vk

    Para un sistema no homogéneo:

        Ax = b

    devuelve:

        x = xp + t1*v1 + ... + tk*vk

    donde xp es una solución particular y los vectores
    vi pertenecen al espacio solución del sistema homogéneo
    asociado.

    No realiza Gauss-Jordan nuevamente.
    Utiliza directamente la matriz reducida que ya fue
    calculada por resolver_sistema().
    """

    if tipo == "ninguna":
        return None

    columnas_pivote, variables_libres = (
        obtener_pivotes_y_libres(
            matriz_reducida,
            cantidad_variables
        )
    )

    # --------------------------------------------------------
    # SISTEMA CON SOLUCIÓN ÚNICA
    # --------------------------------------------------------

    if tipo == "unica":

        return {
            "tipo": "unica",
            "solucion_particular": solucion,
            "vectores_direccion": [],
            "parametros": [],
            "forma_vectorial": solucion
        }

    # --------------------------------------------------------
    # SOLUCIONES INFINITAS
    # --------------------------------------------------------

    parametros = []

    for posicion, variable in enumerate(
        variables_libres
    ):
        parametros.append(
            nombre_parametro(posicion)
        )

    # --------------------------------------------------------
    # SOLUCIÓN PARTICULAR
    #
    # Todas las variables libres se hacen 0.
    # Entonces obtenemos una solución particular
    # del sistema no homogéneo.
    # --------------------------------------------------------

    solucion_particular = [
        0
        for _ in range(cantidad_variables)
    ]

    for fila in matriz_reducida:

        columna_pivote = None

        for j in range(cantidad_variables):

            if not es_cero(fila[j]):

                if j in columnas_pivote:

                    columna_pivote = j

                break

        if columna_pivote is None:
            continue

        solucion_particular[
            columna_pivote
        ] = fila[cantidad_variables]

    # --------------------------------------------------------
    # VECTORES DIRECCIÓN
    #
    # Cada variable libre genera un vector.
    #
    # Ejemplo:
    #
    # x3 = t
    #
    # genera:
    #
    # [4/3, 0, 1]
    #
    # --------------------------------------------------------

    vectores_direccion = []

    for variable_libre in variables_libres:

        vector = [
            0
            for _ in range(cantidad_variables)
        ]

        # La variable libre toma valor 1.
        vector[variable_libre] = 1

        # Las variables básicas se calculan
        # a partir de la matriz reducida.
        for fila in matriz_reducida:

            columna_pivote = None

            for j in range(cantidad_variables):

                if not es_cero(fila[j]):

                    if j in columnas_pivote:
                        columna_pivote = j

                    break

            if columna_pivote is None:
                continue

            coeficiente = fila[
                variable_libre
            ]

            vector[columna_pivote] = -coeficiente

        vector = [
            limpiar_numero(x)
            for x in vector
        ]

        vectores_direccion.append(
            vector
        )

    # --------------------------------------------------------
    # FORMA VECTORIAL
    # --------------------------------------------------------

    if tipo == "infinitas":

        if len(variables_libres) == 1:

            forma_vectorial = {
                "solucion_particular":
                    solucion_particular,

                "parametros":
                    parametros,

                "vectores_direccion":
                    vectores_direccion
            }

        else:

            forma_vectorial = {
                "solucion_particular":
                    solucion_particular,

                "parametros":
                    parametros,

                "vectores_direccion":
                    vectores_direccion
            }

    else:

        forma_vectorial = solucion_particular

    return {
        "tipo": tipo,

        "solucion_particular":
            solucion_particular,

        "vectores_direccion":
            vectores_direccion,

        "parametros":
            parametros,

        "forma_vectorial":
            forma_vectorial
    }

def resolver_sistema(A, b):
    """
    Resuelve la ecuación matricial:

        Ax = b

    utilizando Gauss-Jordan.

    Esta función es el núcleo matemático tanto para:

        1. Ecuaciones matriciales.
        2. Combinación lineal.

    Para combinación lineal:

        A = [v1 v2 ... vk]

    y:

        b = vector objetivo.

    Retorna toda la información necesaria para que el
    controlador y la interfaz puedan mostrar el resultado.
    """

    validar_matriz(A)

    validar_vector(b)

    if len(A) != len(b):

        raise ValueError(
            "A y b deben tener la misma cantidad "
            "de filas/componentes."
        )

    # ---------------------------------------------------------
    # CONSTRUIR [A | b]
    # ---------------------------------------------------------

    matriz_aumentada = construir_matriz_aumentada(
        A,
        b
    )

    # ---------------------------------------------------------
    # GAUSS-JORDAN
    # ---------------------------------------------------------

    resultado_gauss = gauss_jordan(
        matriz_aumentada
    )

    matriz_reducida = (
        resultado_gauss["matriz"]
    )

    # ---------------------------------------------------------
    # INFORMACIÓN DEL SISTEMA
    # ---------------------------------------------------------

    num_ecuaciones = len(A)

    num_variables = len(A[0])

    columnas_pivote, variables_libres = (
        obtener_pivotes_y_libres(
            matriz_reducida,
            num_variables
        )
    )

    rango_A = calcular_rango(
        matriz_reducida,
        num_variables
    )

    rango_Ab = calcular_rango(
        matriz_reducida,
        num_variables + 1
    )

    tipo = detectar_tipo_solucion(
        matriz_reducida,
        num_variables
    )

    # ---------------------------------------------------------
    # SOLUCIÓN
    # ---------------------------------------------------------

    solucion = None
    solucion_parametrica = None

    if tipo == "unica":

        solucion = obtener_solucion_unica(
            matriz_reducida,
            num_variables
        )

    elif tipo == "infinitas":

        solucion_parametrica = (
            obtener_solucion_parametrica(
                matriz_reducida,
                num_variables
            )
        )

    # --------------------------------------------------------
    # CONJUNTO SOLUCIÓN EN FORMA VECTORIAL
    # --------------------------------------------------------

    conjunto_solucion = obtener_conjunto_solucion(
        matriz_reducida,
        num_variables,
        tipo,
        solucion
    )
    # ---------------------------------------------------------
    # RETORNO
    # ---------------------------------------------------------

    return {

        # [A | b]
        "matriz_aumentada":
            matriz_aumentada,

        # Forma reducida
        "matriz_reducida":
            matriz_reducida,

        # Operaciones de Gauss-Jordan
        "proceso":
            resultado_gauss["proceso"],

        # Tipo:
        # "unica"
        # "infinitas"
        # "ninguna"
        "tipo":
            tipo,

        # Solución única
        "solucion":
            solucion,

        # Solución paramétrica
        "solucion_parametrica":
            solucion_parametrica,

        "conjunto_solucion":
        conjunto_solucion,

        # Rangos
        "rango_A":
            rango_A,

        "rango_Ab":
            rango_Ab,

        # Dimensiones
        "num_variables":
            num_variables,

        "num_ecuaciones":
            num_ecuaciones,

        # Pivotes y variables
        "columnas_pivote":
            columnas_pivote,

        "variables_basicas":
            columnas_pivote[:],

        "variables_libres":
            variables_libres
    }

