"""Puente entre la vista y los algoritmos de metodos numericos."""

import os
import sys

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

from metodos_numericos import (
    TIPOS_ERROR,
    bisecar,
    comparar_inestabilidad,
    comparar_truncamiento_redondeo,
    estado_punto_flotante,
    graficar_funcion,
    informe_errores,
    notacion_posicional,
    propagar_error_numerico,
)


class ControladorMetodosNumericos:
    """Valida y conecta los datos de la interfaz con cada modulo numerico."""

    @staticmethod
    def resolver_biseccion(funcion, a, b, tolerancia, max_iteraciones):
        """Ejecuta biseccion propia y agrega una comparacion SciPy si esta instalado."""
        resultado = bisecar(funcion, a, b, tolerancia, max_iteraciones)
        try:
            from scipy.optimize import bisect as scipy_bisect
            if resultado["tabla"] or resultado["iteraciones"] == 0:
                referencia = scipy_bisect(resultado["funcion"], *resultado["intervalo_inicial"])
                resultado["scipy"] = referencia
                resultado["diferencia_scipy"] = abs(resultado["raiz"] - referencia)
            else:
                resultado["scipy"] = resultado["diferencia_scipy"] = None
        except ImportError:
            resultado["scipy"] = resultado["diferencia_scipy"] = None
            resultado["aviso_scipy"] = "SciPy no está instalado; se muestra el resultado del algoritmo propio."
        except (ValueError, RuntimeError, OverflowError) as exc:
            resultado["scipy"] = resultado["diferencia_scipy"] = None
            resultado["aviso_scipy"] = f"No se pudo realizar la comparación con SciPy: {exc}"
        return resultado

    @staticmethod
    def convertir_notacion(valor, base):
        """Entrega la descomposicion posicional para un entero en base 2 o 10."""
        return notacion_posicional(valor, base)

    @staticmethod
    def calcular_errores(valor_verdadero, valor_aproximado):
        """Calcula errores absoluto, relativo y porcentual."""
        return informe_errores(valor_verdadero, valor_aproximado)

    @staticmethod
    def propagar_error(funcion, x, delta_x):
        """Calcula la propagacion para una funcion ingresada por el usuario."""
        return propagar_error_numerico(funcion, x, delta_x)

    @staticmethod
    def comparar_truncamiento_redondeo(x, max_terminos):
        """Devuelve la simulacion iterativa de exp(x) con errores separados."""
        return comparar_truncamiento_redondeo(x, max_terminos)

    @staticmethod
    def comparar_inestabilidad(x):
        """Compara una formula directa susceptible a cancelacion con otra estable."""
        return comparar_inestabilidad(x)

    @staticmethod
    def graficar(funcion, x_min, x_max, ax, raiz=None, intervalo=None, titulo_intervalo=""):
        """Delega el dibujo de la funcion con posible intervalo y raiz de biseccion."""
        return graficar_funcion(funcion, x_min, x_max, ax, raiz, intervalo, titulo_intervalo)

    @staticmethod
    def resumen_punto_flotante():
        """Entrega ejemplos de punto flotante y las definiciones de tipos de error."""
        return {"punto_flotante": estado_punto_flotante(), "tipos_error": TIPOS_ERROR}
