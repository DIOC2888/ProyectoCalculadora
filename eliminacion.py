from config import TOLERANCIA
from formato import (
    mostrar_matriz,
    formatear_numero
)


# ----------------------------------------------------------
# ELIMINACIÓN GAUSSIANA
# Lleva la matriz a forma escalonada
# ----------------------------------------------------------

def eliminacion_gaussiana(
        matriz,
        ecuaciones,
        variables
):

    fila_pivote = 0

    # Guarda las columnas que contienen pivotes
    columnas_pivote = []


    # Recorremos las columnas de las variables
    for columna in range(variables):


        # Si ya no quedan filas disponibles,
        # terminamos
        if fila_pivote >= ecuaciones:
            break


        # --------------------------------------------------
        # BUSCAR UN PIVOTE VÁLIDO
        # --------------------------------------------------

        fila_encontrada = -1

        for fila in range(
            fila_pivote,
            ecuaciones
        ):

            # Buscamos un valor diferente de cero
            if abs(
                matriz[fila][columna]
            ) > TOLERANCIA:

                fila_encontrada = fila

                break


        # Si no hay pivote en esta columna,
        # pasamos a la siguiente
        if fila_encontrada == -1:
            continue


        # --------------------------------------------------
        # INTERCAMBIO DE FILAS
        # --------------------------------------------------

        if fila_encontrada != fila_pivote:

            matriz[
                fila_pivote
            ], matriz[
                fila_encontrada
            ] = (
                matriz[fila_encontrada],
                matriz[fila_pivote]
            )


            print(
                f"F{fila_pivote + 1} "
                f"<-> "
                f"F{fila_encontrada + 1}"
            )

            mostrar_matriz(matriz)


        # Guardamos la columna del pivote
        columnas_pivote.append(
            columna
        )


        # Obtener el pivote
        pivote = matriz[
            fila_pivote
        ][columna]


        # --------------------------------------------------
        # GENERAR CEROS DEBAJO DEL PIVOTE
        # --------------------------------------------------

        for fila in range(
            fila_pivote + 1,
            ecuaciones
        ):

            # Número que queremos eliminar
            numero_eliminar = matriz[
                fila
            ][columna]


            # Solo hacemos la operación
            # si no es cero
            if abs(
                numero_eliminar
            ) > TOLERANCIA:


                # factor =
                # número a eliminar / pivote
                factor = (
                    numero_eliminar
                    / pivote
                )


                print(
                    f"F{fila + 1} -> "
                    f"F{fila + 1} - "
                    f"({formatear_numero(factor)})"
                    f"F{fila_pivote + 1}"
                )


                # Aplicamos la operación
                # a toda la fila
                for j in range(
                    columna,
                    variables + 1
                ):

                    matriz[fila][j] = (
                        matriz[fila][j]
                        - factor
                        * matriz[
                            fila_pivote
                        ][j]
                    )


                    # Limpiar errores pequeños
                    if abs(
                        matriz[fila][j]
                    ) < TOLERANCIA:

                        matriz[fila][j] = 0.0


                mostrar_matriz(matriz)


        # Pasamos al siguiente pivote
        fila_pivote += 1


    return columnas_pivote


# ----------------------------------------------------------
# FORMA ESCALONADA REDUCIDA
# Método de Gauss-Jordan
# ----------------------------------------------------------

def forma_reducida(
        matriz,
        columnas_pivote,
        variables
):

    # Empezamos desde el último pivote
    # y subimos
    for i in range(
        len(columnas_pivote) - 1,
        -1,
        -1
    ):

        columna = columnas_pivote[i]

        pivote = matriz[i][columna]


        # --------------------------------------------------
        # CONVERTIR PIVOTE EN 1
        # Fi -> Fi / pivote
        # --------------------------------------------------

        if abs(
            pivote - 1
        ) > TOLERANCIA:

            print(
                f"F{i + 1} -> "
                f"F{i + 1} / "
                f"{formatear_numero(pivote)}"
            )


            for j in range(
                columna,
                variables + 1
            ):

                matriz[i][j] = (
                    matriz[i][j]
                    / pivote
                )


                if abs(
                    matriz[i][j]
                ) < TOLERANCIA:

                    matriz[i][j] = 0.0


            mostrar_matriz(matriz)


        # --------------------------------------------------
        # GENERAR CEROS ENCIMA DEL PIVOTE
        # --------------------------------------------------

        for fila in range(i):

            factor = matriz[
                fila
            ][columna]


            if abs(
                factor
            ) > TOLERANCIA:


                print(
                    f"F{fila + 1} -> "
                    f"F{fila + 1} - "
                    f"({formatear_numero(factor)})"
                    f"F{i + 1}"
                )


                for j in range(
                    columna,
                    variables + 1
                ):

                    matriz[fila][j] = (
                        matriz[fila][j]
                        - factor
                        * matriz[i][j]
                    )


                    if abs(
                        matriz[fila][j]
                    ) < TOLERANCIA:

                        matriz[fila][j] = 0.0


                mostrar_matriz(matriz)