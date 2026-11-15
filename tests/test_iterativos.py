"""Tarea 8 y cotejo con los ejemplos de la presentación de la sesión 21."""

import math
import os
import sys
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR))
sys.path.insert(0, str(PROJECT_DIR / "Interfaz"))

import numpy as np
from PySide6.QtWidgets import QApplication, QLabel, QTableWidget

from metodos_numericos import resolver_metodo_iterativo
from controlador_metodos_numericos import ControladorMetodosNumericos
from vistas.vista_metodos_numericos import VistaMetodosNumericos


A_SESION21 = [[10, 3, 1], [5, -10, 3], [1, 3, 10]]
B_SESION21 = [14, -5, 14]
A_CINCO = [[5, -1, 0, 1, -1], [1, -5, 1, 0, -1], [1, -1, 5, -1, 0],
           [1, 0, -1, 5, -1], [1, -1, 1, 0, -5]]
B_CINCO = [-10, 1, -2, 1, -11]
METODOS = ("Jacobi", "Gauss-Seidel")


class IterativosTests(unittest.TestCase):
    def test_primeras_iteraciones_del_ejemplo_1(self):
        # Valores obtenidos sustituyendo en los despejes, sin llamar al motor.
        esperados = {
            "Jacobi": [[1.4, 0.5, 1.4], [1.11, 1.62, 1.11]],
            "Gauss-Seidel": [[1.4, 1.2, 0.9], [0.95, 1.245, 0.9315]],
        }
        errores_2 = {"Jacobi": [math.sqrt(4.17), math.sqrt(1.4226)],
                     "Gauss-Seidel": [math.sqrt(4.21), math.sqrt(0.20551725)]}
        for metodo in METODOS:
            r = resolver_metodo_iterativo(A_SESION21, B_SESION21, [0]*3,
                                         1e-4, 2, metodo, criterio_error="euclideo")
            with self.subTest(metodo=metodo):
                np.testing.assert_allclose([f["x"] for f in r["tabla"][1:]], esperados[metodo])
                np.testing.assert_allclose([f["error"] for f in r["tabla"][1:]], errores_2[metodo])
                self.assertEqual(r["tabla"][1]["error_infinito"], 1.4)
                self.assertIsNone(r["tabla"][0]["error"])

    def test_caso_1_dominancia_convergencia_y_referencia(self):
        for criterio in ("infinito", "euclideo"):
            for metodo, iteraciones in (("Jacobi", 16), ("Gauss-Seidel", 5)):
                with self.subTest(criterio=criterio, metodo=metodo):
                    r = resolver_metodo_iterativo(A_SESION21, B_SESION21, [0]*3,
                                                 1e-4, 100, metodo, criterio_error=criterio)
                    self.assertTrue(r["dominante"])
                    self.assertTrue(r["convergio"])
                    self.assertEqual(r["iteraciones"], iteraciones)
                    self.assertLessEqual(r["error"], 1e-4)
                    self.assertGreater(r["tabla"][-2]["error"], 1e-4)
                    np.testing.assert_allclose(r["referencia"], [125/134, 167/134, 125/134])
                    self.assertLess(r["diferencia_referencia"], 2e-5)
                    self.assertAlmostEqual(r["residuo"], np.max(np.abs(np.array(A_SESION21) @ r["solucion"] - B_SESION21)))

    def test_ejemplo_2_tres_iteraciones_y_error_verdadero(self):
        r = resolver_metodo_iterativo(A_CINCO, B_CINCO, [0]*5, 1e-4, 3,
                                     "Gauss-Seidel", criterio_error="euclideo")
        np.testing.assert_allclose([f["x"] for f in r["tabla"][1:]], [
            [-2, -0.6, -0.12, 0.576, 1.896],
            [-1.856, -0.9744, -0.10848, 0.928704, 2.001984],
            [-1.980224, -1.0181376, -0.02184192, 0.992073216, 2.003214336],
        ])
        self.assertAlmostEqual(r["error"], 0.1699055855, places=9)
        self.assertAlmostEqual(r["tabla"][0]["error_referencia_euclideo"], math.sqrt(10))
        self.assertAlmostEqual(r["diferencia_referencia_euclidea"], 0.03564, places=5)
        self.assertFalse(r["convergio"])

    def test_ejemplo_chapra_porcentaje_y_parada_en_cuatro(self):
        A = [[3, -0.1, -0.2], [0.1, 7, -0.3], [0.3, -0.2, 10]]
        for metodo in METODOS:
            with self.subTest(metodo=metodo):
                r = resolver_metodo_iterativo(A, [7.85, -19.3, 71.4], [0]*3,
                                             0.05, 100, metodo, criterio_error="porcentual")
                self.assertEqual(r["iteraciones"], 4)
                self.assertTrue(r["convergio"])
                self.assertAlmostEqual(r["tabla"][1]["error"], 100)
                np.testing.assert_allclose(r["referencia"], [3, -2.5, 7])
                self.assertGreater(r["tabla"][3]["error"], 0.05)
                self.assertLessEqual(r["error"], 0.05)

    def test_el_criterio_elegido_cambia_realmente_la_parada(self):
        for criterio, iteraciones in (("infinito", 1), ("euclideo", 2)):
            r = resolver_metodo_iterativo(np.eye(3), [1]*3, [0]*3, 1.5, 10,
                                         "Jacobi", criterio_error=criterio)
            self.assertEqual(r["iteraciones"], iteraciones)

    def test_porcentual_maneja_componentes_cero_sin_falsa_parada(self):
        r = resolver_metodo_iterativo(np.eye(2), [0, 1], [1, 1], 0.05, 10,
                                     "Jacobi", criterio_error="porcentual")
        self.assertEqual(r["tabla"][1]["error"], math.inf)
        self.assertEqual(r["iteraciones"], 2)
        self.assertEqual(r["error"], 0)
        self.assertTrue(r["convergio"])

    def test_caso_2_reordena_a_y_b_sin_reordenar_variables(self):
        A = np.array([[0, 5, 1], [4, 1, 1], [1, 1, 6]], dtype=float)
        b = np.array([13, 9, 21], dtype=float)
        x0 = np.array([0.25, -1, 0.5])
        for metodo in METODOS:
            with self.subTest(metodo=metodo):
                r = resolver_metodo_iterativo(A, b, x0, 1e-6, 100, metodo)
                self.assertEqual(r["permutacion"], [2, 1, 3])
                self.assertTrue(r["reordenada"])
                self.assertFalse(r["dominante_original"])
                self.assertTrue(r["dominante"])
                np.testing.assert_array_equal(r["b"], [9, 13, 21])
                np.testing.assert_array_equal(r["tabla"][0]["x"], x0)
                np.testing.assert_allclose(r["solucion"], [1, 2, 3], atol=1e-6)
                np.testing.assert_allclose(A @ r["solucion"], b, atol=1e-5)
                np.testing.assert_array_equal(A, [[0, 5, 1], [4, 1, 1], [1, 1, 6]])
                np.testing.assert_array_equal(b, [13, 9, 21])
                np.testing.assert_array_equal(x0, [0.25, -1, 0.5])

    def test_caso_3_divergencia_hasta_el_limite_con_advertencia(self):
        for metodo in METODOS:
            r = resolver_metodo_iterativo([[1, 2], [2, 1]], [3, 3], [0, 0],
                                         1e-4, 15, metodo, reordenar=False)
            with self.subTest(metodo=metodo):
                self.assertFalse(r["dominante"])
                self.assertFalse(r["convergio"])
                self.assertEqual(r["iteraciones"], 15)
                self.assertEqual(r["motivo_parada"], "maximo_iteraciones")
                self.assertTrue(r["advertencias"])
                self.assertGreater(r["residuo"], 100)

    def test_reordenar_puede_hacer_converger_el_caso_3(self):
        r = resolver_metodo_iterativo([[1, 2], [2, 1]], [3, 3], [0, 0],
                                     1e-4, 100, "Jacobi", reordenar=True)
        self.assertTrue(r["convergio"])
        self.assertEqual(r["permutacion"], [2, 1])

    def test_sin_dominancia_puede_converger_y_conserva_orden_valido(self):
        # El antiguo reordenamiento elegía [2, 1] y hacía divergir este sistema.
        for metodo in METODOS:
            r = resolver_metodo_iterativo([[1, 2], [0.1, 1]], [3, 1.1], [0, 0],
                                         1e-6, 100, metodo)
            self.assertFalse(r["dominante"])
            self.assertFalse(r["reordenada"])
            self.assertTrue(r["convergio"])
            np.testing.assert_allclose(r["solucion"], [1, 1], atol=1e-6)

    def test_crecimiento_transitorio_no_interrumpe_una_convergencia(self):
        # Matriz triangular: la matriz de iteración es nilpotente. Aunque los
        # cambios crecen al principio, la solución se alcanza en pasos finitos.
        A = np.eye(8) + 2*np.eye(8, k=1)
        r = resolver_metodo_iterativo(A, [3]*7+[1], [0]*8, 1e-6, 100, "Jacobi")
        self.assertTrue(r["convergio"])
        self.assertTrue(r["advertencias"])
        self.assertEqual(r["iteraciones"], 9)
        np.testing.assert_array_equal(r["solucion"], [1]*8)

    def test_rechaza_diagonal_cero_y_reordenamiento_imposible(self):
        for A, reordenar in (([[0, 1], [1, 2]], False), ([[0, 1], [0, 2]], True)):
            with self.subTest(A=A), self.assertRaisesRegex(ValueError, "diagonal"):
                resolver_metodo_iterativo(A, [1, 2], [0, 0], 1e-4, 10, "Jacobi", reordenar)

    def test_valida_dimensiones_valores_y_parametros(self):
        base = dict(matriz=[[4, 1], [1, 4]], vector=[1, 1], inicial=[0, 0],
                    tolerancia=1e-4, max_iteraciones=10, metodo="Jacobi")
        casos = [dict(matriz=[]), dict(matriz=[[1, 2, 3], [4, 5, 6]]),
                 dict(vector=[1]), dict(inicial=[0]), dict(vector=[math.nan, 1]),
                 dict(inicial=[math.inf, 0]), dict(matriz=[[math.inf, 1], [1, 4]]),
                 dict(tolerancia=0), dict(tolerancia=-1), dict(tolerancia=math.nan),
                 dict(max_iteraciones=0), dict(max_iteraciones=1.5),
                 dict(max_iteraciones=True), dict(max_iteraciones=math.inf),
                 dict(metodo="SOR"), dict(criterio_error="desconocido")]
        for cambios in casos:
            with self.subTest(cambios=cambios), self.assertRaises(ValueError):
                resolver_metodo_iterativo(**{**base, **cambios})

    def test_no_finitos_detienen_sin_marcar_convergencia(self):
        for metodo in METODOS:
            r = resolver_metodo_iterativo([[1e-308, 2], [2, 1e-308]], [1, 1],
                                         [0, 0], 1e-4, 10, metodo, reordenar=False)
            self.assertFalse(r["convergio"])
            self.assertEqual(r["motivo_parada"], "no_finito")
            self.assertTrue(np.isfinite(r["solucion"]).all())


class VistaIterativosTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.view = VistaMetodosNumericos()

    def tearDown(self):
        self.view.close()
        self.view.deleteLater()
        self.app.processEvents()

    def test_controlador_y_tabla_usan_la_norma_elegida(self):
        self.view.selector.setCurrentIndex(4)
        self.view.iter_error.setCurrentIndex(1)
        for fila, valores in zip(self.view.iter_matrix_fields, A_SESION21):
            for campo, valor in zip(fila, valores):
                campo.setText(str(valor))
        for campo, valor in zip(self.view.iter_b_fields, B_SESION21):
            campo.setText(str(valor))
        self.view._calcular_iterativos()
        tabla = self.view.card_proceso.findChildren(QTableWidget)[0]
        self.assertEqual(tabla.rowCount(), 17)
        self.assertIn("₂", tabla.horizontalHeaderItem(4).text())
        self.assertEqual(tabla.item(0, 4).text(), "—")
        self.assertAlmostEqual(float(tabla.item(1, 4).text()), math.sqrt(4.17), places=6)
        self.view.iter_error.setCurrentIndex(2)
        self.assertIn("%", self.view.iter_tol_label.text())
        self.view._limpiar()
        self.assertEqual(self.view.iter_error.currentData(), "infinito")

    def test_comparacion_no_declara_ganador_si_no_convergen(self):
        resultados = [ControladorMetodosNumericos.resolver_iterativo(
            [[1, 2], [2, 1]], [3, 3], [0, 0], 1e-4, 3, metodo, False)
            for metodo in METODOS]
        self.view._mostrar_iterativos(resultados)
        textos = [label.text() for label in self.view.card_proceso.findChildren(QLabel)]
        self.assertTrue(any("no se establece cuál" in texto for texto in textos))
        self.assertFalse(any("Menos iteraciones:" in texto for texto in textos))


if __name__ == "__main__":
    unittest.main()
