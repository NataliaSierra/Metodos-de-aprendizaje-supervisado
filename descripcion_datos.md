# Descripcion del Dataset - Sistema de Transporte Masivo

## Origen de los datos

El dataset fue generado sinteticamente a partir de la base de conocimiento del sistema inteligente de transporte desarrollado en actividades previas. Simula registros historicos de viajes de usuarios del sistema de transporte masivo, incluyendo variables operativas, ambientales y de preferencia.

## Estructura del dataset

**Archivo:** `datos/viajes_historicos.csv`
**Registros:** 1500 viajes simulados
**Variables:** 14 columnas

## Descripcion de variables

| Variable | Tipo | Descripcion |
|----------|------|-------------|
| `origen` | Categorica | Estacion de origen del viaje |
| `destino` | Categorica | Estacion de destino del viaje |
| `hora_dia` | Numerica (0-23) | Hora del dia en que se realiza el viaje |
| `dia_semana` | Numerica (1-7) | Dia de la semana (1=Lunes, 7=Domingo) |
| `num_estaciones` | Numerica | Cantidad de estaciones en el recorrido |
| `num_transbordos` | Numerica (0-2) | Numero de transbordos necesarios |
| `congestion_promedio` | Numerica (1-3) | Nivel de congestion promedio de la ruta |
| `accesibilidad_promedio` | Numerica (1-3) | Nivel de accesibilidad promedio de la ruta |
| `distancia_estimada` | Numerica | Distancia estimada en km (estaciones * 1.5) |
| `es_hora_pico` | Binaria (0/1) | 1 si el viaje es en hora pico (7-9 o 17-19) |
| `clima` | Categorica | Condicion climatica: bueno, regular, malo |
| `tiempo_estimado` | Numerica | Tiempo estimado teorico del recorrido (min) |
| `tiempo_real` | Numerica | Tiempo real observado del viaje (min) |
| `tipo_ruta_elegida` | Categorica | Tipo de ruta seleccionada por el usuario |

## Variables objetivo (targets)

### 1. Clasificacion: `tipo_ruta_elegida`
Categorias posibles:
- **RAPIDA**: Rutas sin transbordos y tiempo < 15 min
- **MENOS_TRANSBORDOS**: Rutas sin transbordos
- **ACCESIBLE**: Rutas con accesibilidad >= 2.5
- **EQUILIBRADA**: Resto de rutas

### 2. Regresion: `tiempo_real`
Tiempo real del viaje en minutos, calculado considerando:
- Tiempo base por estaciones
- Tiempo de transbordos
- Factor climatico (bueno=1.0, regular=1.2, malo=1.4)
- Factor hora pico (1.3)
- Factor congestion (1 + (congestion-1)*0.15)
- Ruido aleatorio normal(0, 2)

## Fuentes de datos reales relacionadas

Para un sistema real, estas fuentes podrian alimentar el modelo:
- **API de transacciones de tarjetas de transporte**: registros de entrada/salida
- **Sensores IoT en estaciones**: conteo de pasajeros, tiempos de espera
- **Sistemas GPS de vehiculos**: tiempos reales de recorrido
- **APIs meteorologicas**: condiciones climaticas historicas
- **Encuestas de satisfaccion**: preferencias de usuarios
- **Sistemas de monitoreo de congestion**: datos en tiempo real

## Resumen estadistico del dataset generado

| Variable | Media | Min | Max |
|----------|-------|-----|-----|
| tiempo_real | 20.33 | 5.0 | 67.0 |
| num_estaciones | - | 1 | 5 |
| num_transbordos | - | 0 | 2 |
| congestion_promedio | - | 1.0 | 3.0 |
| accesibilidad_promedio | - | 1.0 | 3.0 |

## Preprocesamiento aplicado

1. **Codificacion de categoricas**: LabelEncoder manual para origen, destino, clima
2. **Escalado**: StandardScaler manual (z-score) en todas las features
3. **Division**: 80% entrenamiento (1200) / 20% prueba (300) con semilla 42

## Nota sobre implementacion

Los modelos fueron implementados desde cero usando solo la biblioteca estandar de Python (csv, random, math, collections), sin dependencias externas, para garantizar compatibilidad con entornos restringidos por politicas de seguridad (AppLocker/WDAC).
