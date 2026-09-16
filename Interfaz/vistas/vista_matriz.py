import sys
import os

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

from formato import formatear_numero
from fractions import Fraction
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QStackedLayout,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
    QMessageBox,
    QComboBox
   
)
from navbar import Navbar
from sidebar import Sidebar
from sleeping_dog import SleepingDogContainer
from vistas.componentes import BracketWidget, NumberStepper, CollapsibleCard
# Importamos el controlador
from controlador import ControladorMatriz

# Importamos la función para procesar ecuaciones en texto si existe en entrada.py
try:
    from entrada import leer_sistema_desde_texto
except ImportError:
    leer_sistema_desde_texto = None

class VistaMatriz(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.inputs_list = []
        self._build_ui()

    def _volver_a_matriz(self):
            self.results_card.hide()
            self.card.show()
            if hasattr(self, "dog_main"):
                self.dog_main.show()
                
    def _build_ui(self):
        # Layout directo de esta vista
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Área Central con Scroll
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; background-color: #F8FAFC; }")

        main_content = QWidget()
        main_content.setStyleSheet("background-color: #F8FAFC;")

        content_outer_layout = QVBoxLayout(main_content)
        content_outer_layout.setContentsMargins(20, 36, 20, 36)
        content_outer_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        centered_wrapper = QWidget()
        centered_wrapper.setFixedWidth(740)

        content_layout = QVBoxLayout(centered_wrapper)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(24)

        # Encabezado Centrado
        header_box = QVBoxLayout()
        header_box.setSpacing(6)

        title = QLabel("Resolver sistema de ecuaciones")
        title.setStyleSheet("font-size: 24px; font-weight: 800; color: #0F172A;")

        subtitle = QLabel("Ingresa los coeficientes de tu sistema y aplica eliminación por filas.")
        subtitle.setStyleSheet("font-size: 13px; color: #64748B; font-weight: 500;")

        header_box.addWidget(title)
        header_box.addWidget(subtitle)
        content_layout.addLayout(header_box)

        # ... (Resto del diseño de la matriz) ...
        # Tarjeta Principal
        self.card = QFrame()
        self.card.setStyleSheet(
            """
            QFrame#inputCard {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 16px;
            }
        """
        )
        self.card.setObjectName("inputCard")
        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(28, 24, 28, 24)
        card_layout.setSpacing(20)
        
        # Modos
        mode_wrapper = QHBoxLayout()
        
        mode_container = QFrame()
        mode_container.setStyleSheet("background-color: #F1F5F9; border-radius: 10px;")
        mode_layout = QHBoxLayout(mode_container)
        mode_layout.setContentsMargins(4, 4, 4, 4)
        mode_layout.setSpacing(4)
        
        self.btn_matrix = QPushButton("Construir matriz")
        self.btn_equations = QPushButton("Ingresar ecuaciones")
        
        mode_button_style = """
            QPushButton {
                background-color: transparent;
                border: none;
                color: #64748B;
                font-weight: 600;
                font-size: 13px;
                padding: 8px 16px;
                border-radius: 8px;
            }
            QPushButton:hover { color: #1E293B; }
        """
        mode_button_active_style = """
            QPushButton {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                color: #2563EB;
                font-weight: 700;
                font-size: 13px;
                padding: 8px 16px;
                border-radius: 8px;
            }
        """
        
        self.btn_matrix.setStyleSheet(mode_button_active_style)
        self.btn_equations.setStyleSheet(mode_button_style)
        self.btn_matrix.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_equations.setCursor(Qt.CursorShape.PointingHandCursor)
        
        mode_layout.addWidget(self.btn_matrix)
        mode_layout.addWidget(self.btn_equations)
        
        mode_wrapper.addWidget(mode_container, alignment=Qt.AlignmentFlag.AlignLeft)
        card_layout.addLayout(mode_wrapper)
        
        self.stacked_layout = QStackedLayout()
        
        # VISTA 1: MATRIZ
        matrix_view = QWidget()
        matrix_view.setObjectName("VistaMatriz")
        matrix_view.setAccessibleName("VistaMatriz")
        matrix_view.setStyleSheet("background-color: transparent;")
        self.vista_matriz = matrix_view
        matrix_layout = QVBoxLayout(matrix_view)
        matrix_layout.setContentsMargins(0, 0, 0, 0)
        matrix_layout.setSpacing(20)
        
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(24)
        
        eq_box = QVBoxLayout()
        eq_box.setSpacing(6)
        eq_label = QLabel("CANTIDAD DE ECUACIONES")
        eq_label.setStyleSheet("color: #64748B; font-size: 10px; font-weight: 700; letter-spacing: 0.5px; background: transparent;")
        self.stepper_eq = NumberStepper(value=3)
        eq_box.addWidget(eq_label)
        eq_box.addWidget(self.stepper_eq)
        
        var_box = QVBoxLayout()
        var_box.setSpacing(6)
        var_label = QLabel("CANTIDAD DE VARIABLES")
        var_label.setStyleSheet("color: #64748B; font-size: 10px; font-weight: 700; letter-spacing: 0.5px; background: transparent;")
        self.stepper_var = NumberStepper(value=3)
        var_box.addWidget(var_label)
        var_box.addWidget(self.stepper_var)
        
        
        
        controls_layout.addLayout(eq_box)
        controls_layout.addLayout(var_box)
        controls_layout.addStretch()
        matrix_layout.addLayout(controls_layout)
        
        self.matrix_grid_widget = QWidget()
        self.matrix_grid_widget.setStyleSheet("background-color: transparent;")
        self.matrix_grid = QGridLayout(self.matrix_grid_widget)
        self.matrix_grid.setContentsMargins(0, 0, 0, 0)
        self.matrix_grid.setHorizontalSpacing(10)
        self.matrix_grid.setVerticalSpacing(10)
        
        # Encapsulamos la matriz en un layout horizontal con stretch
        matrix_wrapper_layout = QHBoxLayout()
        matrix_wrapper_layout.setContentsMargins(0, 0, 0, 0)
        matrix_wrapper_layout.addWidget(self.matrix_grid_widget)
        matrix_wrapper_layout.addStretch(1)  # <--- ESTE ES EL STRETCH QUE EMPUJA TODO A LA IZQUIERDA
        
        matrix_layout.addLayout(matrix_wrapper_layout)
        action_buttons_layout = QHBoxLayout()
        action_buttons_layout.setSpacing(12)
        
        self.btn_solve = QPushButton("Resolver sistema")
        self.btn_solve.setStyleSheet(
            """
            QPushButton {
                background-color: #2563EB;
                color: white;
                font-weight: 600;
                font-size: 13px;
                padding: 10px 22px;
                border-radius: 10px;
                border: none;
            }
            QPushButton:hover { background-color: #1D4ED8; }
            """
        )
        self.btn_solve.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_solve.clicked.connect(self._on_solve_clicked)
        
        btn_clear = QPushButton("Limpiar")
        btn_clear.setStyleSheet(
            """
            QPushButton {
                background-color: #FFFFFF;
                color: #475569;
                font-weight: 600;
                font-size: 13px;
                padding: 10px 24px;
                border-radius: 10px;
                border: 1px solid #E2E8F0;
            }
            QPushButton:hover { background-color: #F8FAFC; color: #1E293B; }
            """
        )
        btn_clear.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_clear.clicked.connect(self._clear_matrix_inputs)
        
        # Creamos el ComboBox para el método
        self.combo_metodo = QComboBox()
        self.combo_metodo.addItems(["Gauss-Jordan", "Gauss"])
        self.combo_metodo.setFixedWidth(120)
        self.combo_metodo.setFixedHeight(38)
        self.combo_metodo.setCurrentIndex(0)

        """ide6 debe tener un editor interno real sobre el combo para que
        # el texto visible del método seleccionado pueda quedar centrado.
        line_edit = self.combo_metodo.lineEdit()
        if line_edit is not None:
            line_edit.setReadOnly(True)
            line_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)"""

        # Alinea los elementos dentro del menú desplegable usando itemData
        for i in range(self.combo_metodo.count()):
            self.combo_metodo.setItemData(i, Qt.AlignmentFlag.AlignCenter, Qt.ItemDataRole.TextAlignmentRole)

        self.combo_metodo.setStyleSheet("""
            QComboBox {
                background-color: #FFFFFF;
                border: 1px solid #CBD5E1;
                border-radius: 8px;
                padding: 0px 8px;
                font-size: 13px;
                font-weight: 600;
                color: #475569;
                text-align: center;
            }
            QComboBox:focus {
                border: 1px solid #2563EB;
            }
            QComboBox QAbstractItemView {
                text-align: center;
                selection-background-color: #F1F5F9;
                selection-color: #2563EB;
            }
            QComboBox::drop-down {
                border: none;
                width: 22px;
            }
        """)
        
        action_buttons_layout.addWidget(self.btn_solve)
        action_buttons_layout.addWidget(self.combo_metodo)
        action_buttons_layout.addWidget(btn_clear)
        action_buttons_layout.addStretch()
        
        matrix_layout.addLayout(action_buttons_layout)
        
        self.stepper_eq.on_change_callback = self._rebuild_matrix_grid
        self.stepper_var.on_change_callback = self._rebuild_matrix_grid
        
        self._rebuild_matrix_grid()
        
        # VISTA 2: ECUACIONES
        equations_view = QWidget()
        equations_view.setStyleSheet("background-color: transparent;")
        eq_view_layout = QVBoxLayout(equations_view)
        eq_view_layout.setContentsMargins(0, 0, 0, 0)
        eq_view_layout.setSpacing(10)
        
        lbl_eq = QLabel("SISTEMA DE ECUACIONES")
        lbl_eq.setStyleSheet("color: #64748B; font-size: 10px; font-weight: 700; letter-spacing: 0.5px; background: transparent;")
        
        self.txt_equations = QPlainTextEdit()
        self.txt_equations.setStyleSheet(
            """
            QPlainTextEdit {
                background-color: #F8FAFC;
                border: 1px solid #E2E8F0;
                border-radius: 10px;
                padding: 12px;
                font-size: 13px;
                color: #0F172A;
            }
            QPlainTextEdit:focus {
                border: 1.5px solid #2563EB;
                background-color: #FFFFFF;
            }
        """
        )
        self.txt_equations.setPlaceholderText("2x + 3y - z = 5\nx - y + 2z = 4\n3x + 2y + z = 10")
        self.txt_equations.setFixedHeight(120)
        
        lbl_help = QLabel("Escribe una ecuación por línea. Puedes pegar un sistema completo directamente.")
        lbl_help.setStyleSheet("color: #94A3B8; font-size: 11px; background: transparent;")
        
        btn_analyze = QPushButton("Analizar sistema")
        btn_analyze.setStyleSheet(
            """
            QPushButton {
                background-color: #2563EB;
                color: white;
                font-weight: 600;
                font-size: 13px;
                padding: 10px 22px;
                border-radius: 10px;
                border: none;
            }
            QPushButton:hover { background-color: #1D4ED8; }
            """
        )
        btn_analyze.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_analyze.clicked.connect(self._on_analyze_clicked)
        
        eq_view_layout.addWidget(lbl_eq)
        eq_view_layout.addWidget(self.txt_equations)
        eq_view_layout.addWidget(lbl_help)
        eq_view_layout.addWidget(btn_analyze, alignment=Qt.AlignmentFlag.AlignLeft)
        
        self.stacked_layout.addWidget(matrix_view)
        self.stacked_layout.addWidget(equations_view)
        
        card_layout.addLayout(self.stacked_layout)
        content_layout.addWidget(self.card)
        
        # -----------------------------------------------------------------
        # TARJETA DE RESULTADOS (Oculta por defecto)
        # -----------------------------------------------------------------
        self.results_card = QWidget()
        self.results_layout = QVBoxLayout(self.results_card)
        self.results_layout.setContentsMargins(0, 0, 0, 0)
        self.results_layout.setSpacing(16)

        # Instanciamos las 3 tarjetas desplegables requeridas por tu backend
        self.card_matriz = CollapsibleCard("Matriz del Sistema")
        self.card_proceso = CollapsibleCard("Proceso de Eliminación")
        self.card_solucion = CollapsibleCard("Solución del Sistema")

        self.results_layout.addWidget(self.card_matriz)
        self.results_layout.addWidget(self.card_proceso)
        self.results_layout.addWidget(self.card_solucion)

        self.results_card.hide()
        content_layout.addWidget(self.results_card)

        # Perrito central
        self.dog_main = SleepingDogContainer(small=False)
        content_layout.addWidget(
            self.dog_main, alignment=Qt.AlignmentFlag.AlignCenter
        )

        # Conexión de botones de modo
        self.btn_matrix.clicked.connect(
            lambda: self._set_mode(
                0, mode_button_active_style, mode_button_style
            )
        )
        self.btn_equations.clicked.connect(
            lambda: self._set_mode(
                1, mode_button_active_style, mode_button_style
            )
        )

        # -----------------------------------------------------------------
        # ENSAMBLAJE FINAL DE LA JERARQUÍA (Única ejecución)
        # -----------------------------------------------------------------
        content_outer_layout.addWidget(centered_wrapper)
        scroll_area.setWidget(main_content)
        main_layout.addWidget(scroll_area)
        
    def _set_mode(self, index, active_style, inactive_style):
        self.stacked_layout.setCurrentIndex(index)
        if index == 0:
            self.btn_matrix.setStyleSheet(active_style)
            self.btn_equations.setStyleSheet(inactive_style)
        else:
            self.btn_matrix.setStyleSheet(inactive_style)
            self.btn_equations.setStyleSheet(active_style)
        
    def _rebuild_matrix_grid(self):
        while self.matrix_grid.count():
            item = self.matrix_grid.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
        rows = self.stepper_eq.value
        cols = self.stepper_var.value
        self.inputs_list = []
        
        input_style = """
            QLineEdit {
                background-color: #F8FAFC;
                border: 1px solid #E2E8F0;
                border-radius: 8px;
                color: #0F172A;
                font-size: 13px;
                font-weight: 600;
            }
            QLineEdit:focus {
                border: 1.5px solid #2563EB;
                background-color: #FFFFFF;
            }
        """
        
        # Encabezados de columnas (x1, x2, ..., b)
        for c in range(cols):
            lbl = QLabel(f"x<sub>{c+1}</sub>")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet("color: #64748B; font-size: 11px; font-weight: 600; background: transparent;")
            self.matrix_grid.addWidget(lbl, 0, c + 1)
        
        lbl_b = QLabel("b")
        lbl_b.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_b.setStyleSheet("color: #64748B; font-size: 11px; font-weight: 600; background: transparent;")
        self.matrix_grid.addWidget(lbl_b, 0, cols + 2)
        
        # Filas de la matriz
        for r in range(rows):
            row_inputs = []
        
            lbl_e = QLabel(f"E<sub>{r+1}</sub>")
            lbl_e.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_e.setStyleSheet("color: #64748B; font-size: 11px; font-weight: 600; background: transparent;")
            self.matrix_grid.addWidget(lbl_e, r + 1, 0)
        
            for c in range(cols):
                inp = QLineEdit("0")
                inp.setAlignment(Qt.AlignmentFlag.AlignCenter)
                inp.setFixedSize(54, 36)
                inp.setStyleSheet(input_style)
                self.matrix_grid.addWidget(inp, r + 1, c + 1)
                row_inputs.append(inp)
        
            line = QFrame()
            line.setFrameShape(QFrame.Shape.VLine)
            line.setStyleSheet("background-color: #CBD5E1; max-width: 1.5px;")
            line.setFixedHeight(28)
            self.matrix_grid.addWidget(line, r + 1, cols + 1, Qt.AlignmentFlag.AlignCenter)
        
            inp_b = QLineEdit("0")
            inp_b.setAlignment(Qt.AlignmentFlag.AlignCenter)
            inp_b.setFixedSize(54, 36)
            inp_b.setStyleSheet(input_style)
            self.matrix_grid.addWidget(inp_b, r + 1, cols + 2)
            row_inputs.append(inp_b)
        
            self.inputs_list.append(row_inputs)
        
        for c in range(cols + 3):
            self.matrix_grid.setColumnMinimumWidth(c, 54)
        
        self.matrix_grid.setColumnStretch(cols + 3, 1)
        
        
    def _clear_matrix_inputs(self):
        for row in self.inputs_list:
            for inp in row:
                inp.setText("0")
        self.txt_equations.clear()
        self.results_card.hide()
        
        
        
    def _dibujar_matriz_aumentada(self, matriz):
        """Dibuja la matriz con corchetes vectoriales dinámicos e idénticos a la imagen de referencia."""
        if not hasattr(self, "card_matriz") or not self.card_matriz:
            return
        
        container = QWidget()
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Subtítulo
        filas = len(matriz)
        columnas = len(matriz[0]) - 1 if filas > 0 else 0
        lbl_subtitle = QLabel(
            f"SISTEMA ORIGINAL · {filas} ECUACIONES, {columnas} VARIABLES"
        )
        lbl_subtitle.setStyleSheet(
            "font-size: 11px; font-weight: bold; color: #64748B; letter-spacing: 0.5px;"
        )
        main_layout.addWidget(lbl_subtitle)
        main_layout.addSpacing(12)
        
        # Contenedor horizontal que encerrará los corchetes y la cuadrícula numérica
        matrix_wrapper = QHBoxLayout()
        matrix_wrapper.setSpacing(6)
        
        # 1. Corchete Izquierdo
        bracket_left = BracketWidget(is_left=True)
        
        # 2. Grid interno únicamente para los números y la barra vertical
        grid_numbers = QGridLayout()
        grid_numbers.setSpacing(14)
        grid_numbers.setContentsMargins(4, 0, 4, 0)
        
        for r in range(filas):
            for c in range(columnas):
                val = matriz[r][c]
                lbl_val = QLabel(
                    f"{val:g}" if isinstance(val, (int, float)) else str(val)
                )
                lbl_val.setStyleSheet(
                    "font-size: 15px; color: #0F172A; font-family: sans-serif;"
                )
                lbl_val.setAlignment(Qt.AlignmentFlag.AlignCenter)
                grid_numbers.addWidget(lbl_val, r, c)
        
            # Línea divisoria vertical (|)
            line = QFrame()
            line.setFrameShape(QFrame.Shape.VLine)
            line.setStyleSheet(
                "background-color: #E2E8F0; max-width: 1px; border: none;"
            )
            grid_numbers.addWidget(line, r, columnas)
        
            # Vector b
            val_b = matriz[r][-1]
            lbl_b = QLabel(
                f"{val_b:g}" if isinstance(val_b, (int, float)) else str(val_b)
            )
            lbl_b.setStyleSheet(
                "font-size: 15px; font-weight: bold; color: #0F172A; font-family: sans-serif;"
            )
            lbl_b.setAlignment(Qt.AlignmentFlag.AlignCenter)
            grid_numbers.addWidget(lbl_b, r, columnas + 1)
        
        # 3. Corchete Derecho
        bracket_right = BracketWidget(is_left=False)
        
        # Armar la matriz
        matrix_wrapper.addWidget(bracket_left)
        matrix_wrapper.addLayout(grid_numbers)
        matrix_wrapper.addWidget(bracket_right)
        matrix_wrapper.addStretch()
        
        main_layout.addLayout(matrix_wrapper)
        
        self.card_matriz.add_widget(container)
    def renderizar_proceso_eliminacion(self, resultado_dict, metodo="gauss_jordan"):
        """
        Construye el proceso paso a paso manteniendo el mismo espaciado compacto
        en todos los pasos (incluyendo la Forma Escalonada Final).
        """
        if not hasattr(self, "card_proceso") or not self.card_proceso:
            return
        
        # 1. Limpiar layout interno previo
        if hasattr(self.card_proceso, "content_layout"):
            while self.card_proceso.content_layout.count():
                item = self.card_proceso.content_layout.takeAt(0)
                w = item.widget()
                if w:
                    w.deleteLater()
        
        # 2. Selección de pasos según el método seleccionado en los botones
        if metodo == "gauss":
            pasos = resultado_dict.get("pasos_gauss", [])
        else: # "gauss_jordan" o por defecto
            pasos = resultado_dict.get("todos_los_pasos", resultado_dict.get("pasos_gauss", []) + resultado_dict.get("pasos_jordan", []))
        
        if not pasos:
            lbl_vacio = QLabel("No hay pasos de eliminación para mostrar.")
            lbl_vacio.setStyleSheet("color: #64748B; font-style: italic; padding: 12px; border: none;")
            self.card_proceso.add_widget(lbl_vacio)
            return
        
        # 3. Contenedor principal
        container_pasos = QWidget()
        layout_pasos = QVBoxLayout(container_pasos)
        layout_pasos.setContentsMargins(0, 10, 0, 10)
        layout_pasos.setSpacing(16)
        
        total_pasos = len(pasos)
        
        for idx, paso in enumerate(pasos, start=1):
            card_step = QFrame()
            card_step.setObjectName("CardStep")
            card_step.setStyleSheet("""
                QFrame#CardStep {
                    background-color: #FFFFFF;
                    border: 1px solid #E2E8F0;
                    border-radius: 12px;
                }
            """)
            step_layout = QVBoxLayout(card_step)
            step_layout.setContentsMargins(16, 16, 16, 16)
            step_layout.setSpacing(12)
        
            es_ultimo_paso = (idx == total_pasos)
        
            # --- ENCABEZADO (CÍRCULO + COLUMNA DE TEXTOS ALINEADA) ---
            header_step = QHBoxLayout()
            header_step.setContentsMargins(0, 0, 0, 0)
            header_step.setSpacing(12)  # Distancia exacta entre el círculo y los textos
        
            # Círculo del número de paso (Con ObjectName para proteger sus propiedades)
            lbl_num = QLabel(str(idx))
            lbl_num.setObjectName("CirculoPaso")
            lbl_num.setFixedSize(28, 28)
            lbl_num.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_num.setStyleSheet("""
                QLabel#CirculoPaso {
                    background-color: #EEF2FF;
                    color: #4F46E5;
                    font-weight: 700;
                    font-size: 13px;
                    border-radius: 14px;
                    border: none;
                }
            """)
        
            # Columna común para Título y Badge (Asegura alineación a la izquierda idéntica)
            vbox_textos = QVBoxLayout()
            vbox_textos.setContentsMargins(0, 0, 0, 0)
            vbox_textos.setSpacing(6)
        
            # 1. Título superior del paso
            if es_ultimo_paso:
                texto_sub = "FORMA ESCALONADA REDUCIDA FINAL" if metodo == "gauss_jordan" else "FORMA ESCALONADA FINAL"
                lbl_sub = QLabel(texto_sub)
                lbl_sub.setStyleSheet("color: #4F46E5; font-size: 10px; font-weight: 700; letter-spacing: 0.5px; border: none; background: transparent;")
            else:
                lbl_sub = QLabel("OPERACIÓN ELEMENTAL POR FILAS")
                lbl_sub.setStyleSheet("color: #64748B; font-size: 10px; font-weight: 700; letter-spacing: 0.5px; border: none; background: transparent;")
        
            vbox_textos.addWidget(lbl_sub)
        
            # 2. Badge con la operación elemental (Solo si no es el paso final)
            if not es_ultimo_paso:
                operacion_txt = str(paso.get("operacion") or paso.get("descripcion") or f"Paso {idx}")
                
                hbox_badge = QHBoxLayout()
                hbox_badge.setContentsMargins(0, 0, 0, 0) # Margen 0 para alinear con lbl_sub
                
                lbl_op = QLabel(operacion_txt)
                lbl_op.setStyleSheet("""
                    QLabel {
                        background-color: #F8FAFC;
                        color: #0F172A;
                        font-family: 'JetBrains Mono', 'Consolas', monospace;
                        font-weight: 600;
                        font-size: 13px;
                        padding: 6px 12px;
                        border-radius: 8px;
                        border: 1px solid #F1F5F9;
                    }
                """)
                
                hbox_badge.addWidget(lbl_op)
                hbox_badge.addStretch()
                vbox_textos.addLayout(hbox_badge)
        
            header_step.addWidget(lbl_num, alignment=Qt.AlignmentFlag.AlignTop)
            header_step.addLayout(vbox_textos)
            header_step.addStretch()
            step_layout.addLayout(header_step)
        
            # --- DIBUJO DE LA MATRIZ (LIMPIA Y COMPACTA) ---
            matriz_paso = paso.get("matriz")
            if matriz_paso and len(matriz_paso) > 0:
                num_eqs = len(matriz_paso)
                num_vars = len(matriz_paso[0]) - 1
                matriz_widget = QWidget()
                matriz_widget.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        
                matriz_wrapper = QHBoxLayout(matriz_widget)
                matriz_wrapper.setContentsMargins(0, 0, 0, 0)
                matriz_wrapper.setSpacing(4)
        
                if 'BracketWidget' in globals() or hasattr(self, 'BracketWidget'):
                    matriz_wrapper.addWidget(BracketWidget(is_left=True))
        
                grid_numbers = QGridLayout()
                grid_numbers.setVerticalSpacing(4)
                grid_numbers.setHorizontalSpacing(18)
                grid_numbers.setContentsMargins(0, 0, 0, 0)
        
                ALTURA_CELDA = 24
                    
                for r in range(num_eqs):
                    # Coeficientes
                    for c in range(num_vars):
                        val_raw = matriz_paso[r][c]
                        val_str = formatear_numero(val_raw) if isinstance(val_raw, (int, float)) else str(val_raw)
                            
                        lbl_cell = QLabel(val_str)
                        lbl_cell.setFixedHeight(ALTURA_CELDA)
                        lbl_cell.setStyleSheet("""
                            QLabel {
                                font-size: 14px;
                                font-weight: 500;
                                color: #0F172A;
                                border: none;
                                background: transparent;
                                padding: 0px;
                                margin: 0px;
                            }
                        """)
                        lbl_cell.setAlignment(Qt.AlignmentFlag.AlignCenter)
                        grid_numbers.addWidget(lbl_cell, r, c)
        
                    # Término independiente (B)
                    val_b_raw = matriz_paso[r][-1]
                    val_b_str = formatear_numero(val_b_raw) if isinstance(val_b_raw, (int, float)) else str(val_b_raw)
                        
                    lbl_b = QLabel(val_b_str)
                    lbl_b.setFixedHeight(ALTURA_CELDA)
                    lbl_b.setStyleSheet("""
                        QLabel {
                            font-size: 14px;
                            font-weight: 700;
                            color: #0F172A;
                            border: none;
                            background: transparent;
                            padding: 0px;
                            margin: 0px;
                        }
                    """)
                    lbl_b.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    grid_numbers.addWidget(lbl_b, r, num_vars + 1)
        
                # Línea divisoria UNIFICADA
                line = QFrame()
                line.setFrameShape(QFrame.Shape.VLine)
                line.setStyleSheet("background-color: #E2E8F0; max-width: 1px; border: none;")
                grid_numbers.addWidget(line, 0, num_vars, num_eqs, 1)
        
                matriz_wrapper.addLayout(grid_numbers)
        
                if 'BracketWidget' in globals() or hasattr(self, 'BracketWidget'):
                    matriz_wrapper.addWidget(BracketWidget(is_left=False))
        
                # Indentado a 40px (28px del círculo + 12px de spacing) para alinear exacto
                container_matriz_align = QHBoxLayout()
                container_matriz_align.setContentsMargins(40, 0, 0, 0)
                container_matriz_align.addWidget(matriz_widget)
                container_matriz_align.addStretch()
        
                step_layout.addLayout(container_matriz_align)
              
            layout_pasos.addWidget(card_step)
        
        # 4. Insertar en la tarjeta desplegable y expandir
        self.card_proceso.add_widget(container_pasos)
        self.card_proceso.is_expanded = True
        self.card_proceso.content_widget.setVisible(True)
        self.card_proceso.btn_toggle.setText("−")
    def renderizar_tarjeta_solucion(self, resultado):
        """Pobla la tarjeta desplegable 'Solución' arreglando bordes heredados y proporciones de tarjetas."""
        if not hasattr(self, "card_solucion") or not self.card_solucion:
            return
        
        # Obtener el contenedor interno
        contenedor = self.card_solucion.content_widget
        layout_principal = contenedor.layout()
        if not layout_principal:
            layout_principal = QVBoxLayout(contenedor)
            contenedor.setLayout(layout_principal)
        
        # Limpiar contenido previo
        while layout_principal.count():
            item = layout_principal.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
        layout_principal.setSpacing(16)
        
        # Helper para subíndices unicode verdaderos (x₁, x₂, x₃...)
        sub = lambda i: "".join(["₀", "₁", "₂", "₃", "₄", "₅", "₆", "₇", "₈", "₉"][int(d)] for d in str(i + 1))
        
        # Datos backend
        tipo_sistema = resultado.get("tipo_sistema", "inconsistente")
        vars_basicas = resultado.get("variables_basicas", [])
        vars_libres = resultado.get("variables_libres", [])
        soluciones_valores = resultado.get("soluciones_valores", [])
        verificaciones = resultado.get("verificacion", [])
        matriz_orig = resultado.get("matriz_inicial", [])
        
        # =========================================================================
        # 1. SECCIÓN: VARIABLES BÁSICAS Y LIBRES
        # =========================================================================
        layout_vars = QHBoxLayout()
        
        # --- Columna Variables Básicas ---
        vbox_basicas = QVBoxLayout()
        vbox_basicas.setSpacing(8)
        lbl_basicas_title = QLabel("VARIABLES BÁSICAS")
        lbl_basicas_title.setStyleSheet("color: #64748B; font-weight: 700; font-size: 11px; letter-spacing: 0.5px; border: none;")
        vbox_basicas.addWidget(lbl_basicas_title)
        
        hbox_chips = QHBoxLayout()
        hbox_chips.setSpacing(6)
        if vars_basicas:
            for idx in vars_basicas:
                chip = QLabel(f"x{sub(idx)}")
                chip.setStyleSheet("""
                    background-color: #EFF6FF;
                    color: #2563EB;
                    border: 1px solid #BFDBFE;
                    border-radius: 8px;
                    padding: 4px 12px;
                    font-weight: 700;
                    font-size: 13px;
                """)
                hbox_chips.addWidget(chip)
            hbox_chips.addStretch()
        else:
            lbl_none = QLabel("Ninguna")
            lbl_none.setStyleSheet("color: #64748B; font-style: italic; font-size: 13px; border: none;")
            hbox_chips.addWidget(lbl_none)
            hbox_chips.addStretch()
        
        vbox_basicas.addLayout(hbox_chips)
        
        # --- Columna Variables Libres ---
        vbox_libres = QVBoxLayout()
        vbox_libres.setSpacing(8)
        lbl_libres_title = QLabel("VARIABLES LIBRES")
        lbl_libres_title.setStyleSheet("color: #64748B; font-weight: 700; font-size: 11px; letter-spacing: 0.5px; border: none;")
        vbox_libres.addWidget(lbl_libres_title)
        
        if vars_libres:
            hbox_chips_l = QHBoxLayout()
            hbox_chips_l.setSpacing(6)
            for idx in vars_libres:
                chip = QLabel(f"x{sub(idx)}")
                chip.setStyleSheet("""
                    background-color: #F1F5F9;
                    color: #475569;
                    border: 1px solid #CBD5E1;
                    border-radius: 8px;
                    padding: 4px 12px;
                    font-weight: 700;
                    font-size: 13px;
                """)
                hbox_chips_l.addWidget(chip)
            hbox_chips_l.addStretch()
            vbox_libres.addLayout(hbox_chips_l)
        else:
            lbl_none_l = QLabel("Ninguna")
            lbl_none_l.setStyleSheet("color: #64748B; font-style: italic; font-size: 13px; border: none;")
            vbox_libres.addWidget(lbl_none_l)
        
        layout_vars.addLayout(vbox_basicas, stretch=1)
        layout_vars.addLayout(vbox_libres, stretch=1)
        layout_principal.addLayout(layout_vars)
        
        # =========================================================================
        # 2. SECCIÓN: VALORES DE LAS VARIABLES (Estilo rectangular de Imagen 2)
        # =========================================================================
        if tipo_sistema == "determinado" and soluciones_valores:
            vbox_valores = QVBoxLayout()
            vbox_valores.setSpacing(8)
            
            lbl_valores_title = QLabel("VALORES")
            lbl_valores_title.setStyleSheet("color: #64748B; font-weight: 700; font-size: 11px; letter-spacing: 0.5px; border: none;")
            vbox_valores.addWidget(lbl_valores_title)
        
            hbox_cards_valores = QHBoxLayout()
            hbox_cards_valores.setSpacing(16)
        
            for i, val in enumerate(soluciones_valores):
                card_val = QFrame()
                # Nombre de objeto para evitar que los estilos CSS afecten a los QLabel hijos
                card_val.setObjectName("CardValor")
                card_val.setFixedSize(150,70)
                card_val.setStyleSheet("""
                    QFrame#CardValor {
                        background-color: #FFFFFF;
                        border: 1px solid #E2E8F0;
                        border-radius: 12px;
                    }
                """)
                
                v_val_layout = QVBoxLayout(card_val)
                v_val_layout.setContentsMargins(12, 10, 12, 10)
                v_val_layout.setSpacing(2)
                v_val_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
                # Etiqueta de la variable (x₁, x₂, x₃)
                lbl_x = QLabel(f"x{sub(i)}")
                lbl_x.setStyleSheet("color: #64748B; font-weight: 600; font-size: 13px; border: none; background: transparent;")
                lbl_x.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
                # Valor formateado
                val_str = formatear_numero(val)
                lbl_num = QLabel(val_str)
                lbl_num.setStyleSheet("color: #0F172A; font-weight: 800; font-size: 28px; border: none; background: transparent;")
                lbl_num.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
                v_val_layout.addWidget(lbl_x)
                v_val_layout.addWidget(lbl_num)
                
                hbox_cards_valores.addWidget(card_val)
        
            hbox_cards_valores.addStretch()  # Evita que las tarjetas se estiren a los lados
            vbox_valores.addLayout(hbox_cards_valores)
            layout_principal.addLayout(vbox_valores)
            # =========================================================================
        # 3. SECCIÓN: VERIFICACIÓN (Muestra sustitución completa en una línea)
        # =========================================================================
        if tipo_sistema == "determinado" and verificaciones:
            vbox_verif = QVBoxLayout()
            vbox_verif.setSpacing(8)
        
            lbl_verif_title = QLabel("VERIFICACIÓN")
            lbl_verif_title.setStyleSheet("color: #64748B; font-weight: 700; font-size: 11px; letter-spacing: 0.5px; border: none;")
            vbox_verif.addWidget(lbl_verif_title)
        
            frame_verif = QFrame()
            frame_verif.setObjectName("FrameVerif")
            frame_verif.setStyleSheet("""
                QFrame#FrameVerif {
                    background-color: #FFFFFF;
                    border: 1px solid #E2E8F0;
                    border-radius: 12px;
                }
            """)
            
            v_frame_layout = QVBoxLayout(frame_verif)
            v_frame_layout.setContentsMargins(16, 8, 16, 8)
            v_frame_layout.setSpacing(0)
        
            for idx, item in enumerate(verificaciones):
                row_frame = QFrame()
                row_frame.setStyleSheet("border: none; background: transparent;")
                row_layout = QHBoxLayout(row_frame)
                row_layout.setContentsMargins(0, 10, 0, 10)
        
                # Nombre de la ecuación
                eq_num = item.get("ecuacion_num", idx + 1)
                lbl_eq_name = QLabel(f"Ecuación {eq_num}")
                lbl_eq_name.setStyleSheet("color: #0F172A; font-weight: 600; font-size: 13px; border: none;")
        
                # Extracción de campos generados por tu backend en verificacion.py
                str_sust = item.get("sustitucion", "")
                str_ops = item.get("operaciones", "")
                str_res = item.get("resultado", "")
        
                # Construcción paso a paso en una sola línea: Sustitución ➔ Operaciones ➔ Resultado
                # Ejemplo: (1)(1) + (2)(2) - (1)(3) = 2  ➔  1 + 4 - 3 = 2  ➔  2 = 2
                texto_linea = f"{str_sust}   ➔   {str_ops}   ➔   {str_res}"
                
                lbl_eq_val = QLabel(texto_linea)
                lbl_eq_val.setStyleSheet("color: #475569; font-size: 12px; font-family: monospace; border: none;")
        
                # Estado
                es_correcto = item.get("valido", True)
                badge = QLabel("✓ Correcto" if es_correcto else "✕ Incorrecto")
                badge.setStyleSheet(f"""
                    background-color: {"#ECFDF5" if es_correcto else "#FEF2F2"};
                    color: {"#059669" if es_correcto else "#DC2626"};
                    border-radius: 10px;
                    padding: 4px 12px;
                    font-weight: 700;
                    font-size: 11px;
                    border: none;
                """)
        
                row_layout.addWidget(lbl_eq_name)
                row_layout.addStretch()
                row_layout.addWidget(lbl_eq_val)
                row_layout.addSpacing(15)
                row_layout.addWidget(badge)
        
                v_frame_layout.addWidget(row_frame)
        
                if idx < len(verificaciones) - 1:
                    sep = QFrame()
                    sep.setFrameShape(QFrame.Shape.HLine)
                    sep.setStyleSheet("background-color: #F1F5F9; max-height: 1px; border: none;")
                    v_frame_layout.addWidget(sep)
        
            vbox_verif.addWidget(frame_verif)
            layout_principal.addLayout(vbox_verif)
        # Forzar despliegue
        self.card_solucion.is_expanded = True
        self.card_solucion.content_widget.setVisible(True)
        self.card_solucion.btn_toggle.setText("−")
    def _on_solve_clicked(self):
        """Lee la matriz desde los QLineEdit y la procesa con el Controlador."""
        try:
            matriz = []
            for row in self.inputs_list:
                fila_vals = []
                for inp in row:
                    texto = inp.text().strip().replace(",", ".")
                    val = float(texto) if texto else 0.0
                    fila_vals.append(val)
                matriz.append(fila_vals)
            # 1. Obtenemos el método seleccionado por el usuario en la interfaz
            metodo_texto = self.combo_metodo.currentText()
            metodo = "gauss" if metodo_texto == "Gauss" else "gauss_jordan"
            resultado = ControladorMatriz.resolver_sistema(matriz)
            self._mostrar_resultados(resultado, matriz_entrada=matriz,metodo=metodo)
        
        except ValueError:
            QMessageBox.warning(self, "Error de entrada", "Por favor ingresa únicamente valores numéricos válidos.")
        
    def _on_analyze_clicked(self):
        """Procesa el texto ingresado en el modo ecuaciones."""
        texto = self.txt_equations.toPlainText().strip()
        if not texto:
            QMessageBox.warning(self, "Campo vacío", "Por favor ingresa las ecuaciones a analizar.")
            return
        
        if leer_sistema_desde_texto:
            try:
                matriz, eq, var = leer_sistema_desde_texto(texto)
                resultado = ControladorMatriz.resolver_sistema(matriz)
                self._mostrar_resultados(resultado)
            except Exception as e:
                QMessageBox.critical(self, "Error al analizar", f"Ocurrió un error al procesar el sistema: {str(e)}")
        else:
            QMessageBox.information(self, "Modo Ecuaciones", "El módulo de lectura por texto está en integración.")
        
        
    def _mostrar_resultados(
        self, resultado, matriz_entrada=None, metodo="gauss_jordan"
            ):
        """Construye la vista estructurada con Banner, Info del Sistema y Tarjetas Desplegables."""
        # 1. Ocultar la tarjeta de captura principal y la mascota/imagen
        self.card.hide()
        if hasattr(self, "dog_main"):
            self.dog_main.hide()
        
        # 2. Resetear referencias y vaciar el contenedor previo
        self.card_matriz = None
        self.card_proceso = None
        self.card_solucion = None
        
        while self.results_layout.count():
            item = self.results_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
        # 3. Mostrar el contenedor maestro de resultados
        self.results_card.show()
        
        # --- BOTÓN REGRESAR / NUEVO SISTEMA ---
        btn_back = QPushButton("← Nuevo sistema")
        btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_back.setStyleSheet(
            "QPushButton { color: #64748B; font-weight: 600; font-size: 13px; border: none; "
            "background: transparent; text-align: left; padding: 0px; } "
            "QPushButton:hover { color: #0F172A; }"
        )
        btn_back.clicked.connect(self._volver_a_matriz)
        self.results_layout.addWidget(btn_back)
        
        # --- EXTRACCIÓN DINÁMICA DE DATOS DEL RESULTADO ---
        # Mantiene la función lambda para generar subíndices (ej: 0 -> x₁)
        sub = lambda i: "".join(
            ["₀", "₁", "₂", "₃", "₄", "₅", "₆", "₇", "₈", "₉"][int(d)]
            for d in str(i + 1)
        )
        
        if isinstance(resultado, dict):
            rango_a = resultado.get("rango_coeficientes", "-")
            rango_ab = resultado.get("rango_ampliada", "-")
            num_vars = resultado.get("num_variables", "-")
            num_eqs = resultado.get("num_ecuaciones", "-")
            tipo_sistema = resultado.get("tipo_sistema", "inconsistente")
        
            # MANTENEMOS LOS SUBÍNDICES EN PIVOTES Y VARIABLES
            piv_list = resultado.get("columnas_pivote", [])
            pivotes = (
                ", ".join(f"x{sub(p)}" for p in piv_list)
                if piv_list
                else "Ninguna"
            )
        
            v_basicas = resultado.get("variables_basicas", [])
            vars_basicas = (
                ", ".join(f"x{sub(v)}" for v in v_basicas)
                if v_basicas
                else "Ninguna"
            )
        
            v_libres = resultado.get("variables_libres", [])
            vars_libres = (
                ", ".join(f"x{sub(v)}" for v in v_libres)
                if v_libres
                else "Ninguna"
            )
        else:
            rango_a, rango_ab, num_vars, num_eqs = 3, 3, 3, 3
            pivotes = "x₁, x₂, x₃"
            vars_basicas = "x₁, x₂, x₃"
            vars_libres = "Ninguna"
            tipo_sistema = "determinado"
        
        # --- BANNER DE ESTADO ---
        banner = QFrame()
        banner.setObjectName("BannerEstado")
        
        if tipo_sistema == "determinado":
            banner.setStyleSheet("""
                QFrame#BannerEstado {
                    background-color: #ECFDF5;
                    border: 1px solid #A7F3D0;
                    border-radius: 12px;
                    padding: 6px 16px;
                }
            """)
            color_icono = "#059669"
            titulo_estado = "Sistema consistente determinado"
            sub_estado = "Solución única"
            texto_icono = "✓"
            texto_resumen_sol = "solución única"
        elif tipo_sistema == "indeterminado":
            banner.setStyleSheet("""
                QFrame#BannerEstado {
                    background-color: #EFF6FF;
                    border: 1px solid #BFDBFE;
                    border-radius: 12px;
                    padding: 6px 16px;
                }
            """)
            color_icono = "#2563EB"
            titulo_estado = "Sistema consistente indeterminado"
            sub_estado = "Infinitas soluciones"
            texto_icono = "∞"
            texto_resumen_sol = "infinitas soluciones"
        else:  # inconsistente
            banner.setStyleSheet("""
                QFrame#BannerEstado {
                    background-color: #FEF2F2;
                    border: 1px solid #FECACA;
                    border-radius: 12px;
                    padding: 6px 16px;
                }
            """)
            color_icono = "#DC2626"
            titulo_estado = "Sistema inconsistente"
            sub_estado = "Sin solución"
            texto_icono = "✕"
            texto_resumen_sol = "sin solución"
        
        b_layout = QHBoxLayout(banner)
        b_layout.setContentsMargins(0, 4, 0, 4)
        b_layout.setSpacing(12)
        
        lbl_icon = QLabel(texto_icono)
        lbl_icon.setStyleSheet(
            f"color: {color_icono}; font-size: 18px; font-weight: bold; border:"
            " none; background: transparent;"
        )
        b_layout.addWidget(lbl_icon)
        
        text_vbox = QVBoxLayout()
        text_vbox.setSpacing(1)
        text_vbox.setContentsMargins(0, 0, 0, 0)
        
        lbl_status_title = QLabel(titulo_estado)
        lbl_status_title.setStyleSheet(
            f"color: {color_icono}; font-size: 13px; font-weight: 700; border:"
            " none; background: transparent;"
        )
        
        lbl_status_sub = QLabel(sub_estado)
        lbl_status_sub.setStyleSheet(
            f"color: {color_icono}; font-size: 11px; border: none; background:"
            " transparent;"
        )
        
        text_vbox.addWidget(lbl_status_title)
        text_vbox.addWidget(lbl_status_sub)
        
        b_layout.addLayout(text_vbox)
        b_layout.addStretch()
        
        self.results_layout.addWidget(banner)
        
        # --- TARJETA: INFORMACIÓN DEL SISTEMA (DISEÑO LIMPIO TIPO IMAGEN 2 CON SUBÍNDICES) ---
        card_info = QFrame()
        card_info.setStyleSheet(
            "QFrame { background-color: #FFFFFF; border: 1px solid #E2E8F0;"
            " border-radius: 12px; }"
        )
        ci_layout = QVBoxLayout(card_info)
        ci_layout.setContentsMargins(24, 20, 24, 20)
        ci_layout.setSpacing(16)
        
        # 1. Encabezado con barrita azul
        header_info = QHBoxLayout()
        header_info.setContentsMargins(0, 0, 0, 0)
        header_info.setSpacing(8)
        
        bullet = QFrame()
        bullet.setFixedSize(4, 16)
        bullet.setStyleSheet("background-color: #2563EB; border-radius: 2px;")
        
        lbl_info_title = QLabel("Información del sistema")
        lbl_info_title.setStyleSheet(
            "font-size: 15px; font-weight: 700; color: #0F172A; border: none;"
            " background: transparent;"
        )
        
        header_info.addWidget(bullet, 0, Qt.AlignmentFlag.AlignVCenter)
        header_info.addWidget(lbl_info_title, 0, Qt.AlignmentFlag.AlignVCenter)
        header_info.addStretch()
        ci_layout.addLayout(header_info)
        
        # 2. Rejilla de datos sin tarjetas individuales
        grid_widget = QWidget()
        grid_widget.setStyleSheet("border: none; background: transparent;")
        grid_info = QGridLayout(grid_widget)
        grid_info.setContentsMargins(0, 4, 0, 4)
        grid_info.setHorizontalSpacing(12)
        grid_info.setVerticalSpacing(12)
        
        items_datos = [
            ("Rango (A)", str(rango_a), "Columnas pivote", pivotes),
            ("Rango (A|b)", str(rango_ab), "Variables básicas", vars_basicas),
            ("Número de variables", str(num_vars), "Variables libres", vars_libres),
            ("Número de ecuaciones", str(num_eqs), "", ""),
        ]
        
        for row, (lbl_left, val_left, lbl_right, val_right) in enumerate(
            items_datos
        ):
            # Izquierda
            lbl_l = QLabel(lbl_left)
            lbl_l.setStyleSheet(
                "color: #64748B; font-size: 13px; border: none; background:"
                " transparent;"
            )
            grid_info.addWidget(lbl_l, row, 0)
        
            val_l = QLabel(val_left)
            val_l.setStyleSheet(
                "color: #0F172A; font-size: 13px; font-weight: 700; border:"
                " none; background: transparent;"
            )
            val_l.setAlignment(
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            )
            grid_info.addWidget(val_l, row, 1)
        
            # Derecha
            if lbl_right:
                lbl_r = QLabel(lbl_right)
                lbl_r.setStyleSheet(
                    "color: #64748B; font-size: 13px; border: none; background:"
                    " transparent;"
                )
                grid_info.addWidget(lbl_r, row, 3)
        
            if val_right:
                val_r = QLabel(val_right)
                val_r.setStyleSheet(
                    "color: #0F172A; font-size: 13px; font-weight: 700; border:"
                    " none; background: transparent;"
                )
                val_r.setAlignment(
                    Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
                )
                grid_info.addWidget(val_r, row, 4)
        
        # Ajuste de espacio horizontal entre columnas
        grid_info.setColumnStretch(0, 3)
        grid_info.setColumnStretch(1, 1)
        grid_info.setColumnStretch(2, 2)
        grid_info.setColumnStretch(3, 3)
        grid_info.setColumnStretch(4, 2)
        
        ci_layout.addWidget(grid_widget)
        
        # 3. Línea divisoria
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet(
            "background-color: #E2E8F0; max-height: 1px; border: none;"
        )
        ci_layout.addWidget(line)
        
        # 4. Texto dinámico inferior
        lbl_formula = QLabel(
            f"rango(A) = {rango_a} | rango(A|b) = {rango_ab} | n = {num_vars}"
            f"  →  {texto_resumen_sol}"
        )
        lbl_formula.setStyleSheet(
            "color: #475569; font-family: 'Consolas', 'Courier New', monospace;"
            " font-size: 13px; border: none; background: transparent;"
        )
        lbl_formula.setContentsMargins(0, 2, 0, 0)
        ci_layout.addWidget(lbl_formula)
        
        self.results_layout.addWidget(card_info)
        
        # --- TARJETAS DESPLEGABLES ---
        self.card_matriz = CollapsibleCard("Matriz aumentada")
        self.card_proceso = CollapsibleCard("Proceso de eliminación")
        self.card_solucion = CollapsibleCard("Solución")
        
        self.results_layout.addWidget(self.card_matriz)
        self.results_layout.addWidget(self.card_proceso)
        self.results_layout.addWidget(self.card_solucion)
        
        # --- DIBUJAR MATRIZ INICIAL ---
        matriz_a_dibujar = (
            resultado.get("matriz_inicial", matriz_entrada)
            if isinstance(resultado, dict)
            else matriz_entrada
        )
        if matriz_a_dibujar:
            self._dibujar_matriz_aumentada(matriz_a_dibujar)
        
        # --- RENDERIZAR PASOS Y ABRIR TARJETA AUTOMÁTICAMENTE ---
        if isinstance(resultado, dict):
            self.renderizar_proceso_eliminacion(resultado, metodo=metodo)
            self.renderizar_tarjeta_solucion(resultado)
        
        # Forzar despliegue de las tarjetas requeridas
        self.card_proceso.is_expanded = True
        self.card_proceso.content_widget.setVisible(True)
        self.card_proceso.btn_toggle.setText("−")
        
        self.card_matriz.is_expanded = True
        self.card_matriz.content_widget.setVisible(True)
        self.card_matriz.btn_toggle.setText("−")
