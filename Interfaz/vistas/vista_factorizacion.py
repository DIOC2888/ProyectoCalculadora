"""Vista para factorizar A=LU y resolver sistemas cuadrados."""
import os
import sys

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
INTERFACE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)
if INTERFACE_DIR not in sys.path:
    sys.path.insert(0, INTERFACE_DIR)

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit, QPushButton, QFrame, QScrollArea
from formato import formatear_numero, subindice
from controlador import ControladorMatriz
from sleeping_dog import SleepingDogContainer
from vistas.componentes import BracketWidget, NumberStepper, CollapsibleCard


class VistaFactorizacion(QWidget):
    """Captura A y b, y muestra L, U, y y x dentro de una tarjeta de resultados."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: #F8FAFC; }")
        page = QWidget()
        page.setStyleSheet("background: #F8FAFC;")
        outer = QVBoxLayout(page)
        outer.setContentsMargins(20, 36, 20, 36)
        outer.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        content = QWidget()
        content.setFixedWidth(740)
        layout = QVBoxLayout(content)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(24)
        header_box = QVBoxLayout()
        header_box.setSpacing(6)
        title = QLabel("Factorización LU")
        title.setStyleSheet("font-size: 24px; font-weight: 800; color: #0F172A;")
        subtitle = QLabel("Descompón A = LU y resuelve Ax = b mediante sustituciones.")
        subtitle.setStyleSheet("font-size: 13px; color: #64748B; font-weight: 500;")
        header_box.addWidget(title)
        header_box.addWidget(subtitle)
        layout.addLayout(header_box)

        self.card = QFrame()
        self.card.setObjectName("inputCard")
        self.card.setStyleSheet("QFrame#inputCard { background: white; border: 1px solid #E2E8F0; border-radius: 16px; }")
        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(28, 24, 28, 24)
        card_layout.setSpacing(20)

        mode_container = QFrame()
        mode_container.setStyleSheet("background-color: #F1F5F9; border-radius: 10px;")
        mode_layout = QHBoxLayout(mode_container)
        mode_layout.setContentsMargins(4, 4, 4, 4)
        mode_layout.setSpacing(4)
        mode_button = QPushButton("Construir Matriz")
        mode_button.setEnabled(False)
        mode_button.setStyleSheet("QPushButton { background: #FFFFFF; border: 1px solid #E2E8F0; color: #2563EB; font-weight: 700; font-size: 13px; padding: 8px 16px; border-radius: 8px; }")
        mode_layout.addWidget(mode_button, alignment=Qt.AlignmentFlag.AlignLeft)
        card_layout.addWidget(mode_container, alignment=Qt.AlignmentFlag.AlignLeft)

        dims = QHBoxLayout()
        dims.setSpacing(24)
        self.stepper_ecuaciones = self._crear_control_cantidad("CANTIDAD DE ECUACIONES", 3)
        self.stepper_variables = self._crear_control_cantidad("CANTIDAD DE VARIABLES", 3)
        self.stepper_matrices = self._crear_control_cantidad("CANTIDAD DE MATRICES", 1)
        for stepper in (self.stepper_ecuaciones, self.stepper_variables, self.stepper_matrices):
            stepper.on_change_callback = self._build_fields
        for stepper in (self.stepper_ecuaciones, self.stepper_variables, self.stepper_matrices):
            dims.addLayout(stepper._factorizacion_control_layout)
        dims.addStretch()
        card_layout.addLayout(dims)
        input_row = QHBoxLayout()
        input_row.setSpacing(28)
        input_row.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.matrixes_container = QWidget()
        self.matrixes_container.setStyleSheet("background: transparent;")
        self.matrixes_layout = QHBoxLayout(self.matrixes_container)
        self.matrixes_layout.setContentsMargins(0, 0, 0, 0)
        self.matrixes_layout.setSpacing(28)
        self.matrixes_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        input_row.addWidget(self.matrixes_container)
        self.matrix_inputs = []
        self.matrix_grids = []
        self.matrix_brackets = []
        vector_column = QVBoxLayout()
        vector_column.setSpacing(8)
        vector_title = QLabel("VECTOR b")
        vector_title.setStyleSheet("color: #64748B; font-size: 10px; font-weight: 700; letter-spacing: 0.5px; background: transparent;")
        vector_column.addWidget(vector_title)
        vector_row = QHBoxLayout()
        vector_row.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.vector_bracket_left = BracketWidget(is_left=True)
        self.vector_bracket_right = BracketWidget(is_left=False)
        vector_row.addWidget(self.vector_bracket_left)
        self.vector_grid = QGridLayout()
        self.vector_grid.setVerticalSpacing(8)
        vector_row.addLayout(self.vector_grid)
        vector_row.addWidget(self.vector_bracket_right)
        vector_column.addLayout(vector_row)
        self.vector_inputs = []
        input_row.addLayout(vector_column)
        input_row.addStretch()
        card_layout.addLayout(input_row)
        self._build_fields()
        buttons_row = QHBoxLayout()
        self.solve_button = QPushButton("Resolver")
        self.solve_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.solve_button.setStyleSheet("QPushButton { background: #2563EB; color: white; font-weight: 700; padding: 11px 20px; border: 0; border-radius: 10px; } QPushButton:hover { background: #1D4ED8; }")
        self.solve_button.clicked.connect(self._calculate)
        buttons_row.addWidget(self.solve_button)
        clear_button = QPushButton("Limpiar")
        clear_button.setCursor(Qt.CursorShape.PointingHandCursor)
        clear_button.setStyleSheet("QPushButton { background: #FFFFFF; color: #1E293B; padding: 11px 22px; border: 1px solid #CBD5E1; border-radius: 10px; } QPushButton:hover { background: #F8FAFC; }")
        clear_button.clicked.connect(self._clear)
        buttons_row.addWidget(clear_button)
        buttons_row.addStretch()
        card_layout.addLayout(buttons_row)
        layout.addWidget(self.card)

        self.results_card = QWidget()
        result_layout = QVBoxLayout(self.results_card)
        result_layout.setContentsMargins(0, 0, 0, 0)
        result_layout.setSpacing(16)
        back = QPushButton("← Nuevo sistema")
        back.setCursor(Qt.CursorShape.PointingHandCursor)
        back.setStyleSheet("QPushButton { color: #64748B; font-weight: 600; font-size: 13px; border: none; background: transparent; text-align: left; padding: 0px; } QPushButton:hover { color: #0F172A; }")
        back.clicked.connect(self._back)
        result_layout.addWidget(back)
        self.card_proceso = CollapsibleCard("Proceso")
        self.card_solucion = CollapsibleCard("Solución")
        result_layout.addWidget(self.card_proceso)
        result_layout.addWidget(self.card_solucion)
        self.results_card.hide()
        layout.addWidget(self.results_card)
        self.dog_main = SleepingDogContainer(small=False)
        layout.addWidget(self.dog_main, alignment=Qt.AlignmentFlag.AlignCenter)
        outer.addWidget(content)
        scroll.setWidget(page)
        root.addWidget(scroll)

    def _build_fields(self):
        rows = self.stepper_ecuaciones.value
        cols = self.stepper_variables.value
        matrix_count = self.stepper_matrices.value
        while self.matrixes_layout.count():
            item = self.matrixes_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        while self.vector_grid.count():
            item = self.vector_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.matrix_inputs, self.matrix_grids, self.matrix_brackets = [], [], []
        self.vector_inputs = []
        for matrix_index in range(matrix_count):
            column = QWidget()
            column.setStyleSheet("background: transparent;")
            column_layout = QVBoxLayout(column)
            column_layout.setContentsMargins(0, 0, 0, 0)
            column_layout.setSpacing(8)
            matrix_title = QLabel(f"A{subindice(matrix_index + 1)}")
            matrix_title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            matrix_title.setStyleSheet("color: #64748B; font-size: 11px; background: transparent;")
            column_layout.addWidget(matrix_title)
            bracket_row = QHBoxLayout()
            bracket_row.setSpacing(6)
            left, right = BracketWidget(True), BracketWidget(False)
            grid = QGridLayout()
            grid.setHorizontalSpacing(10)
            grid.setVerticalSpacing(8)
            bracket_row.addWidget(left)
            bracket_row.addLayout(grid)
            bracket_row.addWidget(right)
            column_layout.addLayout(bracket_row)
            matrix_rows = []
            for i in range(rows):
                row = []
                for j in range(cols):
                    initial = "1" if i == j else "0"
                    field = QLineEdit(initial)
                    field.setFixedSize(68, 38)
                    field.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    field.setStyleSheet("QLineEdit { background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; color: #0F172A; }")
                    grid.addWidget(field, i, j)
                    row.append(field)
                matrix_rows.append(row)
            left.setFixedHeight(rows * 46)
            right.setFixedHeight(rows * 46)
            self.matrixes_layout.addWidget(column)
            self.matrix_inputs.append(matrix_rows)
            self.matrix_grids.append(grid)
            self.matrix_brackets.append((left, right))
        for i in range(rows):
            b = QLineEdit("1")
            b.setFixedSize(68, 38)
            b.setAlignment(Qt.AlignmentFlag.AlignCenter)
            b.setStyleSheet("QLineEdit { background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; color: #0F172A; }")
            self.vector_grid.addWidget(b, i, 0)
            self.vector_inputs.append(b)
        self.vector_bracket_left.setFixedHeight(rows * 46)
        self.vector_bracket_right.setFixedHeight(rows * 46)
        self.card.adjustSize()

    @staticmethod
    def _crear_control_cantidad(texto, valor):
        caja = QVBoxLayout()
        caja.setSpacing(6)
        etiqueta = QLabel(texto)
        etiqueta.setStyleSheet("color: #64748B; font-size: 10px; font-weight: 700; letter-spacing: 0.5px; background: transparent;")
        control = NumberStepper(value=valor, min_val=1, max_val=10)
        caja.addWidget(etiqueta)
        caja.addWidget(control)
        control._factorizacion_control_layout = caja
        return control

    @staticmethod
    def _clear_layout(layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            elif item.layout() is not None:
                VistaFactorizacion._clear_layout(item.layout())

    @staticmethod
    def _matrix_text(matrix):
        return "[\n" + "\n".join("  [" + ",  ".join(formatear_numero(v) for v in row) + "]" for row in matrix) + "\n]"

    def _calculate(self):
        try:
            self._clear_layout(self.card_proceso.content_layout)
            b = [float(field.text()) for field in self.vector_inputs]
            solutions, process_blocks = [], []
            for index, matrix_fields in enumerate(self.matrix_inputs, start=1):
                A = [[float(field.text()) for field in row] for row in matrix_fields]
                result = ControladorMatriz.factorizar_y_resolver(A, b)
                process_blocks.append((index, result.get("proceso", [])))
                solutions.append((index, result))
            self._render_solutions(solutions)
            self._render_process(process_blocks)
            self.card.hide()
            self.results_card.show()
            self.dog_main.hide()
        except (ValueError, TypeError) as exc:
            self._clear_layout(self.card_proceso.content_layout)
            self._clear_layout(self.card_solucion.content_layout)
            error = QLabel(str(exc))
            error.setWordWrap(True)
            error.setStyleSheet("color: #B91C1C; font-size: 13px; background: transparent;")
            self.card_solucion.add_widget(error)
            self.card_solucion.is_expanded = True
            self.card_solucion.content_widget.setVisible(True)
            self.card_solucion.btn_toggle.setText("−")
            self.card.hide()
            self.results_card.show()
            self.dog_main.hide()

    def _render_process(self, matrix_processes):
        number = 1
        for matrix_index, steps in matrix_processes:
            heading = QLabel(f"PROCESO PARA A{subindice(matrix_index)}")
            heading.setStyleSheet("color: #64748B; font-size: 10px; font-weight: 700; letter-spacing: 0.5px; background: transparent; border: none;")
            self.card_proceso.add_widget(heading)
            for step in steps:
                frame = QFrame()
                frame.setObjectName("LuStepCard")
                frame.setStyleSheet("QFrame#LuStepCard { background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; }")
                row = QHBoxLayout(frame)
                row.setContentsMargins(16, 14, 16, 14)
                row.setSpacing(12)
                badge = QLabel(str(number))
                badge.setFixedSize(28, 28)
                badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
                badge.setStyleSheet("background: #EEF2FF; color: #4F46E5; font-size: 13px; font-weight: 700; border: none; border-radius: 14px;")
                row.addWidget(badge, alignment=Qt.AlignmentFlag.AlignTop)
                detail = QVBoxLayout()
                title = QLabel(step.get("titulo", "PASO"))
                title.setStyleSheet("color: #64748B; font-size: 10px; font-weight: 700; letter-spacing: 0.5px; background: transparent; border: none;")
                description = QLabel(step.get("descripcion", ""))
                description.setWordWrap(True)
                description.setStyleSheet("color: #0F172A; font-family: Consolas, monospace; font-size: 13px; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 10px;")
                detail.addWidget(title)
                detail.addWidget(description)
                for key, label in (("A", "MATRIZ A"), ("L", "MATRIZ L"), ("U", "MATRIZ U"), ("LU", "PRODUCTO L · U"), ("matriz", "MATRIZ AUMENTADA [A|b]")):
                    if key in step:
                        detail.addWidget(self._result_label(label))
                        detail.addWidget(self._matrix_widget(step[key]))
                for key, label in (("b", "VECTOR b"), ("y", "VECTOR y"), ("x", "VECTOR x"), ("Ax", "PRODUCTO A · x")):
                    if key in step:
                        detail.addWidget(self._result_label(label))
                        detail.addWidget(self._vector_widget(step[key]))
                row.addLayout(detail, 1)
                self.card_proceso.add_widget(frame)
                number += 1
        self.card_proceso.is_expanded = True
        self.card_proceso.content_widget.setVisible(True)
        self.card_proceso.btn_toggle.setText("−")
        self.card_solucion.is_expanded = True
        self.card_solucion.content_widget.setVisible(True)
        self.card_solucion.btn_toggle.setText("−")

    def _render_solutions(self, solutions):
        self._clear_layout(self.card_solucion.content_layout)
        for index, result in solutions:
            section = QWidget()
            section.setStyleSheet("background: transparent;")
            section_layout = QVBoxLayout(section)
            section_layout.setContentsMargins(0, 0, 0, 12)
            section_layout.setSpacing(12)
            title = QLabel(f"FACTORIZACIÓN DE A{subindice(index)}")
            title.setStyleSheet("color: #64748B; font-size: 11px; font-weight: 700; letter-spacing: 0.5px; background: transparent;")
            section_layout.addWidget(title)
            for caption, key in (("MATRIZ L", "L"), ("MATRIZ U", "U"), ("PRODUCTO L · U", "LU")):
                section_layout.addWidget(self._result_label(caption))
                section_layout.addWidget(self._matrix_widget(result[key]))
            lu_message = QLabel("La factorización es correcta (L · U = A)." if result["factorizacion_correcta"] else "La factorización no coincide con A.")
            lu_message.setStyleSheet("color: #0F172A; font-size: 13px; font-weight: 600; background: transparent;")
            section_layout.addWidget(lu_message)
            if result["x"] is not None:
                section_layout.addWidget(self._result_label(f"SISTEMA A{subindice(index)}x = b"))
                section_layout.addWidget(self._result_label("VECTOR INTERMEDIO y"))
                section_layout.addWidget(self._vector_widget(result["y"]))
                section_layout.addWidget(self._result_label("VECTOR SOLUCIÓN x"))
                section_layout.addWidget(self._vector_widget(result["x"]))
                check = QLabel("Comprobación exitosa: A · x = b." if result["verificacion_sistema"] else "La comprobación A · x = b no se cumple.")
                check.setStyleSheet("color: #0F172A; font-size: 13px; font-weight: 600; background: transparent;")
                section_layout.addWidget(check)
                section_layout.addWidget(self._result_label("PRODUCTO A · x"))
                section_layout.addWidget(self._vector_widget(result["Ax"]))
                comparison = result.get("comparacion_gauss", {})
                comparison_ok = comparison.get("coincide_con_LU") and comparison.get("solucion_coincide")
                comparison_label = QLabel(
                    "Comparación exitosa: la reducción de [A|b] produce el mismo U, y y x."
                    if comparison_ok else "La reducción ordinaria de [A|b] no coincide con el proceso LU."
                )
                comparison_label.setWordWrap(True)
                comparison_label.setStyleSheet("color: #0F172A; font-size: 13px; font-weight: 600; background: transparent;")
                section_layout.addWidget(comparison_label)
                if comparison.get("matriz_final"):
                    section_layout.addWidget(self._result_label("REDUCCIÓN ORDINARIA FINAL [A|b]"))
                    section_layout.addWidget(self._matrix_widget(comparison["matriz_final"]))
            else:
                section_layout.addWidget(self._result_label(result.get("mensaje_sistema", "No se pudo resolver el sistema.")))
            self.card_solucion.add_widget(section)
        self.card_solucion.is_expanded = True
        self.card_solucion.content_widget.setVisible(True)
        self.card_solucion.btn_toggle.setText("−")

    @staticmethod
    def _result_label(text):
        label = QLabel(text)
        label.setStyleSheet("color: #64748B; font-size: 10px; font-weight: 700; letter-spacing: 0.5px; background: transparent;")
        return label

    def _matrix_widget(self, matrix):
        widget = QWidget()
        widget.setStyleSheet("background: transparent;")
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 2, 0, 2)
        layout.setSpacing(6)
        left, right = BracketWidget(True), BracketWidget(False)
        grid = QGridLayout()
        grid.setContentsMargins(4, 0, 4, 0)
        grid.setHorizontalSpacing(18)
        grid.setVerticalSpacing(4)
        for i, row in enumerate(matrix):
            for j, value in enumerate(row):
                cell = QLabel(formatear_numero(value))
                cell.setMinimumWidth(42)
                cell.setAlignment(Qt.AlignmentFlag.AlignCenter)
                cell.setStyleSheet("color: #0F172A; font-size: 13px; font-family: 'Segoe UI', sans-serif; background: transparent;")
                grid.addWidget(cell, i, j)
        left.setFixedHeight(max(28, len(matrix) * 30))
        right.setFixedHeight(max(28, len(matrix) * 30))
        layout.addWidget(left)
        layout.addLayout(grid)
        layout.addWidget(right)
        layout.addStretch()
        return widget

    def _vector_widget(self, vector):
        return self._matrix_widget([[value] for value in vector])

    def _back(self):
        self.results_card.hide()
        self.card.show()
        self.dog_main.show()

    def _clear(self):
        for matrix in self.matrix_inputs:
            for row in matrix:
                for field in row:
                    field.setText("0")
        for field in self.vector_inputs:
            field.setText("0")
        self._clear_layout(self.card_proceso.content_layout)
        self._clear_layout(self.card_solucion.content_layout)
        self.results_card.hide()
        self.card.show()
        self.dog_main.show()
