import os
import sys

# Garantiza que los módulos de esta interfaz tengan prioridad de importación.

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

if CURRENT_DIR not in sys.path:

    sys.path.insert(0, CURRENT_DIR)

from PySide6.QtGui import QFont
from navbar import Navbar
from sidebar import Sidebar
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QStackedWidget, QHBoxLayout


from styles import APP_STYLE
# Importar los componentes globales
from navbar import Navbar
from sidebar import Sidebar

# Importar las vistas modulares
from vistas.vista_matriz import VistaMatriz
# from vistas.vista_otra import VistaOtra  # Tus futuras vistas


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora Matricial")
        self.resize(1100, 750)

        self._build_ui()

    def _build_ui(self):
        # Layout contenedor principal (vertical: Navbar arriba, contenido abajo)
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. Navbar Superior
        self.navbar = Navbar()
        main_layout.addWidget(self.navbar)

        # 2. Cuerpo (Sidebar + Áreas de contenido)
        body_container = QWidget()
        body_layout = QHBoxLayout(body_container)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)

        # Lateral: Sidebar
        self.sidebar = Sidebar()
        self.sidebar.hide()  # Inicia oculto o visible según prefieras
        self.navbar.menu_clicked.connect(self.sidebar.toggle)
        body_layout.addWidget(self.sidebar)

        # Contenedor dinámico de vistas (QStackedWidget)
        self.stack = QStackedWidget()

        # --- INSTANCIAR VISTAS ---
        self.vista_matriz = VistaMatriz()
        # self.vista_otra = VistaOtra()

        # Añadir vistas al Stack
        self.stack.addWidget(self.vista_matriz)  # Índice 0
        # self.stack.addWidget(self.vista_otra)  # Índice 1

        # =========================================================================
        # VISTA POR DEFECTO:
        # Al abrir main.py se mostrará VistaMatriz inmediatamente
        # =========================================================================
        self.stack.setCurrentWidget(self.vista_matriz)

        body_layout.addWidget(self.stack)
        main_layout.addWidget(body_container)

        self.setCentralWidget(main_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

"""def main():

    app = QApplication(sys.argv)

    app.setFont(QFont("Segoe UI", 10))

    app.setStyleSheet(

        APP_STYLE

    )
    window = MainWindow()

    window.show()

    sys.exit(
        app.exec()

    )

if __name__ == "__main__":

    main()"""