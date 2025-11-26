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
        
        /* RESET PLOTLY */
        .js-plotly-plot, .plot-container {{
            height: 100% !important;
            width: 100% !important;
        }}
        
        header {{ visibility: hidden; }}
        .stDeployButton, div[data-testid="stDecoration"] {{ display: none; }}
        
        /* Ajuste Sidebar Nativo para que parezca el diseño HTML */
        /* MODIFICADO: Padding izquierdo ajustado para sidebar más angosto */
        .block-container {{
            padding-left: 6rem !important; /* 5rem sidebar + 1rem espacio */
            padding-top: 1rem !important;
            padding-right: 2rem !important;
            padding-bottom: 2rem !important;
            max-width: 100%;
        }}
        
        /* Estilizar botones del sidebar para que sean cuadrados redondeados */
        /* MODIFICADO: Botones más grandes para sidebar compacto */
        section[data-testid="stSidebar"] .stButton button {{
            width: 3.5rem;
            height: 3.5rem;
            border-radius: 0.75rem; /* Rounded-xl */
            background-color: white;
            border: none;
            color: #7c3aed; /* Morado por defecto */
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto; /* Centrar horizontalmente */
            padding: 0;
            font-size: 1.5rem; /* Icono más grande */
        }}
        
        /* Hover effect */
        section[data-testid="stSidebar"] .stButton button:hover {{
            background-color: #f3f4f6;
            color: #6d28d9;
            border: 1px solid #7c3aed;
        }}
        
        /* Inputs */
        div[data-baseweb="select"] > div, 
        div[data-baseweb="input"] > div, 
        div[data-baseweb="base-input"] {{
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

        /* --- SIDEBAR MODIFICADO --- */
        section[data-testid="stSidebar"] {{
            width: 5rem !important; /* Ancho reducido a 5rem */
            background-color: #1f2937; /* Gris oscuro */
            padding-top: 1rem;      /* Menos padding superior */
        }}
    </style>
    """, unsafe_allow_html=True)

def render_sidebar():
    """
    Renderiza el Sidebar usando componentes nativos de Streamlit 
    para permitir interacción real (navegación).
    """
    with st.sidebar:
        # --- MODIFICADO: Eliminado el logo morado ---
        
        # Espaciador inicial
        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
        
        # Botón 1: Dashboard
        if st.button("📊", key="btn_dashboard", help="Ver Dashboard"):
            st.session_state["page"] = "dashboard"
            st.rerun()
            
        # Espaciador entre botones
        st.write("") 
        
        # Botón 2: Tabla de Datos
        if st.button("📁", key="btn_table", help="Ver Datos Detallados"):
            st.session_state["page"] = "table"
            st.rerun()

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