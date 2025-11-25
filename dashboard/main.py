import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- IMPORTACIONES LOCALES ---
from data import load_data_simple
from metrics import calculate_growth_and_rebound

# --- Configuración de la Página ---
st.set_page_config(
    page_title="Dashboard COVID-19 (Modular)",
    page_icon="🦠",
    layout="wide"
)

# --- Ejecución: Carga de Datos ---
with st.spinner('Cargando datos históricos...'):
    df_full = load_data_simple()

if df_full.empty:
    st.error("No se pudieron cargar los datos. Verifica tu conexión a internet.")
    st.stop()

# --- UI: Título ---
st.title("📊 Dashboard COVID-19 (Histórico)")
st.markdown(f"Datos del periodo: **{df_full['date'].min().strftime('%d/%m/%Y')}** al **{df_full['date'].max().strftime('%d/%m/%Y')}**")

# --- UI: Sidebar (Filtros) ---
st.sidebar.header("Filtros")

min_date = df_full['date'].min().date()
max_date = df_full['date'].max().date()

date_input = st.sidebar.date_input(
    "Rango de Fechas",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if isinstance(date_input, tuple) and len(date_input) == 2:
    start_date, end_date = date_input
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
else:
    start_date = pd.to_datetime(min_date)
    end_date = pd.to_datetime(max_date)

available_countries = sorted(df_full['country'].unique())
default_countries = ['Mexico', 'Spain', 'Colombia', 'Argentina', 'Peru', 'Chile']
default_selection = [c for c in default_countries if c in available_countries]

selected_countries = st.sidebar.multiselect(
    "Países",
    options=available_countries,
    default=default_selection if default_selection else available_countries[:3]
)

# --- Lógica de Filtrado ---
mask = (
    (df_full['date'] >= start_date) & 
    (df_full['date'] <= end_date) & 
    (df_full['country'].isin(selected_countries))
)
df_filtered = df_full[mask]

# --- UI: Visualización Principal ---
if df_filtered.empty:
    st.warning("Selecciona al menos un país para ver los datos.")
else:
    # 1. Cálculos (Llamada al módulo metrics.py actualizado)
    timeline = df_filtered.groupby('date').sum(numeric_only=True).reset_index()
    insights, timeline_metrics = calculate_growth_and_rebound(timeline)
    
    # 2. Obtener totales para KPIs
    last_day_data = df_filtered[df_filtered['date'] == end_date]
    if last_day_data.empty: 
        last_day_data = df_filtered.loc[df_filtered.groupby('country')['date'].idxmax()]

    total_confirmed = last_day_data['confirmed'].sum()
    total_deceased = last_day_data['deceased'].sum()
    total_active = last_day_data['active'].sum()
    total_recovered = last_day_data['recovered'].sum()
    
    st.header("Resumen del Periodo")

    # Fila 1: KPIs Generales
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Confirmados", f"{total_confirmed:,.0f}")
    col2.metric("Activos", f"{total_active:,.0f}")
    col3.metric("Recuperados", f"{total_recovered:,.0f}")
    col4.metric("Fallecidos", f"{total_deceased:,.0f}")
    
    # Fila 2: Indicadores de Tendencia (Rebrote y Crecimiento)
    st.markdown("### 📈 Indicadores de Tendencia")
    col5, col6 = st.columns(2)
    
    col5.metric("Tasa de Crecimiento (Casos)", f"{insights.get('growth_rate', 0):.2%}")
    
    if insights.get('is_rebounding'):
        col6.metric("Indicador de Rebrote", "⚠️ DETECTADO", delta="- Alerta", delta_color="inverse")
    else:
        col6.metric("Indicador de Rebrote", "🟢 Estable", delta="Sin riesgo", delta_color="normal")

    # Gráficos
    st.header("Evolución Temporal")
    
    # Gráfico de Líneas Multivariable
    fig_line = px.line(
        timeline, 
        x='date', 
        y=['confirmed', 'active', 'recovered', 'deceased'], 
        title="Curva de Evolución (Comparativa)",
        labels={'value': 'Cantidad de Personas', 'variable': 'Indicador', 'date': 'Fecha'}
    )
    st.plotly_chart(fig_line, use_container_width=True)
    
    # Gráfico de Barras de Nuevos Casos con Línea de Tendencia
    if 'new_cases' in timeline_metrics.columns:
        fig_bar = px.bar(
            timeline_metrics, 
            x='date', 
            y='new_cases', 
            title="Nuevos Casos Diarios", 
            color_discrete_sequence=['#FF4B4B']
        )
        if 'new_cases_7day_avg' in timeline_metrics.columns:
             fig_bar.add_scatter(
                x=timeline_metrics['date'], 
                y=timeline_metrics['new_cases_7day_avg'], 
                mode='lines', 
                name='Media 7 días',
                line=dict(color='yellow', width=2)
            )
        st.plotly_chart(fig_bar, use_container_width=True)

    # --- NUEVA SECCIÓN: INSIGHTS DETALLADOS CON PESTAÑAS ---
    st.header("🧠 Insights Automáticos")
    
    # Creamos 3 pestañas para organizar la información
    tab1, tab2, tab3 = st.tabs(["🦠 Contagios", "⚰️ Fallecimientos", "🏥 Recuperaciones"])
    
    # --- PESTAÑA 1: CONTAGIOS ---
    with tab1:
        col_c1, col_c2 = st.columns(2)
        # Insight de Pico Histórico
        p_date = insights.get('new_cases_peak_date')
        p_val = insights.get('new_cases_peak_val', 0)
        if p_date:
            col_c1.info(f"📅 **Récord de Contagios:** El **{p_date.strftime('%d/%m/%Y')}** se registró el máximo histórico del periodo con **{p_val:,.0f}** nuevos casos.")
        
        # Insight de Tendencia (Bajada Drástica vs Rebrote vs Estable)
        if insights.get('new_cases_drop'):
            col_c2.success("📉 **Freno en Contagios:** Los casos han caído drásticamente (>50%) en los últimos días respecto a la semana anterior.")
        elif insights.get('is_rebounding'):
            col_c2.error("⚠️ **Alerta de Rebrote:** Se observa un aumento sostenido en la media de casos en los últimos días.")
        else:
            col_c2.info("⚖️ **Tendencia Estable:** No hay cambios drásticos recientes (ni subidas explosivas ni bajadas repentinas) en el ritmo de contagios.")

    # --- PESTAÑA 2: FALLECIMIENTOS ---
    with tab2:
        col_d1, col_d2 = st.columns(2)
        # Insight de Pico
        p_date = insights.get('new_deaths_peak_date')
        p_val = insights.get('new_deaths_peak_val', 0)
        if p_date:
            col_d1.error(f"⚠️ **Día Crítico:** El **{p_date.strftime('%d/%m/%Y')}** fue el día más letal con **{p_val:,.0f}** fallecidos reportados.")
        
        # Insight de Tendencia
        if insights.get('new_deaths_drop'):
            col_d2.success("🕊️ **Alivio en Mortalidad:** Las muertes diarias han disminuido significativamente en los últimos días.")
        else:
            col_d2.warning("📊 **Sin cambios drásticos:** La tendencia de mortalidad se mantiene dentro del promedio reciente.")

    # --- PESTAÑA 3: RECUPERACIONES ---
    with tab3:
        col_r1, col_r2 = st.columns(2)
        # Insight de Pico
        p_date = insights.get('new_recovered_peak_date')
        p_val = insights.get('new_recovered_peak_val', 0)
        if p_date:
            col_r1.success(f"🏥 **Récord de Altas:** El **{p_date.strftime('%d/%m/%Y')}** se registró el mayor número de recuperados diarios: **{p_val:,.0f}**.")
        
        # Insight de Tendencia
        if insights.get('new_recovered_drop'):
            col_r2.warning("📉 **Ralentización de Altas:** El ritmo de pacientes recuperados ha bajado bruscamente recientemente.")
        else:
            col_r2.info("✅ **Ritmo Constante:** Las recuperaciones mantienen un ritmo estable.")