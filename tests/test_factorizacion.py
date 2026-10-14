"""Regresiones numéricas y estructurales de la factorización LU."""

import copy
import unittest

from factorizacion import MENSAJE_PIVOTEO, factorizar_lu, factorizar_y_resolver


MATRIZ_EJEMPLO = [
    [3, -7, -2, 2], [-3, 5, 1, 0], [6, -4, 0, -5], [-9, 5, -5, 12],
]
VECTOR_EJEMPLO = [-9, 5, 7, 11]


class FactorizacionTests(unittest.TestCase):
    def assertVectorAlmostEqual(self, actual, expected):
        self.assertEqual(len(actual), len(expected))
        for value, target in zip(actual, expected):
            self.assertAlmostEqual(value, target, places=7)

    def test_ejemplo_presentacion_y_entradas_intactas(self):
        A, b = copy.deepcopy(MATRIZ_EJEMPLO), VECTOR_EJEMPLO[:]
        result = factorizar_y_resolver(A, b)
        self.assertEqual(result["L"], [
            [1, 0, 0, 0], [-1, 1, 0, 0], [2, -5, 1, 0], [-3, 8, 3, 1],
        ])
        self.assertEqual(result["U"], [
            [3, -7, -2, 2], [0, -2, -1, 2], [0, 0, -1, 1], [0, 0, 0, -1],
        ])
        self.assertVectorAlmostEqual(result["y"], [-9, -4, 5, 1])
        self.assertVectorAlmostEqual(result["x"], [3, 4, -6, -1])
        self.assertTrue(result["factorizacion_correcta"])
        self.assertTrue(result["verificacion_sistema"])
        self.assertEqual(A, MATRIZ_EJEMPLO)
        self.assertEqual(b, VECTOR_EJEMPLO)

    def test_comparacion_separada_y_sin_operaciones_nulas(self):
        result = factorizar_y_resolver(MATRIZ_EJEMPLO, VECTOR_EJEMPLO)
        self.assertFalse(any(p["tipo"].startswith("comparacion") for p in result["proceso"]))
        self.assertTrue(result["comparacion_gauss"]["solucion_coincide"])
        self.assertEqual(sum(p["tipo"] == "eliminacion" for p in result["proceso"]), 6)
        _, _, steps = factorizar_lu([[1, 0], [0, 1]])
        self.assertFalse(any(p["tipo"] == "eliminacion" for p in steps))

    def test_multiplicador_pequeno_con_efecto_significativo(self):
        result = factorizar_y_resolver([[100000000, 0], [1, 1]], [100000000, 0])
        self.assertVectorAlmostEqual(result["y"], [100000000, -1])
        self.assertVectorAlmostEqual(result["x"], [1, -1])
        self.assertTrue(result["verificacion_sistema"])

    def test_coeficiente_pequeno_en_sustitucion_atras(self):
        result = factorizar_y_resolver([[1, 1e-8], [0, 1]], [0, 100000000])
        self.assertVectorAlmostEqual(result["x"], [-1, 100000000])
        self.assertTrue(result["verificacion_sistema"])

    def test_normaliza_pivote_cercano_a_uno(self):
        result = factorizar_y_resolver([[1.00000005]], [100000000])
        self.assertVectorAlmostEqual(result["x"], [100000000 / 1.00000005])
        self.assertTrue(result["verificacion_sistema"])

    def test_singulares_conservan_lu_y_distinguen_consistencia(self):
        for b, expected in (([3, 6], "indeterminado"), ([3, 7], "inconsistente")):
            with self.subTest(b=b):
                result = factorizar_y_resolver([[1, 2], [2, 4]], b)
                self.assertEqual(result["L"], [[1, 0], [2, 1]])
                self.assertEqual(result["U"], [[1, 2], [0, 0]])
                self.assertTrue(result["factorizacion_correcta"])
                self.assertEqual(result["tipo_sistema"], expected)
                self.assertIsNone(result["x"])
                self.assertNotIn("permutación", result["mensaje_sistema"])

    def test_columna_inicial_nula_y_matriz_rectangular(self):
        A = [[0, 1, 2], [0, 3, 4]]
        result = factorizar_y_resolver(A, [1, 1])
        self.assertEqual(result["L"], [[1, 0], [3, 1]])
        self.assertEqual(result["U"], [[0, 1, 2], [0, 0, -2]])
        self.assertEqual(result["LU"], A)
        self.assertIsNone(result["x"])

    def test_columna_intermedia_nula(self):
        A = [[1, 0, 2], [2, 0, 5], [3, 0, 7]]
        result = factorizar_y_resolver(A, [3, 7, 10])
        self.assertEqual(result["U"], [[1, 0, 2], [0, 0, 1], [0, 0, 0]])
        self.assertEqual(result["LU"], A)
        self.assertEqual(result["tipo_sistema"], "indeterminado")

    def test_matriz_alta_y_matriz_cero(self):
        for A in ([[0, 1], [0, 3], [0, 5]], [[0, 0], [0, 0]]):
            with self.subTest(A=A):
                result = factorizar_y_resolver(A, [0] * len(A))
                self.assertEqual(result["LU"], A)
                self.assertTrue(result["factorizacion_correcta"])
                self.assertIsNone(result["x"])

    def test_intercambio_necesario_sigue_prohibido(self):
        with self.assertRaises(ValueError) as context:
            factorizar_lu([[0, 1], [1, 0]])
        self.assertEqual(str(context.exception), MENSAJE_PIVOTEO)

    def test_rechaza_entradas_malformadas_y_no_finitas(self):
        for A in ([], [[]], [1], [[1], [1, 2]], [[float("nan")]], [[float("inf")]]):
            with self.subTest(A=A), self.assertRaises(ValueError):
                factorizar_lu(A)
        for b in (None, [], ["texto"], [float("nan")], [float("inf")]):
            with self.subTest(b=b), self.assertRaises(ValueError):
                factorizar_y_resolver([[1]], b)


if __name__ == "__main__":
    unittest.main()
