from PySide6.QtCore import Qt
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import QFrame, QGridLayout, QHBoxLayout, QLabel, QPushButton, QVBoxLayout

from sleeping_dog import SleepingDogContainer


class Sidebar(QFrame):
    LOGO_SVG = """<svg width="24" height="24" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
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
        self.setFixedWidth(240)
        self.setStyleSheet(
            """
            Sidebar {
                background-color: #FFFFFF;
                border-right: 1px solid #E2E8F0;
            }
            QLabel#sidebarTitle {
                color: #1E293B;
                font-size: 16px;
                font-weight: 800;
            }
            QLabel#sidebarSub {
                color: #64748B;
                font-size: 8px;
                font-weight: 700;
                letter-spacing: 0.5px;
            }
            QLabel#sectionHeader {
                color: #94A3B8;
                font-size: 10px;
                font-weight: 700;
                letter-spacing: 0.8px;
            }
            QPushButton.nav-btn {
                text-align: left;
                padding: 10px 12px;
                border-radius: 8px;
                font-size: 13px;
                font-weight: 600;
                border: none;
                background: transparent;
                color: #64748B;
            }
            QPushButton.nav-btn:hover {
                background-color: #F8FAFC;
                color: #0F172A;
            }
            QPushButton.nav-btn[active="true"] {
                background-color: #EFF6FF;
                color: #2563EB;
            }
            QLabel.prox-tag {
                color: #94A3B8;
                font-size: 9px;
                font-weight: 600;
            }
        """
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 20, 16, 20)
        layout.setSpacing(16)

        # Header Logo + Texto
        header_layout = QHBoxLayout()
        header_layout.setSpacing(8)

        svg_icon = QSvgWidget()
        svg_icon.load(self.LOGO_SVG.encode("utf-8"))
        svg_icon.setFixedSize(24, 24)

        title_vbox = QVBoxLayout()
        title_vbox.setSpacing(0)

        lbl_title = QLabel("LinearIS")
        lbl_title.setObjectName("sidebarTitle")

        lbl_sub = QLabel("ÁLGEBRA LINEAL")
        lbl_sub.setObjectName("sidebarSub")

        title_vbox.addWidget(lbl_title)
        title_vbox.addWidget(lbl_sub)

        header_layout.addWidget(svg_icon)
        header_layout.addLayout(title_vbox)
        header_layout.addStretch()

        layout.addLayout(header_layout)

        # Herramientas
        lbl_section = QLabel("HERRAMIENTAS")
        lbl_section.setObjectName("sectionHeader")
        layout.addWidget(lbl_section)

        tools_grid = QGridLayout()
        tools_grid.setContentsMargins(0, 0, 0, 0)
        tools_grid.setVerticalSpacing(4)
        tools_grid.setHorizontalSpacing(8)

        items = [
            ("Sistemas de Equaciones", True),
            ("Matrices", False),
            ("Vectores", False),
            ("Espacios vectoriales", False),
            ("Producto interno", False),
            ("Autovalores", False),
            ("Transformaciones", False),
            ("Factorizaciones", False),
        ]

        for row_idx, (name, is_active) in enumerate(items):
            btn = QPushButton(name)
            btn.setProperty("active", is_active)
            btn.setProperty("class", "nav-btn")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)

            tools_grid.addWidget(btn, row_idx, 0)

            if not is_active:
                lbl_tag = QLabel("PRÓX.")
                lbl_tag.setProperty("class", "prox-tag")
                lbl_tag.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                tools_grid.addWidget(lbl_tag, row_idx, 1)

        layout.addLayout(tools_grid)
        layout.addStretch()

        # Perrito en el menú lateral
        self.sidebar_dog = SleepingDogContainer(small=True)
        layout.addWidget(self.sidebar_dog, alignment=Qt.AlignmentFlag.AlignCenter)

    def toggle(self):
        self.setVisible(not self.isVisible())