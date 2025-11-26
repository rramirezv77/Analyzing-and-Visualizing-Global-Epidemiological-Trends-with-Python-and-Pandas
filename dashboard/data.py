import streamlit as st
import pandas as pd
from datetime import datetime

# Mantenemos el caché aquí para que Streamlit no recargue los datos innecesariamente
@st.cache_data(ttl=3600)
def load_data_simple():
    """
    Carga datos desde el repositorio de JHU, inyecta fechas, corrige columnas y ASIGNA CONTINENTES.
    """
    # 1. Definir rango de fechas
    start_date = '2020-01-22' 
    end_date = '2020-03-30'
    
    date_range = pd.date_range(start=start_date, end=end_date)
    
    # UI de carga (Feedback visual)
    status_text = st.empty()
    progress_bar = st.progress(0)
    status_text.text(f"Descargando datos secuencialmente desde {start_date} hasta {end_date}...")
    
    df_list = []
    total_days = len(date_range)
    
    # 2. Bucle de descarga
    for i, single_date in enumerate(date_range):
        progress_bar.progress((i + 1) / total_days)
        
        url = f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{single_date.strftime("%m-%d-%Y")}.csv'
        
        try:
            temp_df = pd.read_csv(url)
            temp_df['date'] = single_date # Inyección crítica de fecha
            df_list.append(temp_df)
        except Exception:
            continue # Saltar fechas con errores

    status_text.text("Procesando y consolidando datos...")
    progress_bar.empty()

    if not df_list:
        return pd.DataFrame()
        
    # 3. Concatenación y Limpieza
    df_final = pd.concat(df_list, ignore_index=True)
    
    rename_map = {
        'Country_Region': 'country',
        'Country/Region': 'country',
        'Confirmed': 'confirmed',
        'Deaths': 'deceased',
        'Recovered': 'recovered',
        'Active': 'active'
    }
    df_final = df_final.rename(columns=rename_map)
    
    # Corrección de duplicados (Merge de Country_Region y Country/Region)
    if df_final.columns.duplicated().any():
        duplicated_cols = df_final.columns[df_final.columns.duplicated()].unique()
        for col in duplicated_cols:
            cols_to_merge = df_final[col]
            merged_col = cols_to_merge.bfill(axis=1).iloc[:, 0]
            df_final = df_final.loc[:, df_final.columns != col]
            df_final[col] = merged_col

    cols_needed = ['country', 'confirmed', 'deceased', 'recovered', 'active', 'date']
    cols_to_use = [c for c in cols_needed if c in df_final.columns]
    df_final = df_final[cols_to_use]

    # Agrupación inicial por País y Fecha
    df_grouped = df_final.groupby(['country', 'date']).sum(numeric_only=True).reset_index()
    
    # Recálculo forzoso de Activos
    if 'deceased' not in df_grouped.columns: df_grouped['deceased'] = 0
    if 'recovered' not in df_grouped.columns: df_grouped['recovered'] = 0
        
    df_grouped['active'] = df_grouped['confirmed'] - df_grouped['deceased'] - df_grouped['recovered']
    df_grouped['active'] = df_grouped['active'].clip(lower=0)
    
    # --- ASIGNACIÓN DE CONTINENTES ---
    # Diccionario manual simple para mapear países comunes a continentes
    continent_map = {
        'US': 'North America', 'Canada': 'North America', 'Mexico': 'North America',
        'Brazil': 'South America', 'Argentina': 'South America', 'Chile': 'South America',
        'Colombia': 'South America', 'Peru': 'South America',
        'Spain': 'Europe', 'Italy': 'Europe', 'France': 'Europe', 'Germany': 'Europe',
        'United Kingdom': 'Europe', 'Russia': 'Europe',
        'China': 'Asia', 'Japan': 'Asia', 'India': 'Asia', 'Korea, South': 'Asia',
        'Australia': 'Oceania',
        'South Africa': 'Africa', 'Egypt': 'Africa', 'Nigeria': 'Africa'
    }
    
    # Función para aplicar el mapa, con valor por defecto 'Other'
    def get_continent(country):
        return continent_map.get(country, 'Other')

    df_grouped['continent'] = df_grouped['country'].apply(get_continent)
    
    status_text.empty()
    return df_grouped