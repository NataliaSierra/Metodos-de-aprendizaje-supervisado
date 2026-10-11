import csv
import random
import math
from collections import Counter, defaultdict
import os

random.seed(42)

ESTACIONES = [
    "A1", "A2", "A3", "A4", "A5",
    "B1", "B2", "B4", "B5",
    "C1", "C3", "C4", "C5",
    "D1", "D3", "D4", "D5",
    "E1", "E3", "E4", "E5"
]

RUTAS_INFO = {
    "A": {"estaciones": ["A1", "A2", "A3", "A4", "A5"], "tiempo": 3, "congestion": 2, "accesibilidad": 3},
    "B": {"estaciones": ["B1", "B2", "A3", "B4", "B5"], "tiempo": 4, "congestion": 3, "accesibilidad": 2},
    "C": {"estaciones": ["C1", "A2", "C3", "C4", "C5"], "tiempo": 3, "congestion": 1, "accesibilidad": 3},
    "D": {"estaciones": ["D1", "B4", "D3", "D4", "D5"], "tiempo": 5, "congestion": 2, "accesibilidad": 2},
    "E": {"estaciones": ["E1", "A5", "E3", "E4", "E5"], "tiempo": 2, "congestion": 1, "accesibilidad": 3},
}

def generar_dataset(n_muestras=1000):
    registros = []

    for _ in range(n_muestras):
        origen = random.choice(ESTACIONES)
        destino = random.choice([e for e in ESTACIONES if e != origen])

        hora = random.randint(0, 23)
        dia = random.randint(1, 7)
        clima = random.choices(["bueno", "regular", "malo"], weights=[0.6, 0.3, 0.1])[0]
        es_hora_pico = 1 if (7 <= hora <= 9 or 17 <= hora <= 19) else 0

        rutas_posibles = []
        for ruta, info in RUTAS_INFO.items():
            if origen in info["estaciones"] or destino in info["estaciones"]:
                rutas_posibles.append(ruta)

        if not rutas_posibles:
            rutas_posibles = list(RUTAS_INFO.keys())

        ruta_elegida = random.choice(rutas_posibles)
        info_ruta = RUTAS_INFO.get(ruta_elegida, RUTAS_INFO["A"])

        try:
            idx_origen = info_ruta["estaciones"].index(origen)
            idx_destino = info_ruta["estaciones"].index(destino)
            num_estaciones = abs(idx_destino - idx_origen) + 1
        except ValueError:
            num_estaciones = random.randint(2, 5)

        num_transbordos = random.randint(0, 2)
        congestion = info_ruta["congestion"] + random.uniform(-0.5, 0.5)
        congestion = max(1, min(3, congestion))
        accesibilidad = info_ruta["accesibilidad"] + random.uniform(-0.5, 0.5)
        accesibilidad = max(1, min(3, accesibilidad))

        tiempo_base = num_estaciones * info_ruta["tiempo"]
        tiempo_transbordo = num_transbordos * random.uniform(2, 5)
        factor_clima = 1.0 if clima == "bueno" else (1.2 if clima == "regular" else 1.4)
        factor_pico = 1.3 if es_hora_pico else 1.0
        factor_congestion = 1 + (congestion - 1) * 0.15

        tiempo_real = (tiempo_base + tiempo_transbordo) * factor_clima * factor_pico * factor_congestion
        tiempo_real += random.gauss(0, 2)
        tiempo_real = max(5, round(tiempo_real, 1))

        if num_transbordos == 0 and tiempo_real < 15:
            tipo_ruta = "RAPIDA"
        elif num_transbordos == 0:
            tipo_ruta = "MENOS_TRANSBORDOS"
        elif accesibilidad >= 2.5:
            tipo_ruta = "ACCESIBLE"
        else:
            tipo_ruta = random.choice(["RAPIDA", "MENOS_TRANSBORDOS", "ACCESIBLE", "EQUILIBRADA"])

        registros.append({
            "origen": origen,
            "destino": destino,
            "hora_dia": hora,
            "dia_semana": dia,
            "num_estaciones": num_estaciones,
            "num_transbordos": num_transbordos,
            "congestion_promedio": round(congestion, 2),
            "accesibilidad_promedio": round(accesibilidad, 2),
            "distancia_estimada": round(num_estaciones * 1.5, 2),
            "es_hora_pico": es_hora_pico,
            "clima": clima,
            "tiempo_estimado": round(tiempo_base + tiempo_transbordo, 1),
            "tiempo_real": tiempo_real,
            "tipo_ruta_elegida": tipo_ruta,
        })

    return registros

def guardar_dataset(datos, ruta):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=datos[0].keys())
        writer.writeheader()
        writer.writerows(datos)
    print(f"Dataset guardado: {ruta} ({len(datos)} registros)")

def cargar_dataset(ruta):
    with open(ruta, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def convertir_tipos(datos):
    for row in datos:
        row['hora_dia'] = int(row['hora_dia'])
        row['dia_semana'] = int(row['dia_semana'])
        row['num_estaciones'] = int(row['num_estaciones'])
        row['num_transbordos'] = int(row['num_transbordos'])
        row['congestion_promedio'] = float(row['congestion_promedio'])
        row['accesibilidad_promedio'] = float(row['accesibilidad_promedio'])
        row['distancia_estimada'] = float(row['distancia_estimada'])
        row['es_hora_pico'] = int(row['es_hora_pico'])
        row['tiempo_estimado'] = float(row['tiempo_estimado'])
        row['tiempo_real'] = float(row['tiempo_real'])
    return datos

def codificar_categoricas(datos):
    estaciones_unicas = sorted(set([r['origen'] for r in datos] + [r['destino'] for r in datos]))
    climas_unicos = sorted(set(r['clima'] for r in datos))
    tipos_unicos = sorted(set(r['tipo_ruta_elegida'] for r in datos))

    mapa_estaciones = {e: i for i, e in enumerate(estaciones_unicas)}
    mapa_climas = {c: i for i, c in enumerate(climas_unicos)}
    mapa_tipos = {t: i for i, t in enumerate(tipos_unicos)}

    for row in datos:
        row['origen_cod'] = mapa_estaciones[row['origen']]
        row['destino_cod'] = mapa_estaciones[row['destino']]
        row['clima_cod'] = mapa_climas[row['clima']]
        row['tipo_ruta_cod'] = mapa_tipos[row['tipo_ruta_elegida']]

    return datos, mapa_tipos

def escalar_datos(datos, features):
    X = [[float(row[f]) for f in features] for row in datos]
    
    medias = []
    desvs = []
    n_features = len(features)
    
    for j in range(n_features):
        columna = [X[i][j] for i in range(len(X))]
        media = sum(columna) / len(columna)
        varianza = sum((x - media) ** 2 for x in columna) / len(columna)
        desv = math.sqrt(varianza) if varianza > 0 else 1
        medias.append(media)
        desvs.append(desv)
    
    X_scaled = []
    for i in range(len(X)):
        fila_scaled = [(X[i][j] - medias[j]) / desvs[j] for j in range(n_features)]
        X_scaled.append(fila_scaled)
    
    return X_scaled, medias, desvs

def dividir_datos(X, y, test_size=0.2):
    n = len(X)
    indices = list(range(n))
    random.shuffle(indices)
    
    n_test = int(n * test_size)
    test_idx = indices[:n_test]
    train_idx = indices[n_test:]
    
    X_train = [X[i] for i in train_idx]
    X_test = [X[i] for i in test_idx]
    y_train = [y[i] for i in train_idx]
    y_test = [y[i] for i in test_idx]
    
    return X_train, X_test, y_train, y_test

def distancia_euclidiana(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))

class KNNClasificador:
    def __init__(self, k=5):
        self.k = k
    
    def fit(self, X, y):
        self.X_train = X
        self.y_train = y
    
    def predict(self, X):
        predicciones = []
        for x in X:
            distancias = [(distancia_euclidiana(x, self.X_train[i]), self.y_train[i]) for i in range(len(self.X_train))]
            distancias.sort(key=lambda t: t[0])
            vecinos = [d[1] for d in distancias[:self.k]]
            conteo = Counter(vecinos)
            pred = conteo.most_common(1)[0][0]
            predicciones.append(pred)
        return predicciones

class KNNRegresor:
    def __init__(self, k=5):
        self.k = k
    
    def fit(self, X, y):
        self.X_train = X
        self.y_train = y
    
    def predict(self, X):
        predicciones = []
        for x in X:
            distancias = [(distancia_euclidiana(x, self.X_train[i]), self.y_train[i]) for i in range(len(self.X_train))]
            distancias.sort(key=lambda t: t[0])
            vecinos = [d[1] for d in distancias[:self.k]]
            pred = sum(vecinos) / len(vecinos)
            predicciones.append(pred)
        return predicciones

class RegresionLineal:
    def __init__(self):
        self.coeficientes = None
        self.intercepto = None
    
    def fit(self, X, y):
        n = len(X)
        p = len(X[0])
        
        self.coeficientes = [0.0] * p
        self.intercepto = sum(y) / n
        
        learning_rate = 0.01
        for _ in range(100):
            for i in range(n):
                pred = self.intercepto + sum(self.coeficientes[j] * X[i][j] for j in range(p))
                error = y[i] - pred
                self.intercepto += learning_rate * error
                for j in range(p):
                    self.coeficientes[j] += learning_rate * error * X[i][j]
    
    def predict(self, X):
        predicciones = []
        for x in X:
            pred = self.intercepto + sum(self.coeficientes[j] * x[j] for j in range(len(self.coeficientes)))
            predicciones.append(pred)
        return predicciones

class ArbolDecisionClasificador:
    def __init__(self, max_depth=5):
        self.max_depth = max_depth
        self.arbol = None
    
    def fit(self, X, y):
        self.arbol = self._construir_arbol(X, y, 0)
    
    def _construir_arbol(self, X, y, depth):
        if depth >= self.max_depth or len(set(y)) == 1:
            conteo = Counter(y)
            return {'tipo': 'hoja', 'clase': conteo.most_common(1)[0][0]}
        
        mejor_feature = None
        mejor_threshold = None
        mejor_gini = float('inf')
        
        for feature_idx in range(len(X[0])):
            valores = sorted(set(x[feature_idx] for x in X))
            for i in range(len(valores) - 1):
                threshold = (valores[i] + valores[i+1]) / 2
                izquierda_y = [y[j] for j in range(len(X)) if X[j][feature_idx] <= threshold]
                derecha_y = [y[j] for j in range(len(X)) if X[j][feature_idx] > threshold]
                
                if len(izquierda_y) == 0 or len(derecha_y) == 0:
                    continue
                
                gini = (len(izquierda_y) * self._gini(izquierda_y) + len(derecha_y) * self._gini(derecha_y)) / len(y)
                
                if gini < mejor_gini:
                    mejor_gini = gini
                    mejor_feature = feature_idx
                    mejor_threshold = threshold
        
        if mejor_feature is None:
            conteo = Counter(y)
            return {'tipo': 'hoja', 'clase': conteo.most_common(1)[0][0]}
        
        izquierda_X = [x for x in X if x[mejor_feature] <= mejor_threshold]
        izquierda_y = [y[j] for j in range(len(X)) if X[j][mejor_feature] <= mejor_threshold]
        derecha_X = [x for x in X if x[mejor_feature] > mejor_threshold]
        derecha_y = [y[j] for j in range(len(X)) if X[j][mejor_feature] > mejor_threshold]
        
        return {
            'tipo': 'nodo',
            'feature': mejor_feature,
            'threshold': mejor_threshold,
            'izquierda': self._construir_arbol(izquierda_X, izquierda_y, depth + 1),
            'derecha': self._construir_arbol(derecha_X, derecha_y, depth + 1)
        }
    
    def _gini(self, y):
        conteo = Counter(y)
        return 1 - sum((count / len(y)) ** 2 for count in conteo.values())
    
    def predict(self, X):
        return [self._predecir_uno(x, self.arbol) for x in X]
    
    def _predecir_uno(self, x, nodo):
        if nodo['tipo'] == 'hoja':
            return nodo['clase']
        if x[nodo['feature']] <= nodo['threshold']:
            return self._predecir_uno(x, nodo['izquierda'])
        else:
            return self._predecir_uno(x, nodo['derecha'])

def accuracy(y_true, y_pred):
    correctos = sum(1 for a, b in zip(y_true, y_pred) if a == b)
    return correctos / len(y_true)

def mean_absolute_error(y_true, y_pred):
    return sum(abs(a - b) for a, b in zip(y_true, y_pred)) / len(y_true)

def mean_squared_error(y_true, y_pred):
    return sum((a - b) ** 2 for a, b in zip(y_true, y_pred)) / len(y_true)

def r2_score(y_true, y_pred):
    media = sum(y_true) / len(y_true)
    ss_tot = sum((y - media) ** 2 for y in y_true)
    ss_res = sum((y_true[i] - y_pred[i]) ** 2 for i in range(len(y_true)))
    return 1 - (ss_res / ss_tot) if ss_tot > 0 else 0

def main():
    print("=" * 60)
    print("SISTEMA DE TRANSPORTE - MODELOS DE APRENDIZAJE SUPERVISADO")
    print("=" * 60)
    
    print("\n[1] Generando dataset sintetico...")
    datos = generar_dataset(1500)
    guardar_dataset(datos, "datos/viajes_historicos.csv")
    
    print("\n[2] Resumen estadistico:")
    tiempos = [d['tiempo_real'] for d in datos]
    print(f"  Tiempo real - Media: {sum(tiempos)/len(tiempos):.2f}, Min: {min(tiempos):.1f}, Max: {max(tiempos):.1f}")
    
    print("\n[3] Preprocesando datos...")
    datos = convertir_tipos(datos)
    datos, mapa_tipos = codificar_categoricas(datos)
    
    features = [
        'origen_cod', 'destino_cod', 'hora_dia', 'dia_semana',
        'num_estaciones', 'num_transbordos', 'congestion_promedio',
        'accesibilidad_promedio', 'distancia_estimada', 'es_hora_pico',
        'clima_cod', 'tiempo_estimado'
    ]
    
    X_scaled, medias, desvs = escalar_datos(datos, features)
    y_clasif = [d['tipo_ruta_cod'] for d in datos]
    y_reg = [d['tiempo_real'] for d in datos]
    
    n = len(X_scaled)
    indices = list(range(n))
    random.shuffle(indices)
    n_test = int(n * 0.2)
    test_idx = indices[:n_test]
    train_idx = indices[n_test:]
    
    X_train = [X_scaled[i] for i in train_idx]
    X_test = [X_scaled[i] for i in test_idx]
    y_clasif_train = [y_clasif[i] for i in train_idx]
    y_clasif_test = [y_clasif[i] for i in test_idx]
    y_reg_train = [y_reg[i] for i in train_idx]
    y_reg_test = [y_reg[i] for i in test_idx]
    
    print("\n[4] Entrenando modelos de CLASIFICACION")
    print("-" * 60)
    
    modelos_clasif = {
        "KNN (k=5)": KNNClasificador(k=5),
        "ArbolDecision": ArbolDecisionClasificador(max_depth=5),
    }
    
    resultados_clasif = {}
    for nombre, modelo in modelos_clasif.items():
        modelo.fit(X_train, y_clasif_train)
        predicciones = modelo.predict(X_test)
        acc = accuracy(y_clasif_test, predicciones)
        resultados_clasif[nombre] = {'accuracy': acc, 'predicciones': predicciones}
        print(f"{nombre}: Accuracy = {acc:.4f}")
    
    print("\n[5] Entrenando modelos de REGRESION")
    print("-" * 60)
    
    modelos_reg = {
        "RegresionLineal": RegresionLineal(),
        "KNNReg (k=5)": KNNRegresor(k=5),
    }
    
    resultados_reg = {}
    for nombre, modelo in modelos_reg.items():
        modelo.fit(X_train, y_reg_train)
        predicciones = modelo.predict(X_test)
        mae = mean_absolute_error(y_reg_test, predicciones)
        rmse = math.sqrt(mean_squared_error(y_reg_test, predicciones))
        r2 = r2_score(y_reg_test, predicciones)
        resultados_reg[nombre] = {'mae': mae, 'rmse': rmse, 'r2': r2, 'predicciones': predicciones}
        print(f"{nombre}: MAE = {mae:.4f}, RMSE = {rmse:.4f}, R2 = {r2:.4f}")
    
    print("\n" + "=" * 60)
    print("RESUMEN FINAL")
    print("=" * 60)
    
    mejor_clasif = max(resultados_clasif, key=lambda k: resultados_clasif[k]['accuracy'])
    print(f"Mejor clasificador: {mejor_clasif} (accuracy={resultados_clasif[mejor_clasif]['accuracy']:.4f})")
    
    mejor_reg = max(resultados_reg, key=lambda k: resultados_reg[k]['r2'])
    print(f"Mejor regresor: {mejor_reg} (R2={resultados_reg[mejor_reg]['r2']:.4f})")
    
    print("\n[6] Artefactos generados:")
    print("  - datos/viajes_historicos.csv")

if __name__ == "__main__":
    main()
