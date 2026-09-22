
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

from ecuaciones import resolver_sistema,resolver_sistema_homogeneo

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
    def evaluar_independencia_lineal(
        vectores
    ):
        """
        Determina si un conjunto de vectores es linealmente
        independiente usando el backend de vectores.py.
        """

        try:

            resultado = (
                backend_vectores
                .verificar_independencia_lineal(
                    vectores
                )
            )

            return {
                "exito": True,
                "operacion": "Independencia lineal",
                "es_independiente": resultado.get(
                    "es_independiente",
                    False
                ),
                "tipo": resultado.get("tipo"),
                "mensaje": resultado.get(
                    "mensaje",
                    "Resultado calculado."
                ),
                "vectores": resultado.get("vectores", []),
                "matriz_generadores": resultado.get("matriz"),
                "matriz_aumentada": resultado.get("matriz_aumentada"),
                "matriz_reducida": resultado.get("matriz_reducida"),
                "proceso": resultado.get("proceso", []),
                "rango_A": resultado.get("rango"),
                "rango_Ab": resultado.get("rango"),
                "num_variables": resultado.get("cantidad_vectores"),
                "num_ecuaciones": resultado.get("dimension"),
                "columnas_pivote": resultado.get(
                    "columnas_pivote",
                    []
                ),
                "variables_basicas": resultado.get(
                    "variables_basicas",
                    []
                ),
                "variables_libres": resultado.get(
                    "variables_libres",
                    []
                ),
                "solucion_parametrica": resultado.get(
                    "solucion_parametrica"
                ),
                "conjunto_solucion": resultado.get(
                    "conjunto_solucion"
                ),
                "relacion_dependencia": resultado.get(
                    "relacion_dependencia"
                ),
                "p_mayor_que_n": resultado.get(
                    "p_mayor_que_n",
                    False
                )
            }

        except (ValueError, TypeError) as e:

            return {
                "exito": False,
                "operacion": "Independencia lineal",
                "es_independiente": False,
                "tipo": None,
                "mensaje": str(e),
                "vectores": vectores,
                "matriz_generadores": None,
                "matriz_aumentada": None,
                "matriz_reducida": None,
                "proceso": [],
                "rango_A": None,
                "rango_Ab": None,
                "num_variables": None,
                "num_ecuaciones": None,
                "columnas_pivote": [],
                "variables_basicas": [],
                "variables_libres": [],
                "solucion_parametrica": None,
                "conjunto_solucion": None,
                "relacion_dependencia": None,
                "p_mayor_que_n": False
            }

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
                "conjunto_solucion":
                resultado.get(
                    "conjunto_solucion"
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
                "conjunto_solucion":
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
    def sumar_matrices(matrices):
        """
        Suma dos o más matrices utilizando el backend.

        Recibe una lista de matrices y devuelve tanto
        el resultado como el proceso de la operación.
        """

        try:

            datos = backend_matrices.sumar_matrices(
                matrices
            )

            return {
                "exito": True,
                "operacion": "Sumar matrices",
                "matrices": matrices,
                "resultado": datos["resultado"],
                "proceso": datos["proceso"],
                "mensaje": (
                    "Suma de matrices realizada correctamente."
                )
            }

        except (ValueError, TypeError) as e:

            return {
                "exito": False,
                "operacion": "Sumar matrices",
                "matrices": matrices,
                "resultado": None,
                "proceso": [],
                "mensaje": str(e)
            }


    @staticmethod
    def restar_matrices(matrices):
        """
        Resta dos o más matrices utilizando el backend.

        Realiza:

            M1 - M2 - M3 - ...

        Devuelve el resultado y el proceso.
        """

        try:

            datos = backend_matrices.restar_matrices(
                matrices
            )

            return {
                "exito": True,
                "operacion": "Restar matrices",
                "matrices": matrices,
                "resultado": datos["resultado"],
                "proceso": datos["proceso"],
                "mensaje": (
                    "Resta de matrices realizada correctamente."
                )
            }

        except (ValueError, TypeError) as e:

            return {
                "exito": False,
                "operacion": "Restar matrices",
                "matrices": matrices,
                "resultado": None,
                "proceso": [],
                "mensaje": str(e)
            }


    @staticmethod
    def multiplicar_matriz_escalar(
        matriz,
        escalar
    ):
        """
        Multiplica una matriz por un escalar utilizando
        el backend.

        Devuelve el resultado y el proceso.
        """

        try:

            escalar = float(escalar)

            datos = backend_matrices.multiplicar_matriz_escalar(
                matriz,
                escalar
            )

            return {
                "exito": True,
                "operacion": "Multiplicar matriz por escalar",
                "matriz": matriz,
                "escalar": escalar,
                "resultado": datos["resultado"],
                "proceso": datos["proceso"],
                "mensaje": (
                    "Multiplicación de matriz por escalar "
                    "realizada correctamente."
                )
            }

        except ValueError:

            return {
                "exito": False,
                "operacion": "Multiplicar matriz por escalar",
                "matriz": matriz,
                "escalar": escalar,
                "resultado": None,
                "proceso": [],
                "mensaje": (
                    "El escalar debe ser un número válido."
                )
            }

        except TypeError as e:

            return {
                "exito": False,
                "operacion": "Multiplicar matriz por escalar",
                "matriz": matriz,
                "escalar": escalar,
                "resultado": None,
                "proceso": [],
                "mensaje": str(e)
            }


    @staticmethod
    def multiplicar_matrices(matrices):
        """
        Multiplica dos o más matrices utilizando el backend.

        Realiza:

            M1 × M2 × M3 × ...

        Las dimensiones deben ser compatibles en cada
        multiplicación consecutiva.
        """

        try:

            datos = backend_matrices.multiplicar_matrices(
                matrices
            )

            return {
                "exito": True,
                "operacion": "Multiplicar matrices",
                "matrices": matrices,
                "resultado": datos["resultado"],
                "proceso": datos["proceso"],
                "mensaje": (
                    "Multiplicación de matrices "
                    "realizada correctamente."
                )
            }

        except (ValueError, TypeError) as e:

            return {
                "exito": False,
                "operacion": "Multiplicar matrices",
                "matrices": matrices,
                "resultado": None,
                "proceso": [],
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

                "operacion":
                    "ecuacion_matricial",

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

                "conjunto_solucion":
                    resultado.get(
                        "conjunto_solucion"
                    ),

                # --------------------------------------------
                # FORMA VECTORIAL
                # --------------------------------------------

                "solucion_particular":
                    (
                        resultado.get("conjunto_solucion", {})
                        .get("solucion_particular")
                        if resultado.get("conjunto_solucion")
                        else None
                    ),

                "vectores_direccion":
                    (
                        resultado.get("conjunto_solucion", {})
                        .get("vectores_direccion", [])
                        if resultado.get("conjunto_solucion")
                        else []
                    ),

                "parametros":
                    (
                        resultado.get("conjunto_solucion", {})
                        .get("parametros", [])
                        if resultado.get("conjunto_solucion")
                        else []
                    ),

                "forma_vectorial":
                    (
                        resultado.get("conjunto_solucion", {})
                        .get("forma_vectorial")
                        if resultado.get("conjunto_solucion")
                        else None
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

                "operacion":
                    "ecuacion_matricial",

                "tipo":
                    None,

                "solucion":
                    None,

                "solucion_parametrica":
                    None,
                "conjunto_solucion":
                   None,
                "solucion_particular":
                    None,

                "vectores_direccion":
                    [],

                "parametros":
                    [],

                "forma_vectorial":
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
    # ========================================================
#       PROPIEDAD DISTRIBUTIVA A(u + v) = Au + Av
# ========================================================

    @staticmethod
    def verificar_distributividad_matriz_vector(
        A,
        u,
        v
    ):
        """
        Verifica la propiedad:

            A(u + v) = Au + Av

        utilizando el backend de matrices.py.
        """

        try:

            resultado = (
                backend_matrices
                .verificar_distributividad_matriz_vector(
                    A,
                    u,
                    v
                )
            )

            if resultado["igualdad"]:

                mensaje = (
                    "Se cumple la propiedad distributiva: "
                    "A(u + v) = Au + Av."
                )

            else:

                mensaje = (
                    "La igualdad A(u + v) = Au + Av "
                    "no se cumple para los datos ingresados."
                )

            return {

                "exito": True,

                "operacion":
                    "Propiedad distributiva",

                "igualdad":
                    resultado["igualdad"],

                "mensaje":
                    mensaje,

                "matriz":
                    resultado["matriz"],

                "u":
                    resultado["u"],

                "v":
                    resultado["v"],

                "u_mas_v":
                    resultado["u_mas_v"],

                "Au":
                    resultado["Au"],

                "Av":
                    resultado["Av"],

                "lado_izquierdo":
                    resultado["lado_izquierdo"],

                "lado_derecho":
                    resultado["lado_derecho"],

                "proceso":
                    resultado["proceso"]
            }

        except (ValueError, TypeError) as e:

            return {

                "exito": False,

                "operacion":
                    "Propiedad distributiva",

                "igualdad":
                    False,

                "mensaje":
                    str(e),

                "proceso":
                    []
            }
    @staticmethod
    def multiplicar_matriz_vector(
        A,
        vector
    ):
        """
        Calcula el producto A por vector usando matrices.py.
        """

        try:

            resultado = (
                backend_matrices
                .multiplicar_matriz_vector(
                    A,
                    vector
                )
            )

            return {
                "exito": True,
                "operacion": "Matriz por vector",
                "matriz": A,
                "vector": vector,
                "resultado": resultado["resultado"],
                "proceso": resultado["proceso"],
                "mensaje": (
                    "El producto de la matriz por el vector "
                    "se realizo correctamente."
                )
            }

        except (ValueError, TypeError) as e:

            return {
                "exito": False,
                "operacion": "Matriz por vector",
                "matriz": A,
                "vector": vector,
                "resultado": None,
                "proceso": [],
                "mensaje": str(e)
            }

    @staticmethod
    def verificar_homogeneidad_matriz_vector(
        A,
        u,
        escalar
    ):
        """
        Verifica la propiedad A(cu) = c(Au).
        """

        try:

            resultado = (
                backend_matrices
                .verificar_homogeneidad_matriz_vector(
                    A,
                    u,
                    escalar
                )
            )

            expresion = (
                resultado["proceso"][-1].get(
                    "operacion",
                    "A(cu) = c(Au)"
                )
                if resultado.get("proceso")
                else "A(cu) = c(Au)"
            )

            if resultado["igualdad"]:
                mensaje = f"Se cumple la propiedad: {expresion}."
            else:
                mensaje = (
                    f"La igualdad {expresion} no se cumple "
                    "para los datos ingresados."
                )

            return {
                "exito": True,
                "operacion": "Propiedad homogenea",
                "igualdad": resultado["igualdad"],
                "mensaje": mensaje,
                "matriz": resultado["matriz"],
                "u": resultado["u"],
                "escalar": resultado["escalar"],
                "cu": resultado["cu"],
                "Au": resultado["Au"],
                "lado_izquierdo": resultado["lado_izquierdo"],
                "lado_derecho": resultado["lado_derecho"],
                "proceso": resultado["proceso"]
            }

        except (ValueError, TypeError) as e:

            return {
                "exito": False,
                "operacion": "Propiedad homogenea",
                "igualdad": False,
                "mensaje": str(e),
                "proceso": []
            }
    @staticmethod
    def evaluar_independencia_columnas(self, A):
        """
         Evalúa la independencia lineal de las columnas de una matriz.
        """

        resultado = backend_matrices.verificar_independencia_columnas(A)

        return {
            "es_independiente": resultado["es_independiente"],
            "tipo": resultado["tipo"],
            "mensaje": resultado["mensaje"],

            # Matriz y dimensiones
            "matriz": resultado["matriz"],
            "cantidad_filas": resultado["cantidad_filas"],
            "cantidad_columnas": resultado["cantidad_columnas"],
            "columnas_mayor_que_filas": resultado["columnas_mayor_que_filas"],

            # Sistema homogéneo
            "vector_cero": resultado["vector_cero"],
            "matriz_aumentada": resultado["matriz_aumentada"],
            "matriz_reducida": resultado["matriz_reducida"],

            # Información del proceso
            "proceso": resultado["proceso"],

             # Información del sistema
            "rango": resultado["rango"],
            "columnas_pivote": resultado["columnas_pivote"],
            "variables_basicas": resultado["variables_basicas"],
            "variables_libres": resultado["variables_libres"],

            # Solución
            "solucion_parametrica": resultado["solucion_parametrica"],
            "conjunto_solucion": resultado["conjunto_solucion"],

            # Dependencia
            "relaciones_dependencia": resultado["relaciones_dependencia"]
    }
        # ========================================================
    #              SISTEMA HOMOGÉNEO Ax = 0
    # ========================================================

    @staticmethod
    def resolver_sistema_homogeneo(A):
        """
        Resuelve un sistema homogéneo:

            Ax = 0

        utilizando el backend de ecuaciones.py.

        Devuelve la información necesaria para mostrar:

        - matriz aumentada
        - matriz reducida
        - proceso de Gauss-Jordan
        - rango
        - columnas pivote
        - variables básicas
        - variables libres
        - solución paramétrica
        - conjunto solución
        - soluciones no triviales
        """

        try:

            resultado = resolver_sistema_homogeneo(A)

            tiene_soluciones_no_triviales = (
                resultado.get(
                    "tiene_soluciones_no_triviales",
                    False
                )
            )

            return {

                "exito": True,

                "operacion":
                    "Sistema homogéneo",

                # --------------------------------------------
                # INFORMACIÓN PRINCIPAL
                # --------------------------------------------

                "es_homogeneo":
                    True,

                "tiene_soluciones_no_triviales":
                    tiene_soluciones_no_triviales,

                "mensaje":
                    resultado.get(
                        "mensaje_homogeneo",
                        "Sistema homogéneo resuelto correctamente."
                    ),

                # --------------------------------------------
                # MATRIZ
                # --------------------------------------------

                "matriz":
                    A,

                "matriz_aumentada":
                    resultado.get(
                        "matriz_aumentada"
                    ),

                "matriz_reducida":
                    resultado.get(
                        "matriz_reducida"
                    ),

                # --------------------------------------------
                # PROCESO GAUSS-JORDAN
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
                        "columnas_pivote",
                        []
                    ),

                "variables_basicas":
                    resultado.get(
                        "variables_basicas",
                        []
                    ),

                "variables_libres":
                    resultado.get(
                        "variables_libres",
                        []
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

                "conjunto_solucion":
                    resultado.get(
                        "conjunto_solucion"
                    )
            }

        except (ValueError, TypeError) as e:

            return {

                "exito": False,

                "operacion":
                    "Sistema homogéneo",

                "es_homogeneo":
                    True,

                "tiene_soluciones_no_triviales":
                    False,

                "matriz":
                    A,

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

                "solucion":
                    None,

                "solucion_parametrica":
                    None,

                "conjunto_solucion":
                    None,

                "mensaje":
                    str(e)
            }