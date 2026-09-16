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
        self.combo_mops_metodo.addItems(["Sumar", "Restar", "Escalar", "Multiplicar"])
        self.combo_mops_metodo.setFixedWidth(120)
        self.combo_mops_metodo.setFixedHeight(38)
        self.combo_mops_metodo.setCurrentIndex(0)
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
                selection-background-color: #F1F5F9;
                selection-color: #2563EB;
            }

            QComboBox::drop-down {
                border: none;
                width: 22px;
            }
        """)

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
       
    def _on_mops_operation_changed(self):

        metodo = self.combo_mops_metodo.currentText()

        es_escalar = metodo == "Escalar"

        # Mostrar escalar solamente en Escalar
        self.mops_escalar_container.setVisible(es_escalar)

        # Cantidad de matrices no aplica para Escalar
        self.stepper_mops_count.setEnabled(not es_escalar)

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

        # ============================================================
        # 2. ELIMINAR SOLAMENTE LAS MATRICES
        #    NO eliminar mops_container ni mops_scroll
        # ============================================================

        while self.mops_layout_inner.count():

            item = self.mops_layout_inner.takeAt(0)

            layout = item.layout()

            if layout is not None:

                while layout.count():

                    sub_item = layout.takeAt(0)

                    widget = sub_item.widget()

                    if widget is not None:
                        widget.deleteLater()

                    sub_layout = sub_item.layout()

                    if sub_layout is not None:

                        while sub_layout.count():

                            sub_sub_item = sub_layout.takeAt(0)

                            widget = sub_sub_item.widget()

                            if widget is not None:
                                widget.deleteLater()

        # ============================================================
        # 3. DIMENSIONES
        # ============================================================

        rows = self.stepper_mops_rows.value
        cols = self.stepper_mops_cols.value

        metodo = self.combo_mops_metodo.currentText()

        es_escalar = metodo == "Escalar"

        # Escalar -> solamente A1
        # Sumar/Restar/Multiplicar -> cantidad seleccionada
        if es_escalar:
            num_matrices = 1
        else:
            num_matrices = self.stepper_mops_count.value

        # Lista nueva
        self.mops_inputs_list = []

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

        bracket_height = rows * 36 + (rows - 1) * 8

        # ============================================================
        # 5. CREAR A1, A2, A3...
        # ============================================================

        for m in range(num_matrices):

            mat_box = QVBoxLayout()
            mat_box.setSpacing(6)
            mat_box.setAlignment(Qt.AlignmentFlag.AlignTop)

            # --------------------------------------------------------
            # Etiqueta A1, A2, A3...
            # --------------------------------------------------------

            lbl_m = QLabel(f"A<sub>{m + 1}</sub>")

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

                    inp.setFixedSize(54, 36)

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

            self.mops_layout_inner.addLayout(mat_box)

        # ============================================================
        # 6. ESCALAR
        # ============================================================

        self.mops_escalar_container.setVisible(es_escalar)

        # ============================================================
        # 7. AJUSTAR EL CONTENEDOR DEL SCROLL
        # ============================================================

        self.mops_layout_inner.activate()

        size = self.mops_layout_inner.sizeHint()

        self.mops_container.setMinimumSize(
            size.width(),
            size.height()
        )

        self.mops_container.resize(
            size.width(),
            size.height()
        )

        self.mops_container.updateGeometry()
        self.mops_scroll.updateGeometry()
        self.mops_scroll.viewport().update()

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

        lbl_x = QLabel("b")
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
    def on_solved_clicked_mops(self):
        pass


    def on_solved_clicked_meqs(self):
            pass
    
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
    def _mostrar_resultados(self, resultado):
        pass
   