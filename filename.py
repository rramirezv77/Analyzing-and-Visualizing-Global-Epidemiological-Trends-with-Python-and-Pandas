import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

# --- Configuración de la Página ---
st.set_page_config(
    page_title="Dashboard Interactivo",
    page_icon="📊",
    layout="wide"
)

# --- Funciones de Carga y Cálculo (con Caché) ---

@st.cache_data
def load_mock_data():
    """
    Genera datos simulados para el dashboard.
    En un caso real, aquí es donde cargarías tus datos desde un CSV o API.
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    dates = pd.date_range(start_date, end_date)
    
    data = []
    geography = {
        'América': ['USA', 'Brasil', 'Canadá', 'México'],
        'Europa': ['Alemania', 'Francia', 'España', 'Italia'],
        'Asia': ['India', 'Japón', 'China', 'Corea del Sur'],
        'África': ['Sudáfrica', 'Nigeria', 'Egipto']
    }
    
    for continent, countries in geography.items():
        for country in countries:
            # Simular una tendencia de casos
            base_confirmed = np.abs(np.random.randint(1000, 5000))
            daily_growth = np.random.rand(len(dates)) * 0.1 - 0.02 # Crecimiento con fluctuaciones
            
            confirmed = base_confirmed + np.cumsum(np.random.randint(50, 500, len(dates)) * (1 + daily_growth).cumprod())
            
            for i, date in enumerate(dates):
                conf = int(confirmed[i])
                # Asegurar que los datos sean consistentes
                recovered = int(conf * np.random.uniform(0.7, 0.9)) # 70-90% de recuperados
                deceased = int(conf * np.random.uniform(0.01, 0.05)) # 1-5% de fallecidos
                active = conf - recovered - deceased
                
                # Asegurarse que activo no sea negativo
                if active < 0:
                    active = 0
                    recovered = conf - deceased
                    
                data.append({
                    'date': date,
                    'continent': continent,
                    'country': country,
                    'confirmed': conf,
                    'active': active,
                    'recovered': recovered,
                    'deceased': deceased
                })
    
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    return df

def calculate_growth_and_rebound(df_grouped):
    """
    Calcula la tasa de crecimiento y el indicador de rebrote.
    """
    if df_grouped.empty or len(df_grouped) < 10:
        return 0, False, pd.DataFrame()

    # 1. Calcular nuevos casos diarios
    df_grouped = df_grouped.sort_values('date')
    df_grouped['new_cases'] = df_grouped['confirmed'].diff().fillna(0)
    
    # 2. Tasa de Crecimiento (media móvil de 7 días del % de cambio)
    daily_growth_rate = df_grouped['new_cases'].pct_change().fillna(0).replace([np.inf, -np.inf], 0)
    avg_growth_rate = daily_growth_rate.rolling(window=7).mean().iloc[-1]
    
    # 3. Indicador de Rebrote (media móvil de 7 días de nuevos casos)
    df_grouped['new_cases_7day_avg'] = df_grouped['new_cases'].rolling(window=7).mean().fillna(0)
    
    # Un "rebrote" se define si la media de 7 días ha crecido en los últimos 3 días consecutivos
    avg_diff = df_grouped['new_cases_7day_avg'].diff().fillna(0)
    is_rebounding = (avg_diff.iloc[-3:] > 0).all() and (len(avg_diff) > 3)
    
    return avg_growth_rate, is_rebounding, df_grouped

# --- Carga Inicial de Datos ---
df_full = load_mock_data()

# --- Título del Dashboard ---
st.title("📊 Dashboard de Seguimiento Interactivo")

# --- Barra Lateral (Filtros) ---
st.sidebar.header("Filtros del Dashboard")

# 1. Filtro de Rango de Fechas
min_date = df_full['date'].min().date()
max_date = df_full['date'].max().date()
date_range = st.sidebar.date_input(
    "Selecciona Rango de Fechas",
    value=(max_date - timedelta(days=90), max_date), # Default: últimos 90 días
    min_value=min_date,
    max_value=max_date,
    format="DD/MM/YYYY"
)

# Manejar el rango de fechas (date_input devuelve una tupla)
if len(date_range) == 2:
    start_date, end_date = date_range
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
else:
    # Caso por defecto si el usuario borra una fecha
    start_date = pd.to_datetime(min_date)
    end_date = pd.to_datetime(max_date)

# 2. Filtro de Continente
all_continents = df_full['continent'].unique()
selected_continents = st.sidebar.multiselect(
    "Selecciona Continente(s)",
    options=all_continents,
    default=all_continents # Default: todos seleccionados
)

# 3. Filtro de País (dependiente del continente)
if not selected_continents:
    available_countries = []
else:
    available_countries = df_full[df_full['continent'].isin(selected_continents)]['country'].unique()

selected_countries = st.sidebar.multiselect(
    "Selecciona País(es)",
    options=available_countries,
    default=available_countries # Default: todos los disponibles
)

# --- Filtrado de Datos (Lógica Principal) ---
if not selected_continents or not selected_countries:
    df_filtered = pd.DataFrame(columns=df_full.columns)
else:
    df_filtered = df_full[
        (df_full['date'] >= start_date) &
        (df_full['date'] <= end_date) &
        (df_full['continent'].isin(selected_continents)) &
        (df_full['country'].isin(selected_countries))
    ]

# --- Cuerpo Principal del Dashboard ---

if df_filtered.empty:
    st.warning("No se encontraron datos para los filtros seleccionados. Por favor, ajuste su selección.")
else:
    # --- 1. Indicadores Principales (KPIs) ---
    st.header("Indicadores Principales (KPIs)")
    
    # Obtener los datos más recientes para los KPIs
    df_latest = df_filtered.loc[df_filtered.groupby('country')['date'].idxmax()]
    
    # Obtener datos del día anterior para el delta
    prev_date = df_filtered['date'].max() - timedelta(days=1)
    df_prev = df_filtered[df_filtered['date'] == prev_date]
    if not df_prev.empty:
        df_prev = df_prev.loc[df_prev.groupby('country')['date'].idxmax()]
    
    # Calcular totales
    total_confirmed = df_latest['confirmed'].sum()
    total_active = df_latest['active'].sum()
    total_recovered = df_latest['recovered'].sum()
    total_deceased = df_latest['deceased'].sum()
    
    # Calcular deltas
    delta_confirmed = total_confirmed - df_prev['confirmed'].sum() if not df_prev.empty else 0
    delta_active = total_active - df_prev['active'].sum() if not df_prev.empty else 0
    delta_recovered = total_recovered - df_prev['recovered'].sum() if not df_prev.empty else 0
    delta_deceased = total_deceased - df_prev['deceased'].sum() if not df_prev.empty else 0

    # Mostrar KPIs en columnas
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Casos Confirmados", f"{total_confirmed:,.0f}", f"{delta_confirmed:,.0f} (vs día ant.)", delta_color="inverse")
    col2.metric("Casos Activos", f"{total_active:,.0f}", f"{delta_active:,.0f} (vs día ant.)")
    col3.metric("Recuperados", f"{total_recovered:,.0f}", f"{delta_recovered:,.0f} (vs día ant.)")
    col4.metric("Fallecidos", f"{total_deceased:,.0f}", f"{delta_deceased:,.0f} (vs día ant.)", delta_color="inverse")

    # --- 2. Tasa de Crecimiento e Indicador de Rebrote ---
    # Agrupar datos por fecha (sumando todos los países seleccionados)
    df_grouped_by_date = df_filtered.groupby('date').sum(numeric_only=True).reset_index()
    
    growth_rate, is_rebounding, df_with_avg = calculate_growth_and_rebound(df_grouped_by_date)


    # --- 3. Visualizaciones Dinámicas ---
    st.header("Visualizaciones Dinámicas")
    
    col_viz1, col_viz2 = st.columns(2)
    
    with col_viz1:
        st.subheader("Evolución de Casos Confirmados")
        fig_line = px.line(
            df_grouped_by_date, 
            x='date', 
            y='confirmed', 
            title="Total de Casos Confirmados en el Tiempo",
            labels={'date': 'Fecha', 'confirmed': 'Casos Confirmados'}
        )
        st.plotly_chart(fig_line, use_container_width=True)

        st.subheader("Nuevos Casos Diarios (con media de 7 días)")
        fig_new_cases = px.bar(
            df_with_avg, 
            x='date', 
            y='new_cases', 
            title="Nuevos Casos Diarios",
            labels={'date': 'Fecha', 'new_cases': 'Nuevos Casos'}
        )
        # Añadir línea de media móvil
        fig_new_cases.add_scatter(
            x=df_with_avg['date'], 
            y=df_with_avg['new_cases_7day_avg'], 
            mode='lines', 
            name='Media Móvil (7 días)',
            line=dict(color='orange')
        )
        st.plotly_chart(fig_new_cases, use_container_width=True)

    with col_viz2:
        st.subheader("Distribución por País (Último Día)")
        df_latest_sorted = df_latest.sort_values('confirmed', ascending=False)
        fig_bar = px.bar(
            df_latest_sorted,
            x='country',
            y='confirmed',
            color='continent',
            title="Casos Confirmados por País (Último día del rango)",
            labels={'country': 'País', 'confirmed': 'Casos Confirmados', 'continent': 'Continente'}
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        
        st.subheader("Composición de Casos (Total del Periodo)")
        totals = {
            'Activos': total_active,
            'Recuperados': total_recovered,
            'Fallecidos': total_deceased
        }
        df_pie = pd.DataFrame(totals.items(), columns=['Tipo', 'Total'])
        
        fig_pie = px.pie(
            df_pie,
            names='Tipo',
            values='Total',
            title='Proporción de Casos Activos vs. Recuperados vs. Fallecidos'
        )
        st.plotly_chart(fig_pie, use_container_width=True)


    # --- 4. Sección de "Insights" y Conclusiones ---
    st.header("Insights Automáticos y Conclusiones")
    st.info(f"Mostrando datos desde **{start_date.strftime('%d/%m/%Y')}** hasta **{end_date.strftime('%d/%m/%Y')}**.")
    
    col_ins1, col_ins2 = st.columns(2)
    
    with col_ins1:
        st.subheader("Indicador de Rebrote")
        if is_rebounding:
            st.error("🔴 **Positivo para Rebrote**")
            st.write("La media móvil de 7 días de nuevos casos ha mostrado un incremento sostenido en los últimos 3 días.")
        else:
            st.success("🟢 **Indicador de Rebrote Negativo**")
            st.write("La tendencia de nuevos casos parece estable o en disminución.")
            
        st.subheader("Tasa de Crecimiento")
        st.metric("Tasa de Crecimiento (Media 7d de % cambio)", f"{growth_rate:.2%}")
        st.caption("Esta métrica indica el cambio porcentual promedio de nuevos casos en los últimos 7 días.")

    with col_ins2:
        st.subheader("Datos Destacados")
        # País con más casos
        if not df_latest.empty:
            top_country = df_latest.sort_values('confirmed', ascending=False).iloc[0]
            st.write(f"🌍 **País con más casos:** {top_country['country']} ({top_country['confirmed']:,.0f} casos).")
        
        # Día con pico de nuevos casos
        if not df_with_avg.empty and 'new_cases' in df_with_avg.columns:
            peak_day = df_with_avg.loc[df_with_avg['new_cases'].idxmax()]
            st.write(f"📈 **Pico de nuevos casos:** {peak_day['new_cases']:,.0f} casos el {peak_day['date'].strftime('%d/%m/%Y')}.")