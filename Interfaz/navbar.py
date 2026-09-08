from PySide6.QtCore import Qt, Signal
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout


class Navbar(QFrame):
    menu_clicked = Signal()

    LOGO_SVG = """<svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M7 6H4V26H7" stroke="#1E3A8A" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M25 6H28V26H25" stroke="#1E3A8A" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
        <circle cx="11.5" cy="11.5" r="1.25" fill="#1E3A8A"/>
        <circle cx="16.0" cy="11.5" r="1.25" fill="#1E3A8A"/>
        <circle cx="20.5" cy="11.5" r="1.25" fill="#1E3A8A"/>
        <circle cx="11.5" cy="16.0" r="1.25" fill="#1E3A8A"/>
        <circle cx="16.0" cy="16.0" r="1.25" fill="#1E3A8A"/>
        <circle cx="20.5" cy="16.0" r="1.25" fill="#1E3A8A"/>
        <circle cx="11.5" cy="20.5" r="1.25" fill="#1E3A8A"/>
        <circle cx="16.0" cy="20.5" r="1.25" fill="#1E3A8A"/>
        <circle cx="20.5" cy="20.5" r="1.25" fill="#1E3A8A"/>
    </svg>"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(64)
        self.setStyleSheet(
            """
            Navbar {
                background-color: #FFFFFF;
                border-bottom: 1px solid #E2E8F0;
            }
            QPushButton#btnMenu {
                border: none;
                background: transparent;
                color: #64748B;
                font-size: 18px;
                font-weight: bold;
                border-radius: 6px;
            }
            QPushButton#btnMenu:hover {
                background-color: #F1F5F9;
                color: #0F172A;
            }
            QLabel#brandTitle {
                color: #0F172A;
                font-size: 18px;
                font-weight: 800;
                line-height: 1.0;
                font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            }
            QLabel#brandSub {
                color: #64748B;
                font-size: 9px;
                font-weight: 700;
                letter-spacing: 0.8px;
                font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            }
        """
        )

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 0, 16, 0)
        layout.setSpacing(12)

        # Botón Hamburguesa (☰)
        btn_menu = QPushButton("☰")
        btn_menu.setObjectName("btnMenu")
        btn_menu.setFixedSize(36, 36)
        btn_menu.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_menu.clicked.connect(self.menu_clicked.emit)

        # Icono SVG
        svg_icon = QSvgWidget()
        svg_icon.load(self.LOGO_SVG.encode("utf-8"))
        svg_icon.setFixedSize(32, 32)

        # Columna para 'LinearIS' y el subtítulo debajo en gris
        text_vbox = QVBoxLayout()
        text_vbox.setSpacing(1)
        text_vbox.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        lbl_title = QLabel("LinearIS")
        lbl_title.setObjectName("brandTitle")

        lbl_sub = QLabel("CALCULADORA DE ÁLGEBRA LINEAL")
        lbl_sub.setObjectName("brandSub")

        text_vbox.addWidget(lbl_title)
        text_vbox.addWidget(lbl_sub)

        layout.addWidget(btn_menu)
        layout.addWidget(svg_icon)
        layout.addLayout(text_vbox)
        layout.addStretch()