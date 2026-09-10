#En componentes.py estan los componentes que se utilizaran por todas las vistas en la calculadora 
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

class BracketWidget(QWidget):
    """Dibuja un corchete de matriz perfecto ([ o ]) que se escala automáticamente al alto exacto del contenido."""

    def __init__(self, is_left=True, parent=None):
        super().__init__(parent)
        self.is_left = is_left
        self.setFixedWidth(12)  # Ancho del corchete

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        pen = QPen(QColor("#1E293B"), 1.5)  # Color y grosor del corchete
        painter.setPen(pen)

        w = self.width()
        h = self.height()
        top_offset = 2
        bottom_offset = 2
        arm_len = 8  # Largo de las pestañas horizontal superior/inferior

        if self.is_left:
            # Línea vertical izquierda
            painter.drawLine(2, top_offset, 2, h - bottom_offset)
            # Pestaña superior
            painter.drawLine(2, top_offset, 2 + arm_len, top_offset)
            # Pestaña inferior
            painter.drawLine(
                2, h - bottom_offset, 2 + arm_len, h - bottom_offset
            )
        else:
            # Línea vertical derecha
            painter.drawLine(w - 2, top_offset, w - 2, h - bottom_offset)
            # Pestaña superior
            painter.drawLine(w - 2, top_offset, w - 2 - arm_len, top_offset)
            # Pestaña inferior
            painter.drawLine(
                w - 2,
                h - bottom_offset,
                w - 2 - arm_len,
                h - bottom_offset,
            )


class NumberStepper(QFrame):
    """Control personalizado con botones − y + exactamente estilo primera imagen."""

    def __init__(self, value=3, min_val=1, max_val=10, parent=None):
        super().__init__(parent)
        self.value = value
        self.min_val = min_val
        self.max_val = max_val
        self.on_change_callback = None

        self.setFixedWidth(105)
        self.setFixedHeight(34)

        self.setStyleSheet(
            """
            QFrame {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 8px;
            }
            QPushButton {
                border: none;
                background: transparent;
                color: #64748B;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                color: #1E293B;
                background-color: #F8FAFC;
            }
            QLabel {
                border: none;
                font-size: 13px;
                font-weight: 700;
                color: #0F172A;
                background: transparent;
            }
        """
        )

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Botón Menos
        self.btn_minus = QPushButton("−")
        self.btn_minus.setFixedSize(32, 32)
        self.btn_minus.setCursor(Qt.CursorShape.PointingHandCursor)

        # Divisor Izquierdo
        line_left = QFrame()
        line_left.setFrameShape(QFrame.Shape.VLine)
        line_left.setStyleSheet("background-color: #E2E8F0; max-width: 1px; border: none;")

        # Valor Central
        self.lbl_val = QLabel(str(self.value))
        self.lbl_val.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Divisor Derecho
        line_right = QFrame()
        line_right.setFrameShape(QFrame.Shape.VLine)
        line_right.setStyleSheet("background-color: #E2E8F0; max-width: 1px; border: none;")

        # Botón Más
        self.btn_plus = QPushButton("+")
        self.btn_plus.setFixedSize(32, 32)
        self.btn_plus.setCursor(Qt.CursorShape.PointingHandCursor)

        layout.addWidget(self.btn_minus)
        layout.addWidget(line_left)
        layout.addWidget(self.lbl_val, stretch=1)
        layout.addWidget(line_right)
        layout.addWidget(self.btn_plus)

        self.btn_minus.clicked.connect(self._decrement)
        self.btn_plus.clicked.connect(self._increment)

    def _decrement(self):
        if self.value > self.min_val:
            self.value -= 1
            self.lbl_val.setText(str(self.value))
            if self.on_change_callback:
                self.on_change_callback()

    def _increment(self):
        if self.value < self.max_val:
            self.value += 1
            self.lbl_val.setText(str(self.value))
            if self.on_change_callback:
                self.on_change_callback()

class CollapsibleCard(QFrame):
    """Tarjeta desplegable para Matriz Aumentada, Proceso y Solución."""

    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setStyleSheet(
            """
            QFrame {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 12px;
            }
        """
        )
        self.is_expanded = False

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 14, 20, 14)
        self.main_layout.setSpacing(10)

        # Encabezado (Título + Botón -/+)
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)

        lbl_title = QLabel(title)
        lbl_title.setStyleSheet(
            "font-size: 15px; font-weight: 700; color: #0F172A; border: none;"
        )
        header_layout.addWidget(lbl_title)
        header_layout.addStretch()

        self.btn_toggle = QPushButton("−" if self.is_expanded else "+")
        self.btn_toggle.setFixedSize(24, 24)
        self.btn_toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_toggle.setStyleSheet(
            "QPushButton { border: none; font-size: 16px; font-weight: bold;"
            " color: #64748B; background: transparent; } QPushButton:hover {"
            " color: #0F172A; }"
        )
        self.btn_toggle.clicked.connect(self.toggle)
        header_layout.addWidget(self.btn_toggle)

        self.main_layout.addLayout(header_layout)

        # Contenedor de contenido interno
        self.content_widget = QWidget()
        self.content_widget.setStyleSheet("border: none; background: transparent;")
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 8, 0, 0)
        self.content_layout.setSpacing(10)

        self.main_layout.addWidget(self.content_widget)
        self.content_widget.setVisible(self.is_expanded)

    def add_widget(self, widget):
        """Añade un widget al contenido de la tarjeta desplegable."""
        self.content_layout.addWidget(widget)

    def toggle(self):
        self.is_expanded = not self.is_expanded
        self.content_widget.setVisible(self.is_expanded)
        self.btn_toggle.setText("−" if self.is_expanded else "+")