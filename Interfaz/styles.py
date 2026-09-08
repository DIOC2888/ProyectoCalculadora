# ==========================================================
# ESTILOS DE LINEARIS
# ==========================================================

BACKGROUND = "#F2F6FB"
WHITE = "#FFFFFF"
PRIMARY = "#1B3D72"
ACCENT = "#2563EB"
TEXT = "#1A2332"
MUTED = "#64748B"
BORDER = "#DDE6EF"


APP_STYLE = f"""
QMainWindow {{
    background-color: {BACKGROUND};
}}

QWidget {{
    font-family: "Segoe UI";
    color: {TEXT};
}}

QFrame#navbar {{
    background-color: {WHITE};
    border-bottom: 1px solid {BORDER};
}}

QFrame#sidebar {{
    background-color: {WHITE};
    border-right: 1px solid {BORDER};
}}

QLabel#logo {{
    color: {PRIMARY};
    font-size: 16px;
    font-weight: 700;
}}

QLabel#logoSubtitle {{
    color: {MUTED};
    font-size: 7px;
    font-weight: 600;
    letter-spacing: 1px;
}}

QPushButton {{
    border: none;
    background: transparent;
}}

QPushButton#menuButton {{
    color: {MUTED};
    font-size: 20px;
    padding: 4px;
}}

QPushButton#menuButton:hover {{
    color: {PRIMARY};
}}

QLabel#pageTitle {{
    color: {TEXT};
    font-size: 21px;
    font-weight: 700;
}}

QLabel#pageSubtitle {{
    color: {MUTED};
    font-size: 12px;
}}

QFrame#inputCard {{
    background-color: {WHITE};
    border: 1px solid {BORDER};
    border-radius: 12px;
}}

QLabel#sectionLabel {{
    color: {PRIMARY};
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 1px;
}}

QPlainTextEdit#equationInput {{
    background-color: {BACKGROUND};
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 10px;
    color: {TEXT};
    font-family: "Consolas";
    font-size: 13px;
}}

QPlainTextEdit#equationInput:focus {{
    border: 1px solid {ACCENT};
}}

QLabel#helpText {{
    color: {MUTED};
    font-size: 10px;
}}

QPushButton#primaryButton {{
    background-color: {ACCENT};
    color: white;
    border-radius: 9px;
    padding: 9px 18px;
    font-size: 12px;
    font-weight: 600;
}}

QPushButton#primaryButton:hover {{
    background-color: #1D4ED8;
}}

QPushButton#primaryButton:pressed {{
    background-color: #1E40AF;
}}

QPushButton#modeButton {{
    color: {MUTED};
    background-color: transparent;
    border-radius: 7px;
    padding: 8px 14px;
    font-size: 11px;
}}

QPushButton#modeButton:hover {{
    color: {ACCENT};
}}

QPushButton#modeButtonActive {{
    color: {ACCENT};
    background-color: {WHITE};
    border: 1px solid {BORDER};
    border-radius: 7px;
    padding: 8px 14px;
    font-size: 11px;
    font-weight: 600;
}}

QFrame#modeContainer {{
    background-color: {BACKGROUND};
    border: 1px solid {BORDER};
    border-radius: 9px;
}}

QLabel#navSection {{
    color: {MUTED};
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 1px;
}}

QPushButton#navItem {{
    text-align: left;
    color: {MUTED};
    padding: 9px 12px;
    border-radius: 7px;
    font-size: 11px;
}}

QPushButton#navItem:hover {{
    background-color: {BACKGROUND};
    color: {TEXT};
}}

QPushButton#navItemActive {{
    text-align: left;
    color: {ACCENT};
    background-color: #EFF6FF;
    padding: 9px 12px;
    border-radius: 7px;
    font-size: 11px;
    font-weight: 600;
}}

QLabel#comingSoon {{
    color: #94A3B8;
    font-size: 8px;
}}
"""