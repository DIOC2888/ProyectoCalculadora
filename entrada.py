from fractions import Fraction
from formato import subindice


# Este modulo se usa en la version de consola del proyecto.
# Centraliza la lectura de numeros para aceptar enteros, decimales
# y fracciones sin cambiar los algoritmos de eliminacion.


# ----------------------------------------------------------
# CONVERTIR ENTRADA A NÚMERO
# Permite escribir:
# 0.5
# 1/2
# -3
# ----------------------------------------------------------

def convertir_numero(texto):
    """Convierte texto ingresado por el usuario a float.

    Fraction permite aceptar entradas como "1/3" o "-2/5".
    """

    # Permitimos usar coma decimal
    texto = texto.replace(",", ".")

    # Fraction puede interpretar enteros,
    # decimales y fracciones
    return float(Fraction(texto))


# ----------------------------------------------------------
# PEDIR UN NÚMERO AL USUARIO
# ----------------------------------------------------------

def pedir_numero(mensaje):
    """Pide un numero hasta recibir una entrada valida."""

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
    """Lee coeficientes desde consola y construye una matriz aumentada."""

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
