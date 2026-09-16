
# controlador_vectores.py
#
# Controlador principal de la Tarea 3.
#
# Su función es conectar la interfaz gráfica con los módulos
# matemáticos del backend.
#
# El controlador NO realiza los cálculos algebraicos directamente.
# Los cálculos son realizados por:
#
#   vectores.py
#   matrices.py
#   ecuaciones.py
#
# El controlador recibe los datos de la vista, llama al backend
# y devuelve resultados estructurados para que la interfaz pueda
# mostrarlos.


import vectores as backend_vectores
import matrices as backend_matrices

from ecuaciones import resolver_sistema

class ControladorVectores:
    """Clase encargada de conectar la interfaz en PySide6
    con la lógica del backend para operaciones vectoriales.
    """

    @staticmethod
    def sumar_vectores(vectores):
        """
        Suma dos o más vectores utilizando el backend.
        """

        try:

            from vectores import sumar_vectores as backend_sumar

            resultado_vector = backend_sumar(vectores)

            return {
                "exito": True,
                "operacion": "Sumar",
                "vectores": vectores,
                "resultado": resultado_vector,
                "mensaje": "La suma de vectores se realizó correctamente."
            }

        except (ValueError, TypeError) as e:

            return {
                "exito": False,
                "operacion": "Sumar",
                "vectores": vectores,
                "resultado": None,
                "mensaje": str(e)
            }


    @staticmethod
    def restar_vectores(vectores):
        """
        Resta dos o más vectores utilizando el backend.
        """

        try:

            from vectores import restar_vectores as backend_restar

            resultado_vector = backend_restar(vectores)

            return {
                "exito": True,
                "operacion": "Restar",
                "vectores": vectores,
                "resultado": resultado_vector,
                "mensaje": "La resta de vectores se realizó correctamente."
            }

        except (ValueError, TypeError) as e:

            return {
                "exito": False,
                "operacion": "Restar",
                "vectores": vectores,
                "resultado": None,
                "mensaje": str(e)
            }


    @staticmethod
    def multiplicar_vector_escalar(vector, escalar):
        """
        Multiplica un vector por un escalar utilizando el backend.
        """

        try:

            from vectores import (
                multiplicar_vector_escalar as backend_escalar
            )

            resultado_vector = backend_escalar(
                vector,
                escalar
            )

            return {
                "exito": True,
                "operacion": "Escalar",
                "vector": vector,
                "escalar": escalar,
                "resultado": resultado_vector,
                "mensaje": (
                    "La multiplicación por escalar "
                    "se realizó correctamente."
                )
            }

        except (ValueError, TypeError) as e:

            return {
                "exito": False,
                "operacion": "Escalar",
                "vector": vector,
                "escalar": escalar,
                "resultado": None,
                "mensaje": str(e)
            }


    @staticmethod
    def calcular_operacion_vectorial(
        vectores,
        operacion,
        escalar=None
    ):
        """
        Método general para las operaciones vectoriales.

        Permite mantener un único punto de entrada desde
        la interfaz.
        """

        if operacion == "Sumar":

            return ControladorVectores.sumar_vectores(
                vectores
            )

        elif operacion == "Restar":

            return ControladorVectores.restar_vectores(
                vectores
            )

        elif operacion == "Escalar":

            return ControladorVectores.multiplicar_vector_escalar(
                vectores[0],
                escalar
            )

        else:

            raise ValueError(
                "Operación vectorial no soportada."
            )

    # ========================================================
    #                 COMBINACIÓN LINEAL
    # ========================================================

    @staticmethod
    def evaluar_combinacion_lineal(
        vectores,
        b
    ):
        """
        Determina si b es combinación lineal de un conjunto
        de vectores generadores.

        Matemáticamente busca:

            b = c1*v1 + c2*v2 + ... + ck*vk

        El backend de vectores construye:

            A = [v1 v2 ... vk]

        y resuelve:

            A*c = b

        El controlador únicamente organiza la información
        para entregarla a la interfaz.
        """

        try:

            resultado = (
                backend_vectores
                .combinacion_lineal(
                    vectores,
                    b
                )
            )

            es_combinacion = resultado.get(
                "es_combinacion",
                False
            )

            tipo = resultado.get(
                "tipo"
            )

            # ------------------------------------------------
            # MENSAJE
            # ------------------------------------------------

            if tipo == "unica":

                mensaje = (
                    "El vector b es combinación lineal "
                    "de los vectores dados y existe una "
                    "única representación."
                )

            elif tipo == "infinitas":

                mensaje = (
                    "El vector b es combinación lineal "
                    "de los vectores dados y existen "
                    "infinitas representaciones."
                )

            elif tipo == "ninguna":

                mensaje = (
                    "El vector b NO es combinación lineal "
                    "de los vectores dados."
                )

            else:

                mensaje = (
                    "No se pudo determinar el tipo de solución."
                )

            # ------------------------------------------------
            # DEVOLVER INFORMACIÓN PARA LA VISTA
            # ------------------------------------------------

            return {

                "exito": True,

                "operacion": "Combinacion lineal",


                # Resultado principal
                "es_combinacion":
                    es_combinacion,

                "tipo":
                    tipo,

                "mensaje":
                    mensaje,

                # Coeficientes si existe solución única
                "coeficientes":
                    resultado.get(
                        "coeficientes"
                    ),

                # Información para infinitas soluciones
                "solucion_parametrica":
                    resultado.get(
                        "solucion_parametrica"
                    ),

                # Información del sistema
                "rango_A":
                    resultado.get(
                        "rango_A"
                    ),

                "rango_Ab":
                    resultado.get(
                        "rango_Ab"
                    ),

                "num_variables":
                    resultado.get(
                        "num_variables"
                    ),

                "num_ecuaciones":
                    resultado.get(
                        "num_ecuaciones"
                    ),

                "columnas_pivote":
                    resultado.get(
                        "columnas_pivote"
                    ),

                "variables_basicas":
                    resultado.get(
                        "variables_basicas"
                    ),

                "variables_libres":
                    resultado.get(
                        "variables_libres"
                    ),

                # Matrices
                "matriz_generadores":
                    resultado.get(
                        "matriz_generadores"
                    ),

                "matriz_aumentada":
                    resultado.get(
                        "matriz_aumentada"
                    ),

                "matriz_reducida":
                    resultado.get(
                        "matriz_reducida"
                    ),

                # Proceso Gauss-Jordan
                "proceso":
                    resultado.get(
                        "proceso",
                        []
                    )
            }

        except (ValueError, TypeError) as e:

            return {

                "exito": False,

                "operacion": "Combinacion lineal",


                "es_combinacion":
                    False,

                "tipo":
                    None,

                "coeficientes":
                    None,

                "solucion_parametrica":
                    None,

                "rango_A":
                    None,

                "rango_Ab":
                    None,

                "num_variables":
                    None,

                "num_ecuaciones":
                    None,

                "columnas_pivote":
                    [],

                "variables_basicas":
                    [],

                "variables_libres":
                    [],

                "matriz_generadores":
                    None,

                "matriz_aumentada":
                    None,

                "matriz_reducida":
                    None,

                "proceso":
                    [],

                "mensaje":
                    str(e)
            }

    # ========================================================
    #              OPERACIONES MATRICIALES
    # ========================================================

    @staticmethod
    def sumar_matrices(A, B):
        """
        Ejecuta la suma de dos matrices.
        """

        try:

            resultado = (
                backend_matrices
                .sumar_matrices(
                    A,
                    B
                )
            )

            return {
                "exito": True,
                "resultado": resultado,
                "mensaje":
                    "Suma de matrices realizada correctamente."
            }

        except (ValueError, TypeError) as e:

            return {
                "exito": False,
                "resultado": None,
                "mensaje": str(e)
            }

    @staticmethod
    def restar_matrices(A, B):
        """
        Ejecuta la resta de dos matrices.
        """

        try:

            resultado = (
                backend_matrices
                .restar_matrices(
                    A,
                    B
                )
            )

            return {
                "exito": True,
                "resultado": resultado,
                "mensaje":
                    "Resta de matrices realizada correctamente."
            }

        except (ValueError, TypeError) as e:

            return {
                "exito": False,
                "resultado": None,
                "mensaje": str(e)
            }

    @staticmethod
    def multiplicar_matriz_escalar(
        A,
        escalar
    ):
        """
        Multiplica una matriz por un escalar.
        """

        try:

            escalar = float(escalar)

            resultado = (
                backend_matrices
                .multiplicar_matriz_escalar(
                    A,
                    escalar
                )
            )

            return {
                "exito": True,
                "resultado": resultado,
                "mensaje": (
                    "Multiplicación de matriz por escalar "
                    "realizada correctamente."
                )
            }

        except ValueError:

            return {
                "exito": False,
                "resultado": None,
                "mensaje":
                    "El escalar debe ser un número válido."
            }

        except TypeError as e:

            return {
                "exito": False,
                "resultado": None,
                "mensaje": str(e)
            }

    @staticmethod
    def multiplicar_matrices(A, B):
        """
        Ejecuta la multiplicación:

            A(m x n) · B(n x p)

        verificando que:

            columnas de A = filas de B
        """

        try:

            resultado = (
                backend_matrices
                .multiplicar_matrices(
                    A,
                    B
                )
            )

            return {
                "exito": True,
                "resultado": resultado,
                "mensaje": (
                    "Multiplicación de matrices "
                    "realizada correctamente."
                )
            }

        except (ValueError, TypeError) as e:

            return {
                "exito": False,
                "resultado": None,
                "mensaje": str(e)
            }

    # ========================================================
    #                  ECUACIONES Ax = b
    # ========================================================

    @staticmethod
    def resolver_ecuacion_matricial(
        A,
        b
    ):
        """
        Resuelve la ecuación matricial:

            Ax = b

        mediante el backend de ecuaciones.py.

        Devuelve toda la información que puede necesitar
        la interfaz:

        - matriz aumentada
        - matriz reducida
        - proceso
        - tipo de solución
        - solución
        - solución paramétrica
        - rangos
        - variables básicas
        - variables libres
        """

        try:

            resultado = resolver_sistema(
                A,
                b
            )

            tipo = resultado.get(
                "tipo"
            )

            return {

                "exito": True,

                # --------------------------------------------
                # INFORMACIÓN PRINCIPAL
                # --------------------------------------------

                "tipo":
                    tipo,

                "mensaje":
                    ControladorVectores
                    ._generar_mensaje_ecuacion(
                        tipo
                    ),

                # --------------------------------------------
                # SOLUCIONES
                # --------------------------------------------

                "solucion":
                    resultado.get(
                        "solucion"
                    ),

                "solucion_parametrica":
                    resultado.get(
                        "solucion_parametrica"
                    ),

                # --------------------------------------------
                # MATRICES
                # --------------------------------------------

                "matriz_aumentada":
                    resultado.get(
                        "matriz_aumentada"
                    ),

                "matriz_reducida":
                    resultado.get(
                        "matriz_reducida"
                    ),

                # --------------------------------------------
                # PROCESO
                # --------------------------------------------

                "proceso":
                    resultado.get(
                        "proceso",
                        []
                    ),

                # --------------------------------------------
                # INFORMACIÓN DEL SISTEMA
                # --------------------------------------------

                "rango_A":
                    resultado.get(
                        "rango_A"
                    ),

                "rango_Ab":
                    resultado.get(
                        "rango_Ab"
                    ),

                "num_variables":
                    resultado.get(
                        "num_variables"
                    ),

                "num_ecuaciones":
                    resultado.get(
                        "num_ecuaciones"
                    ),

                "columnas_pivote":
                    resultado.get(
                        "columnas_pivote"
                    ),

                "variables_basicas":
                    resultado.get(
                        "variables_basicas"
                    ),

                "variables_libres":
                    resultado.get(
                        "variables_libres"
                    )
            }

        except (ValueError, TypeError) as e:

            return {

                "exito": False,

                "tipo":
                    None,

                "solucion":
                    None,

                "solucion_parametrica":
                    None,

                "matriz_aumentada":
                    None,

                "matriz_reducida":
                    None,

                "proceso":
                    [],

                "rango_A":
                    None,

                "rango_Ab":
                    None,

                "num_variables":
                    None,

                "num_ecuaciones":
                    None,

                "columnas_pivote":
                    [],

                "variables_basicas":
                    [],

                "variables_libres":
                    [],

                "mensaje":
                    str(e)
            }

    # ========================================================
    #              MENSAJES DE ECUACIONES
    # ========================================================

    @staticmethod
    def _generar_mensaje_ecuacion(
        tipo
    ):
        """
        Genera el mensaje correspondiente al tipo
        de solución de Ax = b.
        """

        if tipo == "unica":

            return (
                "El sistema tiene una solución única."
            )

        if tipo == "infinitas":

            return (
                "El sistema tiene infinitas soluciones."
            )

        if tipo == "ninguna":

            return (
                "El sistema no tiene solución."
            )

        return (
            "Estado de solución no determinado."
        )

