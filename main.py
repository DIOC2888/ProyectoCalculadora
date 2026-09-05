from entrada import ingresar_matriz

from formato import (
    mostrar_matriz,
    formatear_numero,
    subindice
)

from eliminacion import (
    eliminacion_gaussiana,
    forma_reducida
)

from sistema import (
    clasificar_sistema,
    identificar_variables,
    sustitucion_atras
)

from verificacion import (
    verificar_solucion
)


# ==========================================================
# PROGRAMA PRINCIPAL
# ==========================================================

matriz, ecuaciones, variables = (
    ingresar_matriz()
)


# ----------------------------------------------------------
# GUARDAR MATRIZ ORIGINAL
# ----------------------------------------------------------

matriz_original = []

for fila in matriz:

    matriz_original.append(
        fila.copy()
    )


# ----------------------------------------------------------
# MOSTRAR MATRIZ INICIAL
# ----------------------------------------------------------

print(
    "\nMATRIZ AUMENTADA INICIAL:"
)

mostrar_matriz(matriz)


# ----------------------------------------------------------
# ELIMINACIÓN GAUSSIANA
# ----------------------------------------------------------

print(
    "\nPROCESO DE ELIMINACIÓN:"
)

columnas_pivote = (
    eliminacion_gaussiana(
        matriz,
        ecuaciones,
        variables
    )
)


print(
    "\nMATRIZ ESCALONADA FINAL:"
)

mostrar_matriz(matriz)


# ----------------------------------------------------------
# FORMA ESCALONADA REDUCIDA
# ----------------------------------------------------------

print(
    "¿Desea obtener la "
    "forma escalonada reducida?"
)

print("1. Sí")
print("2. No")


opcion = input(
    "Seleccione una opción: "
)


if (
    opcion == "1"
    or opcion.lower() == "si"
    or opcion.lower() == "sí"
):

    print(
        "\nPROCESO DE GAUSS-JORDAN:"
    )

    forma_reducida(
        matriz,
        columnas_pivote,
        variables
    )


    print(
        "\nMATRIZ ESCALONADA "
        "REDUCIDA FINAL:"
    )

    mostrar_matriz(matriz)


# ----------------------------------------------------------
# CLASIFICAR SISTEMA
# ----------------------------------------------------------

tipo = clasificar_sistema(
    matriz,
    ecuaciones,
    variables,
    columnas_pivote
)


# ----------------------------------------------------------
# SISTEMA INCONSISTENTE
# ----------------------------------------------------------

if tipo == "inconsistente":

    print(
        "\nCLASIFICACIÓN:"
    )

    print(
        "Sistema Inconsistente: "
        "Sin Solución."
    )


# ----------------------------------------------------------
# SISTEMA CONSISTENTE
# ----------------------------------------------------------

else:

    variables_basicas, variables_libres = (
        identificar_variables(
            columnas_pivote,
            variables
        )
    )


    # Mostrar variables básicas
    print(
        "\nVARIABLES BÁSICAS:"
    )

    if len(
        variables_basicas
    ) == 0:

        print("Ninguna")

    else:

        for variable in variables_basicas:

            print(
                f"x{subindice(variable + 1)}"
            )


    # Mostrar variables libres
    print(
        "\nVARIABLES LIBRES:"
    )

    if len(
        variables_libres
    ) == 0:

        print("Ninguna")

    else:

        for variable in variables_libres:

            print(
                f"x{subindice(variable + 1)}"
            )


    # ------------------------------------------------------
    # INFINITAS SOLUCIONES
    # ------------------------------------------------------

    if tipo == "indeterminado":

        print(
            "\nCLASIFICACIÓN:"
        )

        print(
            "Sistema Consistente "
            "Indeterminado: "
            "Presenta Infinitas Soluciones."
        )


    # ------------------------------------------------------
    # SOLUCIÓN ÚNICA
    # ------------------------------------------------------

    elif tipo == "determinado":

        print(
            "\nCLASIFICACIÓN:"
        )

        print(
            "Sistema Consistente "
            "Determinado: "
            "Presenta Solución Única."
        )


        soluciones = (
            sustitucion_atras(
                matriz,
                columnas_pivote,
                variables
            )
        )


        print(
            "\nSOLUCIONES:"
        )


        for i in range(variables):

            print(
                f"x{subindice(i + 1)} = "
                f"{formatear_numero(soluciones[i])}"
            )


        # Verificar utilizando
        # las ecuaciones originales
        verificar_solucion(
            matriz_original,
            soluciones,
            ecuaciones,
            variables
        )