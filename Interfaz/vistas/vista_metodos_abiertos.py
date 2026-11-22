"""Vista del método abierto de Newton-Raphson."""

import os
import re
import sys

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
INTERFACE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
for directory in (PROJECT_DIR, INTERFACE_DIR):
    if directory not in sys.path:
        sys.path.insert(0, directory)

import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox, QFrame, QGridLayout, QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QPushButton, QScrollArea, QSizePolicy, QStackedWidget, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget,
)

from controlador_metodos_abiertos import ControladorMetodosAbiertos
from sleeping_dog import SleepingDogContainer
from vistas.componentes import CollapsibleCard


class VistaMetodosAbiertos(QWidget):
    """Captura los parámetros y presenta el procedimiento de Newton-Raphson."""

    def __init__(self, parent=None):
        super().__init__(parent)
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
        layout.setSpacing(20)

        title = QLabel("Métodos Abiertos")
        title.setStyleSheet("font-size: 24px; font-weight: 800; color: #0F172A;")
        subtitle = QLabel("Newton, secante, derivadas numéricas y raíces de polinomios")
        subtitle.setStyleSheet("font-size: 13px; color: #64748B; font-weight: 500;")
        layout.addWidget(title)
        layout.addWidget(subtitle)

        self.input_card = QFrame()
        self.input_card.setObjectName("inputCard")
        self.input_card.setStyleSheet("QFrame#inputCard { background: white; border: 1px solid #E2E8F0; border-radius: 16px; }")
        card = QVBoxLayout(self.input_card)
        card.setContentsMargins(28, 24, 28, 24)
        card.setSpacing(18)
        selector_row = QHBoxLayout()
        selector_label = QLabel("MÉTODO")
        selector_label.setStyleSheet("color: #64748B; font-size: 10px; font-weight: 700; letter-spacing: 0.5px; background: transparent;")
        self.metodo_selector = QComboBox()
        self.metodo_selector.addItems(("Newton-Raphson", "Secante", "Derivadas numéricas", "Horner y deflación", "Análisis de convergencia"))
        self.metodo_selector.setMinimumHeight(40)
        self.metodo_selector.setStyleSheet("QComboBox { background: #FFFFFF; border: 1px solid #2563EB; border-radius: 8px; padding: 8px 12px; color: #0F172A; } QComboBox QAbstractItemView { background: #FFFFFF; color: #0F172A; selection-background-color: #DBEAFE; }")
        selector_row.addWidget(selector_label)
        selector_row.addWidget(self.metodo_selector, 1)
        card.addLayout(selector_row)
        self.form_pages = QStackedWidget()
        self._crear_formularios()
        self.metodo_selector.currentIndexChanged.connect(self.form_pages.setCurrentIndex)
        card.addWidget(self.form_pages)

        actions = QHBoxLayout()
        self.calculate_button = QPushButton("Calcular")
        self.calculate_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.calculate_button.setStyleSheet("QPushButton { background: #2563EB; color: white; font-weight: 700; padding: 11px 20px; border: 0; border-radius: 10px; } QPushButton:hover { background: #1D4ED8; }")
        self.calculate_button.clicked.connect(self._calcular)
        clear_button = QPushButton("Limpiar")
        clear_button.setCursor(Qt.CursorShape.PointingHandCursor)
        clear_button.setStyleSheet("QPushButton { background: white; color: #1E293B; padding: 11px 22px; border: 1px solid #CBD5E1; border-radius: 10px; } QPushButton:hover { background: #F8FAFC; }")
        clear_button.clicked.connect(self._limpiar)
        actions.addWidget(self.calculate_button)
        actions.addWidget(clear_button)
        actions.addStretch()
        card.addLayout(actions)
        layout.addWidget(self.input_card)

        self.message = QLabel()
        self.message.setWordWrap(True)
        self.message.hide()
        layout.addWidget(self.message)
        self.results = QWidget()
        self.results_layout = QVBoxLayout(self.results)
        self.results_layout.setContentsMargins(0, 0, 0, 0)
        self.results_layout.setSpacing(14)
        back = QPushButton("← Volver a los datos")
        back.setCursor(Qt.CursorShape.PointingHandCursor)
        back.setStyleSheet("QPushButton { color: #64748B; font-weight: 600; font-size: 13px; border: none; background: transparent; text-align: left; padding: 0px; } QPushButton:hover { color: #0F172A; }")
        back.clicked.connect(self._volver_a_datos)
        self.results_layout.addWidget(back)
        self.card_proceso = CollapsibleCard("Procedimiento")
        self.card_proceso.is_expanded = True
        self.card_proceso.content_widget.show()
        self.card_proceso.btn_toggle.setText("−")
        self.results_layout.addWidget(self.card_proceso)
        self.card_solucion = CollapsibleCard("Solución")
        self.card_solucion.is_expanded = True
        self.card_solucion.content_widget.show()
        self.card_solucion.btn_toggle.setText("−")
        self.results_layout.addWidget(self.card_solucion)
        self.results.hide()
        layout.addWidget(self.results)

        self.dog_main = SleepingDogContainer(small=False)
        layout.addWidget(self.dog_main, alignment=Qt.AlignmentFlag.AlignCenter)
        outer.addWidget(content)
        scroll.setWidget(page)
        root.addWidget(scroll)

    def _crear_pagina_campos(self):
        page = QWidget()
        page.setStyleSheet("background: #FFFFFF;")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        grid = QGridLayout()
        grid.setHorizontalSpacing(16)
        grid.setVerticalSpacing(14)
        layout.addLayout(grid)
        return page, layout, grid

    def _agregar_nota(self, layout, texto):
        note = QLabel(texto)
        note.setWordWrap(True)
        note.setStyleSheet("color: #64748B; font-size: 11px; background: transparent;")
        layout.addWidget(note)

    def _crear_formularios(self):
        # Newton-Raphson con derivada simbólica.
        page, page_layout, grid = self._crear_pagina_campos()
        self.funcion = self._campo("Función f(x)")
        self.x0 = self._campo("Valor inicial x₀")
        self.tolerancia = self._campo("Tolerancia del error aproximado (%)", "0.001")
        self.tolerancia_residuo = self._campo("Tolerancia del residuo", "1e-8")
        self.max_iteraciones = self._campo("Máximo de iteraciones", "100")
        self.funcion.setText("x**3 - x - 2")
        self.x0.setText("1.5")
        grid.addLayout(self._envolver("FUNCIÓN f(x)", self.funcion), 0, 0, 1, 2)
        for col, (etiqueta, campo) in enumerate((
            ("VALOR INICIAL x₀", self.x0),
            ("TOLERANCIA DEL ERROR (%)", self.tolerancia),
            ("TOLERANCIA DEL RESIDUO", self.tolerancia_residuo),
            ("MÁXIMO DE ITERACIONES", self.max_iteraciones),
        )):
            grid.addLayout(self._envolver(etiqueta, campo), 1 + col // 2, col % 2)
        self._agregar_nota(page_layout, "Admite x, pi, e, operaciones +, −, ×, ÷, potencias y funciones trigonométricas, exp, log, sqrt y abs. SymPy deriva la expresión algebraicamente antes de iterar; por ejemplo, deriva x³ − x − 2 como 3x² − 1.")
        self.form_pages.addWidget(page)

        # Secante con dos valores iniciales, sin exigir cambio de signo.
        page, page_layout, grid = self._crear_pagina_campos()
        self.funcion_secante = self._campo("Función f(x)")
        self.secante_x0 = self._campo("Valor inicial x₀")
        self.secante_x1 = self._campo("Segundo valor inicial x₁")
        self.secante_tol = self._campo("Tolerancia del error aproximado (%)", "0.001")
        self.secante_residuo = self._campo("Tolerancia del residuo", "1e-8")
        self.secante_max = self._campo("Máximo de iteraciones", "100")
        self.funcion_secante.setText("x**3 - x - 2")
        self.secante_x0.setText("1")
        self.secante_x1.setText("2")
        grid.addLayout(self._envolver("FUNCIÓN f(x)", self.funcion_secante), 0, 0, 1, 2)
        for col, (etiqueta, campo) in enumerate((
            ("VALOR INICIAL x₀", self.secante_x0),
            ("SEGUNDO VALOR x₁", self.secante_x1),
            ("TOLERANCIA DEL ERROR (%)", self.secante_tol),
            ("TOLERANCIA DEL RESIDUO", self.secante_residuo),
            ("MÁXIMO DE ITERACIONES", self.secante_max),
        )):
            grid.addLayout(self._envolver(etiqueta, campo), 1 + col // 2, col % 2)
        self._agregar_nota(page_layout, "La secante estima la pendiente con dos aproximaciones previas. No requiere un intervalo que encierre la raíz; el denominador se revisa antes de dividir.")
        self.form_pages.addWidget(page)

        # Comparación de derivadas numéricas para un mismo punto y paso.
        page, page_layout, grid = self._crear_pagina_campos()
        self.funcion_derivada = self._campo("Función f(x)")
        self.punto_derivada = self._campo("Punto x")
        self.paso_derivada = self._campo("Paso h", "0.01")
        self.funcion_derivada.setText("sin(x)")
        self.punto_derivada.setText("0.5")
        grid.addLayout(self._envolver("FUNCIÓN f(x)", self.funcion_derivada), 0, 0, 1, 2)
        grid.addLayout(self._envolver("PUNTO x", self.punto_derivada), 1, 0)
        grid.addLayout(self._envolver("PASO h > 0", self.paso_derivada), 1, 1)
        self._agregar_nota(page_layout, "Compara diferencias hacia adelante, atrás y centrales con f′(x) simbólica. Adelante y atrás tienen truncamiento O(h); central, O(h²). Reducir h demasiado amplifica redondeo y cancelación.")
        self.form_pages.addWidget(page)

        # Newton para polinomios con esquema de Horner y deflación de una raíz.
        page, page_layout, grid = self._crear_pagina_campos()
        self.coeficientes_horner = self._campo("Coeficientes del polinomio")
        self.horner_x0 = self._campo("Valor inicial x₀")
        self.horner_tol = self._campo("Tolerancia del error aproximado (%)", "0.001")
        self.horner_residuo = self._campo("Tolerancia del residuo", "1e-8")
        self.horner_max = self._campo("Máximo de iteraciones", "100")
        self.coeficientes_horner.setText("1, 0, -1, -2")
        self.horner_x0.setText("1.5")
        grid.addLayout(self._envolver("COEFICIENTES (GRADO MAYOR A CONSTANTE)", self.coeficientes_horner), 0, 0, 1, 2)
        for col, (etiqueta, campo) in enumerate((
            ("VALOR INICIAL x₀", self.horner_x0),
            ("TOLERANCIA DEL ERROR (%)", self.horner_tol),
            ("TOLERANCIA DEL RESIDUO", self.horner_residuo),
            ("MÁXIMO DE ITERACIONES", self.horner_max),
        )):
            grid.addLayout(self._envolver(etiqueta, campo), 1 + col // 2, col % 2)
        self._agregar_nota(page_layout, "Escribe los coeficientes separados por coma, desde el término de mayor grado hasta el término independiente. Horner evalúa p(x) y p′(x) en cada paso; al converger se muestra la deflación por (x − r) y su residuo.")
        self.form_pages.addWidget(page)

        # Estima el orden observado sin precargar aproximaciones.
        page = QWidget()
        page.setStyleSheet("background: #FFFFFF;")
        theory = QVBoxLayout(page)
        theory.setContentsMargins(0, 0, 0, 0)
        theory.setSpacing(10)
        conv_grid = QGridLayout()
        self.aproximaciones_convergencia = [
            self._campo(f"Aproximación x{i}") for i in range(4)
        ]
        for i, campo in enumerate(self.aproximaciones_convergencia):
            conv_grid.addLayout(self._envolver(f"APROXIMACIÓN x{i}", campo), i // 2, i % 2)
        theory.addLayout(conv_grid)
        self._agregar_nota(theory, "Ingresa cuatro iterados consecutivos de un método, en orden. Se estiman p y C a partir de las diferencias entre iterados; este diagnóstico depende de la cercanía a la raíz y no garantiza convergencia.")
        for texto in (
            "Newton-Raphson suele tener orden cuadrático (p = 2) cerca de una raíz simple.",
            "La secante suele tener orden superlineal aproximado p = 1.618 bajo sus hipótesis.",
            "El orden medido es una estimación local; cuatro iterados por sí solos no prueban convergencia global.",
        ):
            bloque = QFrame()
            bloque.setStyleSheet("QFrame { background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 10px; }")
            label = QLabel(texto)
            label.setWordWrap(True)
            label.setStyleSheet("color: #334155; font-size: 12px; background: transparent; border: none; padding: 10px;")
            row = QHBoxLayout(bloque)
            row.setContentsMargins(5, 4, 10, 4)
            bullet = QFrame()
            bullet.setFixedSize(4, 24)
            bullet.setStyleSheet("background: #2563EB; border-radius: 2px;")
            row.addWidget(bullet)
            row.addWidget(label, 1)
            theory.addWidget(bloque)
        self.form_pages.addWidget(page)

    @staticmethod
    def _campo(etiqueta, valor=""):
        campo = QLineEdit(valor)
        campo.setFixedHeight(38)
        campo.setStyleSheet("QLineEdit { background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; color: #0F172A; padding: 0 10px; } QLineEdit:focus { border: 1px solid #2563EB; }")
        campo.setAccessibleName(etiqueta)
        return campo

    @staticmethod
    def _envolver(etiqueta, campo):
        caja = QVBoxLayout()
        caja.setSpacing(6)
        caption = QLabel(etiqueta)
        caption.setStyleSheet("color: #64748B; font-size: 10px; font-weight: 700; letter-spacing: 0.5px; background: transparent;")
        caja.addWidget(caption)
        caja.addWidget(campo)
        return caja

    @staticmethod
    def _expresion_html(expresion):
        texto = str(expresion)
        texto = re.sub(r"\*\*\(([^)]+)\)", r"<sup>\1</sup>", texto)
        texto = re.sub(r"\*\*([+-]?\d+(?:\.\d+)?)", r"<sup>\1</sup>", texto)
        texto = texto.replace("**", "^").replace("*", " · ")
        texto = texto.replace("pi", "π")
        return texto

    def _titulo_seccion(self, texto):
        contenedor = QWidget()
        contenedor.setStyleSheet("background: transparent;")
        fila = QHBoxLayout(contenedor)
        fila.setContentsMargins(0, 6, 0, 2)
        fila.setSpacing(8)
        indicador = QFrame()
        indicador.setFixedSize(4, 16)
        indicador.setStyleSheet("background: #2563EB; border-radius: 2px;")
        titulo = QLabel(texto)
        titulo.setStyleSheet("font-size: 15px; font-weight: 700; color: #0F172A; background: transparent;")
        fila.addWidget(indicador)
        fila.addWidget(titulo)
        fila.addStretch()
        self.card_solucion.add_widget(contenedor)

    def _calcular(self):
        try:
            metodo = self.metodo_selector.currentIndex()
            if metodo == 0:
                resultado = ControladorMetodosAbiertos.resolver_newton_raphson(
                    self.funcion.text(), self.x0.text(), self.tolerancia.text(),
                    self.max_iteraciones.text(), self.tolerancia_residuo.text(),
                )
            elif metodo == 1:
                resultado = ControladorMetodosAbiertos.resolver_secante(
                    self.funcion_secante.text(), self.secante_x0.text(),
                    self.secante_x1.text(), self.secante_tol.text(),
                    self.secante_max.text(), self.secante_residuo.text(),
                )
            elif metodo == 2:
                resultado = ControladorMetodosAbiertos.comparar_derivadas(
                    self.funcion_derivada.text(), self.punto_derivada.text(),
                    self.paso_derivada.text(),
                )
            elif metodo == 3:
                coeficientes = [valor.strip() for valor in self.coeficientes_horner.text().split(",")]
                resultado = ControladorMetodosAbiertos.resolver_polinomio_horner(
                    coeficientes, self.horner_x0.text(), self.horner_tol.text(),
                    self.horner_max.text(), self.horner_residuo.text(),
                )
            else:
                resultado = ControladorMetodosAbiertos.analizar_convergencia(
                    [campo.text() for campo in self.aproximaciones_convergencia]
                )
        except ImportError:
            self.results.hide()
            self.input_card.show()
            self.dog_main.show()
            self.message.setStyleSheet("color: #B91C1C; background: #FEF2F2; border: 1px solid #FECACA; border-radius: 10px; padding: 12px;")
            self.message.setText("Falta instalar SymPy y Pandas. Instala las dependencias del proyecto y vuelve a intentarlo.")
            self.message.show()
            return
        except (ValueError, TypeError, OverflowError, ArithmeticError) as exc:
            self.results.hide()
            self.input_card.show()
            self.dog_main.show()
            self.message.setStyleSheet("color: #B91C1C; background: #FEF2F2; border: 1px solid #FECACA; border-radius: 10px; padding: 12px;")
            self.message.setText(str(exc))
            self.message.show()
            return
        self.message.hide()
        if metodo == 0:
            self._mostrar_resultado(resultado)
        elif metodo == 1:
            self._mostrar_resultado_secante(resultado)
        elif metodo == 2:
            self._mostrar_resultado_derivadas(resultado)
        elif metodo == 3:
            self._mostrar_resultado_horner(resultado)
        else:
            self._mostrar_resultado_convergencia(resultado)

    def _limpiar(self):
        for campo in (
            self.funcion, self.x0, self.funcion_secante, self.secante_x0,
            self.secante_x1, self.funcion_derivada, self.punto_derivada,
            self.coeficientes_horner, self.horner_x0,
            *self.aproximaciones_convergencia,
        ):
            campo.clear()
        self.paso_derivada.setText("0.01")
        for campo in (self.tolerancia, self.secante_tol, self.horner_tol):
            campo.setText("0.001")
        for campo in (self.tolerancia_residuo, self.secante_residuo, self.horner_residuo):
            campo.setText("1e-8")
        for campo in (self.max_iteraciones, self.secante_max, self.horner_max):
            campo.setText("100")
        self.message.hide()
        self.results.hide()
        self.input_card.show()
        self.dog_main.show()
        self._vaciar_resultados()

    def _volver_a_datos(self):
        self.results.hide()
        self.input_card.show()
        self.dog_main.show()
        self.message.hide()

    def _vaciar_resultados(self):
        while self.card_solucion.content_layout.count():
            item = self.card_solucion.content_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        while self.card_proceso.content_layout.count():
            item = self.card_proceso.content_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def _agregar_paso_proceso(self, titulo, descripcion):
        numero = self.card_proceso.content_layout.count() + 1
        paso = QFrame()
        paso.setObjectName("PasoNewtonRaphson")
        paso.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        paso.setStyleSheet("QFrame#PasoNewtonRaphson { background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; }")
        fila = QHBoxLayout(paso)
        fila.setContentsMargins(16, 14, 16, 14)
        fila.setSpacing(12)
        numero_label = QLabel(str(numero))
        numero_label.setFixedSize(28, 28)
        numero_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        numero_label.setStyleSheet("background: #EEF2FF; color: #4F46E5; font-size: 13px; font-weight: 700; border: none; border-radius: 14px;")
        fila.addWidget(numero_label, alignment=Qt.AlignmentFlag.AlignTop)
        contenido = QVBoxLayout()
        contenido.setSpacing(7)
        encabezado = QLabel(titulo.upper())
        encabezado.setStyleSheet("color: #64748B; font-size: 10px; font-weight: 700; letter-spacing: 0.5px; background: transparent; border: none;")
        detalle = QLabel(descripcion)
        detalle.setWordWrap(True)
        detalle.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        detalle.setStyleSheet("color: #334155; font-size: 13px; background: transparent; border: none;")
        contenido.addWidget(encabezado)
        contenido.addWidget(detalle)
        fila.addLayout(contenido, 1)
        self.card_proceso.add_widget(paso)

    @staticmethod
    def _numero_proceso(valor):
        return f"{valor:.10g}"

    def _preparar_resultado(self):
        self._vaciar_resultados()
        self.input_card.hide()
        self.dog_main.hide()
        self.results.show()
        for tarjeta in (self.card_proceso, self.card_solucion):
            tarjeta.is_expanded = True
            tarjeta.content_widget.show()
            tarjeta.btn_toggle.setText("−")

    def _mostrar_procedimiento(self, resultado):
        fmt = self._numero_proceso
        self._agregar_paso_proceso(
            "Planteamiento y derivada",
            f"Se busca f(x) = 0 con f(x) = {resultado['expresion']}. "
            f"La derivada simbólica es f′(x) = {resultado['derivada']}. "
            f"Valor inicial: x₀ = {fmt(resultado['x0'])}.",
        )
        self._agregar_paso_proceso(
            "Recta tangente y corte con el eje x",
            "La tangente en xᵢ es y = f(xᵢ) + f′(xᵢ)(x − xᵢ). "
            "Al buscar su corte con el eje x se fija y = 0 y se despeja "
            "xᵢ₊₁ = xᵢ − f(xᵢ)/f′(xᵢ).",
        )
        self._agregar_paso_proceso(
            "Fórmula de Newton-Raphson",
            "En cada paso se evalúan f(xᵢ) y f′(xᵢ), y se calcula "
            "xᵢ₊₁ = xᵢ − f(xᵢ)/f′(xᵢ). Antes de dividir, el programa comprueba "
            "que |f′(xᵢ)| sea mayor que el umbral 1e-12.",
        )
        self._agregar_paso_proceso(
            "Criterio de error y parada",
            f"Se compara εₐ = |xᵢ₊₁ − xᵢ|/|xᵢ₊₁| × 100 con "
            f"ε = {fmt(resultado['tolerancia'])}%. Si xᵢ₊₁ = 0, se usa el error "
            f"absoluto. También se exige |f(xᵢ₊₁)| ≤ "
            f"{fmt(resultado['tolerancia_residuo'])}; el límite es "
            f"{resultado['max_iteraciones']} iteraciones.",
        )

        filas = resultado["tabla"].to_dict(orient="records")
        if not filas:
            if resultado["motivo_parada"] == "tolerancia":
                descripcion = (
                    f"|f(x₀)| = {fmt(resultado['residuo'])}; la aproximación inicial "
                    "ya satisface la tolerancia del residuo, por lo que no fue necesario iterar."
                )
            elif resultado["motivo_parada"] == "derivada_pequena":
                derivada_inicial = resultado["derivada_funcion"](resultado["x0"])
                descripcion = (
                    f"En x₀ = {fmt(resultado['x0'])}, f′(x₀) = {fmt(derivada_inicial)} "
                    "es cero o demasiado pequeña. El proceso se detuvo antes de dividir."
                )
            else:
                descripcion = resultado["estado"]
            self._agregar_paso_proceso("Revisión del valor inicial", descripcion)

        for indice, fila in enumerate(filas):
            i = fila["i"]
            xi = fila["xi"]
            fxi = fila["fxi"]
            dfxi = fila["dfxi"]
            siguiente = fila["x_siguiente"]
            sustitucion = (
                f"xᵢ₊₁ = xᵢ − f(xᵢ)/f′(xᵢ) = {fmt(xi)} − "
                f"({fmt(fxi)})/({fmt(dfxi)}) = {fmt(siguiente)}."
            )
            if fila["error_porcentual"] is None:
                error = (
                    f"εₐ = |xᵢ₊₁ − xᵢ| = |{fmt(siguiente)} − {fmt(xi)}| "
                    f"= {fmt(fila['error_absoluto'])} (absoluto, porque xᵢ₊₁ = 0)."
                )
            else:
                error = (
                    f"εₐ = |xᵢ₊₁ − xᵢ|/|xᵢ₊₁| × 100 = "
                    f"{fmt(fila['error_porcentual'])}%."
                )
            cumple_error = fila["error_criterio"] <= resultado["tolerancia"]
            cumple_residuo = fila["residuo"] <= resultado["tolerancia_residuo"]
            if indice < len(filas) - 1:
                cierre = "Al menos un criterio todavía no se cumple; se continúa con xᵢ₊₁."
            elif resultado["convergio"]:
                cierre = "Se cumplen el criterio de error y el del residuo; el método se detiene."
            elif resultado["motivo_parada"] == "maximo_iteraciones":
                cierre = f"Se alcanzó el máximo de {resultado['max_iteraciones']} iteraciones sin cumplir ambos criterios."
            elif resultado["motivo_parada"] == "derivada_pequena":
                cierre = "En el siguiente paso la derivada fue cero o demasiado pequeña; se detuvo antes de dividir."
            else:
                cierre = resultado["estado"]
            detalle = "\n".join((
                f"1. Aproximación actual: xᵢ = {fmt(xi)}.",
                f"2. Evaluaciones: f(xᵢ) = {fmt(fxi)}; f′(xᵢ) = {fmt(dfxi)}.",
                f"3. Actualización: {sustitucion}",
                f"4. Error aproximado: {error}",
                f"5. Residuo en la nueva aproximación: |f(xᵢ₊₁)| = {fmt(fila['residuo'])}.",
                f"6. Verificación: εₐ {'≤' if cumple_error else '>'} ε; residuo "
                f"{'≤' if cumple_residuo else '>'} su tolerancia. {cierre}",
            ))
            self._agregar_paso_proceso(f"Iteración {i}", detalle)

        self._agregar_paso_proceso(
            "Resultado final",
            f"{resultado['estado']} Última aproximación: "
            f"x ≈ {fmt(resultado['raiz_aproximada'])}; "
            f"residuo |f(x)| = "
            f"{'no finito' if resultado['residuo'] is None else fmt(resultado['residuo'])}.",
        )
        self._agregar_paso_proceso(
            "Convergencia local",
            "Para una raíz simple y un valor inicial suficientemente cercano, Newton puede "
            "converger cuadráticamente. No es una garantía global; en raíces múltiples el "
            "método estándar suele converger más lentamente.",
        )

    def _agregar_resumen(self, elementos):
        resumen = QFrame()
        resumen.setStyleSheet("QFrame { background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; }")
        grid = QGridLayout(resumen)
        grid.setContentsMargins(20, 16, 20, 16)
        grid.setHorizontalSpacing(24)
        grid.setVerticalSpacing(14)
        for indice, (etiqueta, valor) in enumerate(elementos):
            caja = QVBoxLayout()
            titulo = QLabel(etiqueta.upper())
            titulo.setStyleSheet("color: #64748B; font-size: 10px; font-weight: 700; background: transparent; border: none;")
            contenido = QLabel(str(valor))
            contenido.setWordWrap(True)
            contenido.setStyleSheet("color: #0F172A; font-size: 14px; font-weight: 700; background: transparent; border: none;")
            caja.addWidget(titulo)
            caja.addWidget(contenido)
            grid.addLayout(caja, indice // 2, indice % 2)
        self.card_solucion.add_widget(resumen)

    def _agregar_tabla(self, encabezados, filas, claves):
        tabla = QTableWidget(len(filas), len(encabezados))
        tabla.setHorizontalHeaderLabels(encabezados)
        tabla.verticalHeader().setVisible(False)
        tabla.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        tabla.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        tabla.setAlternatingRowColors(True)
        tabla.setStyleSheet("QTableWidget { background: white; alternate-background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; color: #0F172A; gridline-color: #E2E8F0; } QHeaderView::section { background: #F1F5F9; color: #475569; font-weight: 700; border: none; border-bottom: 1px solid #E2E8F0; padding: 8px 5px; }")
        for fila_indice, fila in enumerate(filas):
            for col_indice, clave in enumerate(claves):
                valor = fila[clave]
                texto = "—" if valor is None else (f"{valor:.8g}" if isinstance(valor, (float, np.floating)) else str(valor))
                celda = QTableWidgetItem(texto)
                celda.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                tabla.setItem(fila_indice, col_indice, celda)
            tabla.setRowHeight(fila_indice, 34)
        tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        tabla.horizontalHeader().setStretchLastSection(True)
        tabla.setMinimumHeight(min(430, max(100, len(filas) * 34 + 42)))
        self.card_solucion.add_widget(tabla)

    def _agregar_grafica(self, funcion, puntos, segmentos, titulo):
        from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
        from matplotlib.figure import Figure

        figure = Figure(figsize=(7, 4.2), tight_layout=True)
        axes = figure.add_subplot(111)
        margen_datos = list(puntos)
        for x1, _, x2, _ in segmentos:
            margen_datos.extend((x1, x2))
        xmin_base, xmax_base = min(margen_datos), max(margen_datos)
        ancho = xmax_base - xmin_base
        margen = max(ancho * 0.2, 0.5)
        xs = np.linspace(xmin_base - margen, xmax_base + margen, 800)
        with np.errstate(all="ignore"):
            ys = np.asarray(funcion(xs), dtype=float)
        if ys.ndim == 0:
            ys = np.full_like(xs, float(ys))
        ys[~np.isfinite(ys)] = np.nan
        axes.plot(xs, ys, color="#2563EB", linewidth=2, label="f(x)")
        axes.axhline(0, color="#64748B", linewidth=1)
        for indice, (x1, y1, x2, y2) in enumerate(segmentos):
            axes.plot([x1, x2], [y1, y2], "--", color="#F59E0B", alpha=0.7,
                      label="Rectas secantes/tangentes" if indice == 0 else None)
        for indice, x in enumerate(puntos):
            try:
                y = float(funcion(x))
            except (ArithmeticError, TypeError, ValueError, OverflowError):
                y = float("nan")
            axes.scatter([x], [y], color="#DC2626" if indice == len(puntos) - 1 else "#F59E0B",
                         s=36, zorder=3, label="Última aproximación" if indice == len(puntos) - 1 else None)
        axes.set_title(titulo)
        axes.set_xlabel("x")
        axes.set_ylabel("f(x)")
        axes.grid(True, alpha=0.25)
        axes.legend()
        canvas = FigureCanvasQTAgg(figure)
        canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        canvas.setMinimumHeight(330)
        self.card_solucion.add_widget(canvas)

    def _mostrar_resultado_secante(self, resultado):
        self._preparar_resultado()
        fmt = self._numero_proceso
        filas = resultado["tabla"].to_dict(orient="records")
        self._agregar_paso_proceso(
            "Fórmula de secante",
            "La pendiente se estima con dos puntos: xᵢ₊₁ = xᵢ − "
            "f(xᵢ)(xᵢ − xᵢ₋₁)/[f(xᵢ) − f(xᵢ₋₁)]. Se empieza con "
            f"x₀ = {fmt(resultado['x0'])} y x₁ = {fmt(resultado['x1'])}; no se requiere cambio de signo. "
            "Si f(xᵢ) − f(xᵢ₋₁) es cero o muy pequeño, el proceso se detiene antes de dividir.",
        )
        for indice, fila in enumerate(filas):
            error = (f"εₐ = {fmt(fila['error_porcentual'])}%" if fila["error_porcentual"] is not None
                     else f"εₐ = {fmt(fila['error_absoluto'])} (absoluto porque xᵢ₊₁ = 0)")
            if indice < len(resultado["tabla"]) - 1:
                decision = "Se continúa con los dos iterados más recientes."
            elif resultado["convergio"]:
                decision = "Se cumplen el error y el residuo; el proceso se detiene."
            else:
                decision = resultado["estado"]
            self._agregar_paso_proceso(
                f"Iteración {fila['i']}",
                f"f(xᵢ₋₁) = {fmt(fila['f_anterior'])}; f(xᵢ) = {fmt(fila['f_actual'])}; "
                f"denominador = {fmt(fila['denominador'])}.\n"
                f"xᵢ₊₁ = {fmt(fila['x_actual'])} − ({fmt(fila['f_actual'])} · "
                f"({fmt(fila['x_actual'])} − {fmt(fila['x_anterior'])}))/"
                f"({fmt(fila['denominador'])}) = {fmt(fila['x_siguiente'])}.\n"
                f"{error}; residuo |f(xᵢ₊₁)| = {fmt(fila['residuo'])}. {decision}",
            )
        self._agregar_paso_proceso("Parada", resultado["estado"])
        self._agregar_paso_proceso("Convergencia", "La secante es superlineal, de orden aproximado 1.618 bajo sus hipótesis; no tiene garantía global.")
        self._agregar_resumen((
            ("Raíz aproximada" if resultado["convergio"] else "Última aproximación", fmt(resultado["raiz_aproximada"])),
            ("Iteraciones", str(resultado["iteraciones"])),
            ("Error alcanzado", "—" if resultado["error_final"] is None else
             (f"{fmt(resultado['error_final'])} (absoluto)" if filas and filas[-1]["error_porcentual"] is None
              else f"{fmt(resultado['error_final'])}%")),
            ("Residuo |f(x)|", fmt(resultado["residuo"])),
            ("Estado", resultado["estado"]),
        ))
        self._titulo_seccion("Tabla de iteraciones")
        self._agregar_tabla(("i", "xᵢ₋₁", "xᵢ", "f(xᵢ₋₁)", "f(xᵢ)", "xᵢ₊₁", "Error criterio", "Residuo"), filas,
                            ("i", "x_anterior", "x_actual", "f_anterior", "f_actual", "x_siguiente", "error_criterio", "residuo"))
        segmentos = [(fila["x_anterior"], fila["f_anterior"], fila["x_actual"], fila["f_actual"])
                     for fila in filas]
        self._agregar_grafica(resultado["funcion"], resultado["aproximaciones"], segmentos,
                              "Aproximaciones por secante")

    def _mostrar_resultado_derivadas(self, resultado):
        self._preparar_resultado()
        fmt = self._numero_proceso
        self._agregar_paso_proceso(
            "Datos y derivada de referencia",
            f"f(x) = {resultado['expresion']}; x = {fmt(resultado['x'])}; "
            f"h = {fmt(resultado['h'])}. La derivada simbólica de referencia es "
            f"f′(x) = {resultado['derivada']}, con f′({fmt(resultado['x'])}) = "
            f"{fmt(resultado['derivada_exacta'])}. Evaluaciones: f(x−h) = "
            f"{fmt(resultado['fx_menos'])}; f(x) = {fmt(resultado['fx'])}; "
            f"f(x+h) = {fmt(resultado['fx_mas'])}.",
        )
        for titulo, texto in (
            ("Adelante", "f′(x) ≈ [f(x+h) − f(x)]/h; usa x y x+h y tiene error de truncamiento O(h)."),
            ("Atrás", "f′(x) ≈ [f(x) − f(x−h)]/h; usa x−h y x y tiene error de truncamiento O(h)."),
            ("Central", "f′(x) ≈ [f(x+h) − f(x−h)]/(2h); usa ambos lados y tiene error de truncamiento O(h²)."),
        ):
            self._agregar_paso_proceso(titulo, texto)
        self._agregar_paso_proceso(
            "Elección del paso h",
            "Disminuir h reduce el error de truncamiento, pero si h es demasiado pequeño "
            "aumentan el redondeo y la cancelación. Cambia h y recalcula para observar el efecto.",
        )
        self._agregar_resumen((
            ("Punto x", fmt(resultado["x"])),
            ("Paso h", fmt(resultado["h"])),
            ("Derivada exacta", fmt(resultado["derivada_exacta"])),
            ("Función", resultado["expresion"]),
        ))
        self._titulo_seccion("Comparación de aproximaciones")
        filas = resultado["tabla"].to_dict(orient="records")
        self._agregar_tabla(("Esquema", "Fórmula", "Aproximación", "Derivada exacta", "Error absoluto", "Orden"),
                            filas, ("esquema", "formula", "aproximacion", "derivada_exacta", "error_absoluto", "orden"))

    def _mostrar_resultado_horner(self, resultado):
        self._preparar_resultado()
        fmt = self._numero_proceso
        coeficientes = ", ".join(fmt(c) for c in resultado["coeficientes"])
        self._agregar_paso_proceso(
            "Polinomio y Horner simultáneo",
            f"Coeficientes en orden descendente: [{coeficientes}]. "
            "Con b₀ = a₀ y c₀ = 0, se repite cᵢ = x·cᵢ₋₁ + bᵢ₋₁ y "
            "bᵢ = x·bᵢ₋₁ + aᵢ. Al final bₙ = p(x) y cₙ = p′(x).",
        )
        for fila in resultado["tabla"].to_dict(orient="records"):
            self._agregar_paso_proceso(
                f"Iteración {fila['i']}",
                f"p(xᵢ) = {fmt(fila['pxi'])}; p′(xᵢ) = {fmt(fila['dpxi'])}. "
                f"xᵢ₊₁ = {fmt(fila['xi'])} − ({fmt(fila['pxi'])})/"
                f"({fmt(fila['dpxi'])}) = {fmt(fila['x_siguiente'])}. "
                f"Error = {fmt(fila['error_criterio'])}"
                f"{'%' if fila['error_porcentual'] is not None else ' (absoluto)'}; "
                f"residuo = {fmt(fila['residuo'])}.",
            )
        if resultado["cociente_deflacion"] is not None:
            quotient = ", ".join(fmt(c) for c in resultado["cociente_deflacion"])
            self._agregar_paso_proceso(
                "Deflación de la raíz aproximada",
                f"Se divide el polinomio entre (x − r), con r ≈ {fmt(resultado['raiz_aproximada'])}. "
                f"Coeficientes del cociente: [{quotient}]. El residuo de deflación es "
                f"{fmt(resultado['resto_deflacion'])}; cada raíz posterior debe refinarse y "
                "verificarse en el polinomio original.",
            )
        else:
            self._agregar_paso_proceso("Parada", resultado["estado"] + " No se aplica la deflación porque no se confirmó convergencia.")
        self._agregar_resumen((
            ("Raíz aproximada" if resultado["convergio"] else "Última aproximación", fmt(resultado["raiz_aproximada"])),
            ("Iteraciones", str(resultado["iteraciones"])),
            ("Residuo |p(x)|", fmt(resultado["residuo"])),
            ("Estado", resultado["estado"]),
        ))
        self._titulo_seccion("Iteraciones de Newton")
        filas = resultado["tabla"].to_dict(orient="records")
        self._agregar_tabla(("i", "xᵢ", "p(xᵢ)", "p′(xᵢ)", "xᵢ₊₁", "Error", "Residuo"),
                            filas, ("i", "xi", "pxi", "dpxi", "x_siguiente", "error_criterio", "residuo"))
        self._titulo_seccion("Evaluación simultánea de Horner")
        horner_rows = resultado["horner"].to_dict(orient="records")
        self._agregar_tabla(("Paso", "Coeficiente aᵢ", "bᵢ para p(x)", "cᵢ para p′(x)"),
                            horner_rows, ("paso", "coeficiente", "b_i", "c_i"))
        if resultado["cociente_deflacion"] is not None:
            etiqueta = QLabel("Cociente de deflación: [" + ", ".join(fmt(c) for c in resultado["cociente_deflacion"]) + "]")
            etiqueta.setWordWrap(True)
            etiqueta.setStyleSheet("color: #334155; background: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 10px; padding: 12px;")
            self.card_solucion.add_widget(etiqueta)
            self._titulo_seccion("Pasos de deflación por Horner")
            deflacion_rows = resultado["deflacion"].to_dict(orient="records")
            self._agregar_tabla(("Paso", "Coeficiente", "r · acumulado", "Nuevo acumulado"),
                                deflacion_rows, ("paso", "coeficiente", "producto", "resultado"))

    def _mostrar_resultado_convergencia(self, resultado):
        self._preparar_resultado()
        fmt = self._numero_proceso
        puntos = resultado["aproximaciones"]
        diferencias = resultado["diferencias"]
        self._agregar_paso_proceso(
            "Diferencias entre iterados",
            "Se calculan Δ₀ = |x₁ − x₀|, Δ₁ = |x₂ − x₁| y Δ₂ = |x₃ − x₂|. "
            f"En este caso: Δ₀ = {fmt(diferencias[0])}, Δ₁ = {fmt(diferencias[1])}, "
            f"Δ₂ = {fmt(diferencias[2])}.",
        )
        self._agregar_paso_proceso(
            "Orden observado",
            "Se estiman q₀ = Δ₁/Δ₀, q₁ = Δ₂/Δ₁ y p = ln(q₁)/ln(q₀). "
            f"Aquí q₀ = {fmt(resultado['razon_1'])}, q₁ = {fmt(resultado['razon_2'])}; "
            f"por tanto p ≈ {fmt(resultado['orden'])}.",
        )
        self._agregar_paso_proceso(
            "Constante y alcance",
            f"La constante observada se estima como C ≈ Δ₂/Δ₁ᵖ = {fmt(resultado['constante'])}. "
            "Es una estimación local basada en solo cuatro iterados; los resultados pueden variar "
            "si todavía se está lejos de la raíz.",
        )
        self._agregar_paso_proceso(
            "Referencia teórica",
            "Newton-Raphson suele tener p = 2 cerca de una raíz simple; la secante suele tener "
            "p ≈ 1.618. Compara el orden calculado con el método que produjo los iterados.",
        )
        self._agregar_resumen((
            ("Orden estimado p", fmt(resultado["orden"])),
            ("Constante estimada C", fmt(resultado["constante"])),
            ("Diferencias decrecen", "Sí" if resultado["contrayendo"] else "No"),
            ("Diagnóstico", resultado["diagnostico"]),
        ))
        self._titulo_seccion("Iterados usados en el análisis")
        filas = []
        for indice, punto in enumerate(puntos):
            filas.append({
                "i": indice,
                "xi": punto,
                "delta": diferencias[indice] if indice < len(diferencias) else None,
                "razon": resultado["razon_1"] if indice == 2 else (
                    resultado["razon_2"] if indice == 3 else None
                ),
            })
        self._agregar_tabla(("i", "xᵢ", "Δ consecutiva", "Razón de errores"),
                            filas, ("i", "xi", "delta", "razon"))

    def _mostrar_resultado(self, resultado):
        from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
        from matplotlib.figure import Figure

        self._preparar_resultado()
        self._mostrar_procedimiento(resultado)

        banner = QFrame()
        banner.setObjectName("estadoNewton")
        if resultado["convergio"]:
            color, fondo, borde, icono = "#059669", "#ECFDF5", "#A7F3D0", "✓"
            titulo_estado = "Convergencia alcanzada"
        else:
            color, fondo, borde, icono = "#B45309", "#FFFBEB", "#FDE68A", "!"
            titulo_estado = "Convergencia no confirmada"
        detalle_estado = ("El error aproximado y el residuo cumplen las tolerancias."
                          if resultado["convergio"] else resultado["estado"])
        banner.setStyleSheet(f"QFrame#estadoNewton {{ background: {fondo}; border: 1px solid {borde}; border-radius: 12px; }}")
        banner_layout = QHBoxLayout(banner)
        banner_layout.setContentsMargins(16, 10, 16, 10)
        banner_layout.setSpacing(12)
        icono_estado = QLabel(icono)
        icono_estado.setStyleSheet(f"color: {color}; font-size: 18px; font-weight: 800; border: none; background: transparent;")
        texto_estado = QLabel(f"<b>{titulo_estado}</b><br>{detalle_estado}")
        texto_estado.setWordWrap(True)
        texto_estado.setStyleSheet(f"color: {color}; font-size: 12px; border: none; background: transparent;")
        banner_layout.addWidget(icono_estado, 0, Qt.AlignmentFlag.AlignTop)
        banner_layout.addWidget(texto_estado, 1)
        self.card_solucion.add_widget(banner)

        formula_card = QFrame()
        formula_card.setStyleSheet("QFrame { background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; }")
        formula_layout = QVBoxLayout(formula_card)
        formula_layout.setContentsMargins(20, 16, 20, 16)
        formula_layout.setSpacing(12)
        heading = QHBoxLayout()
        heading.setSpacing(8)
        accent = QFrame()
        accent.setFixedSize(4, 16)
        accent.setStyleSheet("background: #2563EB; border-radius: 2px;")
        heading_title = QLabel("Función y derivada")
        heading_title.setStyleSheet("font-size: 14px; font-weight: 700; color: #0F172A; border: none; background: transparent;")
        heading.addWidget(accent)
        heading.addWidget(heading_title)
        heading.addStretch()
        formula_layout.addLayout(heading)
        for etiqueta, expresion in (("f(x)", resultado["funcion_simbolica"]),
                                    ("f′(x)", resultado["derivada_simbolica"])):
            fila = QHBoxLayout()
            nombre = QLabel(etiqueta)
            nombre.setFixedWidth(52)
            nombre.setStyleSheet("color: #64748B; font-size: 12px; font-weight: 700; border: none; background: transparent;")
            valor = QLabel(self._expresion_html(expresion))
            valor.setWordWrap(True)
            valor.setTextFormat(Qt.TextFormat.RichText)
            valor.setStyleSheet("color: #0F172A; font-size: 15px; font-weight: 600; border: none; background: transparent;")
            fila.addWidget(nombre)
            fila.addWidget(valor, 1)
            formula_layout.addLayout(fila)
        self.card_solucion.add_widget(formula_card)

        resumen = QFrame()
        resumen.setStyleSheet("QFrame { background: white; border: 1px solid #E2E8F0; border-radius: 12px; }")
        grid = QGridLayout(resumen)
        grid.setContentsMargins(20, 16, 20, 16)
        grid.setHorizontalSpacing(24)
        grid.setVerticalSpacing(14)
        etiqueta_raiz = "RAÍZ APROXIMADA" if resultado["convergio"] else "ÚLTIMA APROXIMACIÓN"
        if resultado["error_final"] is None:
            error_mostrado = "—"
        else:
            usa_error_absoluto = (resultado["tabla"].empty or
                                  resultado["tabla"].iloc[-1]["error_porcentual"] is None)
            unidad_error = " (absoluto)" if usa_error_absoluto else "%"
            error_mostrado = f"{resultado['error_final']:.6g}{unidad_error}"
        items = (
            (etiqueta_raiz, f"{resultado['raiz_aproximada']:.10g}"),
            ("ITERACIONES", str(resultado["iteraciones"])),
            ("ERROR ALCANZADO", error_mostrado),
            ("RESIDUO |f(x)|", "No finito" if resultado["residuo"] is None else f"{resultado['residuo']:.6g}"),
        )
        for idx, (caption, value) in enumerate(items):
            box = QVBoxLayout()
            label = QLabel(caption)
            label.setStyleSheet("color: #64748B; font-size: 10px; font-weight: 700; background: transparent; border: none;")
            text = QLabel(value)
            text.setWordWrap(True)
            text.setStyleSheet("color: #0F172A; font-size: 14px; font-weight: 700; background: transparent; border: none;")
            box.addWidget(label)
            box.addWidget(text)
            grid.addLayout(box, idx // 2, idx % 2)
        self.card_solucion.add_widget(resumen)

        rows = resultado["tabla"].to_dict(orient="records")
        self._titulo_seccion("Detalle de iteraciones")
        if rows:
            headers = ("i", "xᵢ", "f(xᵢ)", "f′(xᵢ)", "xᵢ₊₁", "Error aproximado", "|f(xᵢ₊₁)|")
            table = QTableWidget(len(rows), len(headers))
            table.setHorizontalHeaderLabels(headers)
            table.verticalHeader().setVisible(False)
            table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
            table.setAlternatingRowColors(True)
            table.setStyleSheet("QTableWidget { background: white; alternate-background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; color: #0F172A; gridline-color: #E2E8F0; } QHeaderView::section { background: #F1F5F9; color: #475569; font-weight: 700; border: none; border-bottom: 1px solid #E2E8F0; padding: 8px 5px; }")
            for fila, row in enumerate(rows):
                error = (f"{row['error_porcentual']:.6g}%" if row["error_porcentual"] is not None
                         else f"{row['error_absoluto']:.6g} (abs.)")
                valores = (row["i"], row["xi"], row["fxi"], row["dfxi"],
                           row["x_siguiente"], error, row["residuo"])
                for columna, value in enumerate(valores):
                    texto = f"{value:.8g}" if isinstance(value, (float, np.floating)) else str(value)
                    celda = QTableWidgetItem(texto)
                    celda.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    table.setItem(fila, columna, celda)
                table.setRowHeight(fila, 34)
            table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
            table.horizontalHeader().setStretchLastSection(True)
            table.setMinimumHeight(min(430, max(100, len(rows) * 34 + 42)))
            self.card_solucion.add_widget(table)
        else:
            sin_iteraciones = QLabel(
                "No se realizaron iteraciones: la aproximación inicial ya satisface "
                "el residuo o la derivada no permite calcular el siguiente paso."
            )
            sin_iteraciones.setWordWrap(True)
            sin_iteraciones.setStyleSheet("color: #475569; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 12px;")
            self.card_solucion.add_widget(sin_iteraciones)

        self._titulo_seccion("Gráfica del proceso")
        figure = Figure(figsize=(7, 4.2), tight_layout=True)
        axes = figure.add_subplot(111)
        puntos = resultado["aproximaciones"]
        span = max(puntos) - min(puntos) if len(puntos) > 1 else max(1.0, abs(puntos[0]) * 0.25)
        margen = max(span * 0.2, 0.5)
        xmin, xmax = min(puntos) - margen, max(puntos) + margen
        xs = np.linspace(xmin, xmax, 800)
        with np.errstate(all="ignore"):
            ys = np.asarray(resultado["funcion"](xs), dtype=float)
        if ys.ndim == 0:
            ys = np.full_like(xs, float(ys))
        ys[~np.isfinite(ys)] = np.nan
        axes.plot(xs, ys, color="#2563EB", linewidth=2, label="f(x)")
        axes.axhline(0, color="#64748B", linewidth=1)
        for indice, row in enumerate(rows):
            xi, xnext = row["xi"], row["x_siguiente"]
            tangent_x = np.linspace(min(xi, xnext), max(xi, xnext), 30)
            tangent_y = row["fxi"] + row["dfxi"] * (tangent_x - xi)
            axes.plot(tangent_x, tangent_y, "--", color="#F59E0B", alpha=0.65,
                      label="Tangentes" if indice == 0 else None)
            axes.scatter([xi], [row["fxi"]], color="#F59E0B", s=24, zorder=3)
            axes.plot([xnext, xnext], [0, row["fxi"] + row["dfxi"] * (xnext - xi)],
                      ":", color="#94A3B8", linewidth=1)
        raiz = resultado["raiz_aproximada"]
        marcador = "Raíz aproximada" if resultado["convergio"] else "Última aproximación"
        color_marcador = "#DC2626" if resultado["convergio"] else "#B45309"
        try:
            y_raiz = float(resultado["funcion"](raiz))
        except (ArithmeticError, TypeError, ValueError, OverflowError):
            y_raiz = float("nan")
        axes.scatter([raiz], [y_raiz], color=color_marcador, s=45, zorder=4, label=marcador)
        axes.set_title("Aproximaciones de Newton-Raphson")
        axes.set_xlabel("x")
        axes.set_ylabel("f(x)")
        axes.grid(True, alpha=0.25)
        axes.legend()
        canvas = FigureCanvasQTAgg(figure)
        canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        canvas.setMinimumHeight(330)
        self.card_solucion.add_widget(canvas)
        criterio = QLabel(f"Criterio de parada: error aproximado ≤ {resultado['tolerancia']:g}% y residuo ≤ {resultado['tolerancia_residuo']:g}. Máximo: {resultado['max_iteraciones']} iteraciones.")
        criterio.setWordWrap(True)
        criterio.setStyleSheet("color: #334155; background: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 10px; padding: 12px;")
        self.card_solucion.add_widget(criterio)
