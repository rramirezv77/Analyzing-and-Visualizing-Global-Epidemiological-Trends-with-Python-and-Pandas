import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data import load_data_simple
from metrics import calculate_growth_and_rebound
import ui

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="COVID Dashboard", page_icon="📊", layout="wide")

# 1. Inicializar Estado de Navegación
query_params = st.query_params
current_page = query_params.get("page", "dashboard")

# 2. Estilos y Sidebar
ui.setup_page_style()
ui.render_sidebar()

# 3. Carga de Datos Global
with st.spinner('Cargando sistema...'):
    df_full = load_data_simple()

if df_full.empty:
    st.error("Error al cargar los datos históricos. Por favor, revise su conexión.")
    st.stop()

# --- CONTROLADOR DE VISTAS ---

if current_page == "dashboard":
    # ==========================================
    # VISTA 1: DASHBOARD
    # ==========================================
    
    ui.render_top_banner(title="ANÁLISIS Y VISUALIZACIÓN DE TENDENCIAS EPIDEMIOLÓGICAS GLOBALES")
    
    # Filtros Dashboard
    with st.container():
        c1, c2, c3 = st.columns([1, 1, 2], gap="small")
        
        # Filtro de Rango de Fechas
        with c1:
            min_d, max_d = df_full['date'].min().date(), df_full['date'].max().date()
            d_input = st.date_input("Rango de Fechas", value=(min_d, max_d), min_value=min_d, max_value=max_d)
            start, end = (pd.to_datetime(d_input[0]), pd.to_datetime(d_input[1])) if isinstance(d_input, tuple) and len(d_input) == 2 else (pd.to_datetime(min_d), pd.to_datetime(max_d))
        
        # Filtro de Continentes
        with c2:
            avail_continents = sorted(df_full['continent'].unique())
            sel_continents = st.multiselect("Filtrar Continentes", options=avail_continents, default=[]) 
        
        # Filtro de Países (Dependiente de Continente)
        with c3:
            # Determina el subconjunto de países disponibles
            if sel_continents:
                filtered_countries = df_full[df_full['continent'].isin(sel_continents)]['country'].unique()
            else:
                filtered_countries = df_full['country'].unique()
            avail_countries = sorted(filtered_countries)
            
            # 2. Multiselect
            sel_countries = st.multiselect("Filtrar Países", options=avail_countries, default=[])

    # --- Lógica de Filtrado ---
    
    # País/Continente
    if sel_countries:
        country_mask = df_full['country'].isin(sel_countries)
    elif sel_continents:
        country_mask = df_full['continent'].isin(sel_continents)
    else:
        # Si no hay filtros de ubicación, selecciona todos los datos 
        country_mask = pd.Series(True, index=df_full.index)

    # Máscara de Fecha
    date_mask = (df_full['date'] >= start) & (df_full['date'] <= end)
    
    # Aplicar Filtros
    mask = date_mask & country_mask
    df_filtered = df_full[mask]

    # Validación 
    if df_filtered.empty:
        st.warning("No hay datos disponibles para la combinación de filtros seleccionada.")
        st.stop()

    # --- Cálculos y Renderizado ---
    timeline = df_filtered.groupby('date').sum(numeric_only=True).reset_index()
    insights, timeline_metrics = calculate_growth_and_rebound(timeline)
    last_day = timeline.iloc[-1]

    # Iconos SVG 
    icon_users = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />'
    icon_chart = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />'
    icon_check = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />'
    icon_alert = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6" />'
    icon_trend_up = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />'
    icon_trend_flat = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h14" />'

    # FILA 1: MÉTRICAS
    st.markdown("<div class='mb-6'></div>", unsafe_allow_html=True)
    k1, k2, k3, k4 = st.columns(4, gap="large")
    with k1: ui.metric_card("Confirmados", f"{last_day['confirmed']:,.0f}", "Total Acumulado", icon_users, "purple")
    with k2: ui.metric_card("Activos", f"{last_day['active']:,.0f}", "Casos Actuales", icon_chart, "blue")
    with k3: ui.metric_card("Recuperados", f"{last_day['recovered']:,.0f}", "Alta Médica", icon_check, "green")
    with k4: ui.metric_card("Fallecidos", f"{last_day['deceased']:,.0f}", "Total Bajas", icon_alert, "red")

    # FILA 2: INSIGHTS Y ALERTA
    st.markdown("<div class='mb-6'></div>", unsafe_allow_html=True)
    i1, i2, i3 = st.columns([1, 1, 2], gap="large")
    
    peak_val = insights.get('new_cases_peak_val', 0)
    is_rebound = insights.get('is_rebounding', False)
    growth = insights.get('growth_rate', 0)

    with i1: ui.metric_card("Pico Máximo", f"{peak_val:,.0f}", "Casos/Día", icon_alert, "yellow")
    with i2:
        trend_icon = icon_trend_up if growth > 0 else icon_trend_flat
        trend_color = "red" if is_rebound else "green"
        trend_text = "▲ ALZA" if is_rebound else "▼ ESTABLE"
        ui.metric_card("Tendencia", trend_text, f"{growth:.1%} (7d)", trend_icon, trend_color)
    with i3:
        if is_rebound: ui.alert_card(is_rebound)
        else: st.write("")

    # FILA 3: GRÁFICOS
    st.markdown("<div class='mb-6'></div>", unsafe_allow_html=True)
    g1, g2 = st.columns(2, gap="large")
    CHART_HEIGHT = 400

    with g1:
        fig = px.area(timeline, x='date', y=['recovered', 'active'], 
                      color_discrete_map={'recovered': '#34d399', 'active': '#60a5fa'})
        fig.add_trace(go.Scatter(x=timeline['date'], y=timeline['deceased'], line=dict(color='#f87171', width=2), name='deceased'))
        
        fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, title=None))
        ui.render_chart_card("Curva de Evolución Temporal", fig, height=CHART_HEIGHT)

    with g2:
        fig_bar = px.bar(timeline_metrics, x='date', y='new_cases')
        fig_bar.update_traces(marker_color='#8b5cf6')
        ui.render_chart_card("Nuevos Casos Diarios", fig_bar, height=CHART_HEIGHT)

elif current_page == "table":
    # ==========================================
    # VISTA 2: TABLA DE DATOS
    # ==========================================
    
    ui.render_top_banner(title="REGISTRO DETALLADO DE DATOS EPIDEMIOLÓGICOS")
    
    with st.container():
        t1, t2 = st.columns(2)
        with t1: search_country = st.text_input("🔍 Buscar País", placeholder="Escribe para filtrar...")
        with t2: sort_by = st.selectbox("Ordenar por", ["date", "confirmed", "active", "deceased"], index=0)
    
    df_table = df_full.copy()
    if search_country:
        df_table = df_table[df_table['country'].str.contains(search_country, case=False, na=False)]
    df_table = df_table.sort_values(by=sort_by, ascending=False)
    
    st.markdown("<div class='mb-4'></div>", unsafe_allow_html=True)
    st.markdown(f"""<div class="bg-white shadow-sm rounded-xl border border-gray-100 p-6"><h3 class="font-bold text-lg text-gray-800 mb-4">Registros Detallados ({len(df_table):,.0f} filas)</h3></div>""", unsafe_allow_html=True)
    st.dataframe(df_table, use_container_width=True, hide_index=True, height=600)