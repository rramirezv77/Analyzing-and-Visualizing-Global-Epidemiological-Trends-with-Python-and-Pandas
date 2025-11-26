import streamlit as st
import streamlit.components.v1 as components

# --- CONSTANTES DE COLOR ---
BG_COLOR = "#f3f4f6"   
CARD_COLOR = "#ffffff" 
TEXT_COLOR = "#1f2937" 

def setup_page_style():
    """Inyecta CSS y Tailwind."""
    st.markdown('<script src="https://cdn.tailwindcss.com"></script>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <style>
        html, body, [class*="css"] {{
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif !important;
        }}
        .stApp {{
            background-color: {BG_COLOR};
            color: {TEXT_COLOR};
        }}
        
        /* RESET GLOBAL PLOTLY */
        .js-plotly-plot, .plot-container {{
            height: 100% !important;
            width: 100% !important;
        }}
        
        header {{ visibility: hidden; }}
        .stDeployButton, div[data-testid="stDecoration"] {{ display: none; }}
        
        /* Ajuste del contenido principal para el sidebar de 5rem */
        .block-container {{
            padding-left: 6rem !important; /* 5rem sidebar + 1rem espacio */
            padding-top: 1rem !important;
            padding-right: 2rem !important;
            padding-bottom: 2rem !important;
            max-width: 100%;
        }}
        
        /* Ocultar botones originales de Streamlit para que no se vean dobles */
        div[data-testid="stSidebarContent"] .stButton button {{
            visibility: hidden;
            height: 0;
            padding: 0;
            margin: 0;
            width: 0;
        }}

        /* Estilos de inputs, tags y columns (Mantenidos) */
        div[data-baseweb="select"] > div, div[data-baseweb="input"] > div, div[data-baseweb="base-input"] {{
            background-color: white !important;
            border: 1px solid #e5e7eb !important;
            color: {TEXT_COLOR} !important;
            border-radius: 0.5rem;
        }}
        div[data-baseweb="select"] span {{ color: {TEXT_COLOR} !important; }}
        span[data-baseweb="tag"] {{ background-color: #ef4444 !important; }}
        span[data-baseweb="tag"] span {{ color: white !important; }}
        span[data-baseweb="tag"] svg {{ fill: white !important; color: white !important; }}
        
        div[data-testid="column"] > div > div[data-testid="stVerticalBlock"] {{
            gap: 1rem !important;
        }}

        /* --- SIDEBAR MODIFICADO (Contenedor principal) --- */
        section[data-testid="stSidebar"] {{
            width: 5rem !important; /* Ancho reducido a 5rem */
            background-color: #1f2937; /* Gris oscuro */
            padding-top: 1rem;      
            padding-left: 0.25rem; /* Pequeño ajuste para centrado */
            padding-right: 0.25rem;
        }}
        
        /* --- ESTILO DE BOTONES HTML --- */
        .sidebar-btn-container {{
            width: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 1rem;
            padding-top: 1rem;
        }}
        .sidebar-item {{
            width: 4.2rem;
            height: 4.2rem;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background-color: white; /* Color de fondo */
            border-radius: 0.75rem;
            cursor: pointer;
            transition: all 0.2s;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .sidebar-item:hover {{
            background-color: #f3f4f6;
            transform: scale(1.05);
        }}
        .sidebar-item svg {{
            stroke: #7c3aed; /* Color del icono */
            stroke-width: 2;
            fill: none;
            width: 1.5rem;
            height: 1.5rem;
        }}
        
        /* Estilo para los enlaces de navegación */
        .sidebar-btn-container a {{
            text-decoration: none; /* Quitar subrayado por defecto del enlace */
        }}
    </style>
    """, unsafe_allow_html=True)

def render_sidebar():
    """
    Renderiza el Sidebar usando HTML para el diseño y ENLACES HTML (QUERY PARAMS) para la funcionalidad.
    """
    
    icon_dashboard = '<svg viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" /></svg>'
    icon_table = '<svg viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" /></svg>'
    
    with st.sidebar:
        # Espacio superior
        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
        
        # --- Renderizado de HTML ---
        
        html_content = f"""
        <div class="sidebar-btn-container">
            <a href="?page=dashboard" target="_self">
                 <div class="sidebar-item">
                    {icon_dashboard}
                 </div>
            </a>
            <a href="?page=table" target="_self">
                 <div class="sidebar-item">
                    {icon_table}
                 </div>
            </a>
        </div>
        """
        st.markdown(html_content, unsafe_allow_html=True)


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
    Renderiza gráfico usando alturas fijas en píxeles para evitar cortes.
    """
    chart_height = height - 70 
    
    fig.update_layout(
        autosize=True,
        height=chart_height, 
        margin=dict(l=40, r=10, t=10, b=40), 
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title=None,
        yaxis_title=None
    )
    
    plot_html = fig.to_html(full_html=False, include_plotlyjs='cdn', config={'displayModeBar': False, 'responsive': True})
    
    html_code = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            body {{ margin: 0; padding: 0; overflow: hidden; font-family: sans-serif; }}
            .card {{
                background-color: white;
                border: 1px solid #e5e7eb;
                border-radius: 0.75rem;
                box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
                height: {height}px; 
                display: flex;
                flex-direction: column;
                overflow: hidden;
            }}
            .card-header {{
                padding: 1rem 1.5rem;
                border-bottom: 1px solid #f3f4f6;
                height: 60px;
                display: flex;
                align-items: center;
                flex-shrink: 0;
            }}
            .card-body {{
                padding: 0;
                height: {chart_height}px;
                width: 100%;
                overflow: hidden;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <div class="card-header">
                <h3 class="font-bold text-lg text-gray-800 m-0">{title}</h3>
            </div>
            <div class="card-body">
                {plot_html}
            </div>
        </div>
    </body>
    </html>
    """
    components.html(html_code, height=height+5, scrolling=False)

def alert_card(is_rebounding):
    bg_hex = "#fee2e2" if is_rebounding else "#dcfce7"
    text_hex = "#dc2626" if is_rebounding else "#16a34a"
    icon = "🚨" if is_rebounding else "✅"
    title = "ALERTA DE REBROTE DETECTADA" if is_rebounding else "TENDENCIA ESTABLE"
    desc = "Se observa un aumento sostenido en la media de nuevos casos." if is_rebounding else "No se detectan patrones de crecimiento acelerado."
    
    html = f"""
    <div style="background-color:{bg_hex}; border:1px solid {text_hex}; border-radius:0.75rem; padding:1.5rem; display:flex; align-items:center; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); height:100%;">
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
    
def render_top_banner(title):
    """
    Renderiza el banner oscuro prominente que ocupa todo el ancho, estilo Website Conversions.
    """
    banner_html = f"""
    <div style="
        background-color: #1f2937; 
        color: white; 
        padding: 1.2rem 2rem; 
        margin-bottom: 2rem; 
        border-radius: 0.75rem; 
        display: flex; 
        align-items: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #7c3aed; /* Acento Morado */
    ">
        <h2 style="font-size: 1.5rem; font-weight: 700; margin: 0; letter-spacing: 0.05em; text-transform: uppercase;">{title}</h2>
    </div>
    """
    st.markdown(banner_html, unsafe_allow_html=True)