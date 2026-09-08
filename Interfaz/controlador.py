# Interfaz/controlador.py
import sys
import os

BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from formato import copiar_matriz, obtener_representacion_matriz, subindice, formatear_numero
from eliminacion import resolver_sistema_completo
from sistema import (
    clasificar_sistema,
    calcular_rango,
    identificar_variables,
    sustitucion_atras
)
from verificacion import verificar_solucion


class ControladorMatriz:
    """Clase encargada de conectar la interfaz en PySide6 con la lógica del backend."""

    @staticmethod
    def resolver_sistema(matriz_entrada):
        """
        Recibe la matriz (lista de listas de floats) desde la interfaz PySide6
        y retorna una estructura organizada con métricas, clasificación,
        pasos, matriz reducida y verificación.
        """
        if not matriz_entrada or not matriz_entrada[0]:
            raise ValueError("La matriz no puede estar vacía.")

        columnas = len(matriz_entrada[0])
        if columnas < 2 or any(len(fila) != columnas for fila in matriz_entrada):
            raise ValueError("La matriz debe ser rectangular y tener al menos una variable y un término independiente.")

        ecuaciones = len(matriz_entrada)
        variables = columnas - 1

        # Conservar copias de la matriz inicial
        matriz_original = copiar_matriz(matriz_entrada)
        matriz_trabajo = copiar_matriz(matriz_entrada)

        # 1. Obtener los pasos de eliminación y forma reducida
        res_eliminacion = resolver_sistema_completo(matriz_trabajo, ecuaciones, variables)
        columnas_pivote = res_eliminacion["columnas_pivote"]
        pasos_gauss = res_eliminacion["pasos_gauss"]
        pasos_jordan = res_eliminacion["pasos_jordan"]
        todos_los_pasos = res_eliminacion["todos_los_pasos"]
        matriz_final = res_eliminacion["matriz_final"]

        # 2. Clasificación del sistema y cálculo de rangos
        tipo_sistema = clasificar_sistema(matriz_final, ecuaciones, variables, columnas_pivote)
        rango_coeficientes = calcular_rango(matriz_final, variables)
        rango_ampliada = calcular_rango(matriz_final, variables + 1)

        # 3. Identificación de variables básicas y libres
        vars_basicas, vars_libres = identificar_variables(columnas_pivote, variables)

        # 4. Cálculo de soluciones y verificación si el sistema es consistente
        soluciones_valores = []
        soluciones_texto = []
        reporte_verificacion = []

        if tipo_sistema == "determinado":
            # Solución única por sustitución hacia atrás
            soluciones_valores = sustitucion_atras(matriz_final, columnas_pivote, variables)
            soluciones_texto = [
                f"x{subindice(i + 1)} = {formatear_numero(val)}"
                for i, val in enumerate(soluciones_valores)
            ]
            reporte_verificacion = verificar_solucion(
                matriz_original, soluciones_valores, ecuaciones, variables
            )

        elif tipo_sistema == "indeterminado":
            # Formatear el mensaje indicando las variables libres
            libres_formatted = [f"x{subindice(v + 1)}" for v in vars_libres]
            soluciones_texto = [
                f"El sistema tiene infinitas soluciones.",
                f"Variables libres: {', '.join(libres_formatted)}"
            ]

        else: # inconsistente
            soluciones_texto = ["El sistema es Inconsistente (No tiene solución)."]

        # 5. Estructura completa enviada a la vista
        return {
            "matriz_inicial": matriz_original,
            "matriz_inicial_str": obtener_representacion_matriz(matriz_original),
            "matriz_final": matriz_final,
            "pasos_gauss": pasos_gauss,
            "pasos_jordan": pasos_jordan,
            "todos_los_pasos": todos_los_pasos,
            "tipo_sistema": tipo_sistema,  # "determinado", "indeterminado", "inconsistente"
            "rango_coeficientes": rango_coeficientes,
            "rango_ampliada": rango_ampliada,
            "num_variables": variables,
            "num_ecuaciones": ecuaciones,
            "columnas_pivote": columnas_pivote,
            "variables_basicas": vars_basicas,
            "variables_libres": vars_libres,
            "soluciones_texto": soluciones_texto,
            "soluciones_valores": soluciones_valores,
            "verificacion": reporte_verificacion
        }