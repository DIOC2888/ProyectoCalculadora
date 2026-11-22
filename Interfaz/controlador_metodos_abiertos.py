"""Puente del módulo Newton-Raphson entre la vista y el backend."""

import os
import sys

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

from metodos_numericos import (
    analizar_orden_convergencia,
    comparar_derivadas_numericas,
    resolver_newton_horner,
    resolver_newton_raphson,
    resolver_secante,
)


class ControladorMetodosAbiertos:
    """Valida los datos recibidos y delega el cálculo de Newton-Raphson."""

    @staticmethod
    def resolver_newton_raphson(expresion, x0, tolerancia, max_iteraciones,
                                tolerancia_residuo=1e-8, umbral_derivada=1e-12):
        return resolver_newton_raphson(expresion, x0, tolerancia,
                                       max_iteraciones, tolerancia_residuo,
                                       umbral_derivada)

    @staticmethod
    def resolver_secante(expresion, x_anterior, x_actual, tolerancia,
                         max_iteraciones, tolerancia_residuo=1e-8):
        return resolver_secante(expresion, x_anterior, x_actual, tolerancia,
                                max_iteraciones, tolerancia_residuo)

    @staticmethod
    def comparar_derivadas(expresion, x, h):
        return comparar_derivadas_numericas(expresion, x, h)

    @staticmethod
    def resolver_polinomio_horner(coeficientes, x0, tolerancia,
                                  max_iteraciones, tolerancia_residuo=1e-8):
        return resolver_newton_horner(coeficientes, x0, tolerancia,
                                      max_iteraciones, tolerancia_residuo)

    @staticmethod
    def analizar_convergencia(aproximaciones):
        return analizar_orden_convergencia(aproximaciones)
