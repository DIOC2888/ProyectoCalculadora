from fractions import Fraction
from formato import subindice


# ----------------------------------------------------------
# CONVERTIR ENTRADA A NÚMERO
# Permite escribir:
# 0.5
# 1/2
# -3
# ----------------------------------------------------------

def convertir_numero(texto):

    # Permitimos usar coma decimal
    texto = texto.replace(",", ".")

    # Fraction puede interpretar enteros,
    # decimales y fracciones
    return float(Fraction(texto))


# ----------------------------------------------------------
# PEDIR UN NÚMERO AL USUARIO
# ----------------------------------------------------------

def pedir_numero(mensaje):

    while True:

        try:

            texto = input(mensaje)

            return convertir_numero(texto)

        except ValueError:

            print(
                "Entrada inválida. "
                "Ingrese un número o fracción."
            )


# ----------------------------------------------------------
# INGRESAR MATRIZ
# ----------------------------------------------------------

def ingresar_matriz():

    ecuaciones = int(
        input("Cantidad de ecuaciones: ")
    )

    variables = int(
        input("Cantidad de variables: ")
    )

    matriz = []

    for i in range(ecuaciones):

        fila = []

        print(
            f"\nEcuación {i + 1}"
        )

        # Ingresar coeficientes
        for j in range(variables):

            valor = pedir_numero(
                f"Coeficiente de "
                f"x{subindice(j + 1)}: "
            )

            fila.append(valor)

        # Ingresar término independiente
        independiente = pedir_numero(
            "Término independiente: "
        )

        fila.append(independiente)

        matriz.append(fila)

    return matriz, ecuaciones, variables