# determinantes.py
# Calculo de determinantes sin librerias externas.

from config import TOLERANCIA
from formato import formatear_numero, subindice, superindice
from validaciones import validar_matriz


def _copiar_matriz(matriz):
    """Crea una copia para no alterar la matriz recibida."""

    return [
        fila[:]
        for fila in matriz
    ]


def _formatear(valor):
    """Usa el formateo matematico comun cuando el valor es numerico."""

    if isinstance(valor, (int, float)):
        return formatear_numero(valor)

    return str(valor)


def _validar_matriz_cuadrada(A):
    """Garantiza que det(A) solo se calcule para matrices cuadradas."""

    validar_matriz(A)

    filas = len(A)
    columnas = len(A[0])

    if filas != columnas:
        raise ValueError(
            "El determinante solo se puede calcular en matrices cuadradas."
        )


def _menor(A, fila_eliminar, columna_eliminar):
    """Construye M_ij eliminando una fila y una columna."""

    return [
        [
            valor
            for j, valor in enumerate(fila)
            if j != columna_eliminar
        ]
        for i, fila in enumerate(A)
        if i != fila_eliminar
    ]


def _determinante_recursivo(A):
    """Calcula determinantes de menores sin guardar pasos de interfaz."""

    n = len(A)

    if n == 1:
        return A[0][0]

    if n == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]

    # Se elige la fila con mas ceros para reducir llamadas recursivas.
    fila_desarrollo = max(
        range(n),
        key=lambda i: sum(
            1
            for valor in A[i]
            if abs(valor) <= TOLERANCIA
        )
    )

    total = 0

    for columna, elemento in enumerate(A[fila_desarrollo]):
        if abs(elemento) <= TOLERANCIA:
            continue

        # termino = a_ij * C_ij, con C_ij = (-1)^(i+j) det(M_ij).
        signo = -1 if (fila_desarrollo + columna) % 2 else 1
        total += (
            signo
            * elemento
            * _determinante_recursivo(
                _menor(A, fila_desarrollo, columna)
            )
        )

    return 0 if abs(total) <= TOLERANCIA else total


def _determinante_sarrus(A):
    """Calcula el determinante 3x3 con la regla de Sarrus y sus pasos."""
    a, b, c = A[0]
    d, e, f = A[1]
    g, h, i = A[2]
    positivos = (a * e * i, b * f * g, c * d * h)
    negativos = (c * e * g, a * f * h, b * d * i)
    valor = sum(positivos) - sum(negativos)
    if abs(valor) <= TOLERANCIA:
        valor = 0
    descendentes = (
        f"({_formatear(a)}·{_formatear(e)}·{_formatear(i)} = {_formatear(positivos[0])}) + "
        f"({_formatear(b)}·{_formatear(f)}·{_formatear(g)} = {_formatear(positivos[1])}) + "
        f"({_formatear(c)}·{_formatear(d)}·{_formatear(h)} = {_formatear(positivos[2])})"
    )
    ascendentes = (
        f"({_formatear(c)}·{_formatear(e)}·{_formatear(g)} = {_formatear(negativos[0])}) + "
        f"({_formatear(a)}·{_formatear(f)}·{_formatear(h)} = {_formatear(negativos[1])}) + "
        f"({_formatear(b)}·{_formatear(d)}·{_formatear(i)} = {_formatear(negativos[2])})"
    )
    detalle = (
        f"Descendentes: {descendentes} = {_formatear(sum(positivos))}\n"
        f"Ascendentes: {ascendentes} = {_formatear(sum(negativos))}\n"
        f"det(A) = {_formatear(sum(positivos))} - "
        f"{_formatear(sum(negativos))} = {_formatear(valor)}"
    )
    return valor, detalle


def _determinante_triangular(A):
    """Reduce por operaciones de fila y conserva signo y pivotes."""
    matriz = _copiar_matriz(A)
    n = len(matriz)
    intercambios = 0
    factor_extraido = 1
    proceso = []
    pivotes = []

    for columna in range(n):
        if columna == 0:
            fila_pivote = columna
            if abs(matriz[fila_pivote][columna]) <= TOLERANCIA:
                fila_pivote = next(
                    (
                        fila for fila in range(columna + 1, n)
                        if abs(matriz[fila][columna]) > TOLERANCIA
                    ),
                    columna
                )
        else:
            fila_pivote = max(
                range(columna, n),
                key=lambda fila: abs(matriz[fila][columna])
            )
        if abs(matriz[fila_pivote][columna]) <= TOLERANCIA:
            pivotes.append(0)
            proceso.append({
                "tipo": "formula", "titulo": "PIVOTE NULO",
                "operacion": f"Columna {columna + 1}",
                "detalle": "No hay pivote distinto de cero; det(A) = 0."
            })
            return 0, proceso, intercambios, pivotes, matriz, factor_extraido

        if fila_pivote != columna:
            matriz[columna], matriz[fila_pivote] = matriz[fila_pivote], matriz[columna]
            intercambios += 1
            proceso.append({
                "tipo": "operacion_fila",
                "titulo": "Intercambio de filas",
                "operacion": f"F{columna + 1} ↔ F{fila_pivote + 1}; cambia el signo del determinante",
                "matriz": _copiar_matriz(matriz)
            })

        pivote = matriz[columna][columna]
        if columna == 0 and abs(abs(pivote) - 1) > TOLERANCIA:
            matriz[columna] = [valor / pivote for valor in matriz[columna]]
            factor_extraido *= pivote
            proceso.append({
                "tipo": "operacion_fila",
                "titulo": "Extraer factor de la primera fila",
                "operacion": (
                    f"F1 ← (1/{_formatear(pivote)})F1; "
                    f"se conserva el factor {_formatear(pivote)}"
                ),
                "matriz": _copiar_matriz(matriz)
            })
            pivote = matriz[columna][columna]
        pivotes.append(pivote)
        for fila in range(columna + 1, n):
            factor = matriz[fila][columna] / pivote
            if abs(factor) <= TOLERANCIA:
                continue
            matriz[fila] = [
                matriz[fila][j] - factor * matriz[columna][j]
                for j in range(n)
            ]
            matriz[fila][columna] = 0
            proceso.append({
                "tipo": "operacion_fila",
                "titulo": "Anular entrada bajo el pivote",
                "operacion": (
                    f"F{fila + 1} ← F{fila + 1} - "
                    f"({_formatear(factor)})F{columna + 1}; "
                    "reemplazar una fila por sí misma más un múltiplo de otra "
                    "no cambia el determinante"
                ),
                "matriz": _copiar_matriz(matriz)
            })

    proceso.append({
        "tipo": "operacion_fila",
        "titulo": "FORMA TRIANGULAR",
        "operacion": "Se usa el producto de la diagonal principal",
        "matriz": _copiar_matriz(matriz)
    })

    producto_diagonal = 1
    for pivote in pivotes:
        producto_diagonal *= pivote
    valor = (
        (-1 if intercambios % 2 else 1)
        * factor_extraido
        * producto_diagonal
    )
    if abs(valor) <= TOLERANCIA:
        valor = 0
    proceso.append({
        "tipo": "formula",
        "titulo": "Determinante desde la forma triangular",
        "operacion": "det(A) = (-1)^s · factores extraídos · producto diagonal",
        "detalle": (
            f"Intercambios s = {intercambios}; pivotes = "
            f"{' · '.join(_formatear(p) for p in pivotes)}; "
            f"factor extraído = {_formatear(factor_extraido)}; "
            f"det(A) = {'-1' if intercambios % 2 else '1'} · "
            f"{_formatear(factor_extraido)} · "
            f"{_formatear(producto_diagonal)} = {_formatear(valor)}"
        )
    })
    return valor, proceso, intercambios, pivotes, matriz, factor_extraido


def calcular_determinante(A, metodo="cofactores", eje_desarrollo=None):
    """
    Calcula det(A) usando solo el método solicitado.

    metodo admite "cofactores", "triangular" o "sarrus" (solo 3x3).
    eje_desarrollo permite fijar "fila:i" o "columna:j" en cofactores;
    por omisión se elige el eje que tenga más ceros.
    Devuelve el valor calculado y los pasos para mostrar en la interfaz.
    """

    _validar_matriz_cuadrada(A)

    matriz = _copiar_matriz(A)
    n = len(matriz)

    if metodo == "triangular":
        determinante, pasos, intercambios, pivotes, triangular, factor_extraido = (
            _determinante_triangular(matriz)
        )
        proceso = [{
            "numero": 1, "tipo": "inicio", "titulo": "MATRIZ ORIGINAL",
            "operacion": "A", "matriz": _copiar_matriz(matriz)
        }]
        for paso in pasos:
            paso["numero"] = len(proceso) + 1
            proceso.append(paso)
        proceso.append({
            "numero": len(proceso) + 1, "tipo": "determinante",
            "titulo": "RESULTADO", "operacion": "det(A)",
            "detalle": f"det(A) = {_formatear(determinante)}",
            "valor": determinante
        })
        return {
            "determinante": determinante, "resultado": determinante,
            "matriz": matriz, "metodo": metodo,
            "intercambios_filas": intercambios,
            "factores_diagonales": pivotes,
            "factor_extraido": factor_extraido,
            "matriz_triangular": triangular, "proceso": proceso
        }

    if metodo == "sarrus":
        if n != 3:
            raise ValueError("La regla de Sarrus solo se aplica a matrices 3x3.")
        determinante, detalle = _determinante_sarrus(matriz)
        # La presentación organiza Sarrus repitiendo los dos primeros
        # renglones debajo de la matriz original.
        matriz_extendida = matriz + [fila[:] for fila in matriz[:2]]
        proceso = [{
            "numero": 1, "tipo": "inicio", "titulo": "MATRIZ ORIGINAL",
            "operacion": "A", "matriz": _copiar_matriz(matriz)
        }, {
            "numero": 2, "tipo": "operacion",
            "titulo": "REPETIR LOS DOS PRIMEROS RENGLONES",
            "operacion": "A extendida para identificar las diagonales",
            "matriz": matriz_extendida
        }, {
            "numero": 3, "tipo": "formula", "titulo": "PRODUCTOS DE LAS DIAGONALES",
            "operacion": "Suma descendente menos suma ascendente",
            "detalle": detalle
        }, {
            "numero": 4, "tipo": "determinante", "titulo": "RESULTADO",
            "operacion": "det(A)",
            "detalle": f"det(A) = {_formatear(determinante)}",
            "valor": determinante
        }]
        return {
            "determinante": determinante, "resultado": determinante,
            "matriz": matriz, "metodo": metodo, "proceso": proceso
        }

    if metodo != "cofactores":
        raise ValueError("Selecciona cofactores, forma triangular o Sarrus.")

    proceso = [{
        "numero": 1,
        "tipo": "inicio",
        "titulo": "MATRIZ ORIGINAL",
        "operacion": "A",
        "matriz": _copiar_matriz(matriz)
    }]

    if n == 1:
        determinante = matriz[0][0]
        proceso.append({
            "numero": 2,
            "tipo": "formula",
            "titulo": "DETERMINANTE 1x1",
            "operacion": f"det(A) = {_formatear(determinante)}",
            "detalle": f"det(A) = {_formatear(determinante)}"
        })

        return {
            "determinante": determinante,
            "resultado": determinante,
            "matriz": matriz,
            "metodo": "cofactores",
            "fila_desarrollo": 0,
            "cofactores": [],
            "proceso": proceso
        }

    if n == 2:
        a, b = matriz[0]
        c, d = matriz[1]
        determinante = a * d - b * c
        determinante = 0 if abs(determinante) <= TOLERANCIA else determinante
        proceso.append({
            "numero": 2,
            "tipo": "formula",
            "titulo": "DETERMINANTE 2x2",
            "operacion": "det(A) = ad - bc",
            "detalle": (
                f"det(A) = {_formatear(a)}*{_formatear(d)} - "
                f"{_formatear(b)}*{_formatear(c)}\n"
                f"det(A) = {_formatear(a * d)} - "
                f"{_formatear(b * c)} = {_formatear(determinante)}"
            )
        })

        return {
            "determinante": determinante,
            "resultado": determinante,
            "matriz": matriz,
            "metodo": "cofactores",
            "fila_desarrollo": 0,
            "cofactores": [],
            "proceso": proceso
        }

    ceros_por_fila = [
        sum(1 for valor in fila if abs(valor) <= TOLERANCIA)
        for fila in matriz
    ]
    ceros_por_columna = [
        sum(1 for fila in matriz if abs(fila[columna]) <= TOLERANCIA)
        for columna in range(n)
    ]
    fila_con_mas_ceros = max(range(n), key=lambda i: ceros_por_fila[i])
    columna_con_mas_ceros = max(range(n), key=lambda j: ceros_por_columna[j])
    seleccion_automatica = eje_desarrollo in (None, "auto", "ceros")
    if seleccion_automatica:
        # La presentación recomienda elegir el eje con más ceros.
        desarrollar_por_columna = (
            ceros_por_columna[columna_con_mas_ceros]
            > ceros_por_fila[fila_con_mas_ceros]
        )
        fila_desarrollo = fila_con_mas_ceros
        columna_desarrollo = columna_con_mas_ceros
    else:
        if isinstance(eje_desarrollo, str) and ":" in eje_desarrollo:
            eje, indice_texto = eje_desarrollo.split(":", 1)
            try:
                indice_eje = int(indice_texto)
            except ValueError as error:
                raise ValueError("El eje de desarrollo seleccionado no es válido.") from error
        elif isinstance(eje_desarrollo, (tuple, list)) and len(eje_desarrollo) == 2:
            eje, indice_eje = eje_desarrollo
        else:
            raise ValueError("Selecciona una fila o columna válida para desarrollar.")
        if eje not in ("fila", "columna") or not isinstance(indice_eje, int) or not 0 <= indice_eje < n:
            raise ValueError("La fila o columna de desarrollo está fuera de rango.")
        desarrollar_por_columna = eje == "columna"
        fila_desarrollo = indice_eje if eje == "fila" else fila_con_mas_ceros
        columna_desarrollo = indice_eje if eje == "columna" else columna_con_mas_ceros
    cofactores = []
    terminos_texto = []
    total = 0

    if desarrollar_por_columna:
        indices = [
            (fila, columna_desarrollo, matriz[fila][columna_desarrollo])
            for fila in range(n)
        ]
        titulo_desarrollo = "COLUMNA DE DESARROLLO"
        etiqueta_desarrollo = f"Se desarrolla por C{columna_desarrollo + 1}"
        if seleccion_automatica:
            detalle_desarrollo = (
                f"Se elige C{columna_desarrollo + 1}, que tiene "
                f"{ceros_por_columna[columna_desarrollo]} ceros, la mayor cantidad "
                "entre filas y columnas (en empate se prioriza una fila)."
            )
        else:
            detalle_desarrollo = (
                f"Desarrollo seleccionado: C{columna_desarrollo + 1}; "
                f"contiene {ceros_por_columna[columna_desarrollo]} ceros."
            )
    else:
        indices = [
            (fila_desarrollo, columna, matriz[fila_desarrollo][columna])
            for columna in range(n)
        ]
        titulo_desarrollo = "FILA DE DESARROLLO"
        etiqueta_desarrollo = f"Se desarrolla por F{fila_desarrollo + 1}"
        if seleccion_automatica:
            detalle_desarrollo = (
                f"Se elige F{fila_desarrollo + 1}, que tiene "
                f"{ceros_por_fila[fila_desarrollo]} ceros, la mayor cantidad "
                "entre filas y columnas."
            )
        else:
            detalle_desarrollo = (
                f"Desarrollo seleccionado: F{fila_desarrollo + 1}; "
                f"contiene {ceros_por_fila[fila_desarrollo]} ceros."
            )

    patron_signos = "\n".join(
        "   ".join("+" if (fila + columna) % 2 == 0 else "−" for columna in range(n))
        for fila in range(n)
    )
    proceso.append({
        "numero": 2,
        "tipo": "formula",
        "titulo": "PATRÓN DE SIGNOS DE LOS COFACTORES",
        "operacion": "Cᵢⱼ = (−1)ⁱ⁺ʲ det(Mᵢⱼ)",
        "detalle": (
            f"{patron_signos}\n"
            "Los signos alternan; cada cofactor es el signo por el determinante del menor."
        )
    })

    proceso.append({
        "numero": 3,
        "tipo": "formula",
        "titulo": titulo_desarrollo,
        "operacion": etiqueta_desarrollo,
        "detalle": detalle_desarrollo
    })

    expresion_desarrollo = []
    for fila, columna, elemento in indices:
        if abs(elemento) <= TOLERANCIA:
            continue
        indices_sub = f"{subindice(fila + 1)}{subindice(columna + 1)}"
        exponente = superindice(f"({fila + 1}+{columna + 1})")
        expresion_desarrollo.append(
            f"({_formatear(elemento)})·(−1){exponente}·det(M{indices_sub})"
        )
    proceso.append({
        "numero": 4,
        "tipo": "formula",
        "titulo": "EXPANSIÓN POR COFACTORES",
        "operacion": "Suma de los elementos no nulos por sus cofactores",
        "detalle": (
            "det(A) = " + (" + ".join(expresion_desarrollo) or "0")
        )
    })

    for fila, columna, elemento in indices:
        # Desarrollo por cofactores:
        # 1. Tomar el elemento a_ij.
        # 2. Construir el menor M_ij.
        # 3. Calcular C_ij = (-1)^(i+j) det(M_ij).
        # 4. Sumar a_ij * C_ij al determinante.
        signo = -1 if (fila + columna) % 2 else 1
        menor = _menor(matriz, fila, columna)
        det_menor = _determinante_recursivo(menor)
        cofactor = signo * det_menor
        termino = elemento * cofactor

        if abs(termino) <= TOLERANCIA:
            termino = 0

        # Se acumula la suma de todos los términos del eje elegido.
        total += termino

        signo_texto = "+" if signo > 0 else "-"
        indices_sub = f"{subindice(fila + 1)}{subindice(columna + 1)}"
        nombre_menor = f"M{indices_sub}"
        nombre_cofactor = f"C{indices_sub}"
        nombre_elemento = f"a{indices_sub}"
        exponente_cofactor = superindice(
            f"({fila + 1}+{columna + 1})"
        )
        if len(menor) == 2:
            x, y = menor[0]
            z, w = menor[1]
            detalle_menor = (
                f"det({nombre_menor}) = "
                f"{_formatear(x)}·{_formatear(w)} - "
                f"{_formatear(y)}·{_formatear(z)} = "
                f"{_formatear(x * w)} - {_formatear(y * z)} = "
                f"{_formatear(det_menor)}"
            )
        elif len(menor) == 3:
            _, detalle_sarrus = _determinante_sarrus(menor)
            detalle_menor = (
                f"Sarrus para det({nombre_menor}):\n{detalle_sarrus}"
            )
        else:
            detalle_menor = (
                f"det({nombre_menor}) = "
                f"{_formatear(det_menor)}"
            )
        detalle = (
            f"{nombre_elemento} = {_formatear(elemento)}\n"
            f"{nombre_cofactor} = (−1){exponente_cofactor} "
            f"det({nombre_menor}) = ({signo_texto}) det({nombre_menor})\n"
            f"{detalle_menor}\n"
            f"Término {nombre_elemento}·{nombre_cofactor} = {_formatear(elemento)} · "
            f"{_formatear(cofactor)} = {_formatear(termino)}"
        )

        cofactores.append({
            "fila": fila,
            "columna": columna,
            "elemento": elemento,
            "signo": signo,
            "menor": menor,
            "determinante_menor": det_menor,
            "cofactor": cofactor,
            "termino": termino
        })

        if termino:
            terminos_texto.append(_formatear(termino))
        if abs(elemento) <= TOLERANCIA:
            continue

        proceso.append({
            "numero": len(proceso) + 1,
            "tipo": "operacion",
            "titulo": f"MENOR {nombre_menor}",
            "operacion": f"Menor asociado al término {nombre_elemento}",
            "matriz": menor
        })

        proceso.append({
            "numero": len(proceso) + 1,
            "tipo": "formula",
            "titulo": f"COFACTOR {nombre_cofactor}",
            "operacion": f"{nombre_elemento} · {nombre_cofactor}",
            "detalle": detalle
        })

    determinante = 0 if abs(total) <= TOLERANCIA else total
    expresion = "0"
    if terminos_texto:
        expresion = terminos_texto[0]
        for termino in terminos_texto[1:]:
            if termino.startswith("-"):
                expresion += " - " + termino[1:]
            else:
                expresion += " + " + termino

    proceso.append({
        "numero": len(proceso) + 1,
        "tipo": "determinante",
        "titulo": "RESULTADO",
        "operacion": (
            f"det(A) = {expresion} = {_formatear(determinante)}"
        ),
        "detalle": (
            f"det(A) = {expresion}\n"
            f"det(A) = {_formatear(determinante)}"
        ),
        "valor": determinante
    })

    return {
        "determinante": determinante,
        "resultado": determinante,
        "matriz": matriz,
        "metodo": "cofactores",
        "fila_desarrollo": None if desarrollar_por_columna else fila_desarrollo,
        "columna_desarrollo": columna_desarrollo if desarrollar_por_columna else None,
        "cofactores": cofactores,
        "proceso": proceso
    }


def resolver_sistema_cramer(A, b):
    """Resuelve Ax=b por Cramer y conserva el desarrollo de cada determinante."""
    _validar_matriz_cuadrada(A)
    if not isinstance(b, (list, tuple)) or len(b) != len(A):
        raise ValueError("El vector b debe tener una entrada por cada ecuación.")
    if any(not isinstance(valor, (int, float)) for valor in b):
        raise ValueError("Las entradas del vector b deben ser numéricas.")

    matriz = _copiar_matriz(A)
    vector = list(b)
    base = calcular_determinante(matriz, "cofactores")
    proceso = [{
        "numero": 1, "tipo": "inicio", "titulo": "PASO 1: SISTEMA Ax = b",
        "operacion": "Aplicar la regla de Cramer",
        "matriz": [fila[:] + [vector[i]] for i, fila in enumerate(matriz)]
    }]
    proceso.append({
        "numero": 2, "tipo": "formula", "titulo": "PASO 2: DETERMINANTE PRINCIPAL",
        "operacion": "D = det(A)", "detalle": f"D = { _formatear(base['determinante']) }"
    })
    for paso in base["proceso"][1:]:
        paso_copia = dict(paso)
        paso_copia["numero"] = len(proceso) + 1
        paso_copia["titulo"] = f"D: {paso_copia.get('titulo', 'Paso')}"
        proceso.append(paso_copia)

    if abs(base["determinante"]) <= TOLERANCIA:
        proceso.append({
            "numero": len(proceso) + 1, "tipo": "singular",
            "titulo": "No hay solución única por Cramer",
            "operacion": "det(A) = 0"
        })
        return {
            "exito": True, "operacion": "Cramer", "solucion": None,
            "determinante": base["determinante"], "determinantes_reemplazo": [],
            "proceso": proceso,
            "mensaje": "det(A) = 0; la regla de Cramer no determina una solución única."
        }

    proceso.append({
        "numero": len(proceso) + 1, "tipo": "formula",
        "titulo": "CONDICIÓN ESENCIAL",
        "operacion": "D ≠ 0",
        "detalle": "Como D ≠ 0, el sistema tiene una solución única por Cramer."
    })

    determinantes = []
    solucion = []
    for columna in range(len(matriz)):
        reemplazada = _copiar_matriz(matriz)
        for fila in range(len(matriz)):
            reemplazada[fila][columna] = vector[fila]
        datos = calcular_determinante(reemplazada, "cofactores")
        d_j = datos["determinante"]
        x_j = d_j / base["determinante"]
        determinantes.append(d_j)
        solucion.append(0 if isinstance(x_j, float) and abs(x_j) <= TOLERANCIA else x_j)
        proceso.append({
            "numero": len(proceso) + 1, "tipo": "inicio",
            "titulo": f"PASO 3: REEMPLAZAR COLUMNA {columna + 1}",
            "operacion": (
                f"D{subindice(columna + 1)} = "
                f"det(A{subindice(columna + 1)})"
            ),
            "matriz": reemplazada
        })
        for paso in datos["proceso"][1:]:
            paso_copia = dict(paso)
            paso_copia["numero"] = len(proceso) + 1
            paso_copia["titulo"] = (
                f"D{subindice(columna + 1)}: "
                f"{paso_copia.get('titulo', 'Paso')}"
            )
            proceso.append(paso_copia)
        proceso.append({
            "numero": len(proceso) + 1, "tipo": "formula",
            "titulo": f"PASO 4: CALCULAR x{subindice(columna + 1)}",
            "operacion": (
                f"x{subindice(columna + 1)} = "
                f"D{subindice(columna + 1)} / D"
            ),
            "detalle": (
                f"x{subindice(columna + 1)} = {_formatear(d_j)} / "
                f"{_formatear(base['determinante'])} = {_formatear(solucion[-1])}"
            )
        })

    proceso.append({
        "numero": len(proceso) + 1, "tipo": "resultado",
        "titulo": "SOLUCIÓN", "operacion": "x",
        "resultado": solucion
    })
    return {
        "exito": True, "operacion": "Cramer", "solucion": solucion,
        "resultado": solucion, "determinante": base["determinante"],
        "determinantes_reemplazo": determinantes,
        "proceso": proceso, "mensaje": "Solución calculada por la regla de Cramer."
    }


def verificar_propiedad_determinante(
    A, propiedad, operacion_fila=None, fila_i=None, fila_j=None, k=None,
    B=None
):
    """Verifica las propiedades solicitadas mostrando ambos lados."""
    _validar_matriz_cuadrada(A)
    matriz = _copiar_matriz(A)
    n = len(matriz)
    proceso = [{
        "numero": 1, "tipo": "inicio", "titulo": "Matriz original",
        "operacion": "A", "matriz": _copiar_matriz(matriz)
    }]

    if propiedad == "det_inversa":
        from matrices import invertir_matriz
        datos_a = calcular_determinante(matriz, "cofactores")
        inversa = invertir_matriz(matriz)
        if not inversa["invertible"]:
            raise ValueError("A es singular; det(A⁻¹) no está definido.")
        det_inversa = calcular_determinante(
            inversa["matriz_inversa"], "cofactores"
        )
        esperado = 1 / datos_a["determinante"]
        proceso.extend(
            {**paso, "titulo": f"Calcular det(A): {paso.get('titulo', 'Paso')}"}
            for paso in datos_a["proceso"][1:]
        )
        proceso.extend(
            {**paso, "titulo": f"Inversa de A: {paso.get('titulo', 'Paso')}"}
            for paso in inversa["proceso"][1:]
        )
        proceso.append({
            "tipo": "resultado", "titulo": "Matriz inversa", "operacion": "A⁻¹",
            "matriz": inversa["matriz_inversa"]
        })
        proceso.extend(
            {**paso, "titulo": f"Calcular det(A⁻¹): {paso.get('titulo', 'Paso')}"}
            for paso in det_inversa["proceso"][1:]
        )
        proceso.append({
            "tipo": "formula", "titulo": "Recíproco de det(A)",
            "operacion": f"1 / det(A) = {_formatear(esperado)}",
            "detalle": f"1 / {_formatear(datos_a['determinante'])} = {_formatear(esperado)}"
        })
        actual = det_inversa["determinante"]
        esperado_final = esperado
        expresion = "det(A⁻¹) = 1 / det(A)"

    elif propiedad in ("det_filas", "det_columnas"):
        es_columna = propiedad == "det_columnas"
        nombre_eje = "columna" if es_columna else "fila"
        prefijo_eje = "C" if es_columna else "F"
        if operacion_fila not in ("intercambio", "reemplazo", "escalar"):
            raise ValueError(f"Selecciona una operación de {nombre_eje} válida.")
        if not isinstance(fila_i, int) or not 0 <= fila_i < n:
            raise ValueError(f"Selecciona una {nombre_eje} válida.")
        transformada = _copiar_matriz(matriz)
        datos_a = calcular_determinante(matriz, "cofactores")
        det_a = datos_a["determinante"]
        proceso.extend(
            {**paso, "titulo": f"Calcular det(A): {paso.get('titulo', 'Paso')}"}
            for paso in datos_a["proceso"][1:]
        )
        if operacion_fila == "intercambio":
            if not isinstance(fila_j, int) or not 0 <= fila_j < n or fila_j == fila_i:
                raise ValueError(
                    f"El intercambio requiere dos {nombre_eje}s distintas y válidas."
                )
            if es_columna:
                for fila in range(n):
                    transformada[fila][fila_i], transformada[fila][fila_j] = (
                        transformada[fila][fila_j], transformada[fila][fila_i]
                    )
            else:
                transformada[fila_i], transformada[fila_j] = (
                    transformada[fila_j], transformada[fila_i]
                )
            esperado = -det_a
            operacion = f"{prefijo_eje}{fila_i + 1} ↔ {prefijo_eje}{fila_j + 1}"
            expresion = "det(A nueva) = -det(A)"
        elif operacion_fila == "reemplazo":
            if not isinstance(fila_j, int) or not 0 <= fila_j < n or fila_j == fila_i:
                raise ValueError(
                    f"El reemplazo requiere dos {nombre_eje}s distintas y válidas."
                )
            if not isinstance(k, (int, float)):
                raise ValueError("Indica un valor numérico para k.")
            if es_columna:
                for fila in range(n):
                    transformada[fila][fila_i] += k * transformada[fila][fila_j]
            else:
                transformada[fila_i] = [
                    transformada[fila_i][j] + k * transformada[fila_j][j]
                    for j in range(n)
                ]
            esperado = det_a
            operacion = (
                f"{prefijo_eje}{fila_i + 1} ← {prefijo_eje}{fila_i + 1} + "
                f"({_formatear(k)}){prefijo_eje}{fila_j + 1}"
            )
            expresion = "det(A nueva) = det(A)"
        else:
            if not isinstance(k, (int, float)):
                raise ValueError("Indica un valor numérico para k.")
            if es_columna:
                for fila in range(n):
                    transformada[fila][fila_i] *= k
            else:
                transformada[fila_i] = [
                    k * valor for valor in transformada[fila_i]
                ]
            esperado = k * det_a
            operacion = (
                f"{prefijo_eje}{fila_i + 1} ← ({_formatear(k)})"
                f"{prefijo_eje}{fila_i + 1}"
            )
            expresion = "det(A nueva) = k · det(A)"

        datos_transformada = calcular_determinante(transformada, "cofactores")
        proceso.append({
            "tipo": "operacion_fila",
            "titulo": f"Aplicar operación de {nombre_eje}",
            "operacion": operacion, "matriz": transformada
        })
        proceso.append({
            "tipo": "determinante", "titulo": "Determinante esperado",
            "operacion": expresion,
            "detalle": f"{expresion}; valor esperado = {_formatear(esperado)}"
        })
        proceso.extend(
            {**paso, "titulo": f"A nueva: {paso.get('titulo', 'Paso')}"}
            for paso in datos_transformada["proceso"][1:]
        )
        actual = datos_transformada["determinante"]
        esperado_final = esperado

    elif propiedad == "det_triangular":
        datos_cofactores = calcular_determinante(matriz, "cofactores")
        datos_triangular = calcular_determinante(matriz, "triangular")
        proceso.extend(
            {**paso, "titulo": f"Triangular: {paso.get('titulo', 'Paso')}"}
            for paso in datos_triangular["proceso"][1:]
        )
        proceso.extend(
            {**paso, "titulo": f"Comprobación por cofactores: {paso.get('titulo', 'Paso')}"}
            for paso in datos_cofactores["proceso"][1:]
        )
        actual = datos_triangular["determinante"]
        esperado_final = datos_cofactores["determinante"]
        expresion = "Producto diagonal corregido = expansión por cofactores"

    elif propiedad == "det_multiplicativa":
        if B is None:
            raise ValueError("Ingresa la matriz B para verificar det(AB).")
        _validar_matriz_cuadrada(B)
        matriz_b = _copiar_matriz(B)
        from matrices import multiplicar_matrices

        datos_a = calcular_determinante(matriz, "cofactores")
        datos_b = calcular_determinante(matriz_b, "cofactores")
        datos_producto = multiplicar_matrices([matriz, matriz_b])
        matriz_ab = datos_producto["resultado"]
        datos_ab = calcular_determinante(matriz_ab, "cofactores")

        proceso.append({
            "tipo": "inicio", "titulo": "Matriz B", "operacion": "B",
            "matriz": matriz_b
        })
        proceso.extend(
            {**paso, "titulo": f"Producto AB: {paso.get('titulo', 'Paso')}"}
            for paso in datos_producto.get("proceso", [])
        )
        for etiqueta, datos in (
            ("Determinante de A", datos_a),
            ("Determinante de B", datos_b),
            ("Determinante de AB", datos_ab)
        ):
            proceso.extend(
                {
                    **paso,
                    "titulo": f"{etiqueta}: {paso.get('titulo', 'Paso')}"
                }
                for paso in datos["proceso"][1:]
            )

        esperado_final = (
            datos_a["determinante"] * datos_b["determinante"]
        )
        actual = datos_ab["determinante"]
        expresion = "det(AB) = det(A) · det(B)"
        proceso.append({
            "tipo": "formula", "titulo": "Multiplicatividad",
            "operacion": expresion,
            "detalle": (
                f"det(AB) = {_formatear(actual)}; "
                f"det(A) · det(B) = {_formatear(datos_a['determinante'])} · "
                f"{_formatear(datos_b['determinante'])} = "
                f"{_formatear(esperado_final)}"
            )
        })
    else:
        raise ValueError("Selecciona una propiedad del determinante válida.")

    igualdad = abs(actual - esperado_final) <= TOLERANCIA
    proceso.append({
        "tipo": "verificacion", "titulo": "Comparación final",
        "operacion": expresion,
        "detalle": f"Resultado obtenido: {_formatear(actual)}; esperado: {_formatear(esperado_final)}",
        "resultado": igualdad
    })
    return {
        "exito": True, "operacion": "Propiedad de determinante",
        "propiedad": propiedad, "expresion": expresion,
        "igualdad": igualdad, "valor_obtenido": actual,
        "valor_esperado": esperado_final,
        "proceso": proceso,
        "mensaje": "La propiedad se cumple." if igualdad else "La propiedad no se cumple."
    }
