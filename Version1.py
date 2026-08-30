# ==========================================================
# PROGRAMA 1 - ÁLGEBRA LINEAL
# Solución de sistemas por eliminación por filas
# ==========================================================

TOLERANCIA = 0.0000001


# ----------------------------------------------------------
# 1. INGRESO DE DATOS
# ----------------------------------------------------------

def ingresar_matriz():
    ecuaciones = int(input("Cantidad de ecuaciones: "))
    variables = int(input("Cantidad de variables: "))

    matriz = []

    for i in range(ecuaciones):
        fila = []

        print("\nEcuación", i + 1)

        # Ingresar coeficientes de las variables
        for j in range(variables):
            valor = float(input(f"Coeficiente de x{j + 1}: "))
            fila.append(valor)

        # Ingresar término independiente
        independiente = float(input("Término independiente: "))
        fila.append(independiente)

        matriz.append(fila)

    return matriz, ecuaciones, variables


# ----------------------------------------------------------
# 2. MOSTRAR MATRIZ
# ----------------------------------------------------------

def mostrar_matriz(matriz):
    print()

    for fila in matriz:
        for numero in fila:
            print(f"{numero:10.2f}", end=" ")
        print()

    print()


# ----------------------------------------------------------
# 3. ELIMINACIÓN GAUSSIANA
# Lleva la matriz a FORMA ESCALONADA
# ----------------------------------------------------------

def eliminacion_gaussiana(matriz, ecuaciones, variables):

    fila_pivote = 0
    columnas_pivote = []

    # Recorremos las columnas de las variables
    for columna in range(variables):

        # Si ya no quedan filas disponibles, terminamos
        if fila_pivote >= ecuaciones:
            break

        # Buscar una fila con un valor distinto de cero
        # para usarlo como pivote
        fila_encontrada = -1

        for fila in range(fila_pivote, ecuaciones):

            if abs(matriz[fila][columna]) > TOLERANCIA:
                fila_encontrada = fila
                break

        # Si en esa columna no encontramos pivote,
        # pasamos a la siguiente columna
        if fila_encontrada == -1:
            continue

        # --------------------------------------------------
        # INTERCAMBIO DE FILAS
        # Fi <-> Fj
        # --------------------------------------------------

        if fila_encontrada != fila_pivote:

            matriz[fila_pivote], matriz[fila_encontrada] = (
                matriz[fila_encontrada],
                matriz[fila_pivote]
            )

            print(
                f"Intercambio: F{fila_pivote + 1} "
                f"<-> F{fila_encontrada + 1}"
            )

            mostrar_matriz(matriz)

        # Guardamos la columna donde encontramos un pivote
        columnas_pivote.append(columna)

        pivote = matriz[fila_pivote][columna]

        # --------------------------------------------------
        # GENERAR CEROS DEBAJO DEL PIVOTE
        #
        # factor =
        # numero que queremos eliminar / pivote
        #
        # Fi -> Fi - factor * Fpivote
        # --------------------------------------------------

        for fila in range(fila_pivote + 1, ecuaciones):

            numero_eliminar = matriz[fila][columna]

            if abs(numero_eliminar) > TOLERANCIA:

                factor = numero_eliminar / pivote

                print(
                    f"F{fila + 1} -> F{fila + 1} "
                    f"- ({factor:.2f})F{fila_pivote + 1}"
                )

                # Aplicamos la operación a toda la fila
                for j in range(columna, variables + 1):

                    matriz[fila][j] = (
                        matriz[fila][j]
                        - factor * matriz[fila_pivote][j]
                    )

                    # Limpiar errores decimales muy pequeños
                    if abs(matriz[fila][j]) < TOLERANCIA:
                        matriz[fila][j] = 0.0

                mostrar_matriz(matriz)

        # Pasamos a la siguiente fila de pivote
        fila_pivote += 1

    return columnas_pivote


# ----------------------------------------------------------
# 4. DETECTAR SI EL SISTEMA ES INCONSISTENTE
#
# Ejemplo:
# 0x + 0y + 0z = 5
#
# Eso sería imposible, por lo tanto no hay solución.
# ----------------------------------------------------------

def es_inconsistente(matriz, ecuaciones, variables):

    for i in range(ecuaciones):

        todos_cero = True

        # Revisar solamente los coeficientes
        for j in range(variables):

            if abs(matriz[i][j]) > TOLERANCIA:
                todos_cero = False
                break

        # Si todos los coeficientes son 0
        # pero el término independiente NO es 0
        if todos_cero and abs(matriz[i][variables]) > TOLERANCIA:
            return True

    return False


# ----------------------------------------------------------
# 5. SUSTITUCIÓN HACIA ATRÁS
# Se utiliza cuando existe solución única
# ----------------------------------------------------------

def sustitucion_atras(matriz, columnas_pivote, variables):

    soluciones = [0.0] * variables

    # Empezamos desde el último pivote y subimos
    for i in range(len(columnas_pivote) - 1, -1, -1):

        columna = columnas_pivote[i]

        resultado = matriz[i][variables]

        # Restar las variables que ya conocemos
        for j in range(columna + 1, variables):

            resultado = (
                resultado
                - matriz[i][j] * soluciones[j]
            )

        soluciones[columna] = (
            resultado / matriz[i][columna]
        )

    return soluciones


# ----------------------------------------------------------
# 6. VERIFICAR LA SOLUCIÓN
# Sustituye los resultados en el sistema original
# ----------------------------------------------------------

def verificar_solucion(
        matriz_original,
        soluciones,
        ecuaciones,
        variables
):

    print("\nVERIFICACIÓN:")

    for i in range(ecuaciones):

        lado_izquierdo = 0

        for j in range(variables):

            lado_izquierdo += (
                matriz_original[i][j]
                * soluciones[j]
            )

        lado_derecho = matriz_original[i][variables]

        print(
            f"Ecuación {i + 1}: "
            f"{lado_izquierdo:.2f} = "
            f"{lado_derecho:.2f}",
            end=" "
        )

        if abs(
            lado_izquierdo - lado_derecho
        ) < TOLERANCIA:

            print("✓ Correcto")

        else:
            print("✗ Incorrecto")


# ----------------------------------------------------------
# 7. FORMA ESCALONADA REDUCIDA
#
# Continúa desde la forma escalonada obtenida anteriormente.
#
# 1. Convierte cada pivote en 1.
# 2. Genera ceros ENCIMA de cada pivote.
# ----------------------------------------------------------

def forma_reducida(
        matriz,
        columnas_pivote,
        variables
):

    # Recorremos los pivotes desde abajo hacia arriba
    for i in range(
        len(columnas_pivote) - 1,
        -1,
        -1
    ):

        columna = columnas_pivote[i]

        pivote = matriz[i][columna]

        # --------------------------------------------------
        # CONVERTIR EL PIVOTE EN 1
        #
        # Fi -> Fi / pivote
        # --------------------------------------------------

        if abs(pivote - 1) > TOLERANCIA:

            print(
                f"F{i + 1} -> "
                f"F{i + 1} / {pivote:.2f}"
            )

            for j in range(
                columna,
                variables + 1
            ):

                matriz[i][j] = (
                    matriz[i][j] / pivote
                )

                if abs(
                    matriz[i][j]
                ) < TOLERANCIA:

                    matriz[i][j] = 0.0

            mostrar_matriz(matriz)

        # --------------------------------------------------
        # GENERAR CEROS ENCIMA DEL PIVOTE
        #
        # Fi -> Fi - factor * Fpivote
        # --------------------------------------------------

        for fila in range(i):

            factor = matriz[fila][columna]

            if abs(factor) > TOLERANCIA:

                print(
                    f"F{fila + 1} -> "
                    f"F{fila + 1} "
                    f"- ({factor:.2f})F{i + 1}"
                )

                for j in range(
                    columna,
                    variables + 1
                ):

                    matriz[fila][j] = (
                        matriz[fila][j]
                        - factor * matriz[i][j]
                    )

                    if abs(
                        matriz[fila][j]
                    ) < TOLERANCIA:

                        matriz[fila][j] = 0.0

                mostrar_matriz(matriz)


# ==========================================================
# 8. PROGRAMA PRINCIPAL
# ==========================================================

matriz, ecuaciones, variables = ingresar_matriz()


# ----------------------------------------------------------
# Guardar una copia del sistema original
# La necesitaremos para verificar la solución.
# ----------------------------------------------------------

matriz_original = []

for fila in matriz:
    matriz_original.append(fila.copy())


# ----------------------------------------------------------
# MOSTRAR MATRIZ ORIGINAL
# ----------------------------------------------------------

print("\nMATRIZ AUMENTADA INICIAL:")

mostrar_matriz(matriz)


# ----------------------------------------------------------
# ELIMINACIÓN GAUSSIANA
# ----------------------------------------------------------

print("PROCESO DE ELIMINACIÓN:")

columnas_pivote = eliminacion_gaussiana(
    matriz,
    ecuaciones,
    variables
)


print("\nMATRIZ ESCALONADA FINAL:")

mostrar_matriz(matriz)


# ----------------------------------------------------------
# OPCIÓN DE FORMA ESCALONADA REDUCIDA
# ----------------------------------------------------------

print("¿Desea obtener la forma escalonada reducida?")
print("1. Sí")
print("2. No")

opcion = input("Seleccione una opción: ")


if opcion == "1" or opcion.lower() == "sí" or opcion.lower() == "si":

    print("\nPROCESO DE REDUCCIÓN:")

    forma_reducida(
        matriz,
        columnas_pivote,
        variables
    )

    print(
        "\nMATRIZ ESCALONADA REDUCIDA FINAL:"
    )

    mostrar_matriz(matriz)


# ----------------------------------------------------------
# 9. CLASIFICACIÓN DEL SISTEMA
# ----------------------------------------------------------

if es_inconsistente(
    matriz,
    ecuaciones,
    variables
):

    print("CLASIFICACIÓN:")
    print(
        "Sistema Inconsistente: "
        "Sin Solución."
    )


elif len(columnas_pivote) < variables:

    print("CLASIFICACIÓN:")

    print(
        "Sistema Consistente Indeterminado: "
        "Presenta Infinitas Soluciones."
    )

    print("\nVariables libres:")

    for j in range(variables):

        if j not in columnas_pivote:
            print(f"x{j + 1}")


else:

    print("CLASIFICACIÓN:")

    print(
        "Sistema Consistente Determinado: "
        "Presenta Solución Única."
    )

    # Calcular los valores de las variables
    soluciones = sustitucion_atras(
        matriz,
        columnas_pivote,
        variables
    )

    print("\nSOLUCIONES:")

    for i in range(variables):

        print(
            f"x{i + 1} = "
            f"{soluciones[i]:.4f}"
        )

    # Comprobar las respuestas usando
    # el sistema original
    verificar_solucion(
        matriz_original,
        soluciones,
        ecuaciones,
        variables
    )