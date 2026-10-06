"""Formato de valores matematicos para consola e interfaz.

Centraliza subindices, superindices y conversion de numeros a texto.
Esto evita repetir reglas de presentacion en cada modulo algebraico.
"""

from fractions import Fraction
from config import TOLERANCIA


# Funciones de presentacion matematica.
# Separar este formateo evita repetir logica en consola, backend e interfaz.

# ----------------------------------------------------------
# CONVERTIR NÚMEROS A SUBÍNDICES
# Ejemplo: 1 -> ₁
# ----------------------------------------------------------

def subindice(numero):
    """Convierte digitos normales a simbolos de subindice para x1, x2, etc."""

    tabla = str.maketrans(
        "0123456789",
        "₀₁₂₃₄₅₆₇₈₉"
    )

    return str(numero).translate(tabla)


def superindice(numero):
    """Convierte digitos y signos comunes a simbolos de superindice."""

    tabla = str.maketrans(
        "0123456789+-()",
        "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁽⁾"
    )
    return str(numero).translate(tabla)


# ----------------------------------------------------------
# MOSTRAR DECIMALES COMO FRACCIONES
# ----------------------------------------------------------

def formatear_decimal(numero, decimales=4):
    """Muestra un decimal limpio, eliminando ceros finales innecesarios."""

    if abs(numero - round(numero)) < TOLERANCIA:
        return str(int(round(numero)))

    texto = f"{numero:.{decimales}f}"
    texto = texto.rstrip("0").rstrip(".")

    if texto == "-0" or texto == "":
        return "0"

    return texto


def formatear_numero(numero):
    """Devuelve una representacion amigable para resultados matematicos.

    Si el valor esta cerca de un entero, se muestra como entero. Si se puede
    aproximar bien como fraccion pequena, se muestra como fraccion.
    """

    # Si está muy cerca de un número entero,
    # se muestra como entero
    if abs(numero - round(numero)) < TOLERANCIA:
        return str(int(round(numero)))

    # Convertimos el decimal a fracción
    fraccion = Fraction(numero).limit_denominator(1000)

    if abs(float(fraccion) - numero) > TOLERANCIA:
        return formatear_decimal(numero)

    return (
        f"{fraccion.numerator}/"
        f"{fraccion.denominator}"
    )


# ----------------------------------------------------------
# MOSTRAR MATRIZ AUMENTADA
# ----------------------------------------------------------

def mostrar_matriz(matriz):
    """Imprime una matriz aumentada en formato de consola."""

    print()

    # La última columna es el término independiente
    variables = len(matriz[0]) - 1

    # Encabezados
    print("    ", end="")

    for j in range(variables):

        nombre = "x" + subindice(j + 1)

        print(f"{nombre:>8}", end=" ")

    print(" |       TI")


    # Mostrar las filas
    for fila in matriz:

        print("[ ", end="")

        # Mostrar coeficientes
        for j in range(variables):

            numero = formatear_numero(
                fila[j]
            )

            print(
                f"{numero:>8}",
                end=" "
            )

        # Separar término independiente
        print("|", end=" ")

        independiente = formatear_numero(
            fila[variables]
        )

        print(
            f"{independiente:>8}",
            end=" "
        )

        print("]")

    print()

#Para probar la interfaz 
    # ----------------------------------------------------------
# FUNCIONES PARA EL FRONTEND (GUI)
# ----------------------------------------------------------

def copiar_matriz(matriz):
    """Crea una copia independiente de la matriz."""
    return [fila.copy() for fila in matriz]


def obtener_representacion_matriz(matriz):
    """Devuelve la matriz en un formato de texto limpio para mostrar en la interfaz."""
    variables = len(matriz[0]) - 1
    filas_texto = []

    # Encabezado
    encabezado = "    " + " ".join([f"x{subindice(j + 1):>8}" for j in range(variables)]) + " |       TI"
    filas_texto.append(encabezado)

    # Filas
    for fila in matriz:
        linea = "[ "
        for j in range(variables):
            linea += f"{formatear_numero(fila[j]):>8} "
        linea += f"| {formatear_numero(fila[variables]):>8} ]"
        filas_texto.append(linea)

    return "\n".join(filas_texto)
