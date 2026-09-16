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
from controlador_vectores import ControladorVectores
from vistas.componentes import BracketWidget, NumberStepper, CollapsibleCard
# Importación desde tu nuevo archivo separado

try:
    from entrada import leer_sistema_desde_texto
except ImportError:
    leer_sistema_desde_texto = None


class VistaVectores(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.inputs_list = []
        self.b_inputs_list = []
        self._build_ui()

    def _volver_a_matriz(self):
        self.results_card.hide()
        self.card.show()
        if hasattr(self, "dog_main"):
            self.dog_main.show()
                
    def _build_ui(self):
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

        title = QLabel("Operaciones con Vectores")
        title.setStyleSheet("font-size: 24px; font-weight: 800; color: #0F172A;")

        subtitle = QLabel("Define tus vectores componentes y realiza operaciones algebraicas.")
        subtitle.setStyleSheet("font-size: 13px; color: #64748B; font-weight: 500;")

        header_box.addWidget(title)
        header_box.addWidget(subtitle)
        content_layout.addLayout(header_box)

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
        
        self.btn_matrix = QPushButton("Construir vectores")
        self.btn_equations = QPushButton("Ingresar ecuaciones")
        self.btn_matrix_ops = QPushButton("Operaciones matriciales")
        self.btn_mat_eqs = QPushButton("Ecuaciones matriciales")
        
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
        self.btn_matrix_ops.setStyleSheet(mode_button_style)
        self.btn_mat_eqs.setStyleSheet(mode_button_style)
        self.btn_matrix.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_equations.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_matrix_ops.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_mat_eqs.setCursor(Qt.CursorShape.PointingHandCursor)

        mode_layout.addWidget(self.btn_matrix)
        mode_layout.addWidget(self.btn_equations)
        mode_layout.addWidget(self.btn_matrix_ops)
        mode_layout.addWidget(self.btn_mat_eqs)
        
        mode_wrapper.addWidget(mode_container, alignment=Qt.AlignmentFlag.AlignLeft)
        card_layout.addLayout(mode_wrapper)
        
        self.stacked_layout = QStackedLayout()
        
        # VISTA 1: VECTORES
        matrix_view = QWidget()
        matrix_view.setObjectName("VistaMatriz")
        matrix_view.setAccessibleName("VistaMatriz")
        matrix_view.setStyleSheet("background-color: transparent;")
        self.vista_matriz = matrix_view
        matrix_layout = QVBoxLayout(matrix_view)
        matrix_layout.setContentsMargins(0, 0, 0, 0)
        matrix_layout.setSpacing(20)
        
        # Controles superiores
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
        
        # Control: Cantidad de Vectores
        vec_box = QVBoxLayout()
        vec_box.setSpacing(6)
        vec_label = QLabel("CANTIDAD DE VECTORES")
        vec_label.setStyleSheet("color: #64748B; font-size: 10px; font-weight: 700; letter-spacing: 0.5px; background: transparent;")
        self.stepper_vec = NumberStepper(value=3)
        vec_box.addWidget(vec_label)
        vec_box.addWidget(self.stepper_vec)
        
        controls_layout.addLayout(eq_box)
        controls_layout.addLayout(var_box)
        controls_layout.addLayout(vec_box)
        controls_layout.addStretch()
        matrix_layout.addLayout(controls_layout)
        
     
        # ============================================================
        # ÁREA DINÁMICA DE VECTORES
        # ============================================================

        self.vectors_scroll = QScrollArea()

        self.vectors_scroll.setWidgetResizable(True)
        self.vectors_scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.vectors_scroll.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        self.vectors_scroll.setFrameShape(
            QFrame.Shape.NoFrame
        )

        self.vectors_scroll.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }

            QScrollBar:horizontal {
                height: 8px;
                background: #F1F5F9;
                border-radius: 4px;
            }

            QScrollBar::handle:horizontal {
                background: #CBD5E1;
                border-radius: 4px;
                min-width: 40px;
            }

            QScrollBar::add-line:horizontal,
            QScrollBar::sub-line:horizontal {
                width: 0px;
                background: none;
                border: none;
            }
        """)

        # Widget que contendrá todos los vectores
        self.vectors_container = QWidget()
        self.vectors_container.setSizePolicy(
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.Preferred
        )

        self.vectors_container.setStyleSheet(
            "background-color: transparent;"
        )

        self.vectors_layout = QHBoxLayout(
            self.vectors_container
        )

        self.vectors_layout.setContentsMargins(
            0, 0, 0, 0
        )

        self.vectors_layout.setSpacing(16)

        self.vectors_layout.setAlignment(
            Qt.AlignmentFlag.AlignLeft
        )

        # El scroll mostrará el contenedor completo
        self.vectors_scroll.setWidget(
            self.vectors_container
        )

        # Sección para el valor del Escalar k
        self.escalar_container = QWidget()
        self.escalar_container.setStyleSheet("background-color: transparent;")
        escalar_layout = QVBoxLayout(self.escalar_container)
        escalar_layout.setContentsMargins(0, 0, 0, 0)
        escalar_layout.setSpacing(6)
        
        lbl_k = QLabel("ESCALAR (k)")
        lbl_k.setStyleSheet("color: #64748B; font-size: 10px; font-weight: 700; letter-spacing: 0.5px; background: transparent;")
        self.inp_escalar = QLineEdit("1")
        self.inp_escalar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.inp_escalar.setFixedSize(60, 36)
        self.inp_escalar.setStyleSheet(
            """
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
        )
        escalar_layout.addWidget(lbl_k)
        escalar_layout.addWidget(self.inp_escalar)
        self.escalar_container.hide()

        matrix_wrapper_layout = QHBoxLayout()

        matrix_wrapper_layout.setContentsMargins(
            0, 0, 0, 0
        )

        matrix_wrapper_layout.addWidget(
            self.escalar_container
        )

        matrix_wrapper_layout.addWidget(
            self.vectors_scroll,
            1
        )

        matrix_layout.addLayout(
            matrix_wrapper_layout
        )
                
        # Botones de Acción
        action_buttons_layout = QHBoxLayout()
        action_buttons_layout.setSpacing(12)
        
        self.btn_solve = QPushButton("Calcular")
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
        
        # ComboBox para operaciones de vectores
        self.combo_metodo = QComboBox()
        self.combo_metodo.addItems(["Sumar", "Restar", "Escalar", "Combinación lineal"])
        self.combo_metodo.setFixedWidth(120)
        self.combo_metodo.setFixedHeight(38)
        self.combo_metodo.setCurrentIndex(0)
        self.combo_metodo.currentIndexChanged.connect(self._on_operation_changed)

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
        self.stepper_vec.on_change_callback = self._rebuild_matrix_grid
        
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
        self.txt_equations.setPlaceholderText("v1 = (2, 3, -1)\nv2 = (4, -1, 2)")
        self.txt_equations.setFixedHeight(120)
        
        lbl_help = QLabel("Escribe la definición de tus vectores línea por línea.")
        lbl_help.setStyleSheet("color: #94A3B8; font-size: 11px; background: transparent;")
        
        btn_analyze = QPushButton("Analizar vectores")
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
        
      
        
        card_layout.addLayout(self.stacked_layout)
        content_layout.addWidget(self.card)

       # VISTA 3: OPERACIONES MATRICIALES
        matrix_ops_view = QWidget()
        matrix_ops_view.setStyleSheet("background-color: transparent;")
        mops_layout = QVBoxLayout(matrix_ops_view)
        mops_layout.setContentsMargins(0, 0, 0, 0)
        mops_layout.setSpacing(20)
        
        # Controles superiores
        mops_controls = QHBoxLayout()
        mops_controls.setSpacing(24)
        
        rows_box = QVBoxLayout()
        rows_box.setSpacing(6)
        lbl_rows = QLabel("FILAS (m)")
        lbl_rows.setStyleSheet("color: #64748B; font-size: 10px; font-weight: 700; letter-spacing: 0.5px; background: transparent;")
        self.stepper_mops_rows = NumberStepper(value=3)
        rows_box.addWidget(lbl_rows)
        rows_box.addWidget(self.stepper_mops_rows)
        
        cols_box = QVBoxLayout()
        cols_box.setSpacing(6)
        lbl_cols = QLabel("COLUMNAS (n)")
        lbl_cols.setStyleSheet("color: #64748B; font-size: 10px; font-weight: 700; letter-spacing: 0.5px; background: transparent;")
        self.stepper_mops_cols = NumberStepper(value=3)
        cols_box.addWidget(lbl_cols)
        cols_box.addWidget(self.stepper_mops_cols)
        
        mats_box = QVBoxLayout()
        mats_box.setSpacing(6)
        lbl_mats = QLabel("CANTIDAD DE MATRICES")
        lbl_mats.setStyleSheet("color: #64748B; font-size: 10px; font-weight: 700; letter-spacing: 0.5px; background: transparent;")
        self.stepper_mops_count = NumberStepper(value=3)
        mats_box.addWidget(lbl_mats)
        mats_box.addWidget(self.stepper_mops_count)
        
        mops_controls.addLayout(rows_box)
        mops_controls.addLayout(cols_box)
        mops_controls.addLayout(mats_box)
        mops_controls.addStretch()
        mops_layout.addLayout(mops_controls)
        
        # ============================================================
        # ÁREA DINÁMICA DE MATRICES
        # ============================================================

        self.mops_scroll = QScrollArea()
        self.mops_scroll.setWidgetResizable(False)

        self.mops_scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        self.mops_scroll.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        self.mops_scroll.setFrameShape(
            QFrame.Shape.NoFrame
        )

        self.mops_scroll.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }

            QScrollBar:horizontal {
                height: 8px;
                background: #F1F5F9;
                border-radius: 4px;
            }

            QScrollBar::handle:horizontal {
                background: #CBD5E1;
                border-radius: 4px;
                min-width: 40px;
            }

            QScrollBar::add-line:horizontal,
            QScrollBar::sub-line:horizontal {
                width: 0px;
                background: none;
                border: none;
            }
        """)

        # Contenedor que tendrá todas las matrices
        self.mops_container = QWidget()
        self.mops_container.setStyleSheet(
            "background-color: transparent;"
        )

        self.mops_layout_inner = QHBoxLayout(
            self.mops_container
        )

        self.mops_layout_inner.setContentsMargins(
            0, 0, 0, 0
        )

        self.mops_layout_inner.setSpacing(20)

        self.mops_layout_inner.setAlignment(
            Qt.AlignmentFlag.AlignLeft
        )

        # El scroll contiene el contenedor completo
        self.mops_scroll.setWidget(
            self.mops_container
        )


        # ============================================================
        # ESCALAR
        # ============================================================

        self.mops_escalar_container = QWidget()
        self.mops_escalar_container.setStyleSheet(
            "background-color: transparent;"
        )

        escalar_mat_layout = QVBoxLayout(
            self.mops_escalar_container
        )

        escalar_mat_layout.setContentsMargins(
            0, 0, 0, 0
        )

        escalar_mat_layout.setSpacing(6)

        lbl_k_mat = QLabel("ESCALAR (k)")

        lbl_k_mat.setStyleSheet(
            """
            color: #64748B;
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 0.5px;
            background: transparent;
            """
        )

        self.inp_mops_escalar = QLineEdit("1")

        self.inp_mops_escalar.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.inp_mops_escalar.setFixedSize(
            60, 36
        )

        self.inp_mops_escalar.setStyleSheet(
            self.inp_escalar.styleSheet()
        )

        escalar_mat_layout.addWidget(lbl_k_mat)
        escalar_mat_layout.addWidget(self.inp_mops_escalar)

        self.mops_escalar_container.hide()


        # ============================================================
        # WRAPPER
        # ============================================================

        mops_wrapper_layout = QHBoxLayout()

        mops_wrapper_layout.setContentsMargins(
            0, 0, 0, 0
        )

        mops_wrapper_layout.setSpacing(12)

        mops_wrapper_layout.addWidget(
            self.mops_escalar_container
        )

        mops_wrapper_layout.addWidget(
            self.mops_scroll,
            1
        )

        mops_layout.addLayout(
            mops_wrapper_layout
        )
        
          
        # Botones de Acción y ComboBox
        mops_action_buttons = QHBoxLayout()
        mops_action_buttons.setSpacing(12)
        
        btn_calc_mops = QPushButton("Calcular")
        btn_calc_mops.setStyleSheet(self.btn_solve.styleSheet())
        btn_calc_mops.setCursor(Qt.CursorShape.PointingHandCursor)
        
        btn_clear_mops = QPushButton("Limpiar")
        btn_clear_mops.setStyleSheet(btn_clear.styleSheet())
        btn_clear_mops.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_clear_mops.clicked.connect(self._clear_matrix_ops_inputs)
        
        self.combo_mops_metodo = QComboBox()
        self.combo_mops_metodo.addItems(["Sumar", "Restar", "Escalar"])
        self.combo_mops_metodo.setFixedWidth(120)
        self.combo_mops_metodo.setFixedHeight(38)
        self.combo_mops_metodo.setCurrentIndex(0)
        self.combo_mops_metodo.setStyleSheet(self.combo_metodo.styleSheet())
        self.combo_mops_metodo.currentIndexChanged.connect(self._on_mops_operation_changed)

        for i in range(self.combo_mops_metodo.count()):
            self.combo_mops_metodo.setItemData(i, Qt.AlignmentFlag.AlignCenter, Qt.ItemDataRole.TextAlignmentRole)
        
        mops_action_buttons.addWidget(btn_calc_mops)
        mops_action_buttons.addWidget(self.combo_mops_metodo)
        mops_action_buttons.addWidget(btn_clear_mops)
        mops_action_buttons.addStretch()
        
        mops_layout.addLayout(mops_action_buttons)
        
        # Suscribir steppers de matrices
        self.stepper_mops_rows.on_change_callback = self._rebuild_matrix_ops_grid
        self.stepper_mops_cols.on_change_callback = self._rebuild_matrix_ops_grid
        self.stepper_mops_count.on_change_callback = self._rebuild_matrix_ops_grid
        
        self._rebuild_matrix_ops_grid()
        self.stacked_layout.addWidget(matrix_ops_view)
        # -------------------------------------------------------------
        # VISTA 4: ECUACIONES MATRICIALES (Matriz A + Vector x)
        # -------------------------------------------------------------
        mat_eqs_view = QWidget()
        mat_eqs_view.setStyleSheet("background-color: transparent;")
        meqs_layout = QVBoxLayout(mat_eqs_view)
        meqs_layout.setContentsMargins(0, 0, 0, 0)
        meqs_layout.setSpacing(20)

        # Controles superiores (Filas, Columnas y Variables para el Vector)
        meqs_controls = QHBoxLayout()
        meqs_controls.setSpacing(24)

        rows_box = QVBoxLayout()
        rows_box.setSpacing(6)
        lbl_rows = QLabel("CANTIDAD DE FILAS")
        lbl_rows.setStyleSheet("color: #64748B; font-size: 10px; font-weight: 700; letter-spacing: 0.5px; background: transparent;")
        self.stepper_meqs_rows = NumberStepper(value=3)
        rows_box.addWidget(lbl_rows)
        rows_box.addWidget(self.stepper_meqs_rows)

        cols_box = QVBoxLayout()
        cols_box.setSpacing(6)
        lbl_cols = QLabel("CANTIDAD DE COLUMNAS")
        lbl_cols.setStyleSheet("color: #64748B; font-size: 10px; font-weight: 700; letter-spacing: 0.5px; background: transparent;")
        self.stepper_meqs_cols = NumberStepper(value=3)
        cols_box.addWidget(lbl_cols)
        cols_box.addWidget(self.stepper_meqs_cols)

        vars_box = QVBoxLayout()
        vars_box.setSpacing(6)
        lbl_vars = QLabel("CANTIDAD DE VARIABLES")
        lbl_vars.setStyleSheet("color: #64748B; font-size: 10px; font-weight: 700; letter-spacing: 0.5px; background: transparent;")
        self.stepper_meqs_vars = NumberStepper(value=3)
        vars_box.addWidget(lbl_vars)
        vars_box.addWidget(self.stepper_meqs_vars)

        meqs_controls.addLayout(rows_box)
        meqs_controls.addLayout(cols_box)
        meqs_controls.addLayout(vars_box)
        meqs_controls.addStretch()
        meqs_layout.addLayout(meqs_controls)

        # Área dinámica donde se dibujan Matriz A y Vector x
        self.meqs_container = QWidget()
        self.meqs_container.setStyleSheet("background-color: transparent;")
        self.meqs_layout_inner = QHBoxLayout(self.meqs_container)
        self.meqs_layout_inner.setContentsMargins(0, 0, 0, 0)
        self.meqs_layout_inner.setSpacing(24)
        self.meqs_layout_inner.setAlignment(Qt.AlignmentFlag.AlignLeft)

        meqs_layout.addWidget(self.meqs_container)

        # Botones de Acción (Calcular y Limpiar)
        meqs_actions = QHBoxLayout()
        meqs_actions.setSpacing(12)

        btn_calc_meqs = QPushButton("Calcular")
        btn_calc_meqs.setStyleSheet(self.btn_solve.styleSheet())
        btn_calc_meqs.setCursor(Qt.CursorShape.PointingHandCursor)

        btn_clear_meqs = QPushButton("Limpiar")
        btn_clear_meqs.setStyleSheet(btn_clear.styleSheet())
        btn_clear_meqs.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_clear_meqs.clicked.connect(self._clear_mat_eqs_inputs)

        meqs_actions.addWidget(btn_calc_meqs)
        meqs_actions.addWidget(btn_clear_meqs)
        meqs_actions.addStretch()
        meqs_layout.addLayout(meqs_actions)

        # Añadir las vistas al stacked_layout
        self.stacked_layout.addWidget(matrix_view)
        self.stacked_layout.addWidget(equations_view)
        self.stacked_layout.addWidget(matrix_ops_view)
        self.stacked_layout.addWidget(mat_eqs_view) # Index 3

        # Conectar callbacks de los steppers
        self.stepper_meqs_rows.on_change_callback = self._rebuild_mat_eqs_grid
        self.stepper_meqs_cols.on_change_callback = self._rebuild_mat_eqs_grid
        self.stepper_meqs_vars.on_change_callback = self._rebuild_mat_eqs_grid

        self._rebuild_mat_eqs_grid()
        # TARJETA DE RESULTADOS
        self.results_card = QWidget()
        self.results_layout = QVBoxLayout(self.results_card)
        self.results_layout.setContentsMargins(0, 0, 0, 0)
        self.results_layout.setSpacing(16)

        self.card_matriz = CollapsibleCard("Vectores del Sistema")
        self.card_proceso = CollapsibleCard("Proceso de Operación")
        self.card_solucion = CollapsibleCard("Resultado")

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

        self.btn_matrix.clicked.connect(
            lambda: self._set_mode(
                0, mode_button_active_style, mode_button_style
            )
        )
        self.btn_matrix_ops.clicked.connect(
            lambda: self._set_mode(
                2, mode_button_active_style, mode_button_style
            )
        )
        self.btn_equations.clicked.connect(
            lambda: self._set_mode(
                1, mode_button_active_style, mode_button_style
            )
        )
        self.btn_mat_eqs.clicked.connect(lambda: self._set_mode(3, mode_button_active_style, mode_button_style)) 

        content_outer_layout.addWidget(centered_wrapper)
        scroll_area.setWidget(main_content)
        main_layout.addWidget(scroll_area)

    def _on_operation_changed(self):
        modo = self.combo_metodo.currentText()

        if modo == "Escalar":
            self.escalar_container.show()
            self.stepper_vec.setEnabled(False)

        else:
            self.escalar_container.hide()
            self.stepper_vec.setEnabled(True)

        self._rebuild_matrix_grid()
        
    def _set_mode(self, index, active_style, inactive_style):
        self.stacked_layout.setCurrentIndex(index)
        if index == 0:
            self.btn_matrix.setStyleSheet(active_style)
            self.btn_equations.setStyleSheet(inactive_style)
            self.btn_matrix_ops.setStyleSheet(inactive_style)
            self.btn_mat_eqs.setStyleSheet(inactive_style)
        elif index == 1:
            self.btn_matrix.setStyleSheet(inactive_style)
            self.btn_equations.setStyleSheet(active_style)
            self.btn_matrix_ops.setStyleSheet(inactive_style)
            self.btn_mat_eqs.setStyleSheet(inactive_style)
        elif index == 2:
            self.btn_matrix.setStyleSheet(inactive_style)
            self.btn_equations.setStyleSheet(inactive_style)
            self.btn_matrix_ops.setStyleSheet(active_style)
            self.btn_mat_eqs.setStyleSheet(inactive_style)
        elif index ==3:
            self.btn_matrix.setStyleSheet(inactive_style)
            self.btn_equations.setStyleSheet(inactive_style)
            self.btn_matrix_ops.setStyleSheet(inactive_style)
            self.btn_mat_eqs.setStyleSheet(active_style)

    def _rebuild_matrix_grid(self):
        """
        Reconstruye dinámicamente los vectores según la operación seleccionada.

        Para Sumar, Restar y Escalar se muestran únicamente los vectores
        necesarios para la operación.

        Para Combinación lineal se muestran:
            v1, v2, ..., vk
        como vectores generadores y adicionalmente el vector objetivo b.
        """

        # --------------------------------------------------------
        # LIMPIAR VECTORES ANTERIORES
        # --------------------------------------------------------

        while self.vectors_layout.count():

            item = self.vectors_layout.takeAt(0)

            if item.widget():

                item.widget().deleteLater()

            elif item.layout():

                sub_layout = item.layout()

                while sub_layout.count():

                    sub_item = sub_layout.takeAt(0)

                    if sub_item.widget():
                        sub_item.widget().deleteLater()

        # --------------------------------------------------------
        # LIMPIAR REFERENCIA DEL VECTOR b
        # --------------------------------------------------------

        self.b_inputs_list = []

        # --------------------------------------------------------
        # DATOS DE LA VISTA
        # --------------------------------------------------------

        rows = self.stepper_var.value

        modo = self.combo_metodo.currentText()

        es_escalar = modo == "Escalar"

        es_combinacion = modo == "Combinación lineal"

        # Para escalar solamente necesitamos un vector.
        #
        # Para las demás operaciones usamos la cantidad
        # indicada por el usuario.
        num_vectores = (
            1
            if es_escalar
            else self.stepper_vec.value
        )

        self.inputs_list = []

        # --------------------------------------------------------
        # ESTILO DE LOS INPUTS
        # --------------------------------------------------------

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

        # --------------------------------------------------------
        # ALTURA DE LOS CORCHETES
        # --------------------------------------------------------

        bracket_height = (
            rows * 36
            + (rows - 1) * 8
        )

        # ========================================================
        #                 VECTORES GENERADORES
        # ========================================================

        for v in range(num_vectores):
            vec_widget = QWidget()

            vec_widget.setStyleSheet(
                "background-color: transparent;"
            )

            vec_widget.setMinimumWidth(82)

            vec_box = QVBoxLayout(
                vec_widget
            )

            vec_box.setContentsMargins(
                0, 0, 0, 0
            )

            vec_box.setSpacing(6)

            vec_box.setAlignment(
                Qt.AlignmentFlag.AlignTop
            )

            # --------------------------------------------
            # NOMBRE DEL VECTOR
            # --------------------------------------------

            lbl_v = QLabel(
                f"v<sub>{v + 1}</sub>"
            )

            lbl_v.setAlignment(
                Qt.AlignmentFlag.AlignCenter
            )

            lbl_v.setStyleSheet(
                """
                color: #64748B;
                font-size: 11px;
                font-weight: 600;
                background: transparent;
                """
            )

            vec_box.addWidget(lbl_v)

            # --------------------------------------------
            # FILA DEL VECTOR
            # --------------------------------------------

            vector_row_layout = QHBoxLayout()

            vector_row_layout.setSpacing(4)

            vector_row_layout.setContentsMargins(
                0, 0, 0, 0
            )

            vector_row_layout.setAlignment(
                Qt.AlignmentFlag.AlignCenter
            )

            # Corchete izquierdo

            b_left = BracketWidget(
                is_left=True
            )

            b_left.setFixedHeight(
                bracket_height
            )

            # Inputs

            inputs_column = QVBoxLayout()

            inputs_column.setSpacing(8)

            inputs_column.setContentsMargins(
                0, 0, 0, 0
            )

            vec_inputs = []

            for r in range(rows):

                inp = QLineEdit("0")

                inp.setAlignment(
                    Qt.AlignmentFlag.AlignCenter
                )

                inp.setFixedSize(
                    54,
                    36
                )

                inp.setStyleSheet(
                    input_style
                )

                inputs_column.addWidget(
                    inp
                )

                vec_inputs.append(
                    inp
                )

            # Guardar inputs del vector

            self.inputs_list.append(
                vec_inputs
            )

            # Corchete derecho

            b_right = BracketWidget(
                is_left=False
            )

            b_right.setFixedHeight(
                bracket_height
            )

            # Armar vector

            vector_row_layout.addWidget(
                b_left
            )

            vector_row_layout.addLayout(
                inputs_column
            )

            vector_row_layout.addWidget(
                b_right
            )

            vec_box.addLayout(
                vector_row_layout
            )

            self.vectors_layout.addWidget(
                vec_widget
            )

        # ========================================================
        #                    VECTOR OBJETIVO b
        # ========================================================

        if es_combinacion:

            # Separación visual entre generadores y b

            self.vectors_layout.addSpacing(24)

            # Contenedor del vector b

            b_widget = QWidget()

            b_widget.setStyleSheet(
                "background-color: transparent;"
            )

            b_widget.setMinimumWidth(82)

            b_box = QVBoxLayout(
                b_widget
            )

            b_box.setContentsMargins(
                0, 0, 0, 0
            )

            b_box.setSpacing(6)

            b_box.setAlignment(
                Qt.AlignmentFlag.AlignTop
            )
            # Título b

            lbl_b = QLabel("b")

            lbl_b.setAlignment(
                Qt.AlignmentFlag.AlignCenter
            )

            lbl_b.setStyleSheet(
                """
                color: #2563EB;
                font-size: 11px;
                font-weight: 700;
                background: transparent;
                """
            )

            b_box.addWidget(
                lbl_b
            )

            # Fila del vector b

            b_row_layout = QHBoxLayout()

            b_row_layout.setSpacing(4)

            b_row_layout.setContentsMargins(
                0, 0, 0, 0
            )

            b_row_layout.setAlignment(
                Qt.AlignmentFlag.AlignCenter
            )

            # Corchete izquierdo

            b_left = BracketWidget(
                is_left=True
            )

            b_left.setFixedHeight(
                bracket_height
            )

            # Inputs de b

            b_inputs_column = QVBoxLayout()

            b_inputs_column.setSpacing(8)

            b_inputs_column.setContentsMargins(
                0, 0, 0, 0
            )

            for r in range(rows):

                inp = QLineEdit("0")

                inp.setAlignment(
                    Qt.AlignmentFlag.AlignCenter
                )

                inp.setFixedSize(
                    54,
                    36
                )

                inp.setStyleSheet(
                    input_style
                )

                b_inputs_column.addWidget(
                    inp
                )

                self.b_inputs_list.append(
                    inp
                )

            # Corchete derecho

            b_right = BracketWidget(
                is_left=False
            )

            b_right.setFixedHeight(
                bracket_height
            )

            # Armar vector b

            b_row_layout.addWidget(
                b_left
            )

            b_row_layout.addLayout(
                b_inputs_column
            )

            b_row_layout.addWidget(
                b_right
            )

            b_box.addLayout(
                b_row_layout
            )

            self.vectors_layout.addWidget(
                b_widget
            )
            self.vectors_container.adjustSize()

    def _clear_matrix_inputs(self):

        for vec in self.inputs_list:

            for inp in vec:

                inp.setText("0")

        for inp in self.b_inputs_list:

            inp.setText("0")

        self.inp_escalar.setText("1")

        self.txt_equations.clear()

        self.results_card.hide()
    def _on_mops_operation_changed(self):
        modo = self.combo_mops_metodo.currentText()
        if modo == "Escalar":
            self.mops_escalar_container.show()
            self.stepper_mops_count.setEnabled(False)
        else:
            self.mops_escalar_container.hide()
            self.stepper_mops_count.setEnabled(True)
        self._rebuild_matrix_ops_grid()

    def _rebuild_matrix_ops_grid(self):
        # Limpiar matrices anteriores
        while self.mops_layout_inner.count():
            item = self.mops_layout_inner.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                sub_layout = item.layout()
                while sub_layout.count():
                    sub_item = sub_layout.takeAt(0)
                    if sub_item.widget():
                        sub_item.widget().deleteLater()

        rows = self.stepper_mops_rows.value
        cols = self.stepper_mops_cols.value
        es_escalar = self.combo_mops_metodo.currentText() == "Escalar"
        num_matrices = 1 if es_escalar else self.stepper_mops_count.value
        
        self.mops_inputs_list = []
        
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

        bracket_height = rows * 36 + (rows - 1) * 8

        for m in range(num_matrices):
            # Contenedor de una matriz (Etiqueta + Corchetes con Grid)
            mat_box = QVBoxLayout()
            mat_box.setSpacing(6)
            mat_box.setAlignment(Qt.AlignmentFlag.AlignTop)

            # Etiqueta A1, A2, A3...
            lbl_m = QLabel(f"A<sub>{m+1}</sub>")
            lbl_m.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_m.setStyleSheet("color: #64748B; font-size: 11px; font-weight: 600; background: transparent;")
            mat_box.addWidget(lbl_m)

            # Layout horizontal: [ Corchete Izquierdo | Grid mxn | Corchete Derecho ]
            mat_row_layout = QHBoxLayout()
            mat_row_layout.setSpacing(4)
            mat_row_layout.setContentsMargins(0, 0, 0, 0)

            b_left = BracketWidget(is_left=True)
            b_left.setFixedHeight(bracket_height)

            grid = QGridLayout()
            grid.setSpacing(8)
            grid.setContentsMargins(0, 0, 0, 0)

            mat_inputs = []
            for r in range(rows):
                row_inputs = []
                for c in range(cols):
                    inp = QLineEdit("0")
                    inp.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    inp.setFixedSize(54, 36)
                    inp.setStyleSheet(input_style)
                    grid.addWidget(inp, r, c)
                    row_inputs.append(inp)
                mat_inputs.append(row_inputs)

            self.mops_inputs_list.append(mat_inputs)

            b_right = BracketWidget(is_left=False)
            b_right.setFixedHeight(bracket_height)

            mat_row_layout.addWidget(b_left)
            mat_row_layout.addLayout(grid)
            mat_row_layout.addWidget(b_right)

            mat_box.addLayout(mat_row_layout)
            self.mops_layout_inner.addLayout(mat_box)

    def _clear_matrix_ops_inputs(self):
        for mat in self.mops_inputs_list:
            for row in mat:
                for inp in row:
                    inp.setText("0")
        self.inp_mops_escalar.setText("1")
    def _rebuild_mat_eqs_grid(self):
        # Función recursiva para limpiar layouts y widgets completamente
        def clear_layout(layout):
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                elif item.layout() is not None:
                    clear_layout(item.layout())

        clear_layout(self.meqs_layout_inner)

        rows = self.stepper_meqs_rows.value  # Filas de la Matriz A
        cols = self.stepper_meqs_cols.value  # Columnas de la Matriz A
        vars_count = self.stepper_meqs_vars.value  # Filas del Vector x

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

        self.meqs_matrix_inputs = []
        self.meqs_vector_inputs = []

        # --- 1. MATRIZ A ---
        mat_box = QVBoxLayout()
        mat_box.setSpacing(6)
        mat_box.setAlignment(Qt.AlignmentFlag.AlignTop)

        lbl_a = QLabel("A")
        lbl_a.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_a.setStyleSheet("color: #64748B; font-size: 11px; font-weight: 600; background: transparent;")
        mat_box.addWidget(lbl_a)

        mat_row_layout = QHBoxLayout()
        mat_row_layout.setSpacing(4)
        mat_row_layout.setContentsMargins(0, 0, 0, 0)

        mat_height = rows * 36 + (rows - 1) * 8
        b_left_mat = BracketWidget(is_left=True)
        b_left_mat.setFixedHeight(mat_height)

        grid_mat = QGridLayout()
        grid_mat.setSpacing(8)
        grid_mat.setContentsMargins(0, 0, 0, 0)

        for r in range(rows):
            row_inputs = []
            for c in range(cols):
                inp = QLineEdit("0")
                inp.setAlignment(Qt.AlignmentFlag.AlignCenter)
                inp.setFixedSize(54, 36)
                inp.setStyleSheet(input_style)
                grid_mat.addWidget(inp, r, c)
                row_inputs.append(inp)
            self.meqs_matrix_inputs.append(row_inputs)

        b_right_mat = BracketWidget(is_left=False)
        b_right_mat.setFixedHeight(mat_height)

        mat_row_layout.addWidget(b_left_mat)
        mat_row_layout.addLayout(grid_mat)
        mat_row_layout.addWidget(b_right_mat)

        mat_box.addLayout(mat_row_layout)
        self.meqs_layout_inner.addLayout(mat_box)

        # Separador horizontal entre la matriz y el vector
        self.meqs_layout_inner.addSpacing(16)

        # --- 2. VECTOR x ---
        vec_box = QVBoxLayout()
        vec_box.setSpacing(6)
        vec_box.setAlignment(Qt.AlignmentFlag.AlignTop)

        lbl_x = QLabel("x")
        lbl_x.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_x.setStyleSheet("color: #64748B; font-size: 11px; font-weight: 600; background: transparent;")
        vec_box.addWidget(lbl_x)

        vec_row_layout = QHBoxLayout()
        vec_row_layout.setSpacing(4)
        vec_row_layout.setContentsMargins(0, 0, 0, 0)

        vec_height = vars_count * 36 + (vars_count - 1) * 8
        b_left_vec = BracketWidget(is_left=True)
        b_left_vec.setFixedHeight(vec_height)

        vec_inputs_col = QVBoxLayout()
        vec_inputs_col.setSpacing(8)
        vec_inputs_col.setContentsMargins(0, 0, 0, 0)

        for r in range(vars_count):
            inp = QLineEdit("0")
            inp.setAlignment(Qt.AlignmentFlag.AlignCenter)
            inp.setFixedSize(54, 36)
            inp.setStyleSheet(input_style)
            vec_inputs_col.addWidget(inp)
            self.meqs_vector_inputs.append(inp)

        b_right_vec = BracketWidget(is_left=False)
        b_right_vec.setFixedHeight(vec_height)

        vec_row_layout.addWidget(b_left_vec)
        vec_row_layout.addLayout(vec_inputs_col)
        vec_row_layout.addWidget(b_right_vec)

        vec_box.addLayout(vec_row_layout)
        self.meqs_layout_inner.addLayout(vec_box)

    def _clear_mat_eqs_inputs(self):
        for row in self.meqs_matrix_inputs:
            for inp in row:
                inp.setText("0")
        for inp in self.meqs_vector_inputs:
            inp.setText("0")
 #
 # LOGICA PARA LA TARJETA DE SOLUCION Y CONECTAR CON EL CONTROLADOR
 #
    def _on_analyze_clicked(self):
        """Procesa el texto ingresado en el modo ecuaciones."""
        texto = self.txt_equations.toPlainText().strip()
        if not texto:
            QMessageBox.warning(self, "Campo vacío", "Por favor ingresa las ecuaciones o vectores a analizar.")
            return

        if leer_sistema_desde_texto:
            try:
                matriz, eq, var = leer_sistema_desde_texto(texto)
                # Lógica para procesar la matriz analizada
                resultado = ControladorVectores.evaluar_independencia_lineal(matriz)
                self._mostrar_resultados(resultado)
            except Exception as e:
                QMessageBox.critical(self, "Error al analizar", f"Ocurrió un error al procesar la entrada: {str(e)}")
        else:
            QMessageBox.information(self, "Modo Ecuaciones", "El módulo de lectura por texto está en integración.")
    def _on_solve_clicked(self):
        """
        Ejecuta la operación seleccionada en el ComboBox.

        Sumar:
            v1 + v2 + ... + vk

        Restar:
            v1 - v2

        Escalar:
            k * v1

        Combinación lineal:
            determina si b puede escribirse como
            c1*v1 + c2*v2 + ... + ck*vk
        """

        try:

            modo = self.combo_metodo.currentText()

            # ====================================================
            # LEER VECTORES GENERADORES
            # ====================================================

            vectores = []

            for vec_inputs in self.inputs_list:

                vector = []

                for inp in vec_inputs:

                    texto = (
                        inp.text()
                        .strip()
                        .replace(",", ".")
                    )

                    valor = (
                        float(texto)
                        if texto
                        else 0.0
                    )

                    vector.append(
                        valor
                    )

                vectores.append(
                    vector
                )

            # ====================================================
            # VALIDAR QUE EXISTAN VECTORES
            # ====================================================

            if not vectores:

                QMessageBox.warning(
                    self,
                    "Sin vectores",
                    "Debes ingresar al menos un vector."
                )

                return

            # ====================================================
            # SUMAR
            # ====================================================

            if modo == "Sumar":

                if len(vectores) < 2:

                    QMessageBox.warning(
                        self,
                        "Vectores insuficientes",
                        "Para sumar necesitas al menos dos vectores."
                    )

                    return

                resultado = (
                    ControladorVectores
                    .sumar_vectores(vectores)
                )

            # ====================================================
            # RESTAR
            # ====================================================

            elif modo == "Restar":

                if len(vectores) != 2:

                    QMessageBox.warning(
                        self,
                        "Cantidad de vectores",
                        "La resta requiere exactamente dos vectores."
                    )

                    return

                resultado = (
                    ControladorVectores
                    .restar_vectores(vectores)
                )

            # ====================================================
            # ESCALAR
            # ====================================================

            elif modo == "Escalar":

                texto_escalar = (
                    self.inp_escalar
                    .text()
                    .strip()
                    .replace(",", ".")
                )

                if not texto_escalar:

                    QMessageBox.warning(
                        self,
                        "Escalar vacío",
                        "Debes ingresar un valor para el escalar."
                    )

                    return
                
                escalar = float(texto_escalar)


                resultado = (
                    ControladorVectores
                    .multiplicar_vector_escalar(
                        vectores[0],
                        escalar
                    )
                )

            # ====================================================
            # COMBINACIÓN LINEAL
            # ====================================================

            elif modo == "Combinación lineal":

                # ----------------------------------------------
                # Leer vector b
                # ----------------------------------------------

                b = []

                for inp in self.b_inputs_list:

                    texto = (
                        inp.text()
                        .strip()
                        .replace(",", ".")
                    )

                    valor = (
                        float(texto)
                        if texto
                        else 0.0
                    )

                    b.append(
                        valor
                    )

                if not b:

                    QMessageBox.warning(
                        self,
                        "Vector objetivo vacío",
                        "Debes ingresar el vector b."
                    )

                    return

                # ----------------------------------------------
                # LLAMAR AL CONTROLADOR
                #
                # IMPORTANTE:
                # aquí pasamos solamente los generadores.
                #
                # b se pasa por separado.
                # ----------------------------------------------

                resultado = (
                    ControladorVectores
                    .evaluar_combinacion_lineal(
                        vectores,
                        b
                    )
                )

            # ====================================================
            # OPERACIÓN DESCONOCIDA
            # ====================================================

            else:

                QMessageBox.warning(
                    self,
                    "Operación desconocida",
                    "Selecciona una operación válida."
                )

                return

            # ====================================================
            # COMPROBAR RESULTADO
            # ====================================================

            if not resultado.get(
                "exito",
                False
            ):

                QMessageBox.warning(
                    self,
                    "Error",
                    resultado.get(
                        "mensaje",
                        "No se pudo realizar la operación."
                    )
                )

                return

            # ====================================================
            # MOSTRAR RESULTADOS
            #
            # Por ahora NO modificamos la tarjeta Solución.
            # ====================================================

            self._mostrar_resultados(
                resultado
            )

        except ValueError:

            QMessageBox.warning(
                self,
                "Entrada inválida",
                "Todos los componentes deben ser números válidos."
            )

        except Exception as e:

            print(
                f"Error en _on_solve_clicked: {e}"
            )

            QMessageBox.critical(
                self,
                "Error de Ejecución",
                f"Detalle del error:\n{str(e)}"
            )
    def _crear_proceso_suma(self,vectores, resultado):
        """
        Construye el texto del procedimiento de suma de vectores.
        """
        partes = []

        for a, b in zip(vectores):
            partes.append(
                f"{formatear_numero(a)} + {formatear_numero(b)}"
            )

        resultados = [
            formatear_numero(valor)
            for valor in resultado
        ]

        return (
            "v₁ + v₂ = "
            "[" + "; ".join(partes) + "]"
            " = "
            "[" + "; ".join(resultados) + "]"
        )


    def _crear_proceso_resta(self, vectores, resultado):
            """
            Construye el texto del procedimiento de resta de vectores.
            """
            partes = []

            for a, b in zip(vectores):
                partes.append(
                    f"{formatear_numero(a)} - {formatear_numero(b)}"
                )

            resultados = [
                formatear_numero(valor)
                for valor in resultado
            ]

            return (
                "v₁ − v₂ = "
                "[" + "; ".join(partes) + "]"
                " = "
                "[" + "; ".join(resultados) + "]"
            )


    def _crear_proceso_escalar(self, escalar, vector, resultado):
        """
        Construye el texto del procedimiento de multiplicación
        de un vector por un escalar.
        """
        partes = []

        for valor in vector:
            partes.append(
                f"{formatear_numero(escalar)}"
                f" · "
                f"{formatear_numero(valor)}"
            )

        resultados = [
            formatear_numero(valor)
            for valor in resultado
        ]

        return (
            f"{formatear_numero(escalar)} · v₁ = "
            "["
            + "; ".join(partes)
            + "]"
            " = "
            "["
            + "; ".join(resultados)
            + "]"
        )

    def _crear_card_info_sistema(self, resultado):
        """Construye la tarjeta 'Información del sistema' usando las claves del controlador."""
        card = QFrame()
        card.setObjectName("CardInfoSistema")
        card.setStyleSheet("""
            QFrame#CardInfoSistema {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 12px;
                padding: 20px;
            }
        """)

        layout = QVBoxLayout(card)
        layout.setSpacing(16)
        layout.setContentsMargins(16, 16, 16, 16)

        # --- CABECERA (Barra azul + Título) ---
        header_layout = QHBoxLayout()
        header_layout.setSpacing(8)

        bar_accent = QFrame()
        bar_accent.setFixedWidth(4)
        bar_accent.setFixedHeight(18)
        bar_accent.setStyleSheet("background-color: #2563EB; border-radius: 2px;")

        lbl_title = QLabel("Información del sistema")
        lbl_title.setStyleSheet("color: #0F172A; font-size: 15px; font-weight: 700; border: none;")

        header_layout.addWidget(bar_accent)
        header_layout.addWidget(lbl_title)
        header_layout.addStretch()
        layout.addLayout(header_layout)

        # --- DATOS EXTRAÍDOS ---
        rango_a = resultado.get("rango_A", 0)
        rango_ab = resultado.get("rango_Ab", 0)
        num_vars = resultado.get("num_variables", 0)
        num_eqs = resultado.get("num_ecuaciones", 0)

        pivotes = resultado.get("columnas_pivote", [])
        str_pivotes = ", ".join(map(str, pivotes)) if pivotes else "Ninguna"

        basicas = resultado.get("variables_basicas", [])
        str_basicas = ", ".join([f"x{i+1}" for i in basicas]) if basicas else "Ninguna"

        libres = resultado.get("variables_libres", [])
        str_libres = ", ".join([f"x{i+1}" for i in libres]) if libres else "Ninguna"

        # --- GRID DE PROPIEDADES ---
        grid = QGridLayout()
        grid.setHorizontalSpacing(40)
        grid.setVerticalSpacing(10)

        self._add_info_row(grid, 0, 0, "Rango (A)", str(rango_a))
        self._add_info_row(grid, 1, 0, "Rango (A|b)", str(rango_ab))
        self._add_info_row(grid, 2, 0, "Número de variables", str(num_vars))
        self._add_info_row(grid, 3, 0, "Número de ecuaciones", str(num_eqs))

        self._add_info_row(grid, 0, 2, "Columnas pivote", str_pivotes)
        self._add_info_row(grid, 1, 2, "Variables básicas", str_basicas)
        self._add_info_row(grid, 2, 2, "Variables libres", str_libres)

        layout.addLayout(grid)

        # --- DIVISOR ---
        linea = QFrame()
        linea.setFrameShape(QFrame.Shape.HLine)
        linea.setStyleSheet("background-color: #F1F5F9; border: none; max-height: 1px;")
        layout.addWidget(linea)

        # --- RESUMEN EN CÓDIGO ---
        tipo_sol = resultado.get("tipo", "ninguna")
        if tipo_sol == "unica":
            texto_conclusion = "solución única"
        elif tipo_sol == "infinitas":
            texto_conclusion = "infinitas soluciones"
        else:
            texto_conclusion = "sin solución"

        resumen_txt = f"rango(A) = {rango_a}  |  rango(A|b) = {rango_ab}  |  n = {num_vars}  →  {texto_conclusion}"

        lbl_resumen = QLabel(resumen_txt)
        lbl_resumen.setStyleSheet("""
            color: #475569;
            font-family: 'Consolas', 'Courier New', monospace;
            font-size: 13px;
            border: none;
            padding-top: 4px;
        """)
        layout.addWidget(lbl_resumen)

        return card

    def _add_info_row(self, grid, row, col, label_text, val_text):
        lbl_key = QLabel(label_text)
        lbl_key.setStyleSheet("color: #64748B; font-size: 13px; font-weight: 500; border: none;")

        lbl_val = QLabel(val_text)
        lbl_val.setStyleSheet("color: #0F172A; font-size: 13px; font-weight: 700; border: none;")
        lbl_val.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        grid.addWidget(lbl_key, row, col)
        grid.addWidget(lbl_val, row, col + 1)


    def _crear_card_matriz_aumentada(self, resultado):
        """Construye la tarjeta desplegable 'Matriz aumentada' con corchetes y divisor vertical."""
        # Contenedor Principal (Tarjeta)
        card = QFrame()
        card.setObjectName("CardMatrizAumentada")
        card.setStyleSheet("""
            QFrame#CardMatrizAumentada {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 12px;
            }
        """)

        layout_principal = QVBoxLayout(card)
        layout_principal.setContentsMargins(20, 16, 20, 20)
        layout_principal.setSpacing(12)

        # --- CABECERA (Título + Subtítulo + Botón Colapsar) ---
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)

        title_container = QVBoxLayout()
        lbl_title = QLabel("Matriz aumentada")
        lbl_title.setStyleSheet("color: #0F172A; font-size: 15px; font-weight: 700; border: none;")

        num_eqs = resultado.get("num_ecuaciones", 0)
        num_vars = resultado.get("num_variables", 0)
        lbl_sub = QLabel(f"SISTEMA ORIGINAL · {num_eqs} ECUACIONES, {num_vars} VARIABLES")
        lbl_sub.setStyleSheet("color: #64748B; font-size: 11px; font-weight: 700; letter-spacing: 0.5px; border: none;")

        title_container.addWidget(lbl_title)
        title_container.addWidget(lbl_sub)

        btn_toggle = QPushButton("−")
        btn_toggle.setFixedSize(24, 24)
        btn_toggle.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                color: #64748B;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover { color: #0F172A; }
        """)

        header_layout.addLayout(title_container)
        header_layout.addStretch()
        header_layout.addWidget(btn_toggle)
        layout_principal.addWidget(header_widget)

        # --- CONTENIDO DESPLEGABLE (Matriz con Corchetes) ---
        body_widget = QWidget()
        body_layout = QHBoxLayout(body_widget)
        body_layout.setContentsMargins(10, 10, 10, 10)
        body_layout.setSpacing(0)

        # Obtener matriz aumentada del resultado
        matriz_aug = resultado.get("matriz_aumentada", [])

        if matriz_aug:
            # Corchete Izquierdo
            bracket_left = QLabel("[")
            bracket_left.setStyleSheet("color: #0F172A; font-size: 42px; font-weight: 300; font-family: 'Courier New'; padding-right: 8px;")

            # Grid de Coeficientes y Vector b
            grid_matriz = QGridLayout()
            grid_matriz.setHorizontalSpacing(16)
            grid_matriz.setVerticalSpacing(8)

            for i, fila in enumerate(matriz_aug):
                num_cols = len(fila)
                for j, val in enumerate(fila):
                    lbl_val = QLabel(f"{val:g}" if isinstance(val, (int, float)) else str(val))
                    
                    # Estilo diferenciado para la columna b (negrita)
                    if j == num_cols - 1:
                        lbl_val.setStyleSheet("color: #0F172A; font-size: 14px; font-weight: 800; font-family: 'Consolas', monospace;")
                    else:
                        lbl_val.setStyleSheet("color: #334155; font-size: 14px; font-weight: 500; font-family: 'Consolas', monospace;")
                    
                    lbl_val.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    
                    # Insertar divisor vertical antes de la última columna
                    if j == num_cols - 1:
                        linea_v = QFrame()
                        linea_v.setFrameShape(QFrame.Shape.VLine)
                        linea_v.setStyleSheet("background-color: #CBD5E1; max-width: 1px; border: none;")
                        grid_matriz.addWidget(linea_v, i, j * 2 - 1)
                        grid_matriz.addWidget(lbl_val, i, j * 2)
                    else:
                        grid_matriz.addWidget(lbl_val, i, j * 2)

            # Corchete Derecho
            bracket_right = QLabel("]")
            bracket_right.setStyleSheet("color: #0F172A; font-size: 42px; font-weight: 300; font-family: 'Courier New'; padding-left: 8px;")

            body_layout.addWidget(bracket_left)
            body_layout.addLayout(grid_matriz)
            body_layout.addWidget(bracket_right)
            body_layout.addStretch()

        layout_principal.addWidget(body_widget)

        # Lógica de ocultar/mostrar con el botón colapsar
        def _toggle():
            if body_widget.isVisible():
                body_widget.hide()
                btn_toggle.setText("+")
            else:
                body_widget.show()
                btn_toggle.setText("−")

        btn_toggle.clicked.connect(_toggle)

        return card
    
    def _crear_card_proceso_operacion(self, resultado):
        """
        Construye la tarjeta desplegable 'Proceso' para las operaciones
        de suma, resta y multiplicación por escalar.

        El diseño sigue el mismo estilo visual utilizado en
        renderizar_proceso_eliminacion().
        """

        # ==========================================================
        # TARJETA PRINCIPAL
        # ==========================================================

        card = QFrame()
        card.setObjectName("CardProcesoOperacion")

        card.setStyleSheet("""
            QFrame#CardProcesoOperacion {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 12px;
            }
        """)

        layout_principal = QVBoxLayout(card)
        layout_principal.setContentsMargins(20, 16, 20, 20)
        layout_principal.setSpacing(12)

        # ==========================================================
        # CABECERA
        # ==========================================================

        header_widget = QWidget()
        header_widget.setStyleSheet(
            "background: transparent; border: none;"
        )

        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)

        lbl_title = QLabel("Proceso")

        lbl_title.setStyleSheet("""
            color: #0F172A;
            font-size: 15px;
            font-weight: 700;
            border: none;
            background: transparent;
        """)

        btn_toggle = QPushButton("−")
        btn_toggle.setFixedSize(24, 24)

        btn_toggle.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                color: #64748B;
                font-size: 16px;
                font-weight: bold;
            }

            QPushButton:hover {
                color: #0F172A;
            }
        """)

        header_layout.addWidget(lbl_title)
        header_layout.addStretch()
        header_layout.addWidget(btn_toggle)

        layout_principal.addWidget(header_widget)

        # ==========================================================
        # CONTENIDO
        # ==========================================================

        body_widget = QWidget()

        body_widget.setStyleSheet("""
            QWidget {
                background: transparent;
                border: none;
            }
        """)

        body_layout = QVBoxLayout(body_widget)

        body_layout.setContentsMargins(
            0, 10, 0, 10
        )

        body_layout.setSpacing(16)

        # ==========================================================
        # DATOS
        # ==========================================================

        operacion = str(
            resultado.get("operacion", "")
        )

        vectores = resultado.get(
            "vectores",
            []
        )

        vector_original = resultado.get(
            "vector"
        )

        resultado_vector = resultado.get(
            "resultado",
            []
        )

        escalar = resultado.get(
            "escalar"
        )

        # ==========================================================
        # NOMBRE DE LA OPERACIÓN
        # ==========================================================

        def crear_nombre_operacion(simbolo):

            nombres = []

            for i in range(len(vectores)):

                nombres.append(
                    f"v({i + 1})"
                )

            return f" {simbolo} ".join(nombres)

        # ==========================================================
        # VECTOR VISUAL
        # ==========================================================

        def crear_vector_widget(vector):

            widget = QWidget()

            widget.setStyleSheet("""
                QWidget {
                    background: transparent;
                    border: none;
                }
            """)

            layout = QHBoxLayout(widget)

            layout.setContentsMargins(
                0, 0, 0, 0
            )

            layout.setSpacing(4)

            # ------------------------------------------------------
            # CORCHETE IZQUIERDO
            # ------------------------------------------------------

            try:

                bracket_left = BracketWidget(
                    is_left=True
                )

                layout.addWidget(
                    bracket_left
                )

            except NameError:

                bracket_left = QLabel("[")

                bracket_left.setStyleSheet("""
                    color: #0F172A;
                    font-size: 38px;
                    font-weight: 300;
                    font-family: 'Courier New';
                    border: none;
                    background: transparent;
                    padding: 0px;
                    margin: 0px;
                """)

                layout.addWidget(
                    bracket_left
                )

            # ------------------------------------------------------
            # COMPONENTES
            # ------------------------------------------------------

            grid = QGridLayout()

            grid.setVerticalSpacing(4)
            grid.setHorizontalSpacing(18)
            grid.setContentsMargins(
                0, 0, 0, 0
            )

            ALTURA_CELDA = 24

            for row, valor in enumerate(vector):

                if isinstance(
                    valor,
                    (int, float)
                ):

                    texto = formatear_numero(
                        valor
                    )

                else:

                    texto = str(valor)

                lbl_valor = QLabel(
                    texto
                )

                lbl_valor.setFixedHeight(
                    ALTURA_CELDA
                )

                lbl_valor.setAlignment(
                    Qt.AlignmentFlag.AlignCenter
                )

                lbl_valor.setStyleSheet("""
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

                grid.addWidget(
                    lbl_valor,
                    row,
                    0
                )

            layout.addLayout(grid)

            # ------------------------------------------------------
            # CORCHETE DERECHO
            # ------------------------------------------------------

            try:

                bracket_right = BracketWidget(
                    is_left=False
                )

                layout.addWidget(
                    bracket_right
                )

            except NameError:

                bracket_right = QLabel("]")

                bracket_right.setStyleSheet("""
                    color: #0F172A;
                    font-size: 38px;
                    font-weight: 300;
                    font-family: 'Courier New';
                    border: none;
                    background: transparent;
                    padding: 0px;
                    margin: 0px;
                """)

                layout.addWidget(
                    bracket_right
                )

            return widget

        # ==========================================================
        # VECTORES ORIGINALES
        # ==========================================================

        def crear_vectores_operacion_widget(
            vectores,
            simbolo
        ):

            widget = QWidget()

            widget.setStyleSheet("""
                QWidget {
                    background: transparent;
                    border: none;
                }
            """)

            layout = QHBoxLayout(widget)

            layout.setContentsMargins(
                40, 0, 0, 0
            )

            layout.setSpacing(18)

            for i, vector in enumerate(vectores):

                layout.addWidget(
                    crear_vector_widget(
                        vector
                    )
                )

                if i < len(vectores) - 1:

                    lbl_simbolo = QLabel(
                        simbolo
                    )

                    lbl_simbolo.setAlignment(
                        Qt.AlignmentFlag.AlignCenter
                    )

                    lbl_simbolo.setStyleSheet("""
                        QLabel {
                            color: #0F172A;
                            font-size: 18px;
                            font-weight: 700;
                            border: none;
                            background: transparent;
                        }
                    """)

                    layout.addWidget(
                        lbl_simbolo
                    )

            layout.addStretch()

            return widget

        # ==========================================================
        # OPERACIÓN COMPONENTE A COMPONENTE
        # ==========================================================

        def crear_componentes_widget(
            vectores,
            simbolo
        ):

            widget = QWidget()

            widget.setStyleSheet("""
                QWidget {
                    background: transparent;
                    border: none;
                }
            """)

            layout = QHBoxLayout(widget)

            layout.setContentsMargins(
                40, 0, 0, 0
            )

            layout.setSpacing(4)

            # ------------------------------------------------------
            # CORCHETE IZQUIERDO
            # ------------------------------------------------------

            try:

                bracket_left = BracketWidget(
                    is_left=True
                )

            except NameError:

                bracket_left = QLabel("[")

                bracket_left.setStyleSheet("""
                    color: #0F172A;
                    font-size: 38px;
                    font-weight: 300;
                    font-family: 'Courier New';
                    border: none;
                    background: transparent;
                """)

            layout.addWidget(
                bracket_left
            )

            # ------------------------------------------------------
            # COMPONENTES
            # ------------------------------------------------------

            grid = QGridLayout()

            grid.setVerticalSpacing(4)
            grid.setHorizontalSpacing(18)

            grid.setContentsMargins(
                0, 0, 0, 0
            )

            dimension = len(
                vectores[0]
            )

            for row in range(dimension):

                componentes = []

                for vector in vectores:

                    valor = vector[row]

                    if isinstance(
                        valor,
                        (int, float)
                    ):

                        componentes.append(
                            formatear_numero(
                                valor
                            )
                        )

                    else:

                        componentes.append(
                            str(valor)
                        )

                texto = (
                    f" {simbolo} ".join(
                        componentes
                    )
                )

                lbl = QLabel(
                    texto
                )

                lbl.setFixedHeight(24)

                lbl.setAlignment(
                    Qt.AlignmentFlag.AlignCenter
                )

                lbl.setStyleSheet("""
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

                grid.addWidget(
                    lbl,
                    row,
                    0
                )

            layout.addLayout(
                grid
            )

            # ------------------------------------------------------
            # CORCHETE DERECHO
            # ------------------------------------------------------

            try:

                bracket_right = BracketWidget(
                    is_left=False
                )

            except NameError:

                bracket_right = QLabel("]")

                bracket_right.setStyleSheet("""
                    color: #0F172A;
                    font-size: 38px;
                    font-weight: 300;
                    font-family: 'Courier New';
                    border: none;
                    background: transparent;
                """)

            layout.addWidget(
                bracket_right
            )

            layout.addStretch()

            return widget

        # ==========================================================
        # CREAR UNA TARJETA DE PASO
        # ==========================================================

        def crear_card_paso(
            numero,
            titulo,
            etiqueta,
            contenido_widget
        ):

            card_step = QFrame()

            card_step.setObjectName(
                "CardStepOperacion"
            )

            card_step.setStyleSheet("""
                QFrame#CardStepOperacion {
                    background-color: #FFFFFF;
                    border: 1px solid #E2E8F0;
                    border-radius: 12px;
                }
            """)

            step_layout = QVBoxLayout(
                card_step
            )

            step_layout.setContentsMargins(
                16, 16, 16, 16
            )

            step_layout.setSpacing(12)

            # ------------------------------------------------------
            # HEADER DEL PASO
            # ------------------------------------------------------

            header_step = QHBoxLayout()

            header_step.setContentsMargins(
                0, 0, 0, 0
            )

            header_step.setSpacing(12)

            # Número

            lbl_num = QLabel(
                str(numero)
            )

            lbl_num.setObjectName(
                "CirculoPasoOperacion"
            )

            lbl_num.setFixedSize(
                28, 28
            )

            lbl_num.setAlignment(
                Qt.AlignmentFlag.AlignCenter
            )

            lbl_num.setStyleSheet("""
                QLabel#CirculoPasoOperacion {
                    background-color: #EEF2FF;
                    color: #4F46E5;
                    font-weight: 700;
                    font-size: 13px;
                    border-radius: 14px;
                    border: none;
                }
            """)

            # Columna de textos

            vbox_textos = QVBoxLayout()

            vbox_textos.setContentsMargins(
                0, 0, 0, 0
            )

            vbox_textos.setSpacing(6)

            lbl_titulo = QLabel(
                titulo
            )

            lbl_titulo.setStyleSheet("""
                QLabel {
                    color: #64748B;
                    font-size: 10px;
                    font-weight: 700;
                    letter-spacing: 0.5px;
                    border: none;
                    background: transparent;
                }
            """)

            vbox_textos.addWidget(
                lbl_titulo
            )

            # ------------------------------------------------------
            # BADGE
            # ------------------------------------------------------

            if etiqueta:

                hbox_badge = QHBoxLayout()

                hbox_badge.setContentsMargins(
                    0, 0, 0, 0
                )

                lbl_etiqueta = QLabel(
                    etiqueta
                )

                lbl_etiqueta.setStyleSheet("""
                    QLabel {
                        background-color: #F8FAFC;
                        color: #0F172A;
                        font-family: 'JetBrains Mono',
                                    'Consolas',
                                    monospace;
                        font-weight: 600;
                        font-size: 13px;
                        padding: 6px 12px;
                        border-radius: 8px;
                        border: 1px solid #F1F5F9;
                    }
                """)

                hbox_badge.addWidget(
                    lbl_etiqueta
                )

                hbox_badge.addStretch()

                vbox_textos.addLayout(
                    hbox_badge
                )

            header_step.addWidget(
                lbl_num,
                alignment=Qt.AlignmentFlag.AlignTop
            )

            header_step.addLayout(
                vbox_textos
            )

            header_step.addStretch()

            step_layout.addLayout(
                header_step
            )

            # ------------------------------------------------------
            # CONTENIDO
            # ------------------------------------------------------

            step_layout.addWidget(
                contenido_widget
            )

            return card_step

        # ==========================================================
        # SUMA
        # ==========================================================

        if operacion == "Sumar" and len(vectores) >= 2:

            nombre_operacion = crear_nombre_operacion(
                "+"
            )

            # ------------------------------------------------------
            # PASO 1
            # ------------------------------------------------------

            paso1 = crear_vectores_operacion_widget(
                vectores,
                "+"
            )

            card1 = crear_card_paso(
                1,
                "OPERACIÓN VECTORIAL",
                nombre_operacion,
                paso1
            )

            body_layout.addWidget(
                card1
            )

            # ------------------------------------------------------
            # PASO 2
            # ------------------------------------------------------

            componentes = crear_componentes_widget(
                vectores,
                "+"
            )

            card2 = crear_card_paso(
                2,
                "OPERACIÓN COMPONENTE A COMPONENTE",
                nombre_operacion,
                componentes
            )

            body_layout.addWidget(
                card2
            )

            # ------------------------------------------------------
            # PASO 3
            # ------------------------------------------------------

            resultado_widget = crear_vector_widget(
                resultado_vector
            )

            resultado_wrapper = QWidget()

            resultado_wrapper.setStyleSheet("""
                QWidget {
                    background: transparent;
                    border: none;
                }
            """)

            resultado_layout = QHBoxLayout(
                resultado_wrapper
            )

            resultado_layout.setContentsMargins(
                40, 0, 0, 0
            )

            resultado_layout.addWidget(
                resultado_widget
            )

            resultado_layout.addStretch()

            card3 = crear_card_paso(
                3,
                "RESULTADO",
                None,
                resultado_wrapper
            )

            body_layout.addWidget(
                card3
            )

        # ==========================================================
        # RESTA
        # ==========================================================

        elif operacion == "Restar" and len(vectores) >= 2:

            nombre_operacion = crear_nombre_operacion(
                "−"
            )

            # ------------------------------------------------------
            # PASO 1
            # ------------------------------------------------------

            paso1 = crear_vectores_operacion_widget(
                vectores,
                "−"
            )

            card1 = crear_card_paso(
                1,
                "OPERACIÓN VECTORIAL",
                nombre_operacion,
                paso1
            )

            body_layout.addWidget(
                card1
            )

            # ------------------------------------------------------
            # PASO 2
            # ------------------------------------------------------

            componentes = crear_componentes_widget(
                vectores,
                "−"
            )

            card2 = crear_card_paso(
                2,
                "OPERACIÓN COMPONENTE A COMPONENTE",
                nombre_operacion,
                componentes
            )

            body_layout.addWidget(
                card2
            )

            # ------------------------------------------------------
            # PASO 3
            # ------------------------------------------------------

            resultado_widget = crear_vector_widget(
                resultado_vector
            )

            resultado_wrapper = QWidget()

            resultado_wrapper.setStyleSheet("""
                QWidget {
                    background: transparent;
                    border: none;
                }
            """)

            resultado_layout = QHBoxLayout(
                resultado_wrapper
            )

            resultado_layout.setContentsMargins(
                40, 0, 0, 0
            )

            resultado_layout.addWidget(
                resultado_widget
            )

            resultado_layout.addStretch()

            card3 = crear_card_paso(
                3,
                "RESULTADO",
                None,
                resultado_wrapper
            )

            body_layout.addWidget(
                card3
            )

        # ==========================================================
        # ESCALAR
        # ==========================================================

        elif operacion == "Escalar":

            if vector_original is None:
                vector_original = []

            etiqueta = (
                f"{formatear_numero(escalar)} · v(1)"
            )

            # ------------------------------------------------------
            # PASO 1
            # ------------------------------------------------------

            vector_original_widget = crear_vector_widget(
                vector_original
            )

            wrapper1 = QWidget()

            wrapper1.setStyleSheet("""
                QWidget {
                    background: transparent;
                    border: none;
                }
            """)

            layout1 = QHBoxLayout(wrapper1)

            layout1.setContentsMargins(
                40, 0, 0, 0
            )

            layout1.addWidget(
                vector_original_widget
            )

            layout1.addStretch()

            card1 = crear_card_paso(
                1,
                "OPERACIÓN VECTORIAL",
                etiqueta,
                wrapper1
            )

            body_layout.addWidget(
                card1
            )

            # ------------------------------------------------------
            # PASO 2
            # ------------------------------------------------------

            componentes = []

            for valor in vector_original:

                if isinstance(
                    valor,
                    (int, float)
                ):

                    valor_txt = formatear_numero(
                        valor
                    )

                else:

                    valor_txt = str(valor)

                componentes.append(
                    f"{formatear_numero(escalar)} · "
                    f"{valor_txt}"
                )

            comp_widget = QWidget()

            comp_widget.setStyleSheet("""
                QWidget {
                    background: transparent;
                    border: none;
                }
            """)

            comp_layout = QHBoxLayout(
                comp_widget
            )

            comp_layout.setContentsMargins(
                40, 0, 0, 0
            )

            try:

                comp_layout.addWidget(
                    BracketWidget(
                        is_left=True
                    )
                )

            except NameError:

                bracket = QLabel("[")
                bracket.setStyleSheet("""
                    color: #0F172A;
                    font-size: 38px;
                    font-family: 'Courier New';
                    border: none;
                    background: transparent;
                """)

                comp_layout.addWidget(
                    bracket
                )

            grid = QGridLayout()

            grid.setVerticalSpacing(4)
            grid.setHorizontalSpacing(18)

            for row, texto in enumerate(componentes):

                lbl = QLabel(
                    texto
                )

                lbl.setFixedHeight(24)

                lbl.setAlignment(
                    Qt.AlignmentFlag.AlignCenter
                )

                lbl.setStyleSheet("""
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

                grid.addWidget(
                    lbl,
                    row,
                    0
                )

            comp_layout.addLayout(
                grid
            )

            try:

                comp_layout.addWidget(
                    BracketWidget(
                        is_left=False
                    )
                )

            except NameError:

                bracket = QLabel("]")
                bracket.setStyleSheet("""
                    color: #0F172A;
                    font-size: 38px;
                    font-family: 'Courier New';
                    border: none;
                    background: transparent;
                """)

                comp_layout.addWidget(
                    bracket
                )

            comp_layout.addStretch()

            card2 = crear_card_paso(
                2,
                "OPERACIÓN COMPONENTE A COMPONENTE",
                etiqueta,
                comp_widget
            )

            body_layout.addWidget(
                card2
            )

            # ------------------------------------------------------
            # PASO 3
            # ------------------------------------------------------

            resultado_widget = crear_vector_widget(
                resultado_vector
            )

            wrapper3 = QWidget()

            wrapper3.setStyleSheet("""
                QWidget {
                    background: transparent;
                    border: none;
                }
            """)

            layout3 = QHBoxLayout(wrapper3)

            layout3.setContentsMargins(
                40, 0, 0, 0
            )

            layout3.addWidget(
                resultado_widget
            )

            layout3.addStretch()

            card3 = crear_card_paso(
                3,
                "RESULTADO",
                None,
                wrapper3
            )

            body_layout.addWidget(
                card3
            )

        # ==========================================================
        # SIN DATOS
        # ==========================================================

        else:

            lbl_vacio = QLabel(
                "No hay información del proceso para mostrar."
            )

            lbl_vacio.setStyleSheet("""
                QLabel {
                    color: #64748B;
                    font-size: 13px;
                    font-style: italic;
                    border: none;
                    background: transparent;
                }
            """)

            body_layout.addWidget(
                lbl_vacio
            )

        # ==========================================================
        # AGREGAR BODY
        # ==========================================================

        layout_principal.addWidget(
            body_widget
        )

        # ==========================================================
        # CONTRAER / EXPANDIR
        # ==========================================================

        def _toggle():

            if body_widget.isVisible():

                body_widget.hide()
                btn_toggle.setText("+")

            else:

                body_widget.show()
                btn_toggle.setText("−")

        btn_toggle.clicked.connect(
            _toggle
        )

        return card

    def _crear_card_proceso_eliminacion(self, resultado):
        """
        Construye la tarjeta desplegable 'Proceso de eliminación'
        siguiendo el mismo diseño visual utilizado en vista_matriz.
        """

        # ==========================================================
        # TARJETA PRINCIPAL
        # ==========================================================

        card = QFrame()
        card.setObjectName("CardProcesoEliminacion")

        card.setStyleSheet("""
            QFrame#CardProcesoEliminacion {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 12px;
            }
        """)

        layout_principal = QVBoxLayout(card)

        layout_principal.setContentsMargins(
            20, 16, 20, 20
        )

        layout_principal.setSpacing(12)

        # ==========================================================
        # CABECERA
        # ==========================================================

        header_widget = QWidget()

        header_layout = QHBoxLayout(
            header_widget
        )

        header_layout.setContentsMargins(
            0, 0, 0, 0
        )

        lbl_title = QLabel(
            "Proceso de eliminación"
        )

        lbl_title.setStyleSheet("""
            color: #0F172A;
            font-size: 15px;
            font-weight: 700;
            border: none;
        """)

        btn_toggle = QPushButton("−")

        btn_toggle.setFixedSize(
            24, 24
        )

        btn_toggle.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                color: #64748B;
                font-size: 16px;
                font-weight: bold;
            }

            QPushButton:hover {
                color: #0F172A;
            }
        """)

        header_layout.addWidget(
            lbl_title
        )

        header_layout.addStretch()

        header_layout.addWidget(
            btn_toggle
        )

        layout_principal.addWidget(
            header_widget
        )

        # ==========================================================
        # CONTENIDO DESPLEGABLE
        # ==========================================================

        body_widget = QWidget()

        body_layout = QVBoxLayout(
            body_widget
        )

        body_layout.setContentsMargins(
            0, 10, 0, 10
        )

        body_layout.setSpacing(
            16
        )

        # ==========================================================
        # OBTENER PASOS
        # ==========================================================

        pasos = resultado.get(
            "proceso",
            []
        )

        if not pasos:

            lbl_vacio = QLabel(
                "No hay pasos de eliminación para mostrar."
            )

            lbl_vacio.setStyleSheet("""
                color: #64748B;
                font-size: 13px;
                font-style: italic;
                padding: 12px;
                border: none;
            """)

            body_layout.addWidget(
                lbl_vacio
            )

        else:

            # ======================================================
            # CONTENEDOR DE PASOS
            # ======================================================

            container_pasos = QWidget()

            layout_pasos = QVBoxLayout(
                container_pasos
            )

            layout_pasos.setContentsMargins(
                0, 0, 0, 0
            )

            layout_pasos.setSpacing(
                16
            )

            total_pasos = len(pasos)

            # ======================================================
            # RECORRER PASOS
            # ======================================================

            for idx, paso in enumerate(
                pasos,
                start=1
            ):

                # --------------------------------------------------
                # DATOS DEL PASO
                # --------------------------------------------------

                if isinstance(paso, str):

                    operacion_txt = paso
                    matriz_paso = []

                elif isinstance(paso, dict):

                    operacion_txt = str(
                        paso.get(
                            "operacion"
                        )
                        or paso.get(
                            "descripcion"
                        )
                        or f"Paso {idx}"
                    )

                    matriz_paso = paso.get(
                        "matriz",
                        []
                    )

                else:

                    operacion_txt = str(
                        paso
                    )

                    matriz_paso = []

                # --------------------------------------------------
                # CARD INDIVIDUAL DEL PASO
                # --------------------------------------------------

                card_step = QFrame()

                card_step.setObjectName(
                    "CardStep"
                )

                card_step.setStyleSheet("""
                    QFrame#CardStep {
                        background-color: #FFFFFF;
                        border: 1px solid #E2E8F0;
                        border-radius: 12px;
                    }
                """)

                step_layout = QVBoxLayout(
                    card_step
                )

                step_layout.setContentsMargins(
                    16, 16, 16, 16
                )

                step_layout.setSpacing(
                    12
                )

                # --------------------------------------------------
                # ¿ES EL ÚLTIMO PASO?
                # --------------------------------------------------

                es_ultimo_paso = (
                    idx == total_pasos
                )

                # ==================================================
                # ENCABEZADO DEL PASO
                # ==================================================

                header_step = QHBoxLayout()

                header_step.setContentsMargins(
                    0, 0, 0, 0
                )

                header_step.setSpacing(
                    12
                )

                # --------------------------------------------------
                # CÍRCULO DEL NÚMERO
                # --------------------------------------------------

                lbl_num = QLabel(
                    str(idx)
                )

                lbl_num.setObjectName(
                    "CirculoPaso"
                )

                lbl_num.setFixedSize(
                    28, 28
                )

                lbl_num.setAlignment(
                    Qt.AlignmentFlag.AlignCenter
                )

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

                # --------------------------------------------------
                # COLUMNA DE TEXTOS
                # --------------------------------------------------

                vbox_textos = QVBoxLayout()

                vbox_textos.setContentsMargins(
                    0, 0, 0, 0
                )

                vbox_textos.setSpacing(
                    6
                )

                # --------------------------------------------------
                # TÍTULO
                # --------------------------------------------------

                if es_ultimo_paso:

                    lbl_sub = QLabel(
                        "FORMA ESCALONADA REDUCIDA FINAL"
                    )

                    lbl_sub.setStyleSheet("""
                        color: #4F46E5;
                        font-size: 10px;
                        font-weight: 700;
                        letter-spacing: 0.5px;
                        border: none;
                        background: transparent;
                    """)

                else:

                    lbl_sub = QLabel(
                        "OPERACIÓN ELEMENTAL POR FILAS"
                    )

                    lbl_sub.setStyleSheet("""
                        color: #64748B;
                        font-size: 10px;
                        font-weight: 700;
                        letter-spacing: 0.5px;
                        border: none;
                        background: transparent;
                    """)

                vbox_textos.addWidget(
                    lbl_sub
                )

                # --------------------------------------------------
                # BADGE DE LA OPERACIÓN
                # --------------------------------------------------

                if not es_ultimo_paso:

                    hbox_badge = QHBoxLayout()

                    hbox_badge.setContentsMargins(
                        0, 0, 0, 0
                    )

                    lbl_op = QLabel(
                        operacion_txt
                    )

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

                    hbox_badge.addWidget(
                        lbl_op
                    )

                    hbox_badge.addStretch()

                    vbox_textos.addLayout(
                        hbox_badge
                    )

                # --------------------------------------------------
                # ARMAR ENCABEZADO
                # --------------------------------------------------

                header_step.addWidget(
                    lbl_num,
                    alignment=Qt.AlignmentFlag.AlignTop
                )

                header_step.addLayout(
                    vbox_textos
                )

                header_step.addStretch()

                step_layout.addLayout(
                    header_step
                )

                # ==================================================
                # MATRIZ DEL PASO
                # ==================================================

                if matriz_paso and len(matriz_paso) > 0:

                    num_eqs = len(
                        matriz_paso
                    )

                    num_vars = (
                        len(matriz_paso[0]) - 1
                    )

                    # ------------------------------------------------
                    # CONTENEDOR DE LA MATRIZ
                    # ------------------------------------------------

                    matriz_widget = QWidget()

                    matriz_widget.setSizePolicy(
                        QSizePolicy.Policy.Maximum,
                        QSizePolicy.Policy.Maximum
                    )

                    matriz_wrapper = QHBoxLayout(
                        matriz_widget
                    )

                    matriz_wrapper.setContentsMargins(
                        0, 0, 0, 0
                    )

                    matriz_wrapper.setSpacing(
                        4
                    )

                    # ------------------------------------------------
                    # CORCHETE IZQUIERDO
                    # ------------------------------------------------

                    if 'BracketWidget' in globals() or hasattr(
                        self,
                        'BracketWidget'
                    ):

                        matriz_wrapper.addWidget(
                            BracketWidget(
                                is_left=True
                            )
                        )

                    # ------------------------------------------------
                    # GRID
                    # ------------------------------------------------

                    grid_numbers = QGridLayout()

                    grid_numbers.setVerticalSpacing(
                        4
                    )

                    grid_numbers.setHorizontalSpacing(
                        18
                    )

                    grid_numbers.setContentsMargins(
                        0, 0, 0, 0
                    )

                    ALTURA_CELDA = 24

                    # ------------------------------------------------
                    # COMPONENTES DE LA MATRIZ
                    # ------------------------------------------------

                    for r in range(
                        num_eqs
                    ):

                        # --------------------------------------------
                        # COEFICIENTES
                        # --------------------------------------------

                        for c in range(
                            num_vars
                        ):

                            val_raw = (
                                matriz_paso[r][c]
                            )

                            if isinstance(
                                val_raw,
                                (int, float)
                            ):

                                val_str = (
                                    formatear_numero(
                                        val_raw
                                    )
                                )

                            else:

                                val_str = str(
                                    val_raw
                                )

                            lbl_cell = QLabel(
                                val_str
                            )

                            lbl_cell.setFixedHeight(
                                ALTURA_CELDA
                            )

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

                            lbl_cell.setAlignment(
                                Qt.AlignmentFlag.AlignCenter
                            )

                            grid_numbers.addWidget(
                                lbl_cell,
                                r,
                                c
                            )

                        # --------------------------------------------
                        # TÉRMINO INDEPENDIENTE
                        # --------------------------------------------

                        val_b_raw = (
                            matriz_paso[r][-1]
                        )

                        if isinstance(
                            val_b_raw,
                            (int, float)
                        ):

                            val_b_str = (
                                formatear_numero(
                                    val_b_raw
                                )
                            )

                        else:

                            val_b_str = str(
                                val_b_raw
                            )

                        lbl_b = QLabel(
                            val_b_str
                        )

                        lbl_b.setFixedHeight(
                            ALTURA_CELDA
                        )

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

                        lbl_b.setAlignment(
                            Qt.AlignmentFlag.AlignCenter
                        )

                        grid_numbers.addWidget(
                            lbl_b,
                            r,
                            num_vars + 1
                        )

                    # ------------------------------------------------
                    # LÍNEA DIVISORIA
                    # ------------------------------------------------

                    line = QFrame()

                    line.setFrameShape(
                        QFrame.Shape.VLine
                    )

                    line.setStyleSheet("""
                        background-color: #E2E8F0;
                        max-width: 1px;
                        border: none;
                    """)

                    grid_numbers.addWidget(
                        line,
                        0,
                        num_vars,
                        num_eqs,
                        1
                    )

                    matriz_wrapper.addLayout(
                        grid_numbers
                    )

                    # ------------------------------------------------
                    # CORCHETE DERECHO
                    # ------------------------------------------------

                    if 'BracketWidget' in globals() or hasattr(
                        self,
                        'BracketWidget'
                    ):

                        matriz_wrapper.addWidget(
                            BracketWidget(
                                is_left=False
                            )
                        )

                    # ------------------------------------------------
                    # ALINEACIÓN
                    #
                    # 28 px círculo + 12 px separación
                    # = 40 px
                    # ------------------------------------------------

                    container_matriz_align = QHBoxLayout()

                    container_matriz_align.setContentsMargins(
                        40, 0, 0, 0
                    )

                    container_matriz_align.addWidget(
                        matriz_widget
                    )

                    container_matriz_align.addStretch()

                    step_layout.addLayout(
                        container_matriz_align
                    )

                # ==================================================
                # AGREGAR PASO
                # ==================================================

                layout_pasos.addWidget(
                    card_step
                )

            body_layout.addWidget(
                container_pasos
            )

        # ==========================================================
        # AGREGAR BODY
        # ==========================================================

        layout_principal.addWidget(
            body_widget
        )

        # ==========================================================
        # CONTRAER / EXPANDIR
        # ==========================================================

        def _toggle():

            if body_widget.isVisible():

                body_widget.hide()

                btn_toggle.setText(
                    "+"
                )

            else:

                body_widget.show()

                btn_toggle.setText(
                    "−"
                )

        btn_toggle.clicked.connect(
            _toggle
        )

        return card
    def _crear_card_solucion(self):
        """
        Crea la tarjeta desplegable de Solución.
        El contenido se llena posteriormente mediante
        renderizar_tarjeta_solucion().
        """

        card = QFrame()
        card.setObjectName("CardSolucion")

        card.setStyleSheet("""
            QFrame#CardSolucion {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 12px;
            }
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(0)

        # ---------------------------------------------------------
        # ENCABEZADO
        # ---------------------------------------------------------

        header = QHBoxLayout()
        header.setContentsMargins(0, 0, 0, 0)

        titulo = QLabel("Solución")

        titulo.setStyleSheet("""
            color: #0F172A;
            font-size: 16px;
            font-weight: 700;
            border: none;
            background: transparent;
        """)

        btn_toggle = QPushButton("−")

        btn_toggle.setFixedSize(24, 24)

        btn_toggle.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        btn_toggle.setStyleSheet("""
            QPushButton {
                color: #64748B;
                font-size: 18px;
                font-weight: 600;
                border: none;
                background: transparent;
            }

            QPushButton:hover {
                color: #0F172A;
            }
        """)

        header.addWidget(titulo)
        header.addStretch()
        header.addWidget(btn_toggle)

        layout.addLayout(header)

        # ---------------------------------------------------------
        # CONTENIDO
        # ---------------------------------------------------------

        content_widget = QWidget()

        content_widget.setStyleSheet("""
            QWidget {
                border: none;
                background: transparent;
            }
        """)

        content_layout = QVBoxLayout(content_widget)

        content_layout.setContentsMargins(
            0, 20, 0, 0
        )

        content_layout.setSpacing(16)

        layout.addWidget(content_widget)

        # ---------------------------------------------------------
        # DATOS PARA EL CONTROL DEL DESPLIEGUE
        # ---------------------------------------------------------

        card.content_widget = content_widget
        card.btn_toggle = btn_toggle
        card.is_expanded = True

        def toggle():

            card.is_expanded = not card.is_expanded

            content_widget.setVisible(
                card.is_expanded
            )

            btn_toggle.setText(
                "−" if card.is_expanded else "+"
            )

        btn_toggle.clicked.connect(toggle)

        return card
    def renderizar_tarjeta_solucion(self, resultado):
        """
        Renderiza la tarjeta Solución.

        Para Combinación lineal:
            - Variables básicas
            - Variables libres
            - Valores de los coeficientes
            - Verificación

        Para Sumar, Restar y Escalar:
            - Únicamente muestra el vector resultante.
        """

        if not hasattr(self, "card_solucion") or not self.card_solucion:
            return

        # ============================================================
        # CONTENEDOR INTERNO
        # ============================================================

        contenedor = self.card_solucion.content_widget

        layout_principal = contenedor.layout()

        if not layout_principal:
            layout_principal = QVBoxLayout(contenedor)
            contenedor.setLayout(layout_principal)

        # Limpiar contenido anterior
        while layout_principal.count():

            item = layout_principal.takeAt(0)

            widget = item.widget()

            if widget:
                widget.deleteLater()

        layout_principal.setSpacing(16)

        # ============================================================
        # OPERACIÓN
        # ============================================================

        operacion = resultado.get(
            "operacion",
            ""
        )

        # ============================================================
        # OPERACIONES VECTORIALES SIMPLES
        # ============================================================

        if operacion in (
            "Sumar",
            "Restar",
            "Escalar"
        ):

            vector_resultado = resultado.get(
                "resultado"
            )

            if vector_resultado is None:
                return

            # --------------------------------------------------------
            # TÍTULO
            # --------------------------------------------------------

            lbl_resultado = QLabel("RESULTADO")

            lbl_resultado.setStyleSheet("""
                color: #64748B;
                font-weight: 700;
                font-size: 11px;
                letter-spacing: 0.5px;
                border: none;
            """)

            layout_principal.addWidget(
                lbl_resultado
            )

            # --------------------------------------------------------
            # VECTOR RESULTANTE
            # --------------------------------------------------------

            vector_frame = QFrame()

            vector_frame.setObjectName(
                "VectorResultado"
            )

            vector_frame.setStyleSheet("""
                QFrame#VectorResultado {
                    background-color: #FFFFFF;
                    border: 1px solid #E2E8F0;
                    border-radius: 12px;
                }
            """)

            vector_layout = QHBoxLayout(
                vector_frame
            )

            vector_layout.setContentsMargins(
                20, 14, 20, 14
            )

            vector_layout.setSpacing(4)

            # Corchete izquierdo
            bracket_left = QLabel("[")

            bracket_left.setStyleSheet("""
                color: #0F172A;
                font-size: 42px;
                font-weight: 300;
                font-family: 'Courier New';
                border: none;
                background: transparent;
            """)

            vector_layout.addWidget(
                bracket_left
            )

            # Componentes
            componentes_layout = QVBoxLayout()

            componentes_layout.setSpacing(8)
            componentes_layout.setContentsMargins(
                8, 0, 8, 0
            )

            for valor in vector_resultado:

                lbl_valor = QLabel(
                    formatear_numero(valor)
                )

                lbl_valor.setAlignment(
                    Qt.AlignmentFlag.AlignCenter
                )

                lbl_valor.setStyleSheet("""
                    color: #0F172A;
                    font-size: 18px;
                    font-weight: 700;
                    font-family: 'Consolas', monospace;
                    border: none;
                    background: transparent;
                """)

                componentes_layout.addWidget(
                    lbl_valor
                )

            vector_layout.addLayout(
                componentes_layout
            )

            # Corchete derecho
            bracket_right = QLabel("]")

            bracket_right.setStyleSheet("""
                color: #0F172A;
                font-size: 42px;
                font-weight: 300;
                font-family: 'Courier New';
                border: none;
                background: transparent;
            """)

            vector_layout.addWidget(
                bracket_right
            )

            vector_layout.addStretch()

            layout_principal.addWidget(
                vector_frame
            )

        # ============================================================
        # COMBINACIÓN LINEAL
        # ============================================================

        elif operacion == "Combinacion lineal":

            self._renderizar_solucion_combinacion_lineal(
                resultado,
                layout_principal
            )

        # ============================================================
        # EXPANDIR TARJETA
        # ============================================================

        self.card_solucion.is_expanded = True
        self.card_solucion.content_widget.setVisible(True)
        self.card_solucion.btn_toggle.setText("−")

    def _renderizar_solucion_combinacion_lineal(
    self,
    resultado,
    layout_principal
):
        """
        Renderiza la solución de combinación lineal
        siguiendo el diseño de vista_matriz.
        """

        # ============================================================
        # SUBÍNDICES
        # ============================================================

        def sub(i):

            digitos = [
                "₀", "₁", "₂", "₃", "₄",
                "₅", "₆", "₇", "₈", "₉"
            ]

            return "".join(
                digitos[int(d)]
                for d in str(i + 1)
            )

        # ============================================================
        # DATOS
        # ============================================================

        tipo = resultado.get(
            "tipo"
        )

        vars_basicas = resultado.get(
            "variables_basicas",
            []
        )

        vars_libres = resultado.get(
            "variables_libres",
            []
        )

        coeficientes = resultado.get(
            "coeficientes"
        )

        solucion_parametrica = resultado.get(
            "solucion_parametrica"
        )

        # ============================================================
        # 1. VARIABLES BÁSICAS Y LIBRES
        # ============================================================

        layout_vars = QHBoxLayout()

        # ------------------------------------------------------------
        # VARIABLES BÁSICAS
        # ------------------------------------------------------------

        vbox_basicas = QVBoxLayout()

        vbox_basicas.setSpacing(8)

        lbl_basicas = QLabel(
            "VARIABLES BÁSICAS"
        )

        lbl_basicas.setStyleSheet("""
            color: #64748B;
            font-weight: 700;
            font-size: 11px;
            letter-spacing: 0.5px;
            border: none;
        """)

        vbox_basicas.addWidget(
            lbl_basicas
        )

        chips_basicas = QHBoxLayout()
        chips_basicas.setSpacing(6)

        if vars_basicas:

            for idx in vars_basicas:

                chip = QLabel(
                    f"c{sub(idx)}"
                )

                chip.setStyleSheet("""
                    background-color: #EFF6FF;
                    color: #2563EB;
                    border: 1px solid #BFDBFE;
                    border-radius: 8px;
                    padding: 4px 12px;
                    font-weight: 700;
                    font-size: 13px;
                """)

                chips_basicas.addWidget(
                    chip
                )

            chips_basicas.addStretch()

        else:

            lbl_none = QLabel(
                "Ninguna"
            )

            lbl_none.setStyleSheet("""
                color: #64748B;
                font-style: italic;
                font-size: 13px;
                border: none;
            """)

            chips_basicas.addWidget(
                lbl_none
            )

            chips_basicas.addStretch()

        vbox_basicas.addLayout(
            chips_basicas
        )

        # ------------------------------------------------------------
        # VARIABLES LIBRES
        # ------------------------------------------------------------

        vbox_libres = QVBoxLayout()

        vbox_libres.setSpacing(8)

        lbl_libres = QLabel(
            "VARIABLES LIBRES"
        )

        lbl_libres.setStyleSheet("""
            color: #64748B;
            font-weight: 700;
            font-size: 11px;
            letter-spacing: 0.5px;
            border: none;
        """)

        vbox_libres.addWidget(
            lbl_libres
        )

        chips_libres = QHBoxLayout()
        chips_libres.setSpacing(6)

        if vars_libres:

            for idx in vars_libres:

                chip = QLabel(
                    f"c{sub(idx)}"
                )

                chip.setStyleSheet("""
                    background-color: #F1F5F9;
                    color: #475569;
                    border: 1px solid #CBD5E1;
                    border-radius: 8px;
                    padding: 4px 12px;
                    font-weight: 700;
                    font-size: 13px;
                """)

                chips_libres.addWidget(
                    chip
                )

            chips_libres.addStretch()

            vbox_libres.addLayout(
                chips_libres
            )

        else:

            lbl_none = QLabel(
                "Ninguna"
            )

            lbl_none.setStyleSheet("""
                color: #64748B;
                font-style: italic;
                font-size: 13px;
                border: none;
            """)

            vbox_libres.addWidget(
                lbl_none
            )

        layout_vars.addLayout(
            vbox_basicas,
            stretch=1
        )

        layout_vars.addLayout(
            vbox_libres,
            stretch=1
        )

        layout_principal.addLayout(
            layout_vars
        )

        # ============================================================
        # 2. VALORES DE LOS COEFICIENTES
        # ============================================================

        if tipo == "unica" and coeficientes:

            vbox_valores = QVBoxLayout()

            vbox_valores.setSpacing(8)

            lbl_valores = QLabel(
                "VALORES"
            )

            lbl_valores.setStyleSheet("""
                color: #64748B;
                font-weight: 700;
                font-size: 11px;
                letter-spacing: 0.5px;
                border: none;
            """)

            vbox_valores.addWidget(
                lbl_valores
            )

            cards_layout = QHBoxLayout()

            cards_layout.setSpacing(16)

            for i, valor in enumerate(
                coeficientes
            ):

                card_val = QFrame()

                card_val.setObjectName(
                    "CardCoeficiente"
                )

                card_val.setFixedSize(
                    150,
                    70
                )

                card_val.setStyleSheet("""
                    QFrame#CardCoeficiente {
                        background-color: #FFFFFF;
                        border: 1px solid #E2E8F0;
                        border-radius: 12px;
                    }
                """)

                card_layout = QVBoxLayout(
                    card_val
                )

                card_layout.setContentsMargins(
                    12, 10, 12, 10
                )

                card_layout.setSpacing(2)

                card_layout.setAlignment(
                    Qt.AlignmentFlag.AlignCenter
                )

                lbl_c = QLabel(
                    f"c{sub(i)}"
                )

                lbl_c.setAlignment(
                    Qt.AlignmentFlag.AlignCenter
                )

                lbl_c.setStyleSheet("""
                    color: #64748B;
                    font-weight: 600;
                    font-size: 13px;
                    border: none;
                    background: transparent;
                """)

                lbl_num = QLabel(
                    formatear_numero(valor)
                )

                lbl_num.setAlignment(
                    Qt.AlignmentFlag.AlignCenter
                )

                lbl_num.setStyleSheet("""
                    color: #0F172A;
                    font-weight: 800;
                    font-size: 28px;
                    border: none;
                    background: transparent;
                """)

                card_layout.addWidget(
                    lbl_c
                )

                card_layout.addWidget(
                    lbl_num
                )

                cards_layout.addWidget(
                    card_val
                )

            cards_layout.addStretch()

            vbox_valores.addLayout(
                cards_layout
            )

            layout_principal.addLayout(
                vbox_valores
            )

        # ============================================================
        # 3. SOLUCIÓN PARAMÉTRICA
        # ============================================================

        if tipo == "infinitas" and solucion_parametrica:

            lbl_param = QLabel(
                "SOLUCIÓN PARAMÉTRICA"
            )

            lbl_param.setStyleSheet("""
                color: #64748B;
                font-weight: 700;
                font-size: 11px;
                letter-spacing: 0.5px;
                border: none;
            """)

            layout_principal.addWidget(
                lbl_param
            )

            lbl_param_value = QLabel(
                str(solucion_parametrica)
            )

            lbl_param_value.setWordWrap(
                True
            )

            lbl_param_value.setStyleSheet("""
                color: #0F172A;
                font-family: 'Consolas', monospace;
                font-size: 13px;
                background-color: #F8FAFC;
                border: 1px solid #E2E8F0;
                border-radius: 10px;
                padding: 12px;
            """)

            layout_principal.addWidget(
                lbl_param_value
            )

        # ============================================================
        # 4. VERIFICACIÓN
        # ============================================================

        if tipo == "unica" and coeficientes:

            matriz_A = resultado.get(
                "matriz_generadores",
                []
            )

            matriz_aug = resultado.get(
                "matriz_aumentada",
                []
            )

            if matriz_A and matriz_aug:

                vbox_verif = QVBoxLayout()

                vbox_verif.setSpacing(8)

                lbl_verif = QLabel(
                    "VERIFICACIÓN"
                )

                lbl_verif.setStyleSheet("""
                    color: #64748B;
                    font-weight: 700;
                    font-size: 11px;
                    letter-spacing: 0.5px;
                    border: none;
                """)

                vbox_verif.addWidget(
                    lbl_verif
                )

                frame_verif = QFrame()

                frame_verif.setObjectName(
                    "FrameVerifVectores"
                )

                frame_verif.setStyleSheet("""
                    QFrame#FrameVerifVectores {
                        background-color: #FFFFFF;
                        border: 1px solid #E2E8F0;
                        border-radius: 12px;
                    }
                """)

                verif_layout = QVBoxLayout(
                    frame_verif
                )

                verif_layout.setContentsMargins(
                    16, 8, 16, 8
                )

                verif_layout.setSpacing(0)

                for i, fila in enumerate(
                    matriz_A
                ):

                    terminos = []

                    suma = 0

                    for j, coef in enumerate(
                        coeficientes
                    ):

                        valor_vector = (
                            coef
                            * fila[j]
                        )

                        suma += valor_vector

                        terminos.append(
                            f"({formatear_numero(coef)})"
                            f"({formatear_numero(fila[j])})"
                        )

                    objetivo = matriz_aug[i][-1]

                    expresion = (
                        " + ".join(terminos)
                    )

                    operaciones = []

                    for j, coef in enumerate(
                        coeficientes
                    ):

                        operaciones.append(
                            formatear_numero(
                                coef * fila[j]
                            )
                        )

                    operaciones_txt = (
                        " + ".join(
                            operaciones
                        )
                    )

                    texto = (
                        f"{expresion} = "
                        f"{formatear_numero(objetivo)}"
                        f"   ➔   "
                        f"{operaciones_txt} = "
                        f"{formatear_numero(suma)}"
                        f"   ➔   "
                        f"{formatear_numero(suma)} = "
                        f"{formatear_numero(objetivo)}"
                    )

                    row = QFrame()

                    row.setStyleSheet(
                        "border: none; "
                        "background: transparent;"
                    )

                    row_layout = QHBoxLayout(
                        row
                    )

                    row_layout.setContentsMargins(
                        0, 10, 0, 10
                    )

                    lbl_eq = QLabel(
                        f"Ecuación {i + 1}"
                    )

                    lbl_eq.setStyleSheet("""
                        color: #0F172A;
                        font-weight: 600;
                        font-size: 13px;
                        border: none;
                    """)

                    lbl_texto = QLabel(
                        texto
                    )

                    lbl_texto.setStyleSheet("""
                        color: #475569;
                        font-size: 12px;
                        font-family: monospace;
                        border: none;
                    """)

                    badge = QLabel(
                        "✓ Correcto"
                    )

                    badge.setStyleSheet("""
                        background-color: #ECFDF5;
                        color: #059669;
                        border-radius: 10px;
                        padding: 4px 12px;
                        font-weight: 700;
                        font-size: 11px;
                        border: none;
                    """)

                    row_layout.addWidget(
                        lbl_eq
                    )

                    row_layout.addStretch()

                    row_layout.addWidget(
                        lbl_texto
                    )

                    row_layout.addSpacing(
                        15
                    )

                    row_layout.addWidget(
                        badge
                    )

                    verif_layout.addWidget(
                        row
                    )

                    if i < len(matriz_A) - 1:

                        separador = QFrame()

                        separador.setFrameShape(
                            QFrame.Shape.HLine
                        )

                        separador.setStyleSheet("""
                            background-color: #F1F5F9;
                            max-height: 1px;
                            border: none;
                        """)

                        verif_layout.addWidget(
                            separador
                        )

                vbox_verif.addWidget(
                    frame_verif
                )

                layout_principal.addLayout(
                    vbox_verif
                )

    def _mostrar_resultados(self, resultado):
        """Construye la vista de resultado mostrando únicamente el Banner de Estado."""
        # 1. Ocultar la tarjeta de captura principal y la mascota
        self.card.hide()
        if hasattr(self, "dog_main"):
            self.dog_main.hide()

        # 2. Resetear referencias y vaciar el contenedor previo de resultados
        self.card_matriz = None
        self.card_proceso = None
        self.card_solucion = None

        while self.results_layout.count():
            item = self.results_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # 3. Mostrar el contenedor de resultados
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

        # --- BANNER DE ESTADO ---

        modo = resultado.get("operacion", "")

        banner = QFrame()
        banner.setObjectName("BannerEstado")

        # =========================================================
        # OPERACIONES NORMALES
        # =========================================================

        if modo in ("Sumar", "Restar", "Escalar"):

            banner.setStyleSheet("""
                QFrame#BannerEstado {
                    background-color: #ECFDF5;
                    border: 1px solid #A7F3D0;
                    border-radius: 12px;
                    padding: 6px 16px;
                }
            """)

            color_icono = "#059669"
            titulo_estado = "Operación realizada exitosamente"
            sub_estado = "El resultado se calculó correctamente."
            texto_icono = "✓"

        # =========================================================
        # COMBINACIÓN LINEAL
        # =========================================================

        elif modo == "Combinacion lineal":

            es_combinacion = resultado.get(
                "es_combinacion",
                False
            )

            if es_combinacion:

                banner.setStyleSheet("""
                    QFrame#BannerEstado {
                        background-color: #ECFDF5;
                        border: 1px solid #A7F3D0;
                        border-radius: 12px;
                        padding: 6px 16px;
                    }
                """)

                color_icono = "#059669"
                titulo_estado = "Es combinación lineal"
                sub_estado = (
                    "El vector objetivo se puede expresar "
                    "como combinación lineal."
                )
                texto_icono = "✓"

            else:

                banner.setStyleSheet("""
                    QFrame#BannerEstado {
                        background-color: #FEF2F2;
                        border: 1px solid #FECACA;
                        border-radius: 12px;
                        padding: 6px 16px;
                    }
                """)

                color_icono = "#DC2626"
                titulo_estado = "No es combinación lineal"
                sub_estado = (
                    "El vector objetivo NO se puede expresar "
                    "como combinación lineal."
                )
                texto_icono = "✕"

        else:

            banner.setStyleSheet("""
                QFrame#BannerEstado {
                    background-color: #ECFDF5;
                    border: 1px solid #A7F3D0;
                    border-radius: 12px;
                    padding: 6px 16px;
                }
            """)

            color_icono = "#059669"
            titulo_estado = "Operación realizada exitosamente"
            sub_estado = "El resultado se calculó correctamente."
            texto_icono = "✓"
        b_layout = QHBoxLayout(banner)
        b_layout.setContentsMargins(0, 4, 0, 4)
        b_layout.setSpacing(12)

        lbl_icon = QLabel(texto_icono)
        lbl_icon.setStyleSheet(
            f"color: {color_icono}; font-size: 18px; font-weight: bold; border: none; background: transparent;"
        )
        b_layout.addWidget(lbl_icon)

        text_vbox = QVBoxLayout()
        text_vbox.setSpacing(1)
        text_vbox.setContentsMargins(0, 0, 0, 0)

        lbl_status_title = QLabel(titulo_estado)
        lbl_status_title.setStyleSheet(
            f"color: {color_icono}; font-size: 13px; font-weight: 700; border: none; background: transparent;"
        )

        lbl_status_sub = QLabel(sub_estado)
        lbl_status_sub.setStyleSheet(
            f"color: {color_icono}; font-size: 11px; border: none; background: transparent;"
        )

        text_vbox.addWidget(lbl_status_title)
        text_vbox.addWidget(lbl_status_sub)

        b_layout.addLayout(text_vbox)
        b_layout.addStretch()

        self.results_layout.addWidget(banner)
        # =========================================================
        # OPERACIONES CON VECTORES
        # =========================================================

        if modo in ("Sumar", "Restar", "Escalar"):

            # Tarjeta de proceso
            self.results_layout.addWidget(
                self._crear_card_proceso_operacion(
                    resultado
                )
            )
            
            # ---------------------------------------------------------
            # TARJETA DE SOLUCIÓN
            # ---------------------------------------------------------

            self.card_solucion = self._crear_card_solucion()

            self.results_layout.addWidget(
                self.card_solucion
            )

            self.renderizar_tarjeta_solucion(
                resultado
            )       
                    
         

        # =========================================================
        # COMBINACIÓN LINEAL
        # =========================================================

        elif modo == "Combinacion lineal":

            # Información del sistema
            card_info = self._crear_card_info_sistema(
                resultado
            )

            self.results_layout.addWidget(
                card_info
            )

            # Matriz aumentada
            if resultado.get("matriz_aumentada"):

                self.results_layout.addWidget(
                    self._crear_card_matriz_aumentada(
                        resultado
                    )
                )
            

            # Proceso de Gauss-Jordan
            self.results_layout.addWidget(
                self._crear_card_proceso_eliminacion(
                    resultado
                )
            )

            # ---------------------------------------------------------
            # TARJETA DE SOLUCIÓN
            # ---------------------------------------------------------

            self.card_solucion = self._crear_card_solucion()

            self.results_layout.addWidget(
                self.card_solucion
            )

            self.renderizar_tarjeta_solucion(
                resultado
            )
        # =========================================================
        # ECUACIÓN MATRICIAL
        # =========================================================

        elif modo == "ecuacion_matricial":

            # Información del sistema
            card_info = self._crear_card_info_sistema(
                resultado
            )

            self.results_layout.addWidget(
                card_info
            )

            # Matriz aumentada
            if resultado.get("matriz_aumentada"):

                self.results_layout.addWidget(
                    self._crear_card_matriz_aumentada(
                        resultado
                    )
                )

            # Proceso de Gauss-Jordan
            self.results_layout.addWidget(
                self._crear_card_proceso_eliminacion(
                    resultado
                )
            )