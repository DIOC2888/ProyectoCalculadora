import os
import sys

# Garantiza que los módulos de esta interfaz tengan prioridad de importación.

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

if CURRENT_DIR not in sys.path:

    sys.path.insert(0, CURRENT_DIR)

from PySide6.QtGui import QFont

from PySide6.QtWidgets import QApplication

from main_window import MainWindow

from styles import APP_STYLE

def main():

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

    main()