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


class VistaOperacionesMatriz(QWidget):
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

        title = QLabel("Operaciones con Matrices")
        title.setStyleSheet("font-size: 24px; font-weight: 800; color: #0F172A;")

        subtitle = QLabel("Define los componentes y realiza operaciones algebraicas.")
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
      
        self.btn_matrix_ops.setStyleSheet("""
            QPushButton {
                background-color: #2563EB;
                color: white;
                font-weight: 600;
                font-size: 13px;
                padding: 10px 22px;
                border-radius: 10px;
                border: none;
            }
            QPushButton:hover {
                background-color: #1D4ED8;
            }
        """)
        self.btn_mat_eqs.setStyleSheet("""
            QPushButton {
                background-color: #2563EB;
                color: white;
                font-weight: 600;
                font-size: 13px;
                padding: 10px 22px;
                border-radius: 10px;
                border: none;
            }
            QPushButton:hover {
                background-color: #1D4ED8;
            }
        """)    
        self.btn_matrix_ops.setStyleSheet(mode_button_active_style)
        self.btn_mat_eqs.setStyleSheet(mode_button_style)
        
               
        self.btn_matrix_ops.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_mat_eqs.setCursor(Qt.CursorShape.PointingHandCursor)

    
        mode_layout.addWidget(self.btn_matrix_ops)
        mode_layout.addWidget(self.btn_mat_eqs)
        
        mode_wrapper.addWidget(mode_container, alignment=Qt.AlignmentFlag.AlignLeft)
        card_layout.addLayout(mode_wrapper)
        
        self.stacked_layout = QStackedLayout()
  
      
    
       # VISTA 1: OPERACIONES MATRICIALES
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
        self.mops_scroll.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop
        )

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

        self.mops_container.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Fixed
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
        btn_calc_mops.setStyleSheet("""
            QPushButton {
                background-color: #2563EB;
                color: white;
                font-weight: 600;
                font-size: 13px;
                padding: 10px 22px;
                border-radius: 10px;
                border: none;
            }
            QPushButton:hover {
                background-color: #1D4ED8;
            }
        """)
        btn_calc_mops.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_calc_mops.clicked.connect(self.on_solved_clicked_mops)
        
        btn_clear_mops = QPushButton("Limpiar")
        btn_clear_mops.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF;
                color: #475569;
                font-weight: 600;
                font-size: 13px;
                padding: 10px 24px;
                border-radius: 10px;
                border: 1px solid #E2E8F0;
            }
            QPushButton:hover {
                background-color: #F8FAFC;
                color: #1E293B;
            }
        """)
        btn_clear_mops.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_clear_mops.clicked.connect(self._clear_matrix_ops_inputs)
        
        self.combo_mops_metodo = QComboBox()
        self.combo_mops_metodo.addItems([
            "Sumar",
            "Restar",
            "Escalar",
            "Multiplicar",
            "Matriz por vector",
            "Distributividad",
            "Homogeneidad",
            "Independencia columnas",
            "Asociatividad matrices",
            "Distributiva izquierda",
            "Distributiva derecha",
            "Escalar producto",
            "Identidad"
        ])
        self.combo_mops_metodo.setFixedWidth(220)
        self.combo_mops_metodo.setFixedHeight(38)
        self.combo_mops_metodo.setCurrentIndex(0)
        combo_popup_style = """
            QListView {
                background-color: #FFFFFF;
                color: #0F172A;
                border: 1px solid #CBD5E1;
                border-radius: 8px;
                padding: 4px;
                outline: 0px;
            }
            QListView::item {
                min-height: 30px;
                padding: 6px 10px;
                color: #0F172A;
                background-color: #FFFFFF;
            }
            QListView::item:selected,
            QListView::item:hover {
                background-color: #EFF6FF;
                color: #2563EB;
            }
        """
        self.combo_mops_metodo.setStyleSheet("""
            QComboBox {
                background-color: #FFFFFF;
                border: 1px solid #CBD5E1;
                border-radius: 8px;
                padding: 0px 8px;
                font-size: 13px;
                font-weight: 600;
                color: #475569;
            }

            QComboBox:focus {
                border: 1px solid #2563EB;
            }

            QComboBox QAbstractItemView {
                background-color: #FFFFFF;
                color: #0F172A;
                border: 1px solid #CBD5E1;
                border-radius: 8px;
                outline: 0px;
                padding: 4px;
                selection-background-color: #F1F5F9;
                selection-color: #2563EB;
            }

            QComboBox::drop-down {
                border: none;
                width: 22px;
            }
        """)
        self.combo_mops_metodo.view().setStyleSheet(combo_popup_style)

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
        # VISTA 2: ECUACIONES MATRICIALES (Matriz A + Vector x)
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

        tipo_box = QVBoxLayout()
        tipo_box.setSpacing(6)
        lbl_tipo = QLabel("TIPO DE SISTEMA")
        lbl_tipo.setStyleSheet("color: #64748B; font-size: 10px; font-weight: 700; letter-spacing: 0.5px; background: transparent;")
        self.combo_meqs_tipo = QComboBox()
        self.combo_meqs_tipo.addItems([
            "Ax = b",
            "Sistema homogeneo Ax = 0"
        ])
        self.combo_meqs_tipo.setFixedWidth(240)
        self.combo_meqs_tipo.setFixedHeight(38)
        self.combo_meqs_tipo.setStyleSheet(self.combo_mops_metodo.styleSheet())
        self.combo_meqs_tipo.view().setStyleSheet(combo_popup_style)
        self.combo_meqs_tipo.currentIndexChanged.connect(
            self._on_meqs_tipo_changed
        )
        for i in range(self.combo_meqs_tipo.count()):
            self.combo_meqs_tipo.setItemData(
                i,
                Qt.AlignmentFlag.AlignCenter,
                Qt.ItemDataRole.TextAlignmentRole
            )
        tipo_box.addWidget(lbl_tipo)
        tipo_box.addWidget(self.combo_meqs_tipo)

        meqs_controls.addLayout(rows_box)
        meqs_controls.addLayout(cols_box)
        meqs_controls.addLayout(vars_box)
        meqs_controls.addLayout(tipo_box)
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
        btn_calc_meqs.setStyleSheet("""
            QPushButton {
                background-color: #2563EB;
                color: white;
                font-weight: 600;
                font-size: 13px;
                padding: 10px 22px;
                border-radius: 10px;
                border: none;
            }
            QPushButton:hover {
                background-color: #1D4ED8;
            }
        """)
        btn_calc_meqs.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_calc_meqs.clicked.connect(self.on_solved_clicked_meqs)

        btn_clear_meqs = QPushButton("Limpiar")
        btn_clear_meqs.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF;
                color: #475569;
                font-weight: 600;
                font-size: 13px;
                padding: 10px 24px;
                border-radius: 10px;
                border: 1px solid #E2E8F0;
            }
            QPushButton:hover {
                background-color: #F8FAFC;
                color: #1E293B;
            }
        """)
        btn_clear_meqs.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_clear_meqs.clicked.connect(self._clear_mat_eqs_inputs)

        meqs_actions.addWidget(btn_calc_meqs)
        meqs_actions.addWidget(btn_clear_meqs)
        meqs_actions.addStretch()
        meqs_layout.addLayout(meqs_actions)


        # Conectar callbacks de los steppers
        self.stepper_meqs_rows.on_change_callback = self._rebuild_mat_eqs_grid
        self.stepper_meqs_cols.on_change_callback = self._rebuild_mat_eqs_grid
        self.stepper_meqs_vars.on_change_callback = self._rebuild_mat_eqs_grid

        self._rebuild_mat_eqs_grid()
        
        self.stacked_layout.addWidget(mat_eqs_view) 
        
        # El stacked_layout pertenece a la tarjeta
        card_layout.addLayout(self.stacked_layout)

        # Agregar la tarjeta completa al contenido principal
        content_layout.addWidget(self.card)
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

        self.btn_matrix_ops.clicked.connect(
            lambda: self._set_mode(
                0, mode_button_active_style, mode_button_style
            )
        )
      
        self.btn_mat_eqs.clicked.connect(lambda: self._set_mode(1, mode_button_active_style, mode_button_style)) 

        content_outer_layout.addWidget(centered_wrapper)
        scroll_area.setWidget(main_content)
        main_layout.addWidget(scroll_area)

        
    def _set_mode(self, index, active_style, inactive_style):
        self.stacked_layout.setCurrentIndex(index)
        if index == 0:
          
            self.btn_matrix_ops.setStyleSheet(active_style)
            self.btn_mat_eqs.setStyleSheet(inactive_style)
        else:
            self.btn_matrix_ops.setStyleSheet(inactive_style)
            self.btn_mat_eqs.setStyleSheet(active_style)
       
    def _meqs_es_homogeneo(self):
        return (
            hasattr(self, "combo_meqs_tipo")
            and "homogeneo" in self.combo_meqs_tipo.currentText().lower()
        )

    def _on_meqs_tipo_changed(self):
        es_homogeneo = self._meqs_es_homogeneo()

        self.stepper_meqs_vars.setEnabled(not es_homogeneo)
        self._rebuild_mat_eqs_grid()

    def _mops_propiedades_matriciales(self):
        return (
            "Asociatividad matrices",
            "Distributiva izquierda",
            "Distributiva derecha",
            "Escalar producto",
            "Identidad"
        )

    def _mops_matrices_requeridas(self, metodo):
        if metodo in (
            "Asociatividad matrices",
            "Distributiva izquierda",
            "Distributiva derecha"
        ):
            return 3

        if metodo == "Escalar producto":
            return 2

        if metodo == "Identidad":
            return 1

        return None

    def _set_stepper_value(self, stepper, value):
        stepper.value = value
        stepper.lbl_val.setText(str(value))

    def _on_mops_operation_changed(self):

        metodo = self.combo_mops_metodo.currentText()

        matrices_requeridas = self._mops_matrices_requeridas(metodo)
        if matrices_requeridas is not None:
            self._set_stepper_value(
                self.stepper_mops_count,
                matrices_requeridas
            )

        es_escalar = metodo in (
            "Escalar",
            "Homogeneidad",
            "Escalar producto"
        )
        usa_vector = metodo in (
            "Matriz por vector",
            "Distributividad",
            "Homogeneidad"
        )
        usa_una_matriz = (
            es_escalar
            or usa_vector
            or metodo == "Independencia columnas"
            or metodo == "Identidad"
        )

        # Mostrar escalar solamente cuando la operacion lo usa.
        self.mops_escalar_container.setVisible(
            es_escalar or metodo == "Homogeneidad"
        )

        # Cantidad de matrices no aplica para estas operaciones.
        self.stepper_mops_count.setEnabled(
            not usa_una_matriz
            and matrices_requeridas is None
        )

        # Reconstruir matrices
        self._rebuild_matrix_ops_grid()
    def _rebuild_matrix_ops_grid(self):

        # ============================================================
        # 1. GUARDAR LOS VALORES ACTUALES
        # ============================================================

        valores_actuales = []

        if hasattr(self, "mops_inputs_list"):
            for matriz in self.mops_inputs_list:

                matriz_valores = []

                for fila in matriz:
                    fila_valores = []

                    for inp in fila:
                        fila_valores.append(inp.text())

                    matriz_valores.append(fila_valores)

                valores_actuales.append(matriz_valores)

        valores_vector_u = []
        valores_vector_v = []

        if hasattr(self, "mops_vector_inputs"):
            valores_vector_u = [
                inp.text()
                for inp in self.mops_vector_inputs
            ]

        if hasattr(self, "mops_vector_v_inputs"):
            valores_vector_v = [
                inp.text()
                for inp in self.mops_vector_v_inputs
            ]

        # ============================================================
        # 2. RECREAR EL CONTENEDOR INTERNO DEL SCROLL
        # ============================================================

        old_container = self.mops_scroll.takeWidget()

        if old_container is not None:
            old_container.deleteLater()

        self.mops_container = QWidget()
        self.mops_container.setStyleSheet(
            "background-color: transparent;"
        )
        self.mops_container.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Fixed
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

        self.mops_scroll.setWidget(
            self.mops_container
        )

        # ============================================================
        # 3. DIMENSIONES
        # ============================================================

        rows = self.stepper_mops_rows.value
        cols = self.stepper_mops_cols.value

        metodo = self.combo_mops_metodo.currentText()

        matrices_requeridas = self._mops_matrices_requeridas(metodo)
        es_escalar = metodo in (
            "Escalar",
            "Homogeneidad",
            "Escalar producto"
        )
        usa_vector = metodo in (
            "Matriz por vector",
            "Distributividad",
            "Homogeneidad"
        )
        usa_una_matriz = (
            es_escalar
            or usa_vector
            or metodo == "Independencia columnas"
            or metodo == "Identidad"
        )

        # Estas operaciones usan solamente A1.
        if matrices_requeridas is not None:
            num_matrices = matrices_requeridas
        elif usa_una_matriz:
            num_matrices = 1
        else:
            num_matrices = self.stepper_mops_count.value

        # Lista nueva
        self.mops_inputs_list = []
        self.mops_vector_inputs = []
        self.mops_vector_v_inputs = []

        # ============================================================
        # 4. ESTILO
        # ============================================================

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

        input_width = 54
        input_height = 36
        grid_spacing = 8
        bracket_width = 12
        bracket_gap = 4
        matrix_spacing = 20
        label_height = 16
        label_gap = 6

        bracket_height = rows * input_height + (rows - 1) * grid_spacing
        matrix_width = (
            bracket_width * 2
            + cols * input_width
            + max(0, cols - 1) * grid_spacing
            + bracket_gap * 2
        )
        matrix_height = label_height + label_gap + bracket_height
        vector_count = (
            2
            if metodo == "Distributividad"
            else 1
            if usa_vector
            else 0
        )
        vector_bracket_height = (
            cols * input_height
            + max(0, cols - 1) * grid_spacing
        )
        vector_width = (
            bracket_width * 2
            + input_width
            + bracket_gap * 2
        )
        vector_height = (
            label_height
            + label_gap
            + vector_bracket_height
        )
        content_width = (
            num_matrices * matrix_width
            + vector_count * vector_width
            + max(0, num_matrices + vector_count - 1) * matrix_spacing
        )
        content_height = max(matrix_height, vector_height)

        # ============================================================
        # 5. CREAR A1, A2, A3...
        # ============================================================

        for m in range(num_matrices):

            mat_widget = QWidget()
            mat_widget.setStyleSheet("background-color: transparent;")
            mat_widget.setSizePolicy(
                QSizePolicy.Policy.Fixed,
                QSizePolicy.Policy.Fixed
            )

            mat_box = QVBoxLayout(mat_widget)
            mat_box.setSpacing(6)
            mat_box.setContentsMargins(0, 0, 0, 0)
            mat_box.setAlignment(Qt.AlignmentFlag.AlignTop)

            # --------------------------------------------------------
            # Etiqueta A1, A2, A3...
            # --------------------------------------------------------

            if metodo in self._mops_propiedades_matriciales():
                etiquetas_matrices = ("A", "B", "C")
                etiqueta_matriz = (
                    etiquetas_matrices[m]
                    if m < len(etiquetas_matrices)
                    else f"A<sub>{m + 1}</sub>"
                )
            else:
                etiqueta_matriz = f"A<sub>{m + 1}</sub>"

            lbl_m = QLabel(etiqueta_matriz)

            lbl_m.setAlignment(
                Qt.AlignmentFlag.AlignCenter
            )

            lbl_m.setStyleSheet("""
                color: #64748B;
                font-size: 11px;
                font-weight: 600;
                background: transparent;
            """)

            mat_box.addWidget(lbl_m)

            # --------------------------------------------------------
            # Fila de matriz
            # --------------------------------------------------------

            mat_row_layout = QHBoxLayout()
            mat_row_layout.setSpacing(4)
            mat_row_layout.setContentsMargins(0, 0, 0, 0)

            # Corchete izquierdo
            b_left = BracketWidget(is_left=True)
            b_left.setFixedHeight(bracket_height)

            # Grid
            grid = QGridLayout()
            grid.setSpacing(8)
            grid.setContentsMargins(0, 0, 0, 0)

            mat_inputs = []

            for r in range(rows):

                row_inputs = []

                for c in range(cols):

                    # Valor anterior
                    valor = "0"

                    if (
                        m < len(valores_actuales)
                        and r < len(valores_actuales[m])
                        and c < len(valores_actuales[m][r])
                    ):
                        valor = valores_actuales[m][r][c]

                    inp = QLineEdit(valor)

                    inp.setAlignment(
                        Qt.AlignmentFlag.AlignCenter
                    )

                    inp.setFixedSize(input_width, input_height)

                    inp.setStyleSheet(input_style)

                    grid.addWidget(inp, r, c)

                    row_inputs.append(inp)

                mat_inputs.append(row_inputs)

            self.mops_inputs_list.append(mat_inputs)

            # Corchete derecho
            b_right = BracketWidget(is_left=False)
            b_right.setFixedHeight(bracket_height)

            mat_row_layout.addWidget(b_left)
            mat_row_layout.addLayout(grid)
            mat_row_layout.addWidget(b_right)

            mat_box.addLayout(mat_row_layout)

            mat_widget.setFixedSize(matrix_width, matrix_height)

            self.mops_layout_inner.addWidget(mat_widget)

        # ============================================================
        # 5.1 CREAR VECTORES u / v PARA OPERACIONES MATRIZ-VECTOR
        # ============================================================

        def crear_vector_columna(
            etiqueta,
            valores_previos
        ):
            vec_widget = QWidget()
            vec_widget.setStyleSheet("background-color: transparent;")
            vec_widget.setSizePolicy(
                QSizePolicy.Policy.Fixed,
                QSizePolicy.Policy.Fixed
            )

            vec_box = QVBoxLayout(vec_widget)
            vec_box.setSpacing(6)
            vec_box.setContentsMargins(0, 0, 0, 0)
            vec_box.setAlignment(Qt.AlignmentFlag.AlignTop)

            lbl_vec = QLabel(etiqueta)
            lbl_vec.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_vec.setStyleSheet("""
                color: #64748B;
                font-size: 11px;
                font-weight: 600;
                background: transparent;
            """)
            vec_box.addWidget(lbl_vec)

            vec_row_layout = QHBoxLayout()
            vec_row_layout.setSpacing(4)
            vec_row_layout.setContentsMargins(0, 0, 0, 0)

            b_left = BracketWidget(is_left=True)
            b_left.setFixedHeight(vector_bracket_height)

            vec_inputs_col = QVBoxLayout()
            vec_inputs_col.setSpacing(grid_spacing)
            vec_inputs_col.setContentsMargins(0, 0, 0, 0)

            inputs = []

            for r in range(cols):
                valor = (
                    valores_previos[r]
                    if r < len(valores_previos)
                    else "0"
                )

                inp = QLineEdit(valor)
                inp.setAlignment(Qt.AlignmentFlag.AlignCenter)
                inp.setFixedSize(input_width, input_height)
                inp.setStyleSheet(input_style)
                vec_inputs_col.addWidget(inp)
                inputs.append(inp)

            b_right = BracketWidget(is_left=False)
            b_right.setFixedHeight(vector_bracket_height)

            vec_row_layout.addWidget(b_left)
            vec_row_layout.addLayout(vec_inputs_col)
            vec_row_layout.addWidget(b_right)

            vec_box.addLayout(vec_row_layout)
            vec_widget.setFixedSize(vector_width, vector_height)

            return vec_widget, inputs

        if usa_vector:
            etiqueta_u = "u"

            if metodo == "Matriz por vector":
                etiqueta_u = "x"

            vec_u_widget, self.mops_vector_inputs = (
                crear_vector_columna(
                    etiqueta_u,
                    valores_vector_u
                )
            )

            self.mops_layout_inner.addWidget(vec_u_widget)

        if metodo == "Distributividad":
            vec_v_widget, self.mops_vector_v_inputs = (
                crear_vector_columna(
                    "v",
                    valores_vector_v
                )
            )

            self.mops_layout_inner.addWidget(vec_v_widget)

        # ============================================================
        # 6. ESCALAR
        # ============================================================

        self.mops_escalar_container.setVisible(es_escalar)

        # ============================================================
        # 7. AJUSTAR EL CONTENEDOR DEL SCROLL
        # ============================================================

        scroll_height = content_height + 18

        self.mops_container.setFixedSize(
            content_width,
            content_height
        )

        self.mops_scroll.setFixedHeight(scroll_height)

        self.mops_container.show()
        self.mops_container.updateGeometry()
        self.mops_scroll.updateGeometry()
        self.mops_scroll.horizontalScrollBar().setValue(0)
        self.mops_scroll.viewport().update()

    def _clear_matrix_ops_inputs(self):
        for mat in self.mops_inputs_list:
            for row in mat:
                for inp in row:
                    inp.setText("0")
        for inp in getattr(self, "mops_vector_inputs", []):
            inp.setText("0")
        for inp in getattr(self, "mops_vector_v_inputs", []):
            inp.setText("0")
        self.inp_mops_escalar.setText("1")
    def _rebuild_mat_eqs_grid(self):
        # Guardar valores antes de reconstruir la grilla.
        valores_matriz = []

        if hasattr(self, "meqs_matrix_inputs"):
            for fila_inputs in self.meqs_matrix_inputs:
                valores_matriz.append([
                    inp.text()
                    for inp in fila_inputs
                ])

        valores_vector = []

        if hasattr(self, "meqs_vector_inputs"):
            valores_vector = [
                inp.text()
                for inp in self.meqs_vector_inputs
            ]

        self._clear_layout(self.meqs_layout_inner)

        rows = self.stepper_meqs_rows.value  # Filas de la Matriz A
        cols = self.stepper_meqs_cols.value  # Columnas de la Matriz A
        vars_count = self.stepper_meqs_vars.value  # Filas del Vector x
        es_homogeneo = self._meqs_es_homogeneo()
        if es_homogeneo and self.stepper_meqs_vars.value != cols:
            self.stepper_meqs_vars.value = cols
            self.stepper_meqs_vars.lbl_val.setText(str(cols))
        vector_count = rows if es_homogeneo else vars_count

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
        mat_widget = QWidget()
        mat_widget.setStyleSheet("background-color: transparent;")
        mat_widget.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Fixed
        )

        mat_box = QVBoxLayout(mat_widget)
        mat_box.setSpacing(6)
        mat_box.setContentsMargins(0, 0, 0, 0)
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
                valor = "0"

                if (
                    r < len(valores_matriz)
                    and c < len(valores_matriz[r])
                ):
                    valor = valores_matriz[r][c]

                inp = QLineEdit(valor)
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
        self.meqs_layout_inner.addWidget(mat_widget)

        # Separador horizontal entre la matriz y el vector
        self.meqs_layout_inner.addSpacing(16)

        # --- 2. VECTOR b / 0 ---
        vec_widget = QWidget()
        vec_widget.setStyleSheet("background-color: transparent;")
        vec_widget.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Fixed
        )

        vec_box = QVBoxLayout(vec_widget)
        vec_box.setSpacing(6)
        vec_box.setContentsMargins(0, 0, 0, 0)
        vec_box.setAlignment(Qt.AlignmentFlag.AlignTop)

        lbl_x = QLabel("0 fijo" if es_homogeneo else "b")
        lbl_x.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_x.setStyleSheet("color: #64748B; font-size: 11px; font-weight: 600; background: transparent;")
        vec_box.addWidget(lbl_x)

        vec_row_layout = QHBoxLayout()
        vec_row_layout.setSpacing(4)
        vec_row_layout.setContentsMargins(0, 0, 0, 0)

        vec_height = vector_count * 36 + (vector_count - 1) * 8
        b_left_vec = BracketWidget(is_left=True)
        b_left_vec.setFixedHeight(vec_height)

        vec_inputs_col = QVBoxLayout()
        vec_inputs_col.setSpacing(8)
        vec_inputs_col.setContentsMargins(0, 0, 0, 0)

        for r in range(vector_count):
            if es_homogeneo:
                valor = "0"
            else:
                valor = (
                    valores_vector[r]
                    if r < len(valores_vector)
                    else "0"
                )

            inp = QLineEdit(valor)
            inp.setAlignment(Qt.AlignmentFlag.AlignCenter)
            inp.setFixedSize(54, 36)
            inp.setReadOnly(es_homogeneo)
            input_final_style = input_style
            if es_homogeneo:
                input_final_style += """
                QLineEdit {
                    color: #64748B;
                    background-color: #F1F5F9;
                }
                """
                inp.setToolTip(
                    "En un sistema homogeneo el lado derecho es 0."
                )
            inp.setStyleSheet(input_final_style)
            vec_inputs_col.addWidget(inp)
            self.meqs_vector_inputs.append(inp)

        b_right_vec = BracketWidget(is_left=False)
        b_right_vec.setFixedHeight(vec_height)

        vec_row_layout.addWidget(b_left_vec)
        vec_row_layout.addLayout(vec_inputs_col)
        vec_row_layout.addWidget(b_right_vec)

        vec_box.addLayout(vec_row_layout)
        self.meqs_layout_inner.addWidget(vec_widget)

        self.meqs_container.adjustSize()
        self.meqs_container.updateGeometry()

    def _clear_mat_eqs_inputs(self):
        for row in self.meqs_matrix_inputs:
            for inp in row:
                inp.setText("0")
        for inp in self.meqs_vector_inputs:
            inp.setText("0")
 #
 # LOGICA PARA LA TARJETA DE SOLUCION Y CONECTAR CON EL CONTROLADOR
 #
    def _clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            child_layout = item.layout()

            if widget is not None:
                widget.deleteLater()
            elif child_layout is not None:
                self._clear_layout(child_layout)

    def _leer_float(self, inp):
        texto = inp.text().strip().replace(",", ".")
        return float(texto) if texto else 0.0

    def _leer_matrices_mops(self):
        matrices = []

        for matriz_inputs in self.mops_inputs_list:
            matriz = []

            for fila_inputs in matriz_inputs:
                fila = []

                for inp in fila_inputs:
                    fila.append(self._leer_float(inp))

                matriz.append(fila)

            matrices.append(matriz)

        return matrices

    def _leer_vector_mops(self, inputs):
        return [
            self._leer_float(inp)
            for inp in inputs
        ]

    def _leer_matriz_meqs(self):
        matriz = []

        for fila_inputs in self.meqs_matrix_inputs:
            fila = []

            for inp in fila_inputs:
                fila.append(self._leer_float(inp))

            matriz.append(fila)

        return matriz

    def _leer_vector_meqs(self):
        return [
            self._leer_float(inp)
            for inp in self.meqs_vector_inputs
        ]

    def on_solved_clicked_mops(self):
        try:
            modo = self.combo_mops_metodo.currentText()
            matrices = self._leer_matrices_mops()
            matrices_requeridas = self._mops_matrices_requeridas(modo)

            if modo in ("Sumar", "Restar", "Multiplicar") and len(matrices) < 2:
                QMessageBox.warning(
                    self,
                    "Matrices insuficientes",
                    "Debes ingresar al menos dos matrices."
                )
                return

            if (
                matrices_requeridas is not None
                and len(matrices) < matrices_requeridas
            ):
                QMessageBox.warning(
                    self,
                    "Matrices insuficientes",
                    (
                        "Esta propiedad necesita "
                        f"{matrices_requeridas} "
                        f"{'matrices' if matrices_requeridas != 1 else 'matriz'}."
                    )
                )
                return

            if modo in (
                "Matriz por vector",
                "Distributividad",
                "Homogeneidad",
                "Independencia columnas",
                "Identidad"
            ) and not matrices:
                QMessageBox.warning(
                    self,
                    "Sin matriz",
                    "Debes ingresar la matriz A."
                )
                return

            if modo == "Sumar":
                resultado = ControladorVectores.sumar_matrices(matrices)

            elif modo == "Restar":
                resultado = ControladorVectores.restar_matrices(matrices)

            elif modo == "Escalar":
                if not matrices:
                    QMessageBox.warning(
                        self,
                        "Sin matriz",
                        "Debes ingresar una matriz."
                    )
                    return

                escalar = self._leer_float(self.inp_mops_escalar)
                resultado = ControladorVectores.multiplicar_matriz_escalar(
                    matrices[0],
                    escalar
                )

            elif modo == "Multiplicar":
                resultado = ControladorVectores.multiplicar_matrices(matrices)

            elif modo == "Matriz por vector":
                vector = self._leer_vector_mops(
                    self.mops_vector_inputs
                )
                resultado = ControladorVectores.multiplicar_matriz_vector(
                    matrices[0],
                    vector
                )

            elif modo == "Distributividad":
                u = self._leer_vector_mops(
                    self.mops_vector_inputs
                )
                v = self._leer_vector_mops(
                    self.mops_vector_v_inputs
                )
                resultado = (
                    ControladorVectores
                    .verificar_distributividad_matriz_vector(
                        matrices[0],
                        u,
                        v
                    )
                )

            elif modo == "Homogeneidad":
                u = self._leer_vector_mops(
                    self.mops_vector_inputs
                )
                escalar = self._leer_float(self.inp_mops_escalar)
                resultado = (
                    ControladorVectores
                    .verificar_homogeneidad_matriz_vector(
                        matrices[0],
                        u,
                        escalar
                    )
                )

            elif modo == "Independencia columnas":
                resultado = (
                    ControladorVectores
                    .evaluar_independencia_columnas(
                        matrices[0]
                    )
                )

            elif modo == "Asociatividad matrices":
                resultado = (
                    ControladorVectores
                    .verificar_asociatividad_matrices(
                        matrices[0],
                        matrices[1],
                        matrices[2]
                    )
                )

            elif modo == "Distributiva izquierda":
                resultado = (
                    ControladorVectores
                    .verificar_distributividad_izquierda_matrices(
                        matrices[0],
                        matrices[1],
                        matrices[2]
                    )
                )

            elif modo == "Distributiva derecha":
                resultado = (
                    ControladorVectores
                    .verificar_distributividad_derecha_matrices(
                        matrices[0],
                        matrices[1],
                        matrices[2]
                    )
                )

            elif modo == "Escalar producto":
                escalar = self._leer_float(self.inp_mops_escalar)
                resultado = (
                    ControladorVectores
                    .verificar_escalar_producto_matrices(
                        matrices[0],
                        matrices[1],
                        escalar
                    )
                )

            elif modo == "Identidad":
                resultado = (
                    ControladorVectores
                    .verificar_identidad_matrices(
                        matrices[0]
                    )
                )

            else:
                QMessageBox.warning(
                    self,
                    "Operacion desconocida",
                    "Selecciona una operacion valida."
                )
                return

            if not resultado.get("exito", False):
                QMessageBox.warning(
                    self,
                    "Error",
                    resultado.get(
                        "mensaje",
                        "No se pudo realizar la operacion."
                    )
                )
                return

            self._mostrar_resultados(resultado)

        except ValueError:
            QMessageBox.warning(
                self,
                "Entrada invalida",
                "Todos los componentes deben ser numeros validos."
            )

        except Exception as e:
            QMessageBox.critical(
                self,
                "Error de ejecucion",
                f"Detalle del error:\n{str(e)}"
            )


    def on_solved_clicked_meqs(self):
        try:
            matriz = self._leer_matriz_meqs()

            if self._meqs_es_homogeneo():
                resultado = ControladorVectores.resolver_sistema_homogeneo(
                    matriz
                )

                resultado["operacion"] = "sistema_homogeneo"

            else:
                vector_b = self._leer_vector_meqs()

                resultado = ControladorVectores.resolver_ecuacion_matricial(
                    matriz,
                    vector_b
                )

                resultado["operacion"] = "ecuacion_matricial"

            if not resultado.get("exito", False):
                QMessageBox.warning(
                    self,
                    "Error",
                    resultado.get(
                        "mensaje",
                        "No se pudo resolver la ecuacion matricial."
                    )
                )
                return

            self._mostrar_resultados(resultado)

        except ValueError:
            QMessageBox.warning(
                self,
                "Entrada invalida",
                "Todos los componentes deben ser numeros validos."
            )

        except Exception as e:
            QMessageBox.critical(
                self,
                "Error de ejecucion",
                f"Detalle del error:\n{str(e)}"
            )

    def _formatear_valor(self, valor):
        if isinstance(valor, (int, float)):
            return formatear_numero(valor)

        return str(valor)

    def _crear_card_base(self, titulo):
        card = QFrame()
        card.setObjectName("CardResultadoGenerica")
        card.setStyleSheet("""
            QFrame#CardResultadoGenerica {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 12px;
            }
        """)

        layout_principal = QVBoxLayout(card)
        layout_principal.setContentsMargins(20, 16, 20, 20)
        layout_principal.setSpacing(12)

        header_widget = QWidget()
        header_widget.setStyleSheet("background: transparent; border: none;")
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)

        lbl_title = QLabel(titulo)
        lbl_title.setStyleSheet("""
            color: #0F172A;
            font-size: 15px;
            font-weight: 700;
            border: none;
            background: transparent;
        """)

        btn_toggle = QPushButton("-")
        btn_toggle.setFixedSize(24, 24)
        btn_toggle.setCursor(Qt.CursorShape.PointingHandCursor)
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

        body_widget = QWidget()
        body_widget.setStyleSheet("background: transparent; border: none;")
        body_layout = QVBoxLayout(body_widget)
        body_layout.setContentsMargins(0, 10, 0, 0)
        body_layout.setSpacing(16)
        layout_principal.addWidget(body_widget)

        def _toggle():
            body_widget.setVisible(not body_widget.isVisible())
            btn_toggle.setText("-" if body_widget.isVisible() else "+")

        btn_toggle.clicked.connect(_toggle)

        card.content_widget = body_widget
        card.content_layout = body_layout
        card.btn_toggle = btn_toggle
        card.is_expanded = True

        return card, body_layout

    def _crear_matriz_widget(self, matriz, texto=False, aumentada=False):
        if not matriz:
            lbl = QLabel("Sin datos")
            lbl.setStyleSheet(
                "color: #64748B; font-size: 13px; border: none;"
            )
            return lbl

        widget = QWidget()
        widget.setStyleSheet("background: transparent; border: none;")

        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        filas = len(matriz)
        bracket_height = max(36, filas * 28 + (filas - 1) * 6)

        b_left = BracketWidget(is_left=True)
        b_left.setFixedHeight(bracket_height)
        layout.addWidget(b_left)

        grid = QGridLayout()
        grid.setVerticalSpacing(6)
        grid.setHorizontalSpacing(12 if texto else 18)
        grid.setContentsMargins(0, 0, 0, 0)

        for r, fila in enumerate(matriz):
            last_col = len(fila) - 1

            for c, valor in enumerate(fila):
                lbl_val = QLabel(self._formatear_valor(valor))
                lbl_val.setAlignment(Qt.AlignmentFlag.AlignCenter)
                lbl_val.setMinimumWidth(120 if texto else 44)
                lbl_val.setFixedHeight(24)
                lbl_val.setStyleSheet("""
                    color: #0F172A;
                    font-size: 13px;
                    font-weight: 600;
                    font-family: 'Consolas', 'Courier New', monospace;
                    border: none;
                    background: transparent;
                    padding: 0px;
                    margin: 0px;
                """)

                grid_col = c

                if aumentada and c == last_col:
                    linea_v = QFrame()
                    linea_v.setFrameShape(QFrame.Shape.VLine)
                    linea_v.setStyleSheet(
                        "background-color: #CBD5E1; max-width: 1px; border: none;"
                    )
                    grid.addWidget(linea_v, r, c)
                    grid_col = c + 1

                grid.addWidget(lbl_val, r, grid_col)

        layout.addLayout(grid)

        b_right = BracketWidget(is_left=False)
        b_right.setFixedHeight(bracket_height)
        layout.addWidget(b_right)

        return widget

    def _crear_vector_widget(self, vector, texto=False):
        if vector is None:
            vector = []

        return self._crear_matriz_widget(
            [
                [valor]
                for valor in vector
            ],
            texto=texto
        )

    def _crear_fila_matrices_widget(self, matrices, simbolo=None):
        widget = QWidget()
        widget.setStyleSheet("background: transparent; border: none;")

        layout = QHBoxLayout(widget)
        layout.setContentsMargins(40, 0, 0, 0)
        layout.setSpacing(18)

        for i, matriz in enumerate(matrices):
            layout.addWidget(self._crear_matriz_widget(matriz))

            if simbolo and i < len(matrices) - 1:
                lbl_simbolo = QLabel(simbolo)
                lbl_simbolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
                lbl_simbolo.setStyleSheet("""
                    color: #0F172A;
                    font-size: 18px;
                    font-weight: 800;
                    border: none;
                    background: transparent;
                """)
                layout.addWidget(lbl_simbolo)

        layout.addStretch()
        return widget

    def _crear_card_paso(self, numero, titulo, etiqueta, contenido_widget):
        card_step = QFrame()
        card_step.setObjectName("CardStepOperacionMatriz")
        card_step.setStyleSheet("""
            QFrame#CardStepOperacionMatriz {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 12px;
            }
        """)

        step_layout = QVBoxLayout(card_step)
        step_layout.setContentsMargins(16, 16, 16, 16)
        step_layout.setSpacing(12)

        header_step = QHBoxLayout()
        header_step.setContentsMargins(0, 0, 0, 0)
        header_step.setSpacing(12)

        lbl_num = QLabel(str(numero))
        lbl_num.setFixedSize(28, 28)
        lbl_num.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_num.setStyleSheet("""
            background-color: #EEF2FF;
            color: #4F46E5;
            font-weight: 700;
            font-size: 13px;
            border-radius: 14px;
            border: none;
        """)

        vbox_textos = QVBoxLayout()
        vbox_textos.setContentsMargins(0, 0, 0, 0)
        vbox_textos.setSpacing(6)

        lbl_titulo = QLabel(titulo)
        lbl_titulo.setStyleSheet("""
            color: #64748B;
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 0.5px;
            border: none;
            background: transparent;
        """)
        vbox_textos.addWidget(lbl_titulo)

        if etiqueta:
            badge_layout = QHBoxLayout()
            badge_layout.setContentsMargins(0, 0, 0, 0)

            lbl_etiqueta = QLabel(etiqueta)
            lbl_etiqueta.setStyleSheet("""
                background-color: #F8FAFC;
                color: #0F172A;
                font-family: 'Consolas', 'Courier New', monospace;
                font-weight: 600;
                font-size: 13px;
                padding: 6px 12px;
                border-radius: 8px;
                border: 1px solid #F1F5F9;
            """)
            badge_layout.addWidget(lbl_etiqueta)
            badge_layout.addStretch()
            vbox_textos.addLayout(badge_layout)

        header_step.addWidget(lbl_num, alignment=Qt.AlignmentFlag.AlignTop)
        header_step.addLayout(vbox_textos)
        header_step.addStretch()

        step_layout.addLayout(header_step)
        step_layout.addWidget(contenido_widget)

        return card_step

    def _simbolo_operacion_matriz(self, texto_operacion):
        texto = str(texto_operacion).lower()

        if "rest" in texto or "-" in texto or "âˆ’" in texto:
            return "-"

        if "multip" in texto or "x" in texto or "Ã—" in texto:
            return "x"

        return "+"

    def _crear_card_proceso_matricial(self, resultado):
        card, body_layout = self._crear_card_base("Proceso")
        proceso = resultado.get("proceso", [])
        operacion_general = resultado.get("operacion", "")

        if not proceso:
            lbl_vacio = QLabel("No hay informacion del proceso para mostrar.")
            lbl_vacio.setStyleSheet(
                "color: #64748B; font-size: 13px; border: none;"
            )
            body_layout.addWidget(lbl_vacio)
            return card

        def envolver_con_margen(widget):
            wrapper = QWidget()
            wrapper.setStyleSheet("background: transparent; border: none;")
            wrapper_layout = QHBoxLayout(wrapper)
            wrapper_layout.setContentsMargins(40, 0, 0, 0)
            wrapper_layout.addWidget(widget)
            wrapper_layout.addStretch()
            return wrapper

        def crear_matriz_vector_widget(matriz, vector):
            wrapper = QWidget()
            wrapper.setStyleSheet("background: transparent; border: none;")
            wrapper_layout = QHBoxLayout(wrapper)
            wrapper_layout.setContentsMargins(40, 0, 0, 0)
            wrapper_layout.setSpacing(18)
            wrapper_layout.addWidget(self._crear_matriz_widget(matriz))

            lbl_simbolo = QLabel("x")
            lbl_simbolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_simbolo.setStyleSheet("""
                color: #0F172A;
                font-size: 18px;
                font-weight: 800;
                border: none;
                background: transparent;
            """)
            wrapper_layout.addWidget(lbl_simbolo)
            wrapper_layout.addWidget(self._crear_vector_widget(vector))
            wrapper_layout.addStretch()
            return wrapper

        for indice, paso in enumerate(proceso, start=1):
            numero = paso.get("numero", indice)
            titulo = paso.get("titulo", "PASO")
            operacion_paso = paso.get("operacion", "")
            etiqueta = operacion_paso if isinstance(operacion_paso, str) else ""
            tipo = paso.get("tipo", "")

            if tipo == "operacion":
                if paso.get("matrices"):
                    contenido = self._crear_fila_matrices_widget(
                        paso.get("matrices", []),
                        self._simbolo_operacion_matriz(
                            f"{operacion_general} {etiqueta}"
                        )
                    )

                elif paso.get("matriz_izquierda") and paso.get("matriz_derecha"):
                    contenido = self._crear_fila_matrices_widget(
                        [
                            paso.get("matriz_izquierda"),
                            paso.get("matriz_derecha")
                        ],
                        "x"
                    )

                elif paso.get("matriz") and paso.get("vector"):
                    contenido = crear_matriz_vector_widget(
                        paso.get("matriz", []),
                        paso.get("vector", [])
                    )

                elif paso.get("matriz"):
                    contenido = self._crear_fila_matrices_widget(
                        [paso.get("matriz")]
                    )

                else:
                    contenido = QLabel(str(etiqueta))

            elif tipo == "componentes":
                es_vector_componentes = (
                    isinstance(operacion_paso, list)
                    and (
                        not operacion_paso
                        or not isinstance(operacion_paso[0], list)
                    )
                )

                contenido = QWidget()
                contenido.setStyleSheet("background: transparent; border: none;")
                contenido_layout = QHBoxLayout(contenido)
                contenido_layout.setContentsMargins(40, 0, 0, 0)

                if es_vector_componentes:
                    contenido_layout.addWidget(
                        self._crear_vector_widget(
                            operacion_paso,
                            texto=True
                        )
                    )
                else:
                    contenido_layout.addWidget(
                        self._crear_matriz_widget(
                            operacion_paso
                            if isinstance(operacion_paso, list)
                            else [],
                            texto=True
                        )
                    )

                contenido_layout.addStretch()

            elif tipo == "resultado":
                if paso.get("vector") is not None:
                    contenido = envolver_con_margen(
                        self._crear_vector_widget(
                            paso.get("vector", [])
                        )
                    )
                elif paso.get("resultado") is not None:
                    contenido = envolver_con_margen(
                        self._crear_vector_widget(
                            paso.get("resultado", [])
                        )
                    )
                else:
                    contenido = self._crear_fila_matrices_widget(
                        [paso.get("matriz", [])]
                    )

            elif tipo in (
                "suma_vectores",
                "producto_escalar_vector",
                "lado_izquierdo",
                "producto_Au",
                "producto_Av",
                "lado_derecho"
            ):
                contenido = envolver_con_margen(
                    self._crear_vector_widget(
                        paso.get("resultado", [])
                    )
                )

            elif tipo == "verificacion":
                texto = (
                    "La igualdad se cumple."
                    if paso.get("resultado")
                    else "La igualdad no se cumple."
                )
                contenido = QLabel(texto)
                contenido.setStyleSheet("""
                    color: #0F172A;
                    font-size: 13px;
                    font-weight: 700;
                    border: none;
                    background: transparent;
                    padding-left: 40px;
                """)

            else:
                contenido = QLabel(str(paso))

            body_layout.addWidget(
                self._crear_card_paso(
                    numero,
                    titulo,
                    etiqueta,
                    contenido
                )
            )

        return card

    def _crear_card_proceso_eliminacion(self, resultado):
        card, body_layout = self._crear_card_base("Proceso de eliminacion")
        proceso = resultado.get("proceso", [])

        if not proceso:
            lbl_vacio = QLabel("No hay pasos de eliminacion para mostrar.")
            lbl_vacio.setStyleSheet(
                "color: #64748B; font-size: 13px; border: none;"
            )
            body_layout.addWidget(lbl_vacio)
            return card

        for indice, paso in enumerate(proceso, start=1):
            matriz_paso = paso.get("matriz", [])
            contenido = QWidget()
            contenido.setStyleSheet("background: transparent; border: none;")

            contenido_layout = QHBoxLayout(contenido)
            contenido_layout.setContentsMargins(40, 0, 0, 0)
            contenido_layout.addWidget(
                self._crear_matriz_widget(
                    matriz_paso,
                    aumentada=True
                )
            )
            contenido_layout.addStretch()

            body_layout.addWidget(
                self._crear_card_paso(
                    indice,
                    "OPERACION ELEMENTAL",
                    paso.get("operacion", ""),
                    contenido
                )
            )

        return card

    def _crear_card_solucion(self, titulo="Solucion"):
        card, _ = self._crear_card_base(titulo)
        return card

    def _agregar_titulo_seccion(self, layout, texto):
        lbl = QLabel(texto)
        lbl.setStyleSheet("""
            color: #64748B;
            font-weight: 700;
            font-size: 11px;
            letter-spacing: 0.5px;
            border: none;
            background: transparent;
        """)
        layout.addWidget(lbl)

    def _formatear_vector_texto(self, vector):
        return (
            "["
            + "; ".join(
                self._formatear_valor(valor)
                for valor in vector
            )
            + "]"
        )

    def _texto_conjunto_solucion(self, conjunto):
        if not conjunto:
            return ""

        forma_vectorial = conjunto.get("forma_vectorial")

        if isinstance(forma_vectorial, list):
            return (
                "x = "
                + self._formatear_vector_texto(forma_vectorial)
            )

        solucion_particular = conjunto.get(
            "solucion_particular",
            []
        )
        parametros = conjunto.get("parametros", [])
        vectores_direccion = conjunto.get(
            "vectores_direccion",
            []
        )

        if not solucion_particular and not vectores_direccion:
            return ""

        partes = [
            self._formatear_vector_texto(solucion_particular)
        ]

        for indice, vector in enumerate(vectores_direccion):
            parametro = (
                parametros[indice]
                if indice < len(parametros)
                else f"t{indice + 1}"
            )
            partes.append(
                f"{parametro}"
                f"{self._formatear_vector_texto(vector)}"
            )

        return "x = " + " + ".join(partes)

    def renderizar_tarjeta_solucion(self, resultado):
        if not hasattr(self, "card_solucion") or not self.card_solucion:
            return

        contenedor = self.card_solucion.content_widget
        layout_principal = contenedor.layout()

        while layout_principal.count():
            item = layout_principal.takeAt(0)
            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

            child_layout = item.layout()

            if child_layout is not None:
                self._clear_layout(child_layout)

        operacion = resultado.get("operacion", "")
        propiedades_multiplicacion_matrices = (
            "Propiedad asociativa matrices",
            "Propiedad distributiva izquierda matrices",
            "Propiedad distributiva derecha matrices",
            "Propiedad escalar producto matrices",
            "Propiedad identidad matrices"
        )

        if operacion in (
            "Sumar matrices",
            "Restar matrices",
            "Multiplicar matriz por escalar",
            "Multiplicar matrices"
        ):
            self._agregar_titulo_seccion(layout_principal, "RESULTADO")

            wrapper = QWidget()
            wrapper.setStyleSheet("background: transparent; border: none;")
            wrapper_layout = QHBoxLayout(wrapper)
            wrapper_layout.setContentsMargins(0, 0, 0, 0)
            wrapper_layout.addWidget(
                self._crear_matriz_widget(
                    resultado.get("resultado", [])
                )
            )
            wrapper_layout.addStretch()
            layout_principal.addWidget(wrapper)

        elif operacion == "Matriz por vector":
            self._agregar_titulo_seccion(layout_principal, "RESULTADO")

            wrapper = QWidget()
            wrapper.setStyleSheet("background: transparent; border: none;")
            wrapper_layout = QHBoxLayout(wrapper)
            wrapper_layout.setContentsMargins(0, 0, 0, 0)
            wrapper_layout.addWidget(
                self._crear_vector_widget(
                    resultado.get("resultado", [])
                )
            )
            wrapper_layout.addStretch()
            layout_principal.addWidget(wrapper)

        elif operacion in (
            "Propiedad distributiva",
            "Propiedad homogenea",
            "Propiedad homogÃ©nea"
        ):
            self._agregar_titulo_seccion(layout_principal, "COMPARACION")

            es_homogeneidad = "homog" in operacion.lower()

            if es_homogeneidad:
                escalar_valor = resultado.get("escalar")
                escalar_texto = (
                    self._formatear_valor(escalar_valor)
                    if escalar_valor is not None
                    else "k"
                )
                expresion = (
                    f"A({escalar_texto}u) = "
                    f"{escalar_texto}(Au)"
                )
                titulos_lados = (
                    (
                        f"A({escalar_texto}u)",
                        resultado.get("lado_izquierdo", [])
                    ),
                    (
                        f"{escalar_texto}(Au)",
                        resultado.get("lado_derecho", [])
                    )
                )
            else:
                expresion = "A(u + v) = Au + Av"
                titulos_lados = (
                    (
                        "A(u + v)",
                        resultado.get("lado_izquierdo", [])
                    ),
                    (
                        "Au + Av",
                        resultado.get("lado_derecho", [])
                    )
                )

            lbl_expresion = QLabel(expresion)
            lbl_expresion.setStyleSheet("""
                color: #0F172A;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 14px;
                font-weight: 700;
                background-color: #F8FAFC;
                border: 1px solid #E2E8F0;
                border-radius: 10px;
                padding: 10px 12px;
            """)
            layout_principal.addWidget(lbl_expresion)

            igualdad = resultado.get("igualdad", False)
            lbl_estado = QLabel(
                "La igualdad se cumple."
                if igualdad
                else "La igualdad no se cumple."
            )
            lbl_estado.setStyleSheet("""
                color: #0F172A;
                font-size: 13px;
                font-weight: 700;
                background-color: #F8FAFC;
                border: 1px solid #E2E8F0;
                border-radius: 10px;
                padding: 12px;
            """)
            layout_principal.addWidget(lbl_estado)

            lados_layout = QHBoxLayout()
            lados_layout.setSpacing(18)

            for titulo, vector in titulos_lados:
                columna = QVBoxLayout()
                columna.setSpacing(8)
                lbl_titulo = QLabel(titulo)
                lbl_titulo.setStyleSheet("""
                    color: #64748B;
                    font-weight: 700;
                    font-size: 11px;
                    letter-spacing: 0.5px;
                    border: none;
                """)
                columna.addWidget(lbl_titulo)
                columna.addWidget(
                    self._crear_vector_widget(vector)
                )
                lados_layout.addLayout(columna)

            lados_layout.addStretch()
            layout_principal.addLayout(lados_layout)

        elif operacion in propiedades_multiplicacion_matrices:
            self._agregar_titulo_seccion(layout_principal, "COMPARACION")

            lbl_expresion = QLabel(resultado.get("expresion", ""))
            lbl_expresion.setStyleSheet("""
                color: #0F172A;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 14px;
                font-weight: 700;
                background-color: #F8FAFC;
                border: 1px solid #E2E8F0;
                border-radius: 10px;
                padding: 10px 12px;
            """)
            layout_principal.addWidget(lbl_expresion)

            igualdad = resultado.get("igualdad", False)
            lbl_estado = QLabel(
                "La igualdad se cumple."
                if igualdad
                else "La igualdad no se cumple."
            )
            lbl_estado.setStyleSheet("""
                color: #0F172A;
                font-size: 13px;
                font-weight: 700;
                background-color: #F8FAFC;
                border: 1px solid #E2E8F0;
                border-radius: 10px;
                padding: 12px;
            """)
            layout_principal.addWidget(lbl_estado)

            comparaciones = resultado.get("comparaciones", [])

            lados_layout = QHBoxLayout()
            lados_layout.setSpacing(18)

            for titulo, matriz in comparaciones:
                columna = QVBoxLayout()
                columna.setSpacing(8)

                lbl_titulo = QLabel(str(titulo))
                lbl_titulo.setStyleSheet("""
                    color: #64748B;
                    font-weight: 700;
                    font-size: 11px;
                    letter-spacing: 0.5px;
                    border: none;
                """)
                columna.addWidget(lbl_titulo)
                columna.addWidget(
                    self._crear_matriz_widget(matriz)
                )
                lados_layout.addLayout(columna)

            lados_layout.addStretch()
            layout_principal.addLayout(lados_layout)

        elif (
            operacion == "ecuacion_matricial"
            or operacion == "sistema_homogeneo"
            or resultado.get("es_homogeneo", False)
        ):
            tipo = resultado.get("tipo")
            solucion = resultado.get("solucion") or []
            solucion_parametrica = resultado.get("solucion_parametrica")
            conjunto_solucion = resultado.get("conjunto_solucion")

            if resultado.get("es_homogeneo", False):
                self._agregar_titulo_seccion(
                    layout_principal,
                    (
                        "INDEPENDENCIA DE COLUMNAS"
                        if operacion == "Independencia columnas"
                        else "SISTEMA HOMOGENEO"
                    )
                )

                lbl_mensaje = QLabel(
                    resultado.get(
                        "mensaje",
                        "Sistema homogeneo resuelto correctamente."
                    )
                )
                lbl_mensaje.setWordWrap(True)
                lbl_mensaje.setStyleSheet("""
                    color: #0F172A;
                    font-size: 13px;
                    font-weight: 700;
                    background-color: #F8FAFC;
                    border: 1px solid #E2E8F0;
                    border-radius: 10px;
                    padding: 12px;
                """)
                layout_principal.addWidget(lbl_mensaje)

            layout_vars = QHBoxLayout()
            layout_vars.setSpacing(16)

            for titulo, valores, color in (
                (
                    "VARIABLES BASICAS",
                    resultado.get("variables_basicas", []),
                    "#2563EB"
                ),
                (
                    "VARIABLES LIBRES",
                    resultado.get("variables_libres", []),
                    "#475569"
                )
            ):
                columna = QVBoxLayout()
                columna.setSpacing(8)
                lbl_titulo = QLabel(titulo)
                lbl_titulo.setStyleSheet("""
                    color: #64748B;
                    font-weight: 700;
                    font-size: 11px;
                    letter-spacing: 0.5px;
                    border: none;
                """)
                columna.addWidget(lbl_titulo)

                chips = QHBoxLayout()
                chips.setSpacing(6)

                if valores:
                    for idx in valores:
                        chip = QLabel(f"x{idx + 1}")
                        chip.setStyleSheet(f"""
                            background-color: #F8FAFC;
                            color: {color};
                            border: 1px solid #E2E8F0;
                            border-radius: 8px;
                            padding: 4px 12px;
                            font-weight: 700;
                            font-size: 13px;
                        """)
                        chips.addWidget(chip)

                else:
                    lbl_none = QLabel("Ninguna")
                    lbl_none.setStyleSheet("""
                        color: #64748B;
                        font-style: italic;
                        font-size: 13px;
                        border: none;
                    """)
                    chips.addWidget(lbl_none)

                chips.addStretch()
                columna.addLayout(chips)
                layout_vars.addLayout(columna, stretch=1)

            layout_principal.addLayout(layout_vars)

            if tipo == "unica" and solucion:
                self._agregar_titulo_seccion(layout_principal, "VALORES")

                valores_layout = QHBoxLayout()
                valores_layout.setSpacing(16)

                for i, valor in enumerate(solucion):
                    card_val = QFrame()
                    card_val.setObjectName("CardValorSolucion")
                    card_val.setFixedSize(150, 70)
                    card_val.setStyleSheet("""
                        QFrame#CardValorSolucion {
                            background-color: #FFFFFF;
                            border: 1px solid #E2E8F0;
                            border-radius: 12px;
                        }
                    """)

                    card_layout = QVBoxLayout(card_val)
                    card_layout.setContentsMargins(12, 10, 12, 10)
                    card_layout.setSpacing(2)
                    card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

                    lbl_x = QLabel(f"x{i + 1}")
                    lbl_x.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    lbl_x.setStyleSheet("""
                        color: #64748B;
                        font-weight: 600;
                        font-size: 13px;
                        border: none;
                        background: transparent;
                    """)

                    lbl_val = QLabel(formatear_numero(valor))
                    lbl_val.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    lbl_val.setStyleSheet("""
                        color: #0F172A;
                        font-weight: 800;
                        font-size: 28px;
                        border: none;
                        background: transparent;
                    """)

                    card_layout.addWidget(lbl_x)
                    card_layout.addWidget(lbl_val)
                    valores_layout.addWidget(card_val)

                valores_layout.addStretch()
                layout_principal.addLayout(valores_layout)

            elif tipo == "infinitas" and solucion_parametrica:
                self._agregar_titulo_seccion(
                    layout_principal,
                    "SOLUCION PARAMETRICA"
                )

                soluciones = solucion_parametrica.get("soluciones", [])
                texto = "\n".join(
                    f"x{item.get('variable', 0) + 1} = {item.get('expresion', '')}"
                    for item in soluciones
                )

                lbl_param = QLabel(texto)
                lbl_param.setWordWrap(True)
                lbl_param.setStyleSheet("""
                    color: #0F172A;
                    font-family: 'Consolas', 'Courier New', monospace;
                    font-size: 13px;
                    background-color: #F8FAFC;
                    border: 1px solid #E2E8F0;
                    border-radius: 10px;
                    padding: 12px;
                """)
                layout_principal.addWidget(lbl_param)

            elif tipo == "ninguna":
                lbl_none = QLabel("El sistema no tiene solucion.")
                lbl_none.setStyleSheet("""
                    color: #DC2626;
                    font-size: 13px;
                    font-weight: 700;
                    border: none;
                    background: transparent;
                """)
                layout_principal.addWidget(lbl_none)

            texto_conjunto = self._texto_conjunto_solucion(
                conjunto_solucion
            )

            if tipo != "ninguna" and texto_conjunto:
                self._agregar_titulo_seccion(
                    layout_principal,
                    "CONJUNTO SOLUCION VECTORIAL"
                )

                lbl_conjunto = QLabel(texto_conjunto)
                lbl_conjunto.setWordWrap(True)
                lbl_conjunto.setStyleSheet("""
                    color: #0F172A;
                    font-family: 'Consolas', 'Courier New', monospace;
                    font-size: 13px;
                    background-color: #F8FAFC;
                    border: 1px solid #E2E8F0;
                    border-radius: 10px;
                    padding: 12px;
                """)
                layout_principal.addWidget(lbl_conjunto)

        self.card_solucion.is_expanded = True
        self.card_solucion.content_widget.setVisible(True)
        self.card_solucion.btn_toggle.setText("-")
    
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
        es_homogeneo = resultado.get("es_homogeneo", False)
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
        if es_homogeneo:
            self._add_info_row(
                grid,
                3,
                2,
                "Soluciones no triviales",
                "Si"
                if resultado.get("tiene_soluciones_no_triviales")
                else "No"
            )

        layout.addLayout(grid)

        # --- DIVISOR ---
        linea = QFrame()
        linea.setFrameShape(QFrame.Shape.HLine)
        linea.setStyleSheet("background-color: #F1F5F9; border: none; max-height: 1px;")
        layout.addWidget(linea)

        # --- RESUMEN EN CÓDIGO ---
        tipo_sol = resultado.get("tipo", "ninguna")
        if es_homogeneo:
            texto_conclusion = (
                "soluciones no triviales"
                if resultado.get("tiene_soluciones_no_triviales")
                else "solo solucion trivial"
            )
        elif tipo_sol == "unica":
            texto_conclusion = "solución única"
        elif tipo_sol == "infinitas":
            texto_conclusion = "infinitas soluciones"
        else:
            texto_conclusion = "sin solución"

        prefijo = "Ax = 0  |  " if es_homogeneo else ""
        resumen_txt = f"{prefijo}rango(A) = {rango_a}  |  rango(A|b) = {rango_ab}  |  n = {num_vars}  →  {texto_conclusion}"

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
        subtitulo = (
            f"SISTEMA HOMOGENEO Ax = 0 · {num_eqs} ECUACIONES, {num_vars} VARIABLES"
            if resultado.get("es_homogeneo", False)
            else f"SISTEMA ORIGINAL · {num_eqs} ECUACIONES, {num_vars} VARIABLES"
        )
        lbl_sub = QLabel(subtitulo)
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
                    lbl_val = QLabel(
                        formatear_numero(val)
                        if isinstance(val, (int, float))
                        else str(val)
                    )
                    
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
    def _mostrar_resultados(self, resultado):
        self.card.hide()

        if hasattr(self, "dog_main"):
            self.dog_main.hide()

        self.card_matriz = None
        self.card_proceso = None
        self.card_solucion = None

        while self.results_layout.count():
            item = self.results_layout.takeAt(0)
            widget = item.widget()

            if widget:
                widget.deleteLater()

        self.results_card.show()

        btn_back = QPushButton("<- Nuevo sistema")
        btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_back.setStyleSheet(
            "QPushButton { color: #64748B; font-weight: 600; font-size: 13px; "
            "border: none; background: transparent; text-align: left; padding: 0px; } "
            "QPushButton:hover { color: #0F172A; }"
        )
        btn_back.clicked.connect(self._volver_a_matriz)
        self.results_layout.addWidget(btn_back)

        modo = resultado.get("operacion", "")

        banner = QFrame()
        banner.setObjectName("BannerEstado")

        if modo == "Independencia columnas":
            if resultado.get("es_independiente", False):
                color_icono = "#059669"
                titulo_estado = "Columnas independientes"
                sub_estado = "Ax = 0 solo tiene solucion trivial"
                texto_icono = "OK"
                banner_bg = "#ECFDF5"
                banner_border = "#A7F3D0"
            else:
                color_icono = "#2563EB"
                titulo_estado = "Columnas dependientes"
                sub_estado = "Ax = 0 tiene soluciones no triviales"
                texto_icono = "DEP"
                banner_bg = "#EFF6FF"
                banner_border = "#BFDBFE"

        elif modo == "sistema_homogeneo" or resultado.get("es_homogeneo", False):
            tiene_no_triviales = resultado.get(
                "tiene_soluciones_no_triviales",
                False
            )

            if tiene_no_triviales:
                color_icono = "#2563EB"
                titulo_estado = "Sistema homogeneo con soluciones no triviales"
                sub_estado = "Tiene variables libres"
                texto_icono = "INF"
                banner_bg = "#EFF6FF"
                banner_border = "#BFDBFE"
            else:
                color_icono = "#059669"
                titulo_estado = "Sistema homogeneo con solucion trivial"
                sub_estado = "Solo x = 0"
                texto_icono = "OK"
                banner_bg = "#ECFDF5"
                banner_border = "#A7F3D0"

        elif (
            modo == "ecuacion_matricial"
            or modo == "sistema_homogeneo"
            or resultado.get("es_homogeneo", False)
        ):
            color_icono = "#2563EB"
            titulo_estado = "Sistema no homogeneo"
            sub_estado = "Ax = b"
            texto_icono = "NOH"
            banner_bg = "#EFF6FF"
            banner_border = "#BFDBFE"

        else:
            color_icono = "#059669"
            titulo_estado = "Operacion realizada exitosamente"
            sub_estado = "El resultado se calculo correctamente."
            texto_icono = "OK"
            banner_bg = "#ECFDF5"
            banner_border = "#A7F3D0"

        banner.setStyleSheet(f"""
            QFrame#BannerEstado {{
                background-color: {banner_bg};
                border: 1px solid {banner_border};
                border-radius: 12px;
                padding: 6px 16px;
            }}
        """)

        b_layout = QHBoxLayout(banner)
        b_layout.setContentsMargins(0, 4, 0, 4)
        b_layout.setSpacing(12)

        lbl_icon = QLabel(texto_icono)
        lbl_icon.setStyleSheet(
            f"color: {color_icono}; font-size: 13px; font-weight: 800; "
            "border: none; background: transparent;"
        )
        b_layout.addWidget(lbl_icon)

        text_vbox = QVBoxLayout()
        text_vbox.setSpacing(1)
        text_vbox.setContentsMargins(0, 0, 0, 0)

        lbl_status_title = QLabel(titulo_estado)
        lbl_status_title.setStyleSheet(
            f"color: {color_icono}; font-size: 13px; font-weight: 700; "
            "border: none; background: transparent;"
        )

        lbl_status_sub = QLabel(sub_estado)
        lbl_status_sub.setStyleSheet(
            f"color: {color_icono}; font-size: 11px; "
            "border: none; background: transparent;"
        )

        text_vbox.addWidget(lbl_status_title)
        text_vbox.addWidget(lbl_status_sub)

        b_layout.addLayout(text_vbox)
        b_layout.addStretch()

        self.results_layout.addWidget(banner)

        if modo in (
            "Sumar matrices",
            "Restar matrices",
            "Multiplicar matriz por escalar",
            "Multiplicar matrices",
            "Matriz por vector",
            "Propiedad distributiva",
            "Propiedad homogenea",
            "Propiedad homogÃ©nea",
            "Propiedad asociativa matrices",
            "Propiedad distributiva izquierda matrices",
            "Propiedad distributiva derecha matrices",
            "Propiedad escalar producto matrices",
            "Propiedad identidad matrices"
        ):
            self.results_layout.addWidget(
                self._crear_card_proceso_matricial(resultado)
            )

            self.card_solucion = self._crear_card_solucion("Resultado")
            self.results_layout.addWidget(self.card_solucion)
            self.renderizar_tarjeta_solucion(resultado)

        elif (
            modo == "ecuacion_matricial"
            or modo == "sistema_homogeneo"
            or resultado.get("es_homogeneo", False)
        ):
            self.results_layout.addWidget(
                self._crear_card_info_sistema(resultado)
            )

            if resultado.get("matriz_aumentada"):
                self.results_layout.addWidget(
                    self._crear_card_matriz_aumentada(resultado)
                )

            self.results_layout.addWidget(
                self._crear_card_proceso_eliminacion(resultado)
            )

            self.card_solucion = self._crear_card_solucion("Solucion")
            self.results_layout.addWidget(self.card_solucion)
            self.renderizar_tarjeta_solucion(resultado)

        else:
            self.card_solucion = self._crear_card_solucion("Resultado")
            self.results_layout.addWidget(self.card_solucion)
            self.renderizar_tarjeta_solucion(resultado)
   
