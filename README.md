# Actividad 3 - Metodos de aprendizaje supervisado - Inteligencia Artificial

## Estudiante

**Natalia Sierra Salamando**
**Ingenieria de Software Virtual**

### Corporacion Universitaria Iberoamericana

Sistema de aprendizaje supervisado que entrena modelos de **clasificacion** y **regresion** sobre un dataset sintetico de viajes de transporte masivo. Los modelos aprenden a partir de datos historicos simulados para predecir el tipo de ruta preferido por un usuario y el tiempo real de un viaje.

---

# Tabla de contenidos

* [Descripcion](#descripcion)
* [Objetivos](#objetivos)
* [Dataset](#dataset)
* [Preprocesamiento](#preprocesamiento)
* [Modelos implementados](#modelos-implementados)
* [Metricas de evaluacion](#metricas-de-evaluacion)
* [Arquitectura](#arquitectura)
* [Estructura del proyecto](#estructura-del-proyecto)
* [Como ejecutar](#como-ejecutar)
* [Resultados esperados](#resultados-esperados)
* [Tecnologias](#tecnologias)
* [Autor](#autor)

---

# Descripcion

El proyecto genera 1500 registros sinteticos de viajes en un sistema de transporte con 5 lineas (A-E) y 20 estaciones. A partir de estos datos, entrena 4 modelos de aprendizaje supervisado implementados desde cero:

- **Clasificacion**: predecir el tipo de ruta elegida (RAPIDA, MENOS_TRANSBORDOS, ACCESIBLE, EQUILIBRADA)
- **Regresion**: predecir el tiempo real del viaje en minutos

Todos los modelos estan implementados sin dependencias externas, usando unicamente la biblioteca estandar de Python.

---

# Objetivos

## Objetivo general

Implementar y comparar modelos de aprendizaje supervisado (clasificacion y regresion) sobre datos sinteticos de transporte masivo, desarrollados integramente en Python estandar.

## Objetivos especificos

* Generar un dataset sintetico con variables operativas, ambientales y de preferencia.
* Preprocesar datos: codificar categoricas, escalar features, dividir train/test.
* Implementar KNN (clasificacion y regresion) desde cero.
* Implementar Arbol de Decision desde cero.
* Implementar Regresion Lineal con gradient descent desde cero.
* Evaluar modelos con metricas estandar (accuracy, MAE, RMSE, R2).
* Comparar desempeno entre modelos.

---

# Dataset

**Archivo generado:** `datos/viajes_historicos.csv`
**Registros:** 1500 viajes simulados
**Variables:** 14 columnas

## Variables del dataset

| Variable | Tipo | Descripcion |
|----------|------|-------------|
| `origen` | Categorica | Estacion de origen |
| `destino` | Categorica | Estacion de destino |
| `hora_dia` | Numerica (0-23) | Hora del viaje |
| `dia_semana` | Numerica (1-7) | Dia de la semana |
| `num_estaciones` | Numerica | Estaciones en el recorrido |
| `num_transbordos` | Numerica (0-2) | Transbordos necesarios |
| `congestion_promedio` | Numerica (1-3) | Nivel de congestion |
| `accesibilidad_promedio` | Numerica (1-3) | Nivel de accesibilidad |
| `distancia_estimada` | Numerica | Distancia en km |
| `es_hora_pico` | Binaria (0/1) | Si es hora pico |
| `clima` | Categorica | Bueno, regular, malo |
| `tiempo_estimado` | Numerica | Tiempo teorico (min) |
| `tiempo_real` | Numerica | Tiempo observado (min) |
| `tipo_ruta_elegida` | Categorica | Tipo de ruta seleccionada |

## Targets

### Clasificacion: `tipo_ruta_elegida`
- **RAPIDA**: sin transbordos y tiempo < 15 min
- **MENOS_TRANSBORDOS**: sin transbordos
- **ACCESIBLE**: accesibilidad >= 2.5
- **EQUILIBRADA**: resto

### Regresion: `tiempo_real`
Calculado con factores de: tiempo base, transbordos, clima, hora pico, congestion, mas ruido gaussiano.

---

# Preprocesamiento

1. **Conversion de tipos**: strings a int/float
2. **Codificacion de categoricas**: label encoding manual para origen, destino, clima y tipo_ruta
3. **Escalado z-score**: normalizacion estandar (resta media, divide desviacion) en todas las features
4. **Division**: 80% entrenamiento (1200) / 20% prueba (300) con semilla 42

---

# Modelos implementados

## Clasificacion

### KNN Clasificador (k=5)
- Calcula distancia euclidiana entre el punto a predecir y todos los de entrenamiento
- Selecciona los 5 vecinos mas cercanos
- Votacion mayoritaria: la clase mas frecuente es la prediccion

### Arbol de Decision (max_depth=5)
- Construccion recursiva usando indice Gini
- En cada nodo prueba todos los features y thresholds
- Elige la division que minimice impureza
- Crea hojas puras o hasta profundidad maxima

## Regresion

### Regresion Lineal (gradient descent)
- Inicializa coeficientes en 0, intercepto en la media de y
- Gradient descent: 100 iteraciones, learning_rate=0.01
- Ajusta coeficientes para minimizar el error

### KNN Regresor (k=5)
- Igual que KNN clasificador pero promedia los valores de los 5 vecinos en lugar de votar

---

# Metricas de evaluacion

## Clasificacion
- **Accuracy**: (predicciones correctas) / total

## Regresion
- **MAE**: error absoluto medio
- **RMSE**: raiz del error cuadratico medio
- **R2**: proporcion de varianza explicada (1 = perfecto, 0 = malo)

---

# Arquitectura

```
┌─────────────────────────────────────┐
│       GENERACION DE DATOS           │
│                                     │
│  1500 viajes sinteticos             │
│  Variables operativas, ambientales  │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│        PREPROCESAMIENTO             │
│                                     │
│  Conversion de tipos                │
│  Label encoding                     │
│  Escalado z-score                   │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│        DIVISION TRAIN/TEST          │
│                                     │
│  80% entrenamiento (1200)           │
│  20% prueba (300)                   │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│        MODELOS DE CLASIFICACION     │
│                                     │
│  KNN (k=5)                          │
│  Arbol de Decision (depth=5)        │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│        MODELOS DE REGRESION         │
│                                     │
│  Regresion Lineal                   │
│  KNN Regresor (k=5)                 │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│        EVALUACION                   │
│                                     │
│  Accuracy (clasificacion)           │
│  MAE, RMSE, R2 (regresion)         │
│  Comparacion y mejor modelo         │
└─────────────────────────────────────┘
```

---

# Estructura del proyecto

```
Metodos de aprendizaje supervisado/
│
├── modelo_supervisado.py
├── descripcion_datos.md
├── pruebas_modelo.md
├── README.md
│
└── datos/
    └── viajes_historicos.csv (generado al ejecutar)
```

---

# Como ejecutar

## Requisitos

```
Python 3.8+
```

## Ejecucion

```bash
python modelo_supervisado.py
```

No se requieren dependencias externas. El script:

1. Genera el dataset en `datos/viajes_historicos.csv`
2. Preprocesa los datos
3. Entrena los 4 modelos
4. Evalua cada uno con metricas estandar
5. Muestra el mejor clasificador y mejor regresor

---

# Resultados esperados

```
============================================================
SISTEMA DE TRANSPORTE - MODELOS DE APRENDIZAJE SUPERVISADO
============================================================

[1] Generando dataset sintetico...
Dataset guardado: datos/viajes_historicos.csv (1500 registros)

[2] Resumen estadistico:
  Tiempo real - Media: ~20.33, Min: ~5.0, Max: ~67.0

[3] Preprocesando datos...

[4] Entrenando modelos de CLASIFICACION
------------------------------------------------------------
KNN (k=5): Accuracy = ~0.7133
ArbolDecision: Accuracy = ~0.7633

[5] Entrenando modelos de REGRESION
------------------------------------------------------------
RegresionLineal: MAE = ~2.52, RMSE = ~3.48, R2 = ~0.8851
KNNReg (k=5): MAE = ~3.23, RMSE = ~4.29, R2 = ~0.8250

============================================================
RESUMEN FINAL
============================================================
Mejor clasificador: ArbolDecision (accuracy=~0.7633)
Mejor regresor: RegresionLineal (R2=~0.8851)

[6] Artefactos generados:
  - datos/viajes_historicos.csv
```

Los valores exactos pueden variar ligeramente. Resultados tipicos:

| Tarea | Mejor Modelo | Metrica | Valor |
|-------|-------------|---------|-------|
| Clasificacion | Arbol de Decision | Accuracy | ~76% |
| Regresion | Regresion Lineal | R2 | ~88.5% |

---

# Tecnologias

Solo biblioteca estandar de Python:

* `csv` - lectura/escritura del dataset
* `random` - generacion de datos y division train/test
* `math` - calculos matematicos (distancia, sqrt, potencias)
* `collections` - Counter para votaciones y frecuencias
* `os` - creacion de directorios

No se utilizan librerias externas (numpy, pandas, scikit-learn, etc.).

---

# Autor: Natalia Sierra Salamando

Proyecto desarrollado como implementacion academica de modelos de aprendizaje supervisado para prediccion de rutas y tiempos en transporte masivo.

---

# Resumen

El proyecto implementa un pipeline completo de aprendizaje supervisado:

```
Generacion de datos
        │
        ▼
Preprocesamiento
        │
        ▼
Division train/test
        │
        ▼
Entrenamiento de modelos
        │
        ├── Clasificacion (KNN, Arbol)
        └── Regresion (Lineal, KNN)
        │
        ▼
Evaluacion con metricas
        │
        ▼
Seleccion del mejor modelo
```

Todo implementado desde cero con Python estandar, sin dependencias externas.
