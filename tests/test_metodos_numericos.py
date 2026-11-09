"""Pruebas de requisitos, validaciones e interfaz de metodos numericos."""

import os
import sys
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
PROJECT_DIR = Path(__file__).resolve().parents[1]
INTERFACE_DIR = PROJECT_DIR / "Interfaz"
sys.path.insert(0, str(PROJECT_DIR))
sys.path.insert(0, str(INTERFACE_DIR))

import numpy as np
from matplotlib.figure import Figure
from PySide6.QtWidgets import QApplication, QLabel, QTableWidget

from metodos_numericos import (
    EvaluadorFuncion,
    bisecar,
    comparar_inestabilidad,
    comparar_truncamiento_redondeo,
    estado_punto_flotante,
    graficar_funcion,
    informe_errores,
    notacion_posicional,
    propagar_error_numerico,
)
from controlador_metodos_numericos import ControladorMetodosNumericos
from vistas.vista_metodos_numericos import VistaMetodosNumericos


class BiseccionTests(unittest.TestCase):
    def test_casos_sugeridos_y_cota_teorica(self):
        casos = (
            ("x**3 - 2*x - 5", 2, 3, 2.09455148),
            ("cos(x) - x", 0, 1, 0.73908513),
            ("x**2 - 2", 1, 2, 1.41421356),
            ("x**3 + x - 1", 0, 1, 0.68232780),
        )
        for funcion, a, b, referencia in casos:
            with self.subTest(funcion=funcion):
                resultado = bisecar(funcion, a, b, 1e-4, 100)
                self.assertAlmostEqual(resultado["raiz"], referencia, places=4)
                self.assertEqual(resultado["teoricas"], 14)
                self.assertLessEqual(resultado["cota"], 1e-4)
                self.assertIn("alcanzada", resultado["estado"])

    def test_intervalo_sin_cambio_de_signo_se_rechaza(self):
        with self.assertRaisesRegex(ValueError, "cambio de signo"):
            bisecar("x**2 + 1", -1, 1, 1e-4, 100)

    def test_raiz_exacta_en_extremo(self):
        resultado = bisecar("x**2 - 1", 1, 2, 1e-4, 100)
        self.assertEqual(resultado["raiz"], 1)
        self.assertEqual(resultado["iteraciones"], 0)
        self.assertIn("extremo", resultado["estado"])

    def test_discontinuidad_1_sobre_x_se_rechaza(self):
        with self.assertRaisesRegex(ValueError, "discontinuidad"):
            bisecar("1/x", -1, 1, 1e-4, 100)

    def test_maximo_insuficiente_informa_que_no_garantiza_tolerancia(self):
        resultado = bisecar("x**3 - 2*x - 5", 2, 3, 1e-4, 2)
        self.assertEqual(resultado["iteraciones"], 2)
        self.assertGreater(resultado["cota"], 1e-4)
        self.assertIn("sin garantizar", resultado["estado"])

    def test_valida_extremos_tolerancia_iteraciones_y_dominio(self):
        casos = (
            ("x", 2, 1, 1e-4, 10),
            ("x", 0, 1, 0, 10),
            ("x", 0, 1, 1e-4, 0),
            ("log(x)", -1, 1, 1e-4, 10),
            ("x", 0, 1, 1e-4, 1.5),
        )
        for args in casos:
            with self.subTest(args=args), self.assertRaises(ValueError):
                bisecar(*args)

    def test_tabla_guarda_extremos_antes_de_actualizar_y_no_divide_por_cero(self):
        resultado = bisecar("x", -3, 1, 0.1, 3)
        self.assertEqual(resultado["tabla"][0]["error_relativo"], "—")
        self.assertEqual(resultado["tabla"][1]["a"], -1)
        self.assertEqual(resultado["tabla"][1]["b"], 1)
        self.assertEqual(resultado["tabla"][1]["xr"], 0)
        self.assertEqual(resultado["tabla"][1]["error_relativo"], "No definido")

    def test_sintaxis_de_potencia_y_evaluacion_segura(self):
        self.assertEqual(EvaluadorFuncion("x**2")(3), 9)
        for expresion in ("x^2", "__import__('os')", "x.__class__", "open('x')"):
            with self.subTest(expresion=expresion), self.assertRaises(ValueError):
                EvaluadorFuncion(expresion)

    def test_controlador_compara_con_scipy_si_esta_disponible(self):
        resultado = ControladorMetodosNumericos.resolver_biseccion("x**2 - 2", 1, 2, 1e-4, 100)
        self.assertIn("raiz", resultado)
        if resultado.get("scipy") is not None:
            self.assertAlmostEqual(resultado["diferencia_scipy"], abs(resultado["raiz"] - resultado["scipy"]))


class GraficadorTests(unittest.TestCase):
    def test_funciones_y_restricciones_de_dominio(self):
        casos = (("x", -1, 1), ("x**2", -1, 1), ("1/x", -1, 1),
                 ("sqrt(x)", -1, 1), ("exp(x)", -1, 1),
                 ("log(x)", -1, 2), ("sin(x)", -1, 1), ("abs(x)", -1, 1))
        for funcion, minimo, maximo in casos:
            with self.subTest(funcion=funcion):
                ax = Figure().add_subplot(111)
                graficar_funcion(funcion, minimo, maximo, ax)
                y = np.asarray(ax.lines[0].get_ydata(), dtype=float)
                self.assertGreater(np.isfinite(y).sum(), 0)
                self.assertTrue(ax.get_title())
                self.assertTrue(ax.get_xlabel())
                self.assertTrue(ax.get_ylabel())
                self.assertTrue(ax.get_legend())

    def test_asintota_no_se_conecta_a_traves_de_la_discontinuidad(self):
        ax = Figure().add_subplot(111)
        graficar_funcion("1/(x - 0.1234)", -1, 1, ax)
        xs = np.asarray(ax.lines[0].get_xdata())
        ys = np.asarray(ax.lines[0].get_ydata())
        idx = int(np.argmin(np.abs(xs - 0.1234)))
        self.assertTrue(np.isnan(ys[max(0, idx - 1):idx + 2]).any())

    def test_limites_invalidos_se_rechazan(self):
        with self.assertRaises(ValueError):
            graficar_funcion("x", 1, 1, Figure().add_subplot(111))


class NotacionPosicionalTests(unittest.TestCase):
    def test_ejemplo_decimal_y_equivalencia_binaria(self):
        resultado = notacion_posicional("84506", 10)
        self.assertIn("8 · 10⁴", resultado["expansion"])
        self.assertNotIn("(", resultado["expansion"])
        self.assertNotIn("₁₀", resultado["expansion"])
        self.assertNotIn("^", resultado["expansion"])
        self.assertEqual(int(resultado["binario"], 2), 84506)

    def test_ejemplo_binario_y_equivalencia_decimal(self):
        resultado = notacion_posicional("11110011", 2)
        self.assertEqual(resultado["decimal"], "243")
        self.assertIn("1 · 2⁷", resultado["expansion"])
        self.assertNotIn("(", resultado["expansion"])
        self.assertNotIn("₂", resultado["expansion"])

    def test_negativos_cero_y_base_invalida(self):
        negativo = notacion_posicional("-111", 2)
        self.assertEqual(negativo["decimal"], "−7")
        self.assertEqual(notacion_posicional("0", 10)["decimal"], "0")
        with self.assertRaises(ValueError):
            notacion_posicional("102", 2)


class ErroresNumericosTests(unittest.TestCase):
    def test_calculo_directo_y_valor_verdadero_cero(self):
        resultado = informe_errores(1, 0.99)
        self.assertAlmostEqual(resultado["absoluto"], 0.01)
        self.assertAlmostEqual(resultado["relativo"], 0.01)
        self.assertAlmostEqual(resultado["porcentual"], 1)
        self.assertIsNone(informe_errores(0, 0.1)["relativo"])

    def test_propaga_funcion_ingresada_con_derivada_numerica(self):
        resultado = propagar_error_numerico("sin(x) + x**2", 0.5, 0.01)
        self.assertAlmostEqual(resultado["derivada"], np.cos(0.5) + 1, places=7)
        self.assertAlmostEqual(resultado["cambio_real"], resultado["fx_delta"] - resultado["fx"])
        with self.assertRaises(ValueError):
            propagar_error_numerico("log(x)", 0, 0.1)

    def test_simulacion_de_truncamiento_y_redondeo(self):
        resultado = comparar_truncamiento_redondeo(1, 30)
        self.assertEqual(len(resultado["tabla"]), 30)
        self.assertAlmostEqual(resultado["referencia"], np.e)
        self.assertGreater(resultado["tabla"][0]["error_truncamiento"], 0)
        with self.assertRaises(ValueError):
            comparar_truncamiento_redondeo(1, 1)

    def test_inestabilidad_compara_formas_equivalentes(self):
        resultado = comparar_inestabilidad(1e16)
        self.assertEqual(resultado["directo"], 0)
        self.assertGreater(resultado["reformulado"], 0)
        self.assertLess(resultado["error_reformulado"], resultado["error_directo"])
        with self.assertRaises(ValueError):
            comparar_inestabilidad(-1)

    def test_epsilon_overflow_underflow_y_definiciones(self):
        resultado = estado_punto_flotante()
        self.assertFalse(resultado["igualdad"])
        self.assertEqual(resultado["epsilon"], np.finfo(float).eps)
        self.assertFalse(np.isfinite(resultado["overflow"]))
        self.assertEqual(resultado["underflow"], 0)


class VistaErroresTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.view = VistaMetodosNumericos()

    def test_opciones_de_errores_separadas_y_resultados_bajo_accion(self):
        self.view.selector.setCurrentIndex(3)
        self.assertEqual(self.view.error_option.count(), 6)
        self.assertTrue(self.view.results_card.isHidden())
        self.view.error_option.setCurrentIndex(4)
        self.view._calcular()
        nombres = [label.text().lower() for label in self.view.card_proceso.findChildren(QLabel)]
        for nombre in ("Inherente", "Redondeo", "Truncamiento", "Overflow", "Underflow", "Error del modelo matemático"):
            self.assertTrue(any(nombre.lower() in texto for texto in nombres))
        self.assertFalse(self.view.results_card.isHidden())
        self.assertTrue(self.view.card_solucion.isHidden())
        self.assertTrue(self.view.dog_main.isHidden())
        self.view._volver_a_entrada()
        self.assertFalse(self.view.dog_main.isHidden())

    def test_alto_de_entrada_se_ajusta_a_opcion_y_metodo_actuales(self):
        self.view.selector.setCurrentIndex(3)
        self.view.error_option.setCurrentIndex(1)
        alto_propagar = self.view.pages.sizeHint().height()
        self.view.error_option.setCurrentIndex(4)
        alto_tipos = self.view.pages.sizeHint().height()
        self.assertLess(alto_tipos, alto_propagar)
        self.view.selector.setCurrentIndex(2)
        alto_notacion = self.view.pages.sizeHint().height()
        self.assertLess(alto_notacion, alto_propagar)

    def test_raiz_en_extremo_muestra_paso_sin_tabla_vacia(self):
        resultado = bisecar("x**2 - 1", 1, 2, 1e-4, 100)
        self.view._mostrar_biseccion(resultado)
        textos = [label.text() for label in self.view.card_proceso.findChildren(QLabel)]
        self.assertTrue(any("raíz exacta en un extremo" in texto.lower() for texto in textos))
        self.assertEqual(self.view.card_proceso.findChildren(QTableWidget), [])

    def test_combos_ocultan_flecha_nativa(self):
        for combo in (self.view.selector, self.view.base_selector, self.view.error_option):
            self.assertIn("QComboBox::down-arrow { image: none", combo.styleSheet())

    def test_representacion_punto_flotante_es_opcion_independiente(self):
        self.view.selector.setCurrentIndex(3)
        self.view.error_option.setCurrentIndex(5)
        self.view._calcular()
        textos = [label.text() for label in self.view.card_proceso.findChildren(QLabel)]
        self.assertTrue(any("siguiente número float" in texto for texto in textos))
        self.assertTrue(any("overflow" in texto.lower() for texto in textos))
        self.assertTrue(any("underflow" in texto.lower() for texto in textos))


if __name__ == "__main__":
    unittest.main()
