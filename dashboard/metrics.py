import pandas as pd
import numpy as np

def calculate_growth_and_rebound(df_grouped):
    """
    Calcula métricas avanzadas.
    CORRECCIÓN: Siempre devuelve el DataFrame con columnas calculadas, 
    incluso si hay pocos datos para calcular tendencias complejas.
    """
    # Si está vacío de entrada, devolvemos estructura vacía pero CON columnas para evitar error de Plotly
    if df_grouped.empty:
        return {}, pd.DataFrame(columns=['date', 'new_cases', 'new_deaths', 'new_recovered'])

    # Aseguramos el orden cronológico
    df_grouped = df_grouped.sort_values('date')
    
    # --- 1. CÁLCULO DE DATOS DIARIOS (Siempre se hace) ---
    cols_to_diff = {'confirmed': 'new_cases', 'deceased': 'new_deaths', 'recovered': 'new_recovered'}
    
    for col_acum, col_daily in cols_to_diff.items():
        if col_acum in df_grouped.columns:
            df_grouped[col_daily] = df_grouped[col_acum].diff().fillna(0)
            df_grouped[col_daily] = df_grouped[col_daily].clip(lower=0)
        else:
            df_grouped[col_daily] = 0

    # --- VALIDACIÓN DE CANTIDAD DE DATOS ---
    # Si hay menos de 5 días, no podemos calcular tendencias fiables (growth/rebound),
    # pero SÍ podemos devolver los datos diarios calculados arriba para los gráficos.
    if len(df_grouped) < 5:
        return {}, df_grouped

    # --- 2. CÁLCULO DE PICOS ---
    peaks = {}
    for metric in ['new_cases', 'new_deaths', 'new_recovered']:
        if metric in df_grouped.columns:
            max_idx = df_grouped[metric].idxmax()
            peaks[f'{metric}_peak_date'] = df_grouped.loc[max_idx, 'date']
            peaks[f'{metric}_peak_val'] = df_grouped.loc[max_idx, metric]

    # --- 3. TENDENCIAS ---
    if 'new_cases' in df_grouped.columns:
        # pct_change puede dar inf si empieza en 0, reemplazamos
        daily_growth_rate = df_grouped['new_cases'].pct_change().replace([np.inf, -np.inf], 0).fillna(0)
        avg_growth_rate = daily_growth_rate.rolling(window=7).mean().iloc[-1]
        
        # Rebrote
        df_grouped['new_cases_7day_avg'] = df_grouped['new_cases'].rolling(window=7).mean().fillna(0)
        avg_diff = df_grouped['new_cases_7day_avg'].diff().fillna(0)
        is_rebounding = (avg_diff.iloc[-3:] > 0).all() and (len(avg_diff) > 3)
    else:
        avg_growth_rate = 0
        is_rebounding = False

    # --- 4. EMPAQUETADO ---
    insights = {
        'growth_rate': avg_growth_rate,
        'is_rebounding': is_rebounding,
        **peaks
    }
    
    return insights, df_grouped