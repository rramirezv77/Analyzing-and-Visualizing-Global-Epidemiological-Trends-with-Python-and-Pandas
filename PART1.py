# %% [Celda 1] Importación de Librerías
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sb
import requests
import time
import dask.dataframe as dd
import os
# %pylab inline  # Esta línea es específica de Jupyter, la dejo comentada para scripts estándar.

# Configuración de visualización
pd.set_option('display.max_columns', None)
print("Librerías cargadas correctamente.")

# %% [Celda 2] Configuración de Fechas
# Definir el rango de fechas para el análisis
start_date = '2021-01-01'
end_date = '2021-01-31'

date_range = pd.date_range(start=start_date, end=end_date)
print(f"Analizando rango desde {start_date} hasta {end_date}")

# %% [Celda 3] Método 1: Carga Original (Iterativa)
# Este bloque simula la carga lenta original para comparación
print("Iniciando carga original (iterativa)...")
start_time = time.time()

df_list = []

for single_date in date_range:
    # Construcción de la URL para cada día
    url = f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/refs/heads/master/csse_covid_19_data/csse_covid_19_daily_reports/{single_date.strftime("%m-%d-%Y")}.csv'
    try:
        df_list.append(pd.read_csv(url))
    except Exception as e:
        print(f"Error cargando {url}: {e}")

# Combinar los DataFrames diarios en uno solo
enero = pd.concat(df_list, ignore_index=True)

load_time_original = time.time() - start_time
print(f"Tiempo de carga original: {load_time_original:.2f} segundos")

# %% [Celda 4] Método 2: Optimización con Dask (Paralelo)
# Este bloque usa Dask para leer múltiples archivos en paralelo
print("Iniciando carga optimizada con Dask...")
start_time = time.time()

# Crear lista de URLs
urls = [f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/refs/heads/master/csse_covid_19_data/csse_covid_19_daily_reports/{single_date.strftime("%m-%d-%Y")}.csv' for single_date in date_range]

# Leer con Dask en paralelo
dask_dfs = [dd.read_csv(url) for url in urls]
enero_dask = dd.concat(dask_dfs, ignore_index=True).compute()

load_time_optimized = time.time() - start_time
print(f"Tiempo de carga optimizado con Dask: {load_time_optimized:.2f} segundos")

# Usamos el DataFrame optimizado para los siguientes pasos
enero = enero_dask

# %% [Celda 5] Exploración Inicial de Datos
# 1. Visualizar los primeros registros
print("Primeros 5 registros:")
print(enero.head())

# 2. Mostrar el número total de filas y columnas
print(f'\nFilas en total: {len(enero)}')
print(f'Columnas en total: {len(enero.columns)}')

# %% [Celda 6] Análisis de Tipos de Datos y Nulos
# 3. Describir tipos de datos
print("\nTipos de datos actuales:")
print(enero.dtypes)

# 4. Detectar valores nulos
print("\nValores nulos por columna:")
print(enero.isnull().sum())

# %% [Celda 7] Limpieza de Datos
# 5. Eliminar columnas irrelevantes
cols_to_drop = ['FIPS', 'Admin2', 'Lat', 'Long_', 'Combined_Key']
# Verificamos que existan antes de borrar para evitar errores si se corre la celda dos veces
enero = enero.drop(columns=[c for c in cols_to_drop if c in enero.columns])

# 6. Estandarizar nombres de columnas (snake_case)
enero.columns = enero.columns.str.lower().str.replace(' ', '_')

# 7. Homogeneizar nombres de países
enero['country_region'] = enero['country_region'].replace({'US': 'United States'})

print("Limpieza básica completada. Muestra:")
print(enero[['country_region']].head(1))

# %% [Celda 8] Corrección de Fechas
# 8. Convertir Last_Update a datetime
# Nota: El código original tenía un formato incorrecto (%Y-%M-%D).
# %M es minutos. Se corrige a inferencia automática o formato estándar.
enero['last_update'] = pd.to_datetime(enero['last_update'])

print("\nNuevos tipos de datos (Fechas corregidas):")
print(enero.dtypes)

# %% [Celda 9] Ingeniería de Características (Feature Engineering)
# 9. Crear columna active_cases
# Active = Confirmed - Deaths - Recovered
# Rellenamos NaN con 0 para evitar errores en la resta
enero['active_cases'] = (enero['confirmed'].fillna(0) - 
                         enero['deaths'].fillna(0) - 
                         enero['recovered'].fillna(0))

print("Columna 'active_cases' creada.")
print(enero.head(1))

# %% [Celda 10] Exportación de Datos
# 10. Guardar el DataFrame limpio
output_filename = 'covid_clean_enero2021.csv'
enero.to_csv(output_filename, index=False)

file_size = os.path.getsize(output_filename) / (1024 * 1024)
print(f'El tamaño del archivo {output_filename} es: {file_size:.2f} MB')

# %% [Celda 11] Optimización de Memoria (Downcasting)
print("\nIniciando optimización de memoria...")
start_time = time.time()

# Memoria antes
memory_before = enero.memory_usage(deep=True).sum() / (1024 * 1024)

# Downcast tipos de datos (Enteros)
for col in enero.select_dtypes(include=['int64']):
    enero[col] = pd.to_numeric(enero[col], downcast='integer')

# Downcast tipos de datos (Flotantes)
for col in enero.select_dtypes(include=['float64']):
    enero[col] = pd.to_numeric(enero[col], downcast='float')

dtype_time = time.time() - start_time
memory_after = enero.memory_usage(deep=True).sum() / (1024 * 1024)

print(f"Tiempo para optimización de tipos: {dtype_time:.2f} segundos")
print(f"Uso de memoria antes: {memory_before:.2f} MB")
print(f"Uso de memoria después: {memory_after:.2f} MB")
print(f"Reducción total: {memory_before - memory_after:.2f} MB")

# %% [Celda 12] Documentación (Markdown)
"""
## Documentación de Mejoras

### Optimizaciones Implementadas:
1. **Lectura Eficiente con Dask**: Se reemplazó el loop de pandas con Dask para lectura paralela de CSVs.
   - Mejora: Paralelización reduce drásticamente el tiempo de I/O al hacer peticiones HTTP simultáneas.

2. **Conversión de Tipos (Downcasting)**:
   - Se redujo el uso de memoria convirtiendo `int64` a `int32/int16` y `float64` a `float32`.
   - Esto es crucial cuando se trabaja con grandes volúmenes de datos históricos de COVID.

3. **Limpieza Vectorizada**:
   - Operaciones como `pd.to_datetime` y operaciones aritméticas sobre columnas completas son mucho más rápidas que iterar filas.
"""