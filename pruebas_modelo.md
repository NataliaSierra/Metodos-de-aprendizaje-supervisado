# Pruebas Realizadas al Componente de Aprendizaje Supervisado

## Resumen de ejecucion

**Fecha:** 2026-10-11
**Dataset:** 1500 registros de viajes simulados
**Division:** 80% train (1200) / 20% test (300)
**Random seed:** 42 (reproducible)
**Implementacion:** Python estandar (sin dependencias externas)

## 1. Pruebas de clasificacion (predecir tipo de ruta)

### Modelos evaluados

| Modelo | Accuracy | Observaciones |
|--------|----------|---------------|
| KNN (k=5) | 0.7133 | Buen desempeno, sensible a escala |
| Arbol de Decision (depth=5) | **0.7633** | Mejor accuracy, captura no-linealidades |

### Mejor modelo: Arbol de Decision
- **Accuracy:** 76.33%
- **Observaciones:**
  - Captura relaciones no lineales entre features
  - Interpretabilidad alta (reglas if-then)
  - Sin necesidad de escalado para este modelo

### Distribucion de clases en test

El dataset tiene 4 clases balanceadas:
- ACCESIBLE
- EQUILIBRADA
- MENOS_TRANSBORDOS
- RAPIDA

## 2. Pruebas de regresion (predecir tiempo real)

### Modelos evaluados

| Modelo | MAE (min) | RMSE (min) | R2 |
|--------|-----------|------------|-----|
| Regresion Lineal | 2.52 | 3.48 | **0.8851** |
| KNN Regresor (k=5) | 3.23 | 4.29 | 0.8250 |

### Mejor modelo: Regresion Lineal
- **MAE:** 2.52 minutos (error promedio absoluto)
- **RMSE:** 3.48 minutos
- **R2:** 0.8851 (explica 88.51% de la varianza)
- **Observaciones:**
  - Excelente capacidad de prediccion lineal
  - R2 alto indica relacion lineal fuerte entre features y target
  - Mas eficiente computacionalmente que KNN

## 3. Pruebas de robustez

### 3.1 Escalado de features
- StandardScaler manual aplicado a todas las variables
- Mejora convergencia en modelos basados en distancias (KNN)

### 3.2 Reproducibilidad
- Random seed 42 en todas las operaciones aleatorias
- Resultados reproducibles entre ejecuciones

### 3.3 Implementacion sin dependencias
- Todos los modelos implementados desde cero
- Solo usa biblioteca estandar de Python
- Compatible con entornos con politicas de seguridad restrictivas (AppLocker/WDAC)

## 4. Artefactos generados

| Archivo | Descripcion |
|---------|-------------|
| `datos/viajes_historicos.csv` | Dataset completo (1500 registros, 14 columnas) |
| `modelo_supervisado.py` | Codigo fuente completo |
| `descripcion_datos.md` | Descripcion detallada del dataset |
| `pruebas_modelo.md` | Este documento |

## 5. Analisis de resultados

### Clasificacion
- **Arbol de Decision** supera a KNN por 5 puntos porcentuales
- El problema de clasificacion tiene complejidad moderada (4 clases, relaciones no lineales)
- Accuracy de 76% es aceptable para un problema con factores subjetivos (preferencia de usuario)

### Regresion
- **Regresion Lineal** supera a KNN en R2 (0.885 vs 0.825)
- La prediccion de tiempo real tiene relacion predominantemente lineal con las features
- MAE de 2.5 minutos es preciso para un sistema de transporte

## 6. Comparacion de modelos

| Tarea | Mejor Modelo | Metrica | Valor |
|-------|--------------|---------|-------|
| Clasificacion | Arbol de Decision | Accuracy | 76.33% |
| Regresion | Regresion Lineal | R2 | 88.51% |

## 7. Conclusiones

1. **Regresion Lineal** es el mejor modelo para predecir tiempo real (R2=0.885)
2. **Arbol de Decision** es el mejor modelo para predecir tipo de ruta (accuracy=76.3%)
3. La prediccion de **tiempo real** es mas precisa que la **preferencia de ruta**
4. El dataset sintetico captura relaciones realistas del sistema de transporte
5. La implementacion sin dependencias externas garantiza portabilidad

## 8. Mejoras futuras

- Incrementar volumen de datos (actualmente 1500 registros)
- Incorporar datos reales de sensores y tarjetas de transporte
- Implementar Random Forest o Gradient Boosting desde cero
- Feature engineering adicional (interacciones entre variables)
- Validacion cruzada k-fold implementada manualmente
- Probar redes neuronales simples (perceptron multicapa)

## 9. Como ejecutar

```bash
python modelo_supervisado.py
```

El script genera automaticamente:
1. Dataset sintetico en `datos/viajes_historicos.csv`
2. Entrena modelos de clasificacion y regresion
3. Evalua desempeno con metricas estandar
4. Muestra resumen de resultados en consola
