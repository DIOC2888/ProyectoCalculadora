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
# 3. ELIMINACIÓN POR FILAS
# ----------------------------------------------------------

def eliminacion_gaussiana(matriz, ecuaciones, variables):

    fila_pivote = 0
    columnas_pivote = []

    # Recorremos cada columna de variables
    for columna in range(variables):

        # Buscar una fila que tenga un valor distinto de cero
        # en la columna donde queremos colocar el pivote
        fila_encontrada = -1

        for fila in range(fila_pivote, ecuaciones):
            if abs(matriz[fila][columna]) > TOLERANCIA:
                fila_encontrada = fila
                break

        # Si toda la columna tiene ceros, pasamos a la siguiente
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

        # Guardamos en qué columna está el pivote
        columnas_pivote.append(columna)

        pivote = matriz[fila_pivote][columna]

        # --------------------------------------------------
        # GENERAR CEROS DEBAJO DEL PIVOTE
        # Fi -> Fi - factor * Fpivote
        # --------------------------------------------------

        for fila in range(fila_pivote + 1, ecuaciones):

            numero_eliminar = matriz[fila][columna]

            if abs(numero_eliminar) > TOLERANCIA:

                # factor = número que queremos eliminar / pivote
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

                    # Evitar valores como 0.000000000001
                    if abs(matriz[fila][j]) < TOLERANCIA:
                        matriz[fila][j] = 0.0

                mostrar_matriz(matriz)

        # Pasamos al siguiente pivote
        fila_pivote += 1

        if fila_pivote == ecuaciones:
            break

    return columnas_pivote


# ----------------------------------------------------------
# 4. DETECTAR SI EL SISTEMA ES INCONSISTENTE
# ----------------------------------------------------------

def es_inconsistente(matriz, ecuaciones, variables):

    for i in range(ecuaciones):

        todos_cero = True

        # Revisamos los coeficientes
        for j in range(variables):

            if abs(matriz[i][j]) > TOLERANCIA:
                todos_cero = False
                break

        # Caso:
        # 0x + 0y + 0z = número distinto de cero
        if todos_cero and abs(matriz[i][variables]) > TOLERANCIA:
            return True

    return False


# ----------------------------------------------------------
# 5. SUSTITUCIÓN HACIA ATRÁS
# Se utiliza cuando existe solución única
# ----------------------------------------------------------

def sustitucion_atras(matriz, columnas_pivote, variables):

    soluciones = [0.0] * variables

    # Empezamos desde la última fila con pivote
    for i in range(len(columnas_pivote) - 1, -1, -1):

        columna = columnas_pivote[i]

        resultado = matriz[i][variables]

        # Restamos las variables que ya conocemos
        for j in range(columna + 1, variables):

            resultado -= (
                matriz[i][j] * soluciones[j]
            )

        soluciones[columna] = (
            resultado / matriz[i][columna]
        )

    return soluciones


# ----------------------------------------------------------
# 6. VERIFICAR LA SOLUCIÓN
# Sustituye los valores encontrados en el sistema original
# ----------------------------------------------------------

def verificar_solucion(matriz_original, soluciones, ecuaciones, variables):

    print("\nVERIFICACIÓN:")

    for i in range(ecuaciones):

        lado_izquierdo = 0

        for j in range(variables):

            lado_izquierdo += (
                matriz_original[i][j] * soluciones[j]
            )

        lado_derecho = matriz_original[i][variables]

        print(
            f"Ecuación {i + 1}: "
            f"{lado_izquierdo:.2f} = {lado_derecho:.2f}",
            end=" "
        )

        if abs(lado_izquierdo - lado_derecho) < TOLERANCIA:
            print("✓ Correcto")
        else:
            print("✗ Incorrecto")


# ----------------------------------------------------------
# 7. PROGRAMA PRINCIPAL
# ----------------------------------------------------------

matriz, ecuaciones, variables = ingresar_matriz()

# Guardamos una copia del sistema original para verificar después
matriz_original = []

for fila in matriz:
    matriz_original.append(fila.copy())


print("\nMATRIZ AUMENTADA INICIAL:")
mostrar_matriz(matriz)


print("PROCESO DE ELIMINACIÓN:")

columnas_pivote = eliminacion_gaussiana(
    matriz,
    ecuaciones,
    variables
)


print("\nMATRIZ ESCALONADA FINAL:")
mostrar_matriz(matriz)


# ----------------------------------------------------------
# 8. CLASIFICACIÓN DEL SISTEMA
# ----------------------------------------------------------

if es_inconsistente(matriz, ecuaciones, variables):

    print("CLASIFICACIÓN:")
    print("Sistema Inconsistente: Sin Solución.")


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

    soluciones = sustitucion_atras(
        matriz,
        columnas_pivote,
        variables
    )

    print("\nSOLUCIONES:")

    for i in range(variables):
        print(f"x{i + 1} = {soluciones[i]:.4f}")

    verificar_solucion(
        matriz_original,
        soluciones,
        ecuaciones,
        variables
    )