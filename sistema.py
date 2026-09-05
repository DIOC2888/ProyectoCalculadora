from config import TOLERANCIA


# ----------------------------------------------------------
# DETECTAR SISTEMA INCONSISTENTE
# ----------------------------------------------------------

def es_inconsistente(
        matriz,
        ecuaciones,
        variables
):

    for i in range(ecuaciones):

        todos_cero = True


        # Revisar coeficientes
        for j in range(variables):

            if abs(
                matriz[i][j]
            ) > TOLERANCIA:

                todos_cero = False

                break


        # Ejemplo:
        #
        # 0x + 0y + 0z = 5
        #
        # Esto representa 0 = 5
        if (
            todos_cero
            and abs(
                matriz[i][variables]
            ) > TOLERANCIA
        ):

            return True


    return False


# ----------------------------------------------------------
# IDENTIFICAR VARIABLES BÁSICAS Y LIBRES
# ----------------------------------------------------------

def identificar_variables(
        columnas_pivote,
        variables
):

    variables_basicas = []
    variables_libres = []


    for j in range(variables):

        # Si la columna tiene pivote,
        # la variable es básica
        if j in columnas_pivote:

            variables_basicas.append(j)

        # Si no tiene pivote,
        # es variable libre
        else:

            variables_libres.append(j)


    return (
        variables_basicas,
        variables_libres
    )


# ----------------------------------------------------------
# CLASIFICAR SISTEMA
# ----------------------------------------------------------

def clasificar_sistema(
        matriz,
        ecuaciones,
        variables,
        columnas_pivote
):

    # Primero comprobamos contradicciones
    if es_inconsistente(
        matriz,
        ecuaciones,
        variables
    ):

        return "inconsistente"


    # Si faltan pivotes para alguna variable,
    # existen infinitas soluciones
    if len(
        columnas_pivote
    ) < variables:

        return "indeterminado"


    # Si hay pivote para todas las variables
    return "determinado"


# ----------------------------------------------------------
# SUSTITUCIÓN HACIA ATRÁS
# ----------------------------------------------------------

def sustitucion_atras(
        matriz,
        columnas_pivote,
        variables
):

    # Creamos una lista para guardar
    # las soluciones
    soluciones = [0.0] * variables


    # Empezamos desde la última fila
    # y vamos subiendo
    for i in range(
        len(columnas_pivote) - 1,
        -1,
        -1
    ):

        columna = columnas_pivote[i]


        # Empezamos con el término independiente
        resultado = matriz[i][variables]


        # Restamos las variables
        # que ya conocemos
        for j in range(
            columna + 1,
            variables
        ):

            resultado = (
                resultado
                - matriz[i][j]
                * soluciones[j]
            )


        # Despejamos la variable
        soluciones[columna] = (
            resultado
            / matriz[i][columna]
        )


    return soluciones
