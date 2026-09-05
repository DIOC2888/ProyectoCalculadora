from config import TOLERANCIA
from formato import (
    formatear_numero,
    subindice
)


# ----------------------------------------------------------
# VERIFICAR SOLUCIÓN
# ----------------------------------------------------------

def verificar_solucion(
        matriz_original,
        soluciones,
        ecuaciones,
        variables
):

    print(
        "\nVERIFICACIÓN DE LA SOLUCIÓN:"
    )


    # Recorremos cada ecuación
    for i in range(ecuaciones):

        print(
            f"\nEcuación {i + 1}:"
        )


        lado_izquierdo = 0

        ecuacion_original = ""

        sustitucion = ""

        productos = ""


        for j in range(variables):


            coeficiente = (
                matriz_original[i][j]
            )

            solucion = soluciones[j]

            producto = (
                coeficiente
                * solucion
            )

            lado_izquierdo += producto


            # ----------------------------------------------
            # CONSTRUIR ECUACIÓN ORIGINAL
            # ----------------------------------------------

            coef_abs = formatear_numero(
                abs(coeficiente)
            )


            if j == 0:

                if coeficiente < 0:

                    ecuacion_original += "-"

                ecuacion_original += (
                    f"{coef_abs}"
                    f"x{subindice(j + 1)}"
                )


            else:

                if coeficiente < 0:

                    ecuacion_original += " - "

                else:

                    ecuacion_original += " + "


                ecuacion_original += (
                    f"{coef_abs}"
                    f"x{subindice(j + 1)}"
                )


            # ----------------------------------------------
            # CONSTRUIR SUSTITUCIÓN
            # ----------------------------------------------

            if j > 0:

                if coeficiente < 0:

                    sustitucion += " - "
                    productos += " - "

                else:

                    sustitucion += " + "
                    productos += " + "


            elif coeficiente < 0:

                sustitucion += "-"
                productos += "-"


            sustitucion += (
                f"({formatear_numero(abs(coeficiente))})"
                f"({formatear_numero(solucion)})"
            )


            productos += (
                formatear_numero(
                    abs(producto)
                )
            )


        lado_derecho = (
            matriz_original[i][variables]
        )


        # ----------------------------------------------
        # MOSTRAR PROCEDIMIENTO
        # ----------------------------------------------

        print("\nEcuación original:")

        print(
            f"{ecuacion_original} = "
            f"{formatear_numero(lado_derecho)}"
        )


        print("\nSustitución:")

        print(
            f"{sustitucion} = "
            f"{formatear_numero(lado_derecho)}"
        )


        print("\nOperaciones:")

        print(
            f"{productos} = "
            f"{formatear_numero(lado_derecho)}"
        )


        print("\nResultado:")

        print(
            f"{formatear_numero(lado_izquierdo)} "
            f"= "
            f"{formatear_numero(lado_derecho)}"
        )


        # ----------------------------------------------
        # COMPROBAR RESULTADO
        # ----------------------------------------------

        if abs(
            lado_izquierdo
            - lado_derecho
        ) < TOLERANCIA:

            print(
                "/ Ecuación verificada correctamente"
            )

        else:

            print(
                "X La ecuación no se cumple"
            )