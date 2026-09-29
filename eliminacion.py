from config import TOLERANCIA
from formato import (
    copiar_matriz,
    mostrar_matriz,
    formatear_numero,
    obtener_representacion_matriz,
   
)


# Este modulo modifica matrices aumentadas mediante operaciones
# elementales y guarda un historial para mostrar el proceso en la GUI.


# ----------------------------------------------------------
# ELIMINACIÓN GAUSSIANA
# Lleva la matriz a forma escalonada
# ----------------------------------------------------------

def eliminacion_gaussiana(
        matriz,
        ecuaciones,
        variables
):
    """Convierte la matriz aumentada a forma escalonada y registra pasos.

    Este primer recorrido solo crea ceros debajo de cada pivote. Despues,
    forma_reducida() completa Gauss-Jordan creando ceros encima.
    """

    fila_pivote = 0

    # Guarda las columnas que contienen pivotes.
    columnas_pivote = []

    # Cada paso incluye la operacion y una copia de la matriz para la GUI.
    pasos = []

    # Recorremos las columnas de las variables de izquierda a derecha.
    # Si una columna no tiene pivote, se salta y puede producir una
    # variable libre en la solucion.
    for columna in range(variables):


        # Si ya no quedan filas disponibles,
        # terminamos
        if fila_pivote >= ecuaciones:
            break


        # --------------------------------------------------
        # BUSCAR UN PIVOTE VÁLIDO
        # --------------------------------------------------
        # Buscamos desde la fila actual hacia abajo para no modificar
        # las filas que ya tienen pivotes correctos.

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
        # Si el pivote aparece mas abajo, subimos esa fila. Este paso
        # evita dividir entre cero y mantiene el metodo ordenado.

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

            # Registrar el intercambio para la vista de proceso.
            operacion_str = f"F{fila_pivote + 1} <-> F{fila_encontrada + 1}"
            
            matriz_formateada = [[formatear_numero(val) for val in fila_mat] for fila_mat in matriz]
            
            pasos.append({
                "operacion": operacion_str,
                "matriz": matriz_formateada,
                "matriz_str": obtener_representacion_matriz(matriz)
            })

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
        # Para cada fila inferior, calculamos cuanto de la fila pivote
        # debe restarse para anular la entrada de esta columna.

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
                # Registrar la eliminacion para la vista de proceso.
                operacion_str = (
                    f"F{fila + 1} -> "
                    f"F{fila + 1} - "
                    f"({formatear_numero(factor)})"
                    f"F{fila_pivote + 1}"
                )
                
                matriz_formateada = [[formatear_numero(val) for val in fila_mat] for fila_mat in matriz]
                
                pasos.append({
                    "operacion": operacion_str,
                    "matriz": matriz_formateada,
                    "matriz_str": obtener_representacion_matriz(matriz)
                })

        # Pasamos al siguiente pivote
        fila_pivote += 1


    return columnas_pivote, pasos


# ----------------------------------------------------------
# FORMA ESCALONADA REDUCIDA
# Método de Gauss-Jordan
# ----------------------------------------------------------

def forma_reducida(
        matriz,
        columnas_pivote,
        variables
):
    """Aplica Gauss-Jordan desde los pivotes para obtener forma reducida.

    Trabaja de abajo hacia arriba porque la eliminacion gaussiana ya dejo
    ceros debajo de los pivotes; falta limpiar lo que quedo encima.
    """

    pasos = []

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
        # Normalizar permite leer directamente la variable basica en la
        # columna pivote: la entrada principal queda como 1.

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
            # Registrar la normalizacion para la vista de proceso.
            operacion_str = (
                f"F{i + 1} -> "
                f"F{i + 1} / "
                f"{formatear_numero(pivote)}"
            )

            matriz_formateada = [[formatear_numero(val) for val in fila_mat] for fila_mat in matriz]

            pasos.append({
                "operacion": operacion_str,
                "matriz": matriz_formateada,
                "matriz_str": obtener_representacion_matriz(matriz)
            })
        # --------------------------------------------------
        # GENERAR CEROS ENCIMA DEL PIVOTE
        # --------------------------------------------------
        # Ahora se usa la fila pivote normalizada para cancelar las
        # entradas superiores en la misma columna.

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


                # Registrar la eliminacion hacia arriba para la vista.
                operacion_str = (
                    f"F{fila + 1} -> "
                    f"F{fila + 1} - "
                    f"({formatear_numero(factor)})"
                    f"F{i + 1}"
                )
                mostrar_matriz(matriz)

                matriz_formateada = [[formatear_numero(val) for val in fila_mat] for fila_mat in matriz]

                pasos.append({
                    "operacion": operacion_str,
                    "matriz": matriz_formateada,
                    "matriz_str": obtener_representacion_matriz(matriz)
                })

    return pasos
    # ----------------------------------------------------------
# FUNCIÓN INTEGRADORA PARA OBTENER TODOS LOS PASOS
# ----------------------------------------------------------

def resolver_sistema_completo(matriz, ecuaciones, variables):
    """Ejecuta Gauss y Gauss-Jordan y unifica todos los datos del proceso."""

    # Hacer una copia para no modificar la matriz original si fuera necesario
    matriz_trabajo = copiar_matriz(matriz)
    
    # 1. Eliminacion hacia abajo: forma escalonada.
    columnas_pivote, pasos_gauss = eliminacion_gaussiana(matriz_trabajo, ecuaciones, variables)
    
    # 2. Eliminacion hacia arriba: forma escalonada reducida.
    pasos_jordan = forma_reducida(matriz_trabajo, columnas_pivote, variables)
    
    return {
        "matriz_final": matriz_trabajo,
        "columnas_pivote": columnas_pivote,
        "pasos_gauss": pasos_gauss,
        "pasos_jordan": pasos_jordan,
        "todos_los_pasos": pasos_gauss + pasos_jordan
    }
             
