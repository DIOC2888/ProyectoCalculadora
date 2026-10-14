"""Comprobaciones de la vista LU sin abrir ventanas en el escritorio."""

import os
import sys
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "Interfaz"))

from PySide6.QtCore import QCoreApplication, QEvent
from PySide6.QtWidgets import QApplication, QLabel
from vistas.componentes import CollapsibleCard
from vistas.vista_factorizacion import VistaFactorizacion


class VistaFactorizacionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.view = VistaFactorizacion()

    def tearDown(self):
        self.view.close()
        self.view.deleteLater()
        QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)

    def calculate(self, A, b):
        self.view.stepper_ecuaciones.value = len(A)
        self.view.stepper_variables.value = len(A[0])
        self.view._build_fields()
        for i, row in enumerate(A):
            for j, value in enumerate(row):
                self.view.matrix_inputs[0][i][j].setText(str(value))
        for field, value in zip(self.view.vector_inputs, b):
            field.setText(str(value))
        self.view._calculate()
        QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)

    def test_resultado_primero_y_detalles_plegados_por_etapa(self):
        self.calculate([[2, 1], [1, 1]], [3, 2])
        layout = self.view.results_card.layout()
        self.assertLess(layout.indexOf(self.view.card_solucion), layout.indexOf(self.view.card_proceso))
        self.assertTrue(self.view.card_solucion.is_expanded)
        self.assertFalse(self.view.card_proceso.is_expanded)
        stages = self.view.card_proceso.findChildren(CollapsibleCard)
        self.assertEqual(len(stages), 5)
        self.assertTrue(all(not stage.is_expanded for stage in stages))
        self.assertIsNotNone(self.view.findChild(CollapsibleCard, "LuComparison-A1"))
        labels = [label.text() for label in self.view.card_proceso.findChildren(QLabel)]
        self.assertIn("MATRIZ AUMENTADA [L|b]", labels)
        self.assertIn("MATRIZ AUMENTADA [U|y]", labels)

    def test_singular_muestra_factorizacion_y_diagnostico(self):
        self.calculate([[1, 2], [2, 4]], [3, 6])
        labels = [label.text() for label in self.view.card_solucion.findChildren(QLabel)]
        self.assertIn("MATRIZ L FINAL", labels)
        self.assertIn("MATRIZ U FINAL", labels)
        self.assertTrue(any("infinitas soluciones" in text for text in labels))
        self.assertFalse(any("permutación" in text for text in labels))

    def test_no_muestra_multiplicador_no_nulo_como_cero(self):
        widget = self.view._matrix_widget([[1e-8]])
        grid = widget.layout().itemAt(1).layout()
        self.assertEqual(grid.itemAtPosition(0, 0).widget().text(), "1e-08")
        widget.deleteLater()

    def test_error_limpia_resultado_anterior(self):
        self.calculate([[1]], [2])
        self.calculate([[1]], ["nan"])
        labels = [label.text() for label in self.view.card_solucion.findChildren(QLabel)]
        self.assertTrue(any("números finitos" in text for text in labels))
        self.assertNotIn("MATRIZ L FINAL", labels)
        self.assertEqual(self.view.card_proceso.content_layout.count(), 0)


if __name__ == "__main__":
    unittest.main()
