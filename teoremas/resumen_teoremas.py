"""Resumen de teoremas clave para la calculadora de algebra lineal.

Agrupa propiedades por modulo y las entrega en formato reutilizable.
Las cadenas pueden incluir HTML basico porque QLabel las renderiza
como texto enriquecido dentro de la interfaz.
"""

# teoremas/resumen_teoremas.py
# Resumen corto de propiedades clave por modulo.
# Las cadenas pueden incluir HTML basico porque QLabel las renderiza como RichText.


TEOREMAS_CLAVE = {
    "Sistemas de ecuaciones": [
        "Un sistema A x = b es consistente si rango(A) = rango(A|b).",
        "Si rango(A) = rango(A|b) = n, la solucion es unica.",
        "Si rango(A) = rango(A|b) &lt; n, hay infinitas soluciones.",
        "Si rango(A) != rango(A|b), el sistema no tiene solucion."
    ],
    "Vectores e independencia lineal": [
        "Un conjunto de k vectores en R<sup>n</sup> es L.I. si A c = 0 solo tiene la solucion trivial.",
        "La relacion c<sub>1</sub>v<sub>1</sub> + c<sub>2</sub>v<sub>2</sub> + ... + c<sub>k</sub>v<sub>k</sub> = 0 solo acepta c<sub>1</sub> = c<sub>2</sub> = ... = c<sub>k</sub> = 0.",
        "Si A c = 0 tiene variables libres, existen soluciones no triviales y los vectores son dependientes.",
        "Un vector b es combinacion lineal de v<sub>1</sub>, ..., v<sub>k</sub> si el sistema A c = b es consistente.",
        "Si k &gt; n en R<sup>n</sup>, el conjunto es necesariamente dependiente."
    ],
    "Matrices e inversa": [
        "La transpuesta A<sup>T</sup> se obtiene intercambiando filas por columnas.",
        "Una matriz cuadrada A tiene inversa si y solo si det(A) != 0.",
        "Para 2x2, A<sup>-1</sup> = (1/det(A)) [[d, -b], [-c, a]].",
        "Para matrices mayores, A<sup>-1</sup> se obtiene reduciendo [A | I] hasta [I | A<sup>-1</sup>].",
        "Por adjunta: A<sup>-1</sup> = (1/det(A)) adj(A), si det(A) != 0.",
        "(A<sup>-1</sup>)<sup>-1</sup> = A.",
        "(AB)<sup>-1</sup> = B<sup>-1</sup>A<sup>-1</sup>, si A y B son invertibles.",
        "(A<sup>T</sup>)<sup>-1</sup> = (A<sup>-1</sup>)<sup>T</sup>.",
        "I<sub>m</sub>A = A = A I<sub>n</sub> cuando las dimensiones son compatibles."
    ],
    "Teorema de la matriz invertible": [
        "A es invertible si y solo si A tiene n posiciones pivote.",
        "A es invertible si y solo si sus columnas son linealmente independientes.",
        "A es invertible si y solo si sus columnas generan R<sup>n</sup>.",
        "A es invertible si y solo si det(A) != 0.",
        "Si det(A) = 0, A es singular y no tiene inversa."
    ],
    "Determinantes": [
        "El determinante solo se define para matrices cuadradas.",
        "Por cofactores: det(A) = suma de a<sub>ij</sub>C<sub>ij</sub> sobre una fila o columna.",
        "El cofactor se calcula como C<sub>ij</sub> = (-1)<sup>i+j</sup> det(M<sub>ij</sub>).",
        "det(AB) = det(A)det(B), cuando A y B son cuadradas del mismo orden.",
        "det(A<sup>-1</sup>) = 1/det(A), si A es invertible.",
        "Si A es triangular, det(A) es el producto de las entradas de la diagonal.",
        "Si det(A) = 0, la matriz es singular y no tiene inversa.",
        "Conviene desarrollar por la fila o columna con mas ceros para reducir calculos."
    ]
}


LOGOS_ASCII = {
    "Sistemas de ecuaciones": [
        "======================================================",
        "[  [1 2 | 3]  ]  MODULO: SISTEMAS DE ECUACIONES (SEL)",
        "[  [0 1 | 5]  ]  Metodos: Gauss, Gauss-Jordan",
        "======================================================"
    ],
    "Vectores e independencia lineal": [
        "======================================================",
        "MODULO: VECTORES E INDEPENDENCIA LINEAL",
        "Combinaciones Lineales, L.I. y L.D.",
        "A x = 0",
        "======================================================"
    ],
    "Matrices e inversa": [
        "======================================================",
        "[ A ][ B ]   MODULO: ALGEBRA DE MATRICES",
        "[ C ][ D ]   Operaciones, Traspuesta y Matriz Inversa",
        "======================================================"
    ],
    "Teorema de la matriz invertible": [
        "======================================================",
        "A invertible <=> pivotes, columnas L.I. y det(A) != 0",
        "A^-1 = (1/det(A)) adj(A)",
        "======================================================"
    ],
    "Determinantes": [
        "======================================================",
        "| A |        MODULO: DETERMINANTES Y PROPIEDADES",
        "cofactores   Desarrollo, singularidad e inversa",
        "======================================================"
    ]
}


def obtener_teoremas_clave():
    """Devuelve los teoremas y logos disponibles para la interfaz."""

    return {
        "teoremas": TEOREMAS_CLAVE,
        "logos": LOGOS_ASCII
    }
