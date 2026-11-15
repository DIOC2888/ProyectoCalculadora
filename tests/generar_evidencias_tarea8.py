"""Genera tablas, gráficas y capturas de los tres casos obligatorios.

Ejecutar desde la raíz: python tests/generar_evidencias_tarea8.py
Las capturas usan la misma vista Qt de la calculadora, en modo offscreen.
"""

import csv
import os
import sys
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "Interfaz"))

import numpy as np
from matplotlib import get_data_path
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtWidgets import QApplication, QTableWidget

from metodos_numericos import resolver_metodo_iterativo
from vistas.vista_metodos_numericos import VistaMetodosNumericos


CASOS = (
    dict(id="caso1", titulo="Convergencia: ejemplo 1 de la sesión 21",
         A=[[10, 3, 1], [5, -10, 3], [1, 3, 10]], b=[14, -5, 14],
         reordenar=True, maximo=100),
    dict(id="caso2", titulo="Diagonal cero y reordenamiento válido",
         A=[[0, 5, 1], [4, 1, 1], [1, 1, 6]], b=[13, 9, 21],
         reordenar=True, maximo=100),
    dict(id="caso3", titulo="Falta de convergencia en el orden original",
         A=[[1, 2], [2, 1]], b=[3, 3], reordenar=False, maximo=15),
)
TOLERANCIA = 0.0001
METODOS = ("Jacobi", "Gauss-Seidel")


def tabla_csv(r, destino):
    with destino.open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.writer(stream)
        writer.writerow(["k", *(f"x{i+1}" for i in range(len(r["b"]))),
                         "error_infinito", "error_euclideo", "error_porcentual",
                         "diferencia_referencia_euclidea", "residuo_infinito"])
        for fila in r["tabla"]:
            writer.writerow([fila["k"], *fila["x"], fila["error_infinito"],
                             fila["error_euclideo"], fila["error_porcentual"],
                             fila["error_referencia_euclideo"], fila["residuo"]])


def grafica(resultados, caso, destino):
    figure = Figure(figsize=(9, 4.8), layout="constrained")
    FigureCanvasAgg(figure)
    ax = figure.add_subplot(111)
    for r in resultados:
        filas = [f for f in r["tabla"][1:] if np.isfinite(f["error"]) and f["error"] > 0]
        ax.semilogy([f["k"] for f in filas], [f["error"] for f in filas],
                    marker="o", markersize=4, label=r["metodo"])
    ax.axhline(TOLERANCIA, color="gray", linestyle="--", label="Tolerancia = 0.0001")
    ax.set(title=caso["titulo"], xlabel="Iteración k",
           ylabel="Error entre iteraciones (norma infinito)")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend()
    figure.savefig(destino, dpi=160)


def capturas(app, caso, resultados, carpeta):
    vista = VistaMetodosNumericos()
    vista.resize(1000, 950)
    vista.selector.setCurrentIndex(4)
    vista.iter_n.value = len(caso["b"])
    vista.iter_n.lbl_val.setText(str(len(caso["b"])))
    vista._rebuild_iterative_matrix()
    vista.iter_method.setCurrentText("Comparar ambos")
    vista.iter_tol.setText(str(TOLERANCIA))
    vista.iter_max.setText(str(caso["maximo"]))
    vista.iter_reorder.setChecked(caso["reordenar"])
    for campos, valores in zip(vista.iter_matrix_fields, caso["A"]):
        for campo, valor in zip(campos, valores):
            campo.setText(str(valor))
    for campo, valor in zip(vista.iter_b_fields, caso["b"]):
        campo.setText(str(valor))
    vista.show()
    for _ in range(3):
        app.processEvents()
    vista.card.grab().save(str(carpeta / f"{caso['id']}_entrada.png"))
    # Ejecutar el mismo camino de captura/controlador usado por el botón.
    vista._calcular_iterativos()
    for _ in range(3):
        app.processEvents()
    vista.card_solucion.grab().save(str(carpeta / f"{caso['id']}_resultados.png"))
    tablas = vista.card_proceso.findChildren(QTableWidget)
    for tabla, r in zip(tablas, resultados):
        ancho = tabla.horizontalHeader().length() + 4
        alto = tabla.horizontalHeader().height() + sum(tabla.rowHeight(i) for i in range(tabla.rowCount())) + 4
        tabla.setFixedSize(ancho, alto)
        app.processEvents()
        tabla.grab().save(str(carpeta / f"{caso['id']}_{r['metodo']}_tabla.png"))
    vista.close()
    vista.deleteLater()
    app.processEvents()


def escribir_guia(todos, carpeta):
    texto = """# Verificación de Jacobi y Gauss-Seidel: Tarea 8

## Qué explica la diferencia con la presentación

Los algoritmos de actualización son correctos: Jacobi utiliza exclusivamente el
vector anterior y Gauss-Seidel usa inmediatamente cada componente nueva.
La diferencia principal está en la medida de error elegida.

| Fuente o ejemplo | Error para decidir la parada | Opción en la calculadora |
| --- | --- | --- |
| Tarea 8, apartado 3.2 | maxᵢ |xᵢ⁽ᵏ⁾ − xᵢ⁽ᵏ⁻¹⁾| | Norma infinito (Tarea 8) |
| Sesión 21, ejemplos 1 y 2 | √Σᵢ(xᵢ⁽ᵏ⁾ − xᵢ⁽ᵏ⁻¹⁾)² | Norma euclídea (presentación) |
| Sesión 21, ejemplo de Chapra, diapositivas 23 y 24 | maxᵢ 100·|Δxᵢ|/|xᵢ⁽ᵏ⁾| | Relativo porcentual máximo (Chapra) |

En las expresiones de la tabla, las barras verticales significan valor absoluto.
Para estos tres casos obligatorios se usa **el mismo criterio: norma infinito**,
con **ε = 0.0001** y **x⁽⁰⁾ = 0** en todas las componentes.
El residuo siempre es ‖Ax − b‖∞. El cambio entre iteraciones, el error frente a
una solución de referencia y el residuo son cantidades distintas. Alcanzar ε en
la primera cantidad no garantiza que el residuo sea menor que ε.

En el ejemplo 1 de la presentación, la primera aproximación de Jacobi es
(1.4, 0.5, 1.4): norma infinito = 1.4, norma euclídea = √4.17 = 2.042057786.
En Gauss-Seidel es (1.4, 1.2, 0.9): norma infinito = 1.4, norma euclídea =
√4.21 = 2.051828453. Ambos criterios absolutos llegan a ε = 0.0001 en
16 iteraciones para Jacobi y 5 para Gauss-Seidel en este ejemplo concreto.
Con otras tolerancias pueden terminar en iteraciones diferentes.

La diapositiva 6 contiene una errata en Jacobi, k = 11: **x₂ = 1.2461093684**,
en lugar de 1.246709. Otros valores de las tablas están truncados a diferentes
cantidades de decimales. El programa conserva toda la precisión durante el
cálculo y redondea únicamente al mostrar resultados. En k = 0 se muestra «—»
porque no existe una iteración previa con la que calcular un cambio.

El ejemplo 2 (cinco variables) también coincide. Tras tres pasos de Gauss-Seidel:

    x⁽³⁾ = (−1.980224, −1.0181376, −0.02184192, 0.992073216, 2.003214336)
    ‖Δx‖∞ = 0.124224
    ‖Δx‖₂ = 0.1699055855

En el ejemplo de Chapra, al elegir el criterio porcentual con ε = **0.05**
(es decir, **0.05 %**), ambos métodos paran en la iteración 4. No se debe
introducir una tolerancia porcentual como si fuera una tolerancia absoluta.
Cuando una componente se acerca a cero, una norma absoluta suele ser más útil.

## Cómo repetir las pruebas en la calculadora

Abrir el menú, entrar a **Métodos Numéricos**, elegir **Métodos iterativos:
Jacobi y Gauss-Seidel**, seleccionar **Comparar ambos**, y dejar el criterio
**Norma infinito (Tarea 8)**. Introducir los datos de cada caso y pulsar Calcular.
Los archivos PNG son capturas de los componentes reales de la interfaz Qt,
generadas en modo offscreen. Cada caso incluye entradas, resumen, las dos
tablas completas, sus CSV y una gráfica comparativa.

"""
    for caso, resultados in todos:
        num = caso["id"][-1]
        texto += f"## Caso {num}: {caso['titulo']}\n\n"
        texto += "```text\nA = " + "\n    ".join(str(fila) for fila in caso["A"])
        texto += f"\nb = {caso['b']}\nx⁽⁰⁾ = {[0]*len(caso['b'])}\n"
        texto += f"ε = {TOLERANCIA}\nMáximo de iteraciones = {caso['maximo']}\n"
        texto += f"Reordenamiento = {'activado' if caso['reordenar'] else 'DESACTIVADO'}\n```\n\n"
        if num == "1":
            texto += ("Comprueba la convergencia en una matriz estrictamente dominante: "
                      "10 > 3+1, 10 > 5+3 y 10 > 1+3. La solución de referencia es "
                      "(125/134, 167/134, 125/134). Se utiliza el mismo sistema del ejemplo 1 de la presentación.\n\n")
        elif num == "2":
            texto += ("Comprueba el tratamiento del cero a₁₁. El orden de ecuaciones encontrado es "
                      "**[2, 1, 3]**. La nueva diagonal es (4, 5, 6), estrictamente dominante. "
                      "El vector b pasa a (9, 13, 21); el orden de las variables y de x⁽⁰⁾ no cambia. "
                      "La solución de referencia es **(1, 2, 3)**.\n\n")
        else:
            texto += ("Comprueba una falta de convergencia real: en el orden indicado, el error "
                      "crece, con radio espectral 2 para Jacobi y 4 para Gauss-Seidel. "
                      "Aunque la solución exacta es (1, 1), las iteraciones se alejan. "
                      "El programa advierte del crecimiento y llega al máximo de 15 pasos. "
                      "**Desactivar el reordenamiento es esencial:** si se activa, intercambia "
                      "las dos filas, obtiene dominancia y ambos métodos convergen.\n\n"
                      "La ausencia de dominancia por sí sola no demuestra divergencia. "
                      "Por ejemplo, A = [[1, 2], [0.1, 1]], b = [3, 1.1] converge con ambos "
                      "métodos en su orden original, sin ser estrictamente dominante.\n\n")
        texto += "| Método | Iteraciones | Error ∞ final | Residuo ∞ | Diferencia ∞ con NumPy | Estado |\n"
        texto += "| --- | ---: | ---: | ---: | ---: | --- |\n"
        for r in resultados:
            estado = "Convergencia" if r["convergio"] else "Máximo / no convergencia"
            texto += (f"| {r['metodo']} | {r['iteraciones']} | {r['error']:.10g} | "
                      f"{r['residuo']:.10g} | {r['diferencia_referencia']:.10g} | {estado} |\n")
        texto += "\n"
        for r in resultados:
            texto += f"- {r['metodo']}: x = ({', '.join(f'{v:.10g}' for v in r['solucion'])}).\n"
        texto += f"\n![Datos introducidos]({caso['id']}_entrada.png)\n\n"
        texto += f"![Resumen de resultados]({caso['id']}_resultados.png)\n\n"
        for r in resultados:
            archivo = f"{caso['id']}_{r['metodo']}"
            texto += f"![Tabla {r['metodo']}]({archivo}_tabla.png)\n\n"
            texto += f"[Tabla completa de {r['metodo']} en CSV]({archivo}.csv)\n\n"
        texto += f"![Gráfica comparativa]({caso['id']}_grafica.png)\n\n"
    texto += """## Validaciones adicionales y correcciones

- Un cero en la diagonal con reordenamiento desactivado genera un mensaje de error.
- A = [[0, 1], [0, 2]] no admite diagonal no nula por permutación de filas y se rechaza.
- Se validan dimensiones, valores finitos, tolerancia positiva y máximo entero positivo.
- Se evita declarar un método más rápido cuando alguno no alcanza la tolerancia.
- Si no se encuentra un orden dominante y la diagonal original ya es válida, se
  conserva ese orden. Una permutación arbitraria puede destruir la convergencia.
- Cinco aumentos seguidos del error generan una advertencia. El proceso continúa
  hasta ε o el límite: el crecimiento transitorio no demuestra divergencia.
- Los valores no finitos detienen el proceso con un diagnóstico.
- NumPy se usa para validar las aproximaciones, después de ejecutar las
  iteraciones propias. No sustituye Jacobi ni Gauss-Seidel.

## Ejecución reproducible

Desde la raíz del proyecto en PowerShell:

```powershell
.\\venv\\Scripts\\python.exe -m unittest discover -s tests -v
.\\venv\\Scripts\\python.exe tests/generar_evidencias_tarea8.py
```

Las pruebas automáticas de `tests/test_iterativos.py` comprueban estos casos,
los tres ejemplos de la presentación, los criterios de parada y regresiones
de los ajustes realizados. El segundo comando regenera esta guía y las evidencias.

## Uso en el informe y la defensa

La Tarea 8 pide un informe PDF con portada oficial, objetivo, explicación de
algoritmos y validaciones, comparación y capturas legibles de los tres casos.
Esta guía aporta los datos y las evidencias numéricas para ese informe; no es
el PDF final de entrega. Añadir la portada y los datos reales del grupo.

En la defensa se puede explicar: «Jacobi calcula todas las componentes a partir
del vector anterior. Gauss-Seidel aprovecha las componentes nuevas de inmediato.
Usamos la norma infinito recomendada en la tarea y verificamos con el residuo y
NumPy. La presentación usa otra norma en algunos ejemplos. La dominancia estricta
garantiza convergencia, pero hay sistemas que convergen sin cumplirla».

Fuentes revisadas: `Tarea 8 (Elaboracion Programa 8_Python).pdf`, apartados 3 a 7;
`Sesion 21_Ejercicios acerca de Metodos iterativos_Jacobi y Gauss Seidel.pptx`,
diapositivas 3 a 9, 17 a 24. Los ejercicios de relajación de la diapositiva 25
no forman parte de los tres casos obligatorios del PDF de la Tarea 8.
"""
    # Las barras de valor absoluto deben escaparse dentro de tablas Markdown.
    texto = texto.replace("| maxᵢ |xᵢ⁽ᵏ⁾ − xᵢ⁽ᵏ⁻¹⁾| |", "| maxᵢ \\|xᵢ⁽ᵏ⁾ − xᵢ⁽ᵏ⁻¹⁾\\| |")
    texto = texto.replace("| maxᵢ 100·|Δxᵢ|/|xᵢ⁽ᵏ⁾| |", "| maxᵢ 100·\\|Δxᵢ\\|/\\|xᵢ⁽ᵏ⁾\\| |")
    (carpeta / "GUIA_PRUEBAS.md").write_text(texto, encoding="utf-8")


def main():
    carpeta = ROOT / "output" / "pruebas_tarea8"
    carpeta.mkdir(parents=True, exist_ok=True)
    app = QApplication.instance() or QApplication([])
    app.setStyle("Fusion")
    # El complemento offscreen de Qt en Windows no carga siempre las fuentes
    # del sistema. Registrar las fuentes disponibles evita capturas con cuadrados.
    fuentes = Path(get_data_path()) / "fonts" / "ttf"
    for nombre in ("DejaVuSans.ttf", "DejaVuSans-Bold.ttf"):
        QFontDatabase.addApplicationFont(str(fuentes / nombre))
    app.setFont(QFont("DejaVu Sans", 9))
    todos = []
    for caso in CASOS:
        resultados = [resolver_metodo_iterativo(caso["A"], caso["b"], [0]*len(caso["b"]),
                                              TOLERANCIA, caso["maximo"], metodo,
                                              caso["reordenar"]) for metodo in METODOS]
        for r in resultados:
            tabla_csv(r, carpeta / f"{caso['id']}_{r['metodo']}.csv")
            print(caso["id"], r["metodo"], r["iteraciones"], r["estado"])
        grafica(resultados, caso, carpeta / f"{caso['id']}_grafica.png")
        capturas(app, caso, resultados, carpeta)
        todos.append((caso, resultados))
    escribir_guia(todos, carpeta)
    print("Evidencias:", carpeta)


if __name__ == "__main__":
    main()
