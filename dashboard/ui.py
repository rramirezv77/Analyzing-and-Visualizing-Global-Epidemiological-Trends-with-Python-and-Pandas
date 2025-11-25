import streamlit as st
import streamlit.components.v1 as components

# --- CONSTANTES DE COLOR ---
BG_COLOR = "#f3f4f6"   
CARD_COLOR = "#ffffff" 
TEXT_COLOR = "#1f2937" 

def setup_page_style():
    """Inyecta CSS y Tailwind."""
    st.markdown("""
    <script src="https://cdn.tailwindcss.com"></script>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <style>
        html, body, [class*="css"] {{
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif !important;
        }}
        .stApp {{
            background-color: {BG_COLOR};
            color: {TEXT_COLOR};
        }}
        
        .js-plotly-plot, .plot-container {{
            height: 100% !important;
            width: 100% !important;
        }}
        
        header {{ visibility: hidden; }}
        .stDeployButton, div[data-testid="stDecoration"] {{ display: none; }}
        
        .block-container {{
            padding-left: 6rem !important;
            padding-top: 1rem !important;
            padding-right: 2rem !important;
            padding-bottom: 2rem !important;
            max-width: 100%;
        }}
        
        div[data-baseweb="select"] > div, 
        div[data-baseweb="input"] > div, 
        div[data-baseweb="base-input"] {{
            background-color: white !important;
            border: 1px solid #e5e7eb !important;
            color: {TEXT_COLOR} !important;
            border-radius: 0.5rem;
        }}
        div[data-baseweb="select"] span {{ color: {TEXT_COLOR} !important; }}
        
        span[data-baseweb="tag"] {{ 
            background-color: #ef4444 !important; 
        }}
        span[data-baseweb="tag"] span {{
            color: white !important; 
        }}
        span[data-baseweb="tag"] svg {{
            fill: white !important;
            color: white !important;
        }}
        
        div[data-testid="column"] > div > div[data-testid="stVerticalBlock"] {{
            gap: 1rem !important;
        }}
    </style>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Sidebar fijo."""
    sidebar_html = """
    <aside style="position:fixed; top:0; left:0; z-index:50; height:100vh; width:5rem; background-color:#1f2937; display:flex; flex-direction:column; align-items:center; box-shadow: 2px 0 5px rgba(0,0,0,0.1);">
        <a href="#" style="display:flex; justify-content:center; align-items:center; height:5rem; width:5rem; background-color:#7c3aed;">
            <svg fill="none" viewBox="0 0 64 64" style="height:2.5rem; width:2.5rem;">
                <path d="M32 14.2c-8 0-12.9 4-14.9 11.9 3-4 6.4-5.6 10.4-4.5 2.3.6 4 2.3 5.7 4 2.9 3 6.3 6.4 13.7 6.4 7.9 0 12.9-4 14.8-11.9-3 4-6.4 5.5-10.3 4.4-2.3-.5-4-2.2-5.7-4-3-3-6.3-6.3-13.7-6.3zM17.1 32C9.2 32 4.2 36 2.3 43.9c3-4 6.4-5.5 10.3-4.4 2.3.5 4 2.2 5.7 4 3 3 6.3 6.3 13.7 6.3 8 0 12.9-4 14.9-11.9-3 4-6.4 5.6-10.4 4.5-2.3-.6-4-2.3-5.7-4-2.9-3-6.3-6.4-13.7-6.4z" fill="#fff"/>
            </svg>
        </a>
        <div style="flex-grow:1; display:flex; flex-direction:column; width:100%; align-items:center; padding-top:1.5rem; gap:1rem;">
            <div style="display:flex; justify-content:center; align-items:center; padding:0.75rem; color:#7c3aed; background-color:white; border-radius:0.5rem; width:3rem; height:3rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <svg fill="none" viewBox="0 0 24 24" stroke="currentColor" style="height:1.5rem; width:1.5rem;">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
            </div>
        </div>
    </aside>
    """
    st.markdown(sidebar_html, unsafe_allow_html=True)

def render_header(title="Dashboard", subtitle="COVID-19 Global Tracking"):
    header_html = f"""
    <header class="flex items-center justify-between h-20 px-6 bg-white border-b border-gray-200 mb-8 rounded-xl shadow-sm" style="background-color:white; border-radius:0.75rem; margin-bottom:2rem; padding:0 1.5rem; display:flex; align-items:center; justify-content:space-between;">
        <div class="flex flex-col">
            <h1 class="text-2xl font-bold text-gray-800 m-0" style="color:#1f2937; font-size:1.5rem; font-weight:700; margin:0;">{title}</h1>
            <span class="text-sm text-gray-500" style="color:#6b7280; font-size:0.875rem;">{subtitle}</span>
        </div>
        <div class="flex items-center space-x-4">
            <div class="h-10 w-10 bg-purple-100 rounded-full flex items-center justify-center text-purple-600 font-bold border border-purple-200" style="background-color:#f3e8ff; color:#7c3aed; display:flex; align-items:center; justify-content:center;">
                AU
            </div>
        </div>
    </header>
    """
    st.markdown(header_html, unsafe_allow_html=True)

def metric_card(title, value, subtitle, icon_path, color_theme="purple"):
    colors = {
        "purple": ("#f3e8ff", "#7c3aed"),
        "green": ("#dcfce7", "#16a34a"),
        "red": ("#fee2e2", "#dc2626"),
        "blue": ("#dbeafe", "#2563eb"),
        "yellow": ("#fef9c3", "#ca8a04"),
    }
    bg_hex, text_hex = colors.get(color_theme, colors["purple"])
    
    html = f"""
    <div style="background-color:white; padding:1.5rem; border-radius:0.75rem; display:flex; align-items:center; box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05); border:1px solid #e5e7eb; height:100%;">
        <div style="background-color:{bg_hex}; color:{text_hex}; height:4rem; width:4rem; border-radius:9999px; margin-right:1rem; display:inline-flex; align-items:center; justify-content:center; flex-shrink:0;">
            <svg aria-hidden="true" fill="none" viewBox="0 0 24 24" stroke="currentColor" style="height:2rem; width:2rem;">
                {icon_path}
            </svg>
        </div>
        <div style="flex-grow: 1; min-width: 0;">
            <span style="display:block; font-size:1.5rem; font-weight:700; color:#1f2937; line-height:1.2;">{value}</span>
            <span style="display:block; font-size:0.75rem; font-weight:600; color:#6b7280; text-transform:uppercase; letter-spacing:0.05em;">{title}</span>
            <span style="display:block; font-size:0.75rem; color:#9ca3af; margin-top:0.25rem;">{subtitle}</span>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_chart_card(title, fig, height=400):
    """
    Renderiza gráfico dentro de iframe CON MÁRGENES MEJORADOS.
    """
    # AJUSTE DE MÁRGENES:
    # Aumentamos 'b' (bottom) a 45px para dar espacio a las fechas
    # Aumentamos 'l' (left) a 40px para los números del eje Y
    fig.update_layout(
        autosize=True,
        margin=dict(l=40, r=20, t=10, b=45), 
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    plot_html = fig.to_html(full_html=False, include_plotlyjs='cdn', config={'displayModeBar': False})
    
    html_code = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            body {{ margin: 0; padding: 0; overflow: hidden; }} 
            /* Contenedor del gráfico ocupa el 95% de altura para evitar scroll */
            .chart-container {{ height: 95%; width: 100%; }}
        </style>
    </head>
    <body>
        <div class="bg-white shadow-sm rounded-xl border border-gray-100 flex flex-col h-full w-full overflow-hidden">
            <div class="px-6 py-4 border-b border-gray-100 flex justify-between items-center bg-white flex-shrink-0">
                <h3 class="font-bold text-lg text-gray-800 m-0">{title}</h3>
            </div>
            <div class="p-2 flex-grow w-full bg-white relative" style="height: {height-60}px;">
                <div class="chart-container">{plot_html}</div>
            </div>
        </div>
    </body>
    </html>
    """
    components.html(html_code, height=height, scrolling=False)

def alert_card(is_rebounding):
    bg_hex = "#fee2e2" if is_rebounding else "#dcfce7"
    text_hex = "#dc2626" if is_rebounding else "#16a34a"
    icon = "🚨" if is_rebounding else "✅"
    title = "ALERTA DE REBROTE DETECTADA" if is_rebounding else "TENDENCIA ESTABLE"
    desc = "Se observa un aumento sostenido en la media de nuevos casos." if is_rebounding else "No se detectan patrones de crecimiento acelerado."
    
    html = f"""
    <div style="background-color:{bg_hex}; border:1px solid {text_hex}; border-radius:0.75rem; padding:1.5rem; display:flex; align-items:center; box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05); height:100%;">
        <div style="font-size:2.5rem; margin-right:1.5rem;">{icon}</div>
        <div>
            <h4 style="margin:0; color:{text_hex}; font-weight:700; font-size:1.1rem; margin-bottom:0.25rem;">{title}</h4>
            <p style="margin:0; color:{text_hex}; font-size:0.95rem; opacity:0.9; line-height:1.4;">{desc}</p>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def get_chart_config():
    return dict(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#4b5563'), 
        margin=dict(l=10, r=10, t=10, b=10),
        height=300,
        showlegend=False
    )