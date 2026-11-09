"""Vista de los cuatro modulos de metodos numericos de la calculadora."""

import os
import sys

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
INTERFACE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
for directory in (PROJECT_DIR, INTERFACE_DIR):
    if directory not in sys.path:
        sys.path.insert(0, directory)

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox, QFrame, QGridLayout, QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QPushButton, QScrollArea, QStackedWidget, QSizePolicy, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget,
)

from controlador_metodos_numericos import ControladorMetodosNumericos
from sleeping_dog import SleepingDogContainer
from vistas.componentes import CollapsibleCard


class _CurrentPageStack(QStackedWidget):
    """Ajusta su alto a la página visible para no reservar el espacio de otras opciones."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        self.currentChanged.connect(self._fit_current_page)

    def sizeHint(self):
        page = self.currentWidget()
        return page.sizeHint() if page is not None else super().sizeHint()

    def minimumSizeHint(self):
        page = self.currentWidget()
        return page.minimumSizeHint() if page is not None else super().minimumSizeHint()

    def _fit_current_page(self):
        page = self.currentWidget()
        if page is not None:
            self.setFixedHeight(page.sizeHint().height())
        self.updateGeometry()


class VistaMetodosNumericos(QWidget):
    """Captura los datos, delega calculos al controlador y presenta resultados."""

    METODOS = (
        "Método de Bisección",
        "Graficador de funciones",
        "Notación posicional (base 10 y base 2)",
        "Errores numéricos",
    )

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ultimo_resultado_biseccion = None
        self._construir_interfaz()

    def _construir_interfaz(self):
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

        title = QLabel("Métodos Numéricos")
        title.setStyleSheet("font-size: 24px; font-weight: 800; color: #0F172A;")
        subtitle = QLabel("Explora raíces, gráficas, representación numérica y errores.")
        subtitle.setStyleSheet("font-size: 13px; color: #64748B; font-weight: 500;")
        layout.addWidget(title)
        layout.addWidget(subtitle)

        self.card = QFrame()
        self.card.setObjectName("inputCard")
        self.card.setStyleSheet("QFrame#inputCard { background: white; border: 1px solid #E2E8F0; border-radius: 16px; }")
        card = QVBoxLayout(self.card)
        card.setContentsMargins(28, 24, 28, 24)
        card.setSpacing(20)
        selector_row = QHBoxLayout()
        selector_label = QLabel("MÉTODO")
        selector_label.setStyleSheet(self._label_style())
        self.selector = QComboBox()
        self.selector.addItems(self.METODOS)
        self.selector.setMinimumHeight(40)
        self.selector.setStyleSheet(self._combo_style())
        selector_row.addWidget(selector_label)
        selector_row.addWidget(self.selector, 1)
        card.addLayout(selector_row)

        self.pages = _CurrentPageStack()
        self.pages.setObjectName("methodPages")
        self.pages.setStyleSheet("QStackedWidget#methodPages { background: transparent; border: none; }")
        self._crear_formulario_biseccion()
        self._crear_formulario_grafica()
        self._crear_formulario_posicional()
        self._crear_formulario_errores()
        self.pages._fit_current_page()
        card.addWidget(self.pages)
        self.selector.currentIndexChanged.connect(self.pages.setCurrentIndex)

        actions = QHBoxLayout()
        self.solve_button = QPushButton("Calcular")
        self.solve_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.solve_button.setStyleSheet("QPushButton { background: #2563EB; color: white; font-weight: 700; padding: 11px 20px; border: 0; border-radius: 10px; } QPushButton:hover { background: #1D4ED8; }")
        self.solve_button.clicked.connect(self._calcular)
        clear_button = QPushButton("Limpiar")
        clear_button.setCursor(Qt.CursorShape.PointingHandCursor)
        clear_button.setStyleSheet("QPushButton { background: white; color: #1E293B; padding: 11px 22px; border: 1px solid #CBD5E1; border-radius: 10px; } QPushButton:hover { background: #F8FAFC; }")
        clear_button.clicked.connect(self._limpiar)
        actions.addWidget(self.solve_button)
        actions.addWidget(clear_button)
        actions.addStretch()
        card.addLayout(actions)
        layout.addWidget(self.card)

        self.results_card = QWidget()
        result_layout = QVBoxLayout(self.results_card)
        result_layout.setContentsMargins(0, 0, 0, 0)
        result_layout.setSpacing(16)
        back = QPushButton("← Volver a los datos")
        back.setCursor(Qt.CursorShape.PointingHandCursor)
        back.setStyleSheet("QPushButton { color: #64748B; font-weight: 600; font-size: 13px; border: none; background: transparent; text-align: left; padding: 0px; } QPushButton:hover { color: #0F172A; }")
        back.clicked.connect(self._volver_a_entrada)
        result_layout.addWidget(back)
        self.card_proceso = CollapsibleCard("Procedimiento")
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

    @staticmethod
    def _label_style():
        return "color: #64748B; font-size: 10px; font-weight: 700; letter-spacing: 0.5px; background: transparent;"

    @staticmethod
    def _combo_style():
        return ("QComboBox { background: #FFFFFF; border: 1px solid #2563EB; border-radius: 8px; "
                "padding: 8px 12px; color: #0F172A; } QComboBox:focus { border: 1px solid #2563EB; } "
                "QComboBox::drop-down { border: none; width: 0px; } "
                "QComboBox::down-arrow { image: none; width: 0px; height: 0px; }")

    @staticmethod
    def _field(label, default=""):
        wrapper = QVBoxLayout()
        wrapper.setSpacing(6)
        caption = QLabel(label.upper())
        caption.setStyleSheet(VistaMetodosNumericos._label_style())
        edit = QLineEdit(str(default))
        edit.setFixedHeight(38)
        edit.setStyleSheet("QLineEdit { background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; color: #0F172A; padding: 0 10px; } QLineEdit:focus { border: 1px solid #2563EB; }")
        wrapper.addWidget(caption)
        wrapper.addWidget(edit)
        return wrapper, edit

    def _form_page(self, helper):
        page = QWidget()
        page.setStyleSheet("background: #FFFFFF;")
        self.pages.addWidget(page)
        helper(page)

    def _crear_formulario_biseccion(self):
        def build(page):
            grid = QGridLayout(page)
            grid.setHorizontalSpacing(16)
            grid.setVerticalSpacing(14)
            self.funcion_bis, self.expresion_bis = self._field("Función f(x)", "x**3 - 2*x - 5")
            grid.addLayout(self.funcion_bis, 0, 0, 1, 2)
            self.a_field = self._field("Extremo inferior a", "2")[1]
            self.b_field = self._field("Extremo superior b", "3")[1]
            self.tol_field = self._field("Tolerancia absoluta E", "0.0001")[1]
            self.iter_field = self._field("Máximo de iteraciones", "100")[1]
            for col, (label, field) in enumerate((("EXTREMO INFERIOR a", self.a_field), ("EXTREMO SUPERIOR b", self.b_field), ("TOLERANCIA ABSOLUTA E", self.tol_field), ("MÁXIMO DE ITERACIONES", self.iter_field))):
                box = QVBoxLayout()
                caption = QLabel(label)
                caption.setStyleSheet(self._label_style())
                box.addWidget(caption)
                field.setFixedHeight(38)
                field.setStyleSheet("QLineEdit { background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; color: #0F172A; padding: 0 10px; } QLineEdit:focus { border: 1px solid #2563EB; }")
                box.addWidget(field)
                grid.addLayout(box, 1 + col // 2, col % 2)
            note = QLabel("Usa ** para potencias; se admiten sin, cos, tan, exp, log, sqrt, abs, pi y e. La continuidad en el intervalo es un supuesto que debe revisar quien usa el método.")
            note.setWordWrap(True)
            note.setStyleSheet("color: #64748B; font-size: 11px; background: transparent;")
            grid.addWidget(note, 3, 0, 1, 2)
        self._form_page(build)

    def _crear_formulario_grafica(self):
        def build(page):
            grid = QGridLayout(page)
            grid.setHorizontalSpacing(16)
            self.funcion_graf, self.expresion_graf = self._field("Función f(x)", "1/x")
            grid.addLayout(self.funcion_graf, 0, 0, 1, 2)
            self.xmin_field = self._field("Límite inferior xₘᵢₙ", "-3")[1]
            self.xmax_field = self._field("Límite superior xₘₐₓ", "3")[1]
            for col, (label, field) in enumerate((("LÍMITE INFERIOR xₘᵢₙ", self.xmin_field), ("LÍMITE SUPERIOR xₘₐₓ", self.xmax_field))):
                box = QVBoxLayout()
                caption = QLabel(label)
                caption.setStyleSheet(self._label_style())
                box.addWidget(caption)
                field.setFixedHeight(38)
                field.setStyleSheet("QLineEdit { background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; color: #0F172A; padding: 0 10px; }")
                box.addWidget(field)
                grid.addLayout(box, 1, col)
            self.use_bisection = __import__("PySide6.QtWidgets", fromlist=["QCheckBox"]).QCheckBox("Marcar la raíz e intervalo de la última bisección")
            self.use_bisection.setStyleSheet("color: #64748B; font-size: 12px; background: transparent;")
            grid.addWidget(self.use_bisection, 2, 0, 1, 2)
            note = QLabel("Admite funciones lineales, polinomiales, racionales, radicales, exponenciales, logarítmicas, trigonométricas y de valor absoluto.")
            note.setWordWrap(True)
            note.setStyleSheet("color: #64748B; font-size: 11px; background: transparent;")
            grid.addWidget(note, 3, 0, 1, 2)
        self._form_page(build)

    def _crear_formulario_posicional(self):
        def build(page):
            grid = QGridLayout(page)
            self.valor_pos_layout, self.valor_pos = self._field("Número entero", "84506")
            box = QVBoxLayout()
            caption = QLabel("BASE DE ENTRADA")
            caption.setStyleSheet(self._label_style())
            box.addWidget(caption)
            self.base_selector = QComboBox()
            self.base_selector.addItems(("10", "2"))
            self.base_selector.setFixedHeight(38)
            self.base_selector.setStyleSheet(self._combo_style())
            box.addWidget(self.base_selector)
            grid.addLayout(self.valor_pos_layout, 0, 0)
            grid.addLayout(box, 0, 1)
            note = QLabel("Se muestra cada dígito multiplicado por su potencia y su equivalente en la otra base. Si el entero es negativo, el signo se conserva y se descompone el valor absoluto.")
            note.setWordWrap(True)
            note.setStyleSheet("color: #64748B; font-size: 11px; background: transparent;")
            grid.addWidget(note, 1, 0, 1, 2)
        self._form_page(build)

    def _crear_formulario_errores(self):
        page = QWidget()
        page.setStyleSheet("background: #FFFFFF;")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)
        caption = QLabel("OPCIÓN DE ANÁLISIS")
        caption.setStyleSheet(self._label_style())
        self.error_option = QComboBox()
        self.error_option.addItems((
            "Cálculo directo",
            "Propagación del error",
            "Truncamiento vs. redondeo",
            "Inestabilidad numérica",
            "Tipos de errores",
            "Representación de punto flotante",
        ))
        self.error_option.setMinimumHeight(38)
        self.error_option.setStyleSheet(self._combo_style())
        layout.addWidget(caption)
        layout.addWidget(self.error_option)
        self.error_pages = _CurrentPageStack()
        self.error_pages.setObjectName("errorPages")
        self.error_pages.setStyleSheet("QStackedWidget#errorPages { background: #FFFFFF; border: none; }")
        self.error_pages.addWidget(self._formulario_error_directo())
        self.error_pages.addWidget(self._formulario_propagar())
        self.error_pages.addWidget(self._formulario_truncamiento())
        self.error_pages.addWidget(self._formulario_inestabilidad())
        self.error_pages.addWidget(self._formulario_info("Consulta las definiciones y ejemplos de las seis fuentes de error numérico."))
        self.error_pages.addWidget(self._formulario_info("Consulta la comparación 0.1 + 0.2, el épsilon de máquina y ejemplos de overflow y underflow."))
        self.error_pages._fit_current_page()
        self.error_option.currentIndexChanged.connect(self.error_pages.setCurrentIndex)
        self.error_option.currentIndexChanged.connect(self._actualizar_altura_error)
        layout.addWidget(self.error_pages)
        self.pages.addWidget(page)

    def _actualizar_altura_error(self):
        self.error_pages._fit_current_page()
        pagina_errores = self.pages.widget(3)
        if pagina_errores is not None:
            pagina_errores.updateGeometry()
        self.pages._fit_current_page()

    def _formulario_error_directo(self):
        page = QWidget()
        page.setStyleSheet("background: #FFFFFF;")
        grid = QGridLayout(page)
        grid.setContentsMargins(0, 8, 0, 0)
        grid.setHorizontalSpacing(16)
        grid.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.xv_field = self._new_line_edit("1")
        self.xa_field = self._new_line_edit("0.99")
        for col, (label, field) in enumerate((("VALOR VERDADERO xᵥ", self.xv_field), ("VALOR APROXIMADO xₐ", self.xa_field))):
            grid.addLayout(self._field_layout(label, field), 0, col)
        return page

    def _formulario_propagar(self):
        page = QWidget()
        page.setStyleSheet("background: #FFFFFF;")
        grid = QGridLayout(page)
        grid.setContentsMargins(0, 8, 0, 0)
        grid.setHorizontalSpacing(16)
        grid.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.expresion_prop = self._new_line_edit("sin(x) + x**2")
        self.x_prop_field = self._new_line_edit("0.5")
        self.dx_prop_field = self._new_line_edit("0.01")
        grid.addLayout(self._field_layout("FUNCIÓN f(x)", self.expresion_prop), 0, 0, 1, 2)
        grid.addLayout(self._field_layout("PUNTO x", self.x_prop_field), 1, 0)
        grid.addLayout(self._field_layout("PERTURBACIÓN Δx", self.dx_prop_field), 1, 1)
        note = QLabel("La derivada se estima numéricamente con diferencias centrales: f′(x) ≈ [f(x+h) − f(x−h)]/(2h).")
        note.setWordWrap(True)
        note.setStyleSheet("color: #64748B; font-size: 11px; background: transparent;")
        grid.addWidget(note, 2, 0, 1, 2)
        return page

    def _formulario_truncamiento(self):
        page = QWidget()
        page.setStyleSheet("background: #FFFFFF;")
        grid = QGridLayout(page)
        grid.setContentsMargins(0, 8, 0, 0)
        grid.setHorizontalSpacing(16)
        grid.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.x_series_field = self._new_line_edit("1")
        self.terms_field = self._new_line_edit("30")
        grid.addLayout(self._field_layout("VALOR x PARA exp(x)", self.x_series_field), 0, 0)
        grid.addLayout(self._field_layout("MÁXIMO DE TÉRMINOS (2–200)", self.terms_field), 0, 1)
        note = QLabel("Simula la serie de Taylor término a término. Grafica el error de truncamiento y el error de redondeo estimado en cada iteración.")
        note.setWordWrap(True)
        note.setStyleSheet("color: #64748B; font-size: 11px; background: transparent;")
        grid.addWidget(note, 1, 0, 1, 2)
        return page

    def _formulario_inestabilidad(self):
        page = QWidget()
        page.setStyleSheet("background: #FFFFFF;")
        grid = QGridLayout(page)
        grid.setContentsMargins(0, 8, 0, 0)
        grid.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.x_instability_field = self._new_line_edit("1e16")
        grid.addLayout(self._field_layout("VALOR x (x ≥ 0)", self.x_instability_field), 0, 0)
        note = QLabel("Compara √(x+1) − √x con su forma racionalizada 1/[√(x+1) + √x]. Ambas son equivalentes, pero la resta directa puede perder precisión.")
        note.setWordWrap(True)
        note.setStyleSheet("color: #64748B; font-size: 11px; background: transparent;")
        grid.addWidget(note, 1, 0)
        return page

    @staticmethod
    def _formulario_info(texto):
        page = QWidget()
        page.setStyleSheet("background: #FFFFFF;")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 8, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        note = QLabel(texto)
        note.setWordWrap(True)
        note.setStyleSheet("color: #64748B; font-size: 12px; background: transparent;")
        layout.addWidget(note)
        return page

    @staticmethod
    def _new_line_edit(default=""):
        edit = QLineEdit(default)
        edit.setFixedHeight(38)
        edit.setStyleSheet("QLineEdit { background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; color: #0F172A; padding: 0 10px; } QLineEdit:focus { border: 1px solid #2563EB; }")
        return edit

    @staticmethod
    def _field_layout(label, field):
        box = QVBoxLayout()
        box.setContentsMargins(0, 0, 0, 0)
        box.setSpacing(6)
        caption = QLabel(label)
        caption.setStyleSheet(VistaMetodosNumericos._label_style())
        caption.setFixedHeight(16)
        field.setFixedHeight(38)
        field.setStyleSheet("QLineEdit { background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; color: #0F172A; padding: 0 10px; } QLineEdit:focus { border: 1px solid #2563EB; }")
        box.addWidget(caption)
        box.addWidget(field)
        return box

    def _calcular(self):
        try:
            metodo = self.selector.currentIndex()
            if metodo == 0:
                result = ControladorMetodosNumericos.resolver_biseccion(
                    self.expresion_bis.text(), self.a_field.text(), self.b_field.text(),
                    self.tol_field.text(), self.iter_field.text(),
                )
                self.ultimo_resultado_biseccion = result
                self._mostrar_biseccion(result)
            elif metodo == 1:
                self._mostrar_grafica()
            elif metodo == 2:
                result = ControladorMetodosNumericos.convertir_notacion(
                    self.valor_pos.text(), int(self.base_selector.currentText())
                )
                self._mostrar_notacion(result)
            else:
                self._calcular_error_seleccionado()
                return
        except (ValueError, TypeError, OverflowError, ArithmeticError) as exc:
            self._mostrar_error(str(exc))

    def _calcular_error_seleccionado(self):
        try:
            opcion = self.error_option.currentIndex()
            if opcion == 0:
                resultado = ControladorMetodosNumericos.calcular_errores(
                    self.xv_field.text(), self.xa_field.text()
                )
                self._mostrar_errores(resultado)
            elif opcion == 1:
                resultado = ControladorMetodosNumericos.propagar_error(
                    self.expresion_prop.text(), self.x_prop_field.text(), self.dx_prop_field.text()
                )
                self._mostrar_propagacion(resultado)
            elif opcion == 2:
                resultado = ControladorMetodosNumericos.comparar_truncamiento_redondeo(
                    self.x_series_field.text(), self.terms_field.text()
                )
                self._mostrar_comparacion_errores(resultado)
            else:
                if opcion == 3:
                    resultado = ControladorMetodosNumericos.comparar_inestabilidad(
                        self.x_instability_field.text()
                    )
                    self._mostrar_inestabilidad(resultado)
                elif opcion == 4:
                    self._mostrar_tipos_error()
                else:
                    self._mostrar_representacion()
        except (ValueError, TypeError, OverflowError, ArithmeticError) as exc:
            self._mostrar_error(str(exc))

    def _mostrar_propagacion(self, result):
        self._preparar_resultados(procedimiento_abierto=True)
        self._agregar_metrica(self.card_solucion.content_layout, "Derivada numérica f′(x)", f"{result['derivada']:.12g}")
        self._agregar_metrica(self.card_solucion.content_layout, "Cambio aproximado Δy", f"{result['cambio_aproximado']:.12g}")
        self._agregar_metrica(self.card_solucion.content_layout, "Cambio real Δy", f"{result['cambio_real']:.12g}")
        self._agregar_metrica(self.card_solucion.content_layout, "Diferencia absoluta", f"{result['diferencia']:.12g}")
        self._agregar_paso("Función y perturbación", f"f(x) = {self.expresion_prop.text()}, x = {self.x_prop_field.text()} y Δx = {self.dx_prop_field.text()}.")
        self._agregar_paso("Derivada numérica", f"f′(x) ≈ [f(x+h) − f(x−h)]/(2h), con h = {result['h']:.6g}.")
        self._agregar_paso("Cambio aproximado", f"Δy ≈ f′(x) · Δx = {result['cambio_aproximado']:.12g}.")
        self._agregar_paso("Cambio real", f"Δy = f(x + Δx) − f(x) = {result['fx_delta']:.12g} − {result['fx']:.12g} = {result['cambio_real']:.12g}.")
        self._agregar_paso("Orden de aproximación", "La estimación mediante derivada es de primer orden en Δx; suele mejorar cuando la perturbación es pequeña.")

    def _mostrar_comparacion_errores(self, result):
        from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
        from matplotlib.figure import Figure

        self._preparar_resultados(procedimiento_abierto=True)
        ultimo = result["tabla"][-1]
        self._agregar_metrica(self.card_solucion.content_layout, "Suma float final", f"{ultimo['suma']:.16g}")
        self._agregar_metrica(self.card_solucion.content_layout, "Referencia exp(x)", f"{result['referencia']:.16g}")
        self._agregar_metrica(self.card_solucion.content_layout, "Error de truncamiento final", f"{ultimo['error_truncamiento']:.6g}")
        self._agregar_metrica(self.card_solucion.content_layout, "Error de redondeo final", f"{ultimo['error_redondeo']:.6g}")

        figure = Figure(figsize=(8, 4.8), tight_layout=True)
        canvas = FigureCanvasQTAgg(figure)
        ax = figure.add_subplot(111)
        n_values = [fila["n"] for fila in result["tabla"]]
        trunc_values = [max(fila["error_truncamiento"], 1e-300) for fila in result["tabla"]]
        rounding_values = [max(fila["error_redondeo"], 1e-300) for fila in result["tabla"]]
        ax.plot(n_values, trunc_values, color="#2563EB", linewidth=2, label="Error de truncamiento")
        ax.plot(n_values, rounding_values, color="#EA580C", linewidth=2, label="Error de redondeo")
        ax.set_yscale("log")
        ax.set_title("Truncamiento y redondeo en la serie de exp(x)")
        ax.set_xlabel("Términos de la serie")
        ax.set_ylabel("Error absoluto (escala logarítmica)")
        ax.grid(True, alpha=0.3)
        ax.legend()
        canvas.setMinimumHeight(380)
        self.card_solucion.add_widget(canvas)
        self._agregar_paso("Serie de Taylor", f"Aproximación iterativa de {result['funcion']} para x = {result['x']:g}. La tabla compara en cada n la suma calculada en float con la referencia de alta precisión.")
        self._agregar_paso("Separación de errores", "El error de truncamiento compara la suma ideal de n términos con exp(x); el error de redondeo compara la suma float con esa misma suma ideal.")
        headers = ("n", "Suma float", "Error de truncamiento", "Error de redondeo")
        table = QTableWidget(len(result["tabla"]), len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.setAlternatingRowColors(True)
        table.setStyleSheet("QTableWidget { background: white; alternate-background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; color: #0F172A; gridline-color: #E2E8F0; } QHeaderView::section { background: #F1F5F9; color: #475569; font-weight: 700; border: none; border-bottom: 1px solid #E2E8F0; padding: 8px 5px; }")
        for i, fila in enumerate(result["tabla"]):
            valores = (fila["n"], fila["suma"], fila["error_truncamiento"], fila["error_redondeo"])
            for j, valor in enumerate(valores):
                item = QTableWidgetItem(f"{valor:.8g}" if isinstance(valor, float) else str(valor))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                table.setItem(i, j, item)
            table.setRowHeight(i, 32)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        table.horizontalHeader().setStretchLastSection(True)
        table.setMinimumHeight(min(420, max(120, len(result["tabla"]) * 32 + 42)))
        self.card_proceso.add_widget(table)

    def _mostrar_inestabilidad(self, result):
        self._preparar_resultados(procedimiento_abierto=True)
        self._agregar_metrica(self.card_solucion.content_layout, "Resultado directo", f"{result['directo']:.12g}")
        self._agregar_metrica(self.card_solucion.content_layout, "Resultado reformulado", f"{result['reformulado']:.12g}")
        self._agregar_metrica(self.card_solucion.content_layout, "Referencia de alta precisión", f"{result['referencia']:.12g}")
        self._agregar_metrica(self.card_solucion.content_layout, "Error absoluto directo", f"{result['error_directo']:.6g}")
        self._agregar_metrica(self.card_solucion.content_layout, "Error absoluto reformulado", f"{result['error_reformulado']:.6g}")
        self._agregar_paso("Forma directa", f"Para x = {result['x']:.12g}: {result['formula_directa']} = {result['directo']:.12g}. Restar dos raíces muy cercanas puede causar cancelación y pérdida de cifras significativas.")
        self._agregar_paso("Forma racionalizada", f"{result['formula_reformulada']} = {result['reformulado']:.12g}. La reformulación reduce la cancelación. Referencia de alta precisión: {result['referencia']:.12g}.")

    @staticmethod
    def _limpiar_layout(layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.hide()
                widget.deleteLater()
            elif item.layout() is not None:
                VistaMetodosNumericos._limpiar_layout(item.layout())

    def _preparar_resultados(self, procedimiento_abierto=False):
        self._limpiar_layout(self.card_solucion.content_layout)
        self._limpiar_layout(self.card_proceso.content_layout)
        self.card_solucion.show()
        self._numero_paso = 0
        self.card_solucion.is_expanded = True
        self.card_solucion.content_widget.show()
        self.card_solucion.btn_toggle.setText("−")
        self.card_proceso.is_expanded = procedimiento_abierto
        self.card_proceso.content_widget.setVisible(procedimiento_abierto)
        self.card_proceso.btn_toggle.setText("−" if procedimiento_abierto else "+")
        self.card.hide()
        self.results_card.show()
        self.dog_main.hide()

    @staticmethod
    def _texto_resultado(texto, estilo="normal"):
        label = QLabel(texto)
        label.setWordWrap(True)
        if estilo == "titulo":
            label.setStyleSheet("color: #64748B; font-size: 10px; font-weight: 700; letter-spacing: 0.5px; background: transparent; border: none;")
        elif estilo == "valor":
            label.setStyleSheet("color: #0F172A; font-size: 15px; font-weight: 700; background: transparent; border: none;")
        elif estilo == "error":
            label.setStyleSheet("color: #B91C1C; font-size: 13px; background: transparent; border: none;")
        else:
            label.setStyleSheet("color: #334155; font-size: 13px; background: transparent; border: none;")
        return label

    def _agregar_paso(self, titulo, descripcion):
        self._numero_paso = getattr(self, "_numero_paso", 0) + 1
        frame = QFrame()
        frame.setObjectName("NumericMethodStep")
        frame.setStyleSheet("QFrame#NumericMethodStep { background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; }")
        row = QHBoxLayout(frame)
        row.setContentsMargins(16, 14, 16, 14)
        row.setSpacing(12)
        badge = QLabel(str(self._numero_paso))
        badge.setFixedSize(28, 28)
        badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        badge.setStyleSheet("background: #EEF2FF; color: #4F46E5; font-size: 13px; font-weight: 700; border: none; border-radius: 14px;")
        row.addWidget(badge, alignment=Qt.AlignmentFlag.AlignTop)
        body = QVBoxLayout()
        body.setSpacing(7)
        heading = self._texto_resultado(titulo.upper(), "titulo")
        detail = self._texto_resultado(descripcion)
        detail.setStyleSheet("color: #334155; font-size: 13px; background: transparent; border: none;")
        body.addWidget(heading)
        body.addWidget(detail)
        row.addLayout(body, 1)
        self.card_proceso.add_widget(frame)

    def _agregar_metrica(self, contenedor, titulo, valor):
        bloque = QFrame()
        bloque.setStyleSheet("QFrame { background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 10px; }")
        caja = QVBoxLayout(bloque)
        caja.setContentsMargins(14, 11, 14, 11)
        caja.setSpacing(5)
        caja.addWidget(self._texto_resultado(titulo.upper(), "titulo"))
        caja.addWidget(self._texto_resultado(str(valor), "valor"))
        contenedor.addWidget(bloque)

    def _mostrar_error(self, mensaje):
        self._preparar_resultados()
        self.card_solucion.add_widget(self._texto_resultado("No se pudo completar el cálculo. Corrige los datos e inténtalo de nuevo.", "error"))
        self.card_solucion.add_widget(self._texto_resultado(mensaje))

    def _mostrar_biseccion(self, result):
        self._preparar_resultados(procedimiento_abierto=True)
        resumen = QGridLayout()
        resumen.setHorizontalSpacing(12)
        resumen.setVerticalSpacing(10)
        items = [
            ("Raíz aproximada xᵣ", f"{result['raiz']:.12g}"),
            ("f(xᵣ)", f"{result['f_raiz']:.8g}"),
            ("Cota del error Eᵦ", f"{result['cota']:.6g}"),
            ("Estado", result["estado"]),
            ("Iteraciones ejecutadas", result["iteraciones"]),
            ("Mínimo teórico de iteraciones", result["teoricas"]),
            ("Error relativo aproximado", result["error_relativo"]),
        ]
        for i, (titulo, valor) in enumerate(items):
            frame = QFrame()
            frame.setStyleSheet("QFrame { background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 10px; }")
            box = QVBoxLayout(frame)
            box.setContentsMargins(14, 11, 14, 11)
            box.setSpacing(5)
            box.addWidget(self._texto_resultado(titulo.upper(), "titulo"))
            box.addWidget(self._texto_resultado(str(valor), "valor"))
            resumen.addWidget(frame, i // 2, i % 2)
        resumen_widget = QWidget()
        resumen_widget.setLayout(resumen)
        self.card_solucion.add_widget(resumen_widget)
        if result.get("diferencia_scipy") is not None:
            self.card_solucion.add_widget(self._texto_resultado(
                f"Comparación con SciPy: raíz = {result['scipy']:.12g}; diferencia absoluta = {result['diferencia_scipy']:.6g}."
            ))
        elif result.get("aviso_scipy"):
            self.card_solucion.add_widget(self._texto_resultado(result["aviso_scipy"]))
        headers = ("k", "a", "b", "xᵣ", "f(a)", "f(b)", "f(xᵣ)", "Eᵦ", "εₐ")
        if not result["tabla"]:
            a, b = result["intervalo_inicial"]
            fa, fb = result["funcion"](a), result["funcion"](b)
            raiz_extremo = a if fa == 0 else b
            self._agregar_paso("Raíz exacta en un extremo", f"f({raiz_extremo:g}) = 0. La raíz ya está en un extremo del intervalo [{a:g}, {b:g}], por lo que no se requieren iteraciones ni una tabla de bisección.")
            return
        self._agregar_paso("Procedimiento de bisección", "La tabla registra a, b y sus evaluaciones antes de actualizar el intervalo. Eᵦ es el semiancho usado en esa iteración. La continuidad debe verificarse matemáticamente; un cambio de signo por sí solo no la garantiza.")
        table = QTableWidget(len(result["tabla"]), len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        table.setAlternatingRowColors(True)
        table.setStyleSheet("QTableWidget { background: white; alternate-background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; color: #0F172A; gridline-color: #E2E8F0; } QHeaderView::section { background: #F1F5F9; color: #475569; font-weight: 700; border: none; border-bottom: 1px solid #E2E8F0; padding: 8px 5px; }")
        for row_index, row in enumerate(result["tabla"]):
            values = (row["k"], row["a"], row["b"], row["xr"], row["fa"], row["fb"], row["fr"], row["eb"], row["error_relativo"])
            for col_index, value in enumerate(values):
                text = f"{value:.8g}" if isinstance(value, float) else str(value)
                cell = QTableWidgetItem(text)
                cell.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                table.setItem(row_index, col_index, cell)
            table.setRowHeight(row_index, 34)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        table.horizontalHeader().setStretchLastSection(True)
        table.setMinimumHeight(min(430, max(100, len(result["tabla"]) * 34 + 42)))
        self.card_proceso.add_widget(table)

    def _mostrar_grafica(self):
        from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
        from matplotlib.figure import Figure
        raiz = intervalo = None
        if self.use_bisection.isChecked():
            if not self.ultimo_resultado_biseccion:
                raise ValueError("Primero ejecute una bisección para marcar su raíz e intervalo.")
            anterior = self.ultimo_resultado_biseccion
            raiz = anterior["raiz"]
            intervalo = anterior["intervalo_inicial"]
        self._preparar_resultados(procedimiento_abierto=True)
        figure = Figure(figsize=(8, 4.8), tight_layout=True)
        canvas = FigureCanvasQTAgg(figure)
        ControladorMetodosNumericos.graficar(
            self.expresion_graf.text(), self.xmin_field.text(), self.xmax_field.text(),
            figure.add_subplot(111), raiz, intervalo, "Intervalo inicial de bisección",
        )
        canvas.setMinimumHeight(390)
        self.card_solucion.add_widget(canvas)
        self._agregar_paso("Función", f"f(x) = {self.expresion_graf.text()}.")
        self._agregar_paso("Intervalo mostrado", f"[{self.xmin_field.text()}, {self.xmax_field.text()}]. Se evalúan 1,201 puntos.")
        self._agregar_paso("Dominio", "Se omiten los valores fuera del dominio, no reales o no finitos.")

    def _mostrar_notacion(self, result):
        self._preparar_resultados(procedimiento_abierto=True)
        self._agregar_metrica(self.card_solucion.content_layout, "Equivalencia decimal · base 10", result["decimal"])
        self._agregar_metrica(self.card_solucion.content_layout, "Equivalencia binaria · base 2", result["binario"])
        self._agregar_paso("Base de origen", f"El número ingresado se interpreta en base {result['base']}.")
        self._agregar_paso("Descomposición posicional", result["expansion"])
        self._agregar_paso("Suma de los valores posicionales", result["suma"])

    def _mostrar_errores(self, result):
        self._preparar_resultados(procedimiento_abierto=True)
        self._agregar_metrica(self.card_solucion.content_layout, "Error absoluto", f"{result['absoluto']:.12g}")
        if result["relativo"] is None:
            relativo = porcentual = "No definido porque xᵥ = 0"
        else:
            relativo = f"{result['relativo']:.12g}"
            porcentual = f"{result['porcentual']:.12g}%"
        self._agregar_metrica(self.card_solucion.content_layout, "Error relativo", relativo)
        self._agregar_metrica(self.card_solucion.content_layout, "Error relativo porcentual", porcentual)
        for titulo, detalle in self._detalle_errores(result):
            self._agregar_paso(titulo, detalle)

    def _mostrar_tipos_error(self):
        self._preparar_resultados(procedimiento_abierto=True)
        self.card_solucion.hide()
        definiciones = ControladorMetodosNumericos.resumen_punto_flotante()["tipos_error"]
        for nombre, definicion, ejemplo in definiciones:
            self._agregar_paso(nombre, f"{definicion}\nEjemplo: {ejemplo}")

    def _mostrar_representacion(self):
        self._preparar_resultados(procedimiento_abierto=True)
        fp = ControladorMetodosNumericos.resumen_punto_flotante()["punto_flotante"]
        self._agregar_metrica(self.card_solucion.content_layout, "0.1 + 0.2 == 0.3", str(fp["igualdad"]))
        self._agregar_metrica(self.card_solucion.content_layout, "Suma almacenada", f"{fp['suma']:.17g}")
        self._agregar_metrica(self.card_solucion.content_layout, "Épsilon de máquina", f"{fp['epsilon']:.17g}")
        self._agregar_paso("Representación binaria", "La igualdad puede ser False porque 0.1 y 0.2 no tienen una representación binaria finita; las aproximaciones almacenadas no suman exactamente el valor almacenado para 0.3.")
        self._agregar_paso("Épsilon de máquina", f"ε = {fp['epsilon']:.17g}. Es la distancia entre 1.0 y el siguiente número float representable mayor en doble precisión.")
        self._agregar_paso("Ejemplo de overflow", f"1e308 × 1e308 = {fp['overflow']}; máximo finito aproximado = {fp['maximo']:.6g}.")
        self._agregar_paso("Ejemplo de underflow", f"1e-300 × 1e-300 = {fp['underflow']}; mínimo subnormal aproximado = {fp['minimo_subnormal']:.6g}.")
        self._agregar_paso("Interpretación", "Overflow y underflow dependen del tipo numérico, la operación y la plataforma; estos son resultados observados en el entorno actual.")

    def _detalle_errores(self, result):
        xv = self.xv_field.text().strip()
        xa = self.xa_field.text().strip()
        rows = [("Valor verdadero", f"xᵥ = {xv}"),
                ("Valor aproximado", f"xₐ = {xa}"),
                ("Error absoluto", f"Eₐ = |xᵥ − xₐ| = |{xv} − {xa}| = {result['absoluto']:.12g}")]
        if result["relativo"] is None:
            rows.append(("Error relativo", "Eᵣ = |xᵥ − xₐ| / |xᵥ|; no está definido porque xᵥ = 0."))
            rows.append(("Error relativo porcentual", "No está definido porque xᵥ = 0."))
        else:
            rows.append(("Error relativo", f"Eᵣ = |xᵥ − xₐ| / |xᵥ| = {result['relativo']:.12g}"))
            rows.append(("Error relativo porcentual", f"Eᵣ(%) = Eᵣ × 100 = {result['porcentual']:.12g}%"))
        return rows

    def _volver_a_entrada(self):
        self.results_card.hide()
        self.card.show()
        self.dog_main.show()

    def _limpiar(self):
        self.expresion_bis.setText("")
        self.a_field.setText("")
        self.b_field.setText("")
        self.tol_field.setText("")
        self.iter_field.setText("")
        self.expresion_graf.setText("")
        self.xmin_field.setText("")
        self.xmax_field.setText("")
        self.valor_pos.setText("")
        self.xv_field.setText("")
        self.xa_field.setText("")
        self.expresion_prop.setText("")
        self.x_prop_field.setText("")
        self.dx_prop_field.setText("")
        self.x_series_field.setText("")
        self.terms_field.setText("")
        self.x_instability_field.setText("")
        self.error_option.setCurrentIndex(0)
        self.use_bisection.setChecked(False)
        self._limpiar_layout(self.card_solucion.content_layout)
        self._limpiar_layout(self.card_proceso.content_layout)
        self.results_card.hide()
        self.card.show()
        self.dog_main.show()
