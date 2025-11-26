import pandas as pd
import numpy as np

def calculate_growth_and_rebound(df_grouped):
    """
    Calcula métricas avanzadas incluyendo tendencias de Fallecidos y Recuperados.
    """
    empty_df = pd.DataFrame(columns=['date', 'new_cases', 'new_deaths', 'new_recovered', 'new_cases_7day_avg'])
    
    if df_grouped.empty:
        return {}, empty_df

    df_grouped = df_grouped.sort_values('date')
    
    # --- 1. CÁLCULO DE DATOS DIARIOS (Nuevos Casos, Muertes, Recuperados) ---
    cols = {'confirmed': 'new_cases', 'deceased': 'new_deaths', 'recovered': 'new_recovered'}
    for c_sum, c_new in cols.items():
        if c_sum in df_grouped.columns:
            df_grouped[c_new] = df_grouped[c_sum].diff().fillna(0).clip(lower=0)
        else:
            df_grouped[c_new] = 0
            
    # --- CÁLCULO DE MEDIAS MÓVILES  ---
    df_grouped['new_deaths_7d'] = df_grouped['new_deaths'].rolling(window=7).mean().fillna(0)
    df_grouped['new_recovered_7d'] = df_grouped['new_recovered'].rolling(window=7).mean().fillna(0)

    # no calculara nada con menos de 5 datos
    if len(df_grouped) < 5:
        return {}, df_grouped

    # --- 2. CÁLCULO DE PICOS  ---
    peaks = {}
    for metric in ['new_cases', 'new_deaths', 'new_recovered']:
        if metric in df_grouped.columns:
            max_idx = df_grouped[metric].idxmax()
            peaks[f'{metric}_peak_date'] = df_grouped.loc[max_idx, 'date']
            peaks[f'{metric}_peak_val'] = df_grouped.loc[max_idx, metric]

    # --- 3. TENDENCIAS AVANZADAS Y BANDERAS ---
    
    # Tasa de Crecimiento
    if 'new_cases' in df_grouped.columns:
        growth = df_grouped['new_cases'].pct_change().replace([np.inf, -np.inf], 0).fillna(0)
        avg_growth = growth.rolling(window=7).mean().iloc[-1]
        
        df_grouped['new_cases_7day_avg'] = df_grouped['new_cases'].rolling(window=7).mean().fillna(0)
        diffs = df_grouped['new_cases_7day_avg'].diff().fillna(0)
        is_rebound = (diffs.iloc[-3:] > 0).all() and len(diffs) > 3
    else:
        avg_growth = 0
        is_rebound = False

    # 3.1.Muertes 
    avg_period_deaths = df_grouped['new_deaths_7d'].mean()
    last_7d_deaths = df_grouped['new_deaths_7d'].iloc[-1]
    
    high_deaths = last_7d_deaths > avg_period_deaths * 1.5  # 50% por encima del promedio
    low_deaths = last_7d_deaths < avg_period_deaths * 0.5   # 50% por debajo del promedio

    # 3.2. Recuperación 
    avg_period_recovered = df_grouped['new_recovered_7d'].mean()
    last_7d_recovered = df_grouped['new_recovered_7d'].iloc[-1]
    
    high_recovered = last_7d_recovered > avg_period_recovered * 1.5
    low_recovered = last_7d_recovered < avg_period_recovered * 0.5

    # --- 4. EMPAQUETADO FINAL ---
    insights = {
        'growth_rate': avg_growth,
        'is_rebounding': is_rebound,
        'high_deaths': high_deaths,
        'low_deaths': low_deaths,
        'high_recovered': high_recovered,
        'low_recovered': low_recovered,
        **peaks
    }
    
    return insights, df_grouped