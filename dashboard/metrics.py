import pandas as pd
import numpy as np

def calculate_growth_and_rebound(df_grouped):
    """
    Calcula métricas avanzadas, picos y tendencias para Casos, Fallecidos y Recuperados.
    Devuelve:
        - insights (dict): Diccionario con banderas y valores clave.
        - df_grouped (DataFrame): DataFrame enriquecido con datos diarios.
    """
    # Validación básica: si no hay suficientes datos, retornamos vacío
    if df_grouped.empty or len(df_grouped) < 5:
        return {}, pd.DataFrame()

    # Aseguramos el orden cronológico para los cálculos de diff y rolling
    df_grouped = df_grouped.sort_values('date')
    
    # --- 1. CÁLCULO DE DATOS DIARIOS (Diff) ---
    # Calculamos la diferencia diaria (hoy - ayer) para obtener los "Nuevos" casos/muertes/recuperados
    cols_to_diff = {'confirmed': 'new_cases', 'deceased': 'new_deaths', 'recovered': 'new_recovered'}
    
    for col_acum, col_daily in cols_to_diff.items():
        # Verificamos que la columna acumulada exista
        if col_acum in df_grouped.columns:
            df_grouped[col_daily] = df_grouped[col_acum].diff().fillna(0)
            # Limpiamos valores negativos que a veces aparecen por correcciones en los datos oficiales
            df_grouped[col_daily] = df_grouped[col_daily].clip(lower=0)
        else:
            df_grouped[col_daily] = 0

    # --- 2. CÁLCULO DE PICOS (Máximos Históricos del Periodo) ---
    # Buscamos qué día tuvo el valor más alto para cada métrica
    peaks = {}
    for metric in ['new_cases', 'new_deaths', 'new_recovered']:
        if metric in df_grouped.columns:
            max_idx = df_grouped[metric].idxmax()
            peaks[f'{metric}_peak_date'] = df_grouped.loc[max_idx, 'date']
            peaks[f'{metric}_peak_val'] = df_grouped.loc[max_idx, metric]

    # --- 3. CÁLCULO DE TENDENCIAS (Crecimiento y Rebrote) ---
    # Tasa de Crecimiento de Casos (Media móvil de 7 días del cambio porcentual)
    if 'new_cases' in df_grouped.columns:
        daily_growth_rate = df_grouped['new_cases'].pct_change().fillna(0).replace([np.inf, -np.inf], 0)
        avg_growth_rate = daily_growth_rate.rolling(window=7).mean().iloc[-1]
        
        # Detección de Rebrote:
        # Calculamos la media móvil de 7 días de los nuevos casos
        df_grouped['new_cases_7day_avg'] = df_grouped['new_cases'].rolling(window=7).mean().fillna(0)
        # Vemos si esa media ha subido consecutivamente en los últimos 3 días
        avg_diff = df_grouped['new_cases_7day_avg'].diff().fillna(0)
        is_rebounding = (avg_diff.iloc[-3:] > 0).all() and (len(avg_diff) > 3)
    else:
        avg_growth_rate = 0
        is_rebounding = False

    # --- 4. DETECCIÓN DE BAJADAS DRÁSTICAS (Drops) ---
    # Comparamos la situación actual (últimos 3 días) vs la situación previa (semana anterior)
    drops = {}
    for metric in ['new_cases', 'new_deaths', 'new_recovered']:
        if metric in df_grouped.columns:
            # Promedio de los últimos 3 días
            recent_avg = df_grouped[metric].iloc[-3:].mean()
            # Promedio de los 7 días anteriores a esos 3
            prev_avg = df_grouped[metric].iloc[-10:-3].mean()
            
            # Si la media reciente es MENOR al 50% de la media anterior, consideramos que hubo un "frenazo"
            # (Solo si la media anterior era relevante, > 10 casos, para evitar ruido con números pequeños)
            if prev_avg > 10 and recent_avg < (prev_avg * 0.5):
                drops[f'{metric}_drop'] = True
            else:
                drops[f'{metric}_drop'] = False

    # --- 5. EMPAQUETADO DE RESULTADOS ---
    insights = {
        'growth_rate': avg_growth_rate,
        'is_rebounding': is_rebounding,
        **peaks, # Incluye todas las fechas y valores de picos
        **drops  # Incluye todas las banderas de bajada drástica
    }
    
    return insights, df_grouped