import streamlit as st
import pandas as pd
from io import StringIO
import os
import json
import time
import datetime
import re
import altair as alt

# Favorites database file
FAVORITES_FILE = "favorites.json"
PORTFOLIO_FILE = "portfolio.json"
STUDIED_MATCHES_FILE = "studied_matches.json"

def load_favorites():
    if "favorites" not in st.session_state:
        if os.path.exists(FAVORITES_FILE):
            try:
                with open(FAVORITES_FILE, "r", encoding="utf-8") as f:
                    st.session_state.favorites = json.load(f)
            except Exception:
                st.session_state.favorites = []
        else:
            st.session_state.favorites = []

def save_favorites():
    try:
        with open(FAVORITES_FILE, "w", encoding="utf-8") as f:
            json.dump(st.session_state.favorites, f, indent=2, ensure_ascii=False)
    except Exception:
        pass

def load_portfolio():
    if "portfolio" not in st.session_state:
        if os.path.exists(PORTFOLIO_FILE):
            try:
                with open(PORTFOLIO_FILE, "r", encoding="utf-8") as f:
                    st.session_state.portfolio = json.load(f)
            except Exception:
                st.session_state.portfolio = []
        else:
            st.session_state.portfolio = []

def save_portfolio():
    try:
        with open(PORTFOLIO_FILE, "w", encoding="utf-8") as f:
            json.dump(st.session_state.portfolio, f, indent=2, ensure_ascii=False)
    except Exception:
        pass

def load_studied_matches():
    if "studied_matches" not in st.session_state:
        if os.path.exists(STUDIED_MATCHES_FILE):
            try:
                with open(STUDIED_MATCHES_FILE, "r", encoding="utf-8") as f:
                    st.session_state.studied_matches = json.load(f)
            except Exception:
                st.session_state.studied_matches = []
        else:
            st.session_state.studied_matches = []

def save_studied_matches():
    try:
        with open(STUDIED_MATCHES_FILE, "w", encoding="utf-8") as f:
            json.dump(st.session_state.studied_matches, f, indent=2, ensure_ascii=False)
    except Exception:
        pass

# Load databases at startup
load_favorites()
load_portfolio()
load_studied_matches()

def translate_market_to_spanish(market: str) -> str:
    if not market:
        return ""
    
    # Check if combined bet
    if " + " in market:
        parts = market.split(" + ")
        translated_parts = [translate_market_to_spanish(p.strip()) for p in parts]
        return " + ".join(translated_parts)
        
    m = market
    
    # Replacements for double chance
    m = m.replace("or Draw double chance", "o empate (doble oportunidad)")
    m = m.replace("or Draw", "o empate")
    m = m.replace("double chance", "doble oportunidad")
    
    # Replacements for draw no bet
    m = m.replace("draw no bet", "empate no válido")
    
    # Team win to nil / win
    m = re.sub(r'\b([A-Za-z\s]+) win to nil\b', r'Gana \1 sin encajar', m, flags=re.IGNORECASE)
    m = re.sub(r'\b([A-Za-z\s]+) win\b', r'Gana \1', m, flags=re.IGNORECASE)
    m = re.sub(r'\bDraw\b', 'Empate', m, flags=re.IGNORECASE)
    
    # Goals over / under
    m = re.sub(r'\bUnder\s+([\d\.]+)\s+goals\b', r'Menos de \1 goles', m, flags=re.IGNORECASE)
    m = re.sub(r'\bOver\s+([\d\.]+)\s+goals\b', r'Más de \1 goles', m, flags=re.IGNORECASE)
    
    # Both teams to score
    m = m.replace("Both teams to score - Yes", "Ambos equipos marcan: Sí")
    m = m.replace("Both teams to score - No", "Ambos equipos marcan: No")
    m = m.replace("both teams to score", "ambos equipos marcan")
    
    # Team goals
    m = re.sub(r'\b([A-Za-z\s]+)\s+over\s+([\d\.]+)\s+team\s+goals\b', r'\1 más de \2 goles', m, flags=re.IGNORECASE)
    m = re.sub(r'\b([A-Za-z\s]+)\s+under\s+([\d\.]+)\s+team\s+goals\b', r'\1 menos de \2 goles', m, flags=re.IGNORECASE)
    
    # Asian handicap
    m = re.sub(r'\b([A-Za-z\s]+)\s+([\+\-\d\.]+)\s+Asian\s+handicap\b', r'\1 hándicap asiático \2', m, flags=re.IGNORECASE)
    m = re.sub(r'\b([A-Za-z\s]+)\s+handicap\s+([\+\-\d\.]+)\b', r'\1 hándicap \2', m, flags=re.IGNORECASE)
    m = re.sub(r'\bAsian handicap\b', 'hándicap asiático', m, flags=re.IGNORECASE)
    m = re.sub(r'\bhandicap\b', 'hándicap', m, flags=re.IGNORECASE)
    
    # Cards
    m = m.replace("most cards", "más tarjetas")
    m = re.sub(r'\bTotal\s+cards\s+over\s+([\d\.]+)\b', r'Más de \1 tarjetas', m, flags=re.IGNORECASE)
    m = re.sub(r'\bTotal\s+cards\s+under\s+([\d\.]+)\b', r'Menos de \1 tarjetas', m, flags=re.IGNORECASE)
    m = re.sub(r'\b([A-Za-z\s]+)\s+over\s+([\d\.]+)\s+cards\b', r'\1 más de \2 tarjetas', m, flags=re.IGNORECASE)
    m = re.sub(r'\b([A-Za-z\s]+)\s+under\s+([\d\.]+)\s+cards\b', r'\1 menos de \2 tarjetas', m, flags=re.IGNORECASE)
    
    # Corners
    m = re.sub(r'\bTotal\s+corners\s+over\s+([\d\.]+)\b', r'Más de \1 córners', m, flags=re.IGNORECASE)
    m = re.sub(r'\bTotal\s+corners\s+under\s+([\d\.]+)\b', r'Menos de \1 córners', m, flags=re.IGNORECASE)
    m = re.sub(r'\b([A-Za-z\s]+)\s+over\s+([\d\.]+)\s+corners\b', r'\1 más de \2 córners', m, flags=re.IGNORECASE)
    m = re.sub(r'\b([A-Za-z\s]+)\s+under\s+([\d\.]+)\s+corners\b', r'\1 menos de \2 córners', m, flags=re.IGNORECASE)
    m = m.replace("corners", "córners")
    
    # Shots
    m = re.sub(r'\bTotal\s+shots\s+over\s+([\d\.]+)\b', r'Más de \1 tiros', m, flags=re.IGNORECASE)
    m = re.sub(r'\bTotal\s+shots\s+under\s+([\d\.]+)\b', r'Menos de \1 tiros', m, flags=re.IGNORECASE)
    m = re.sub(r'\b([A-Za-z\s]+)\s+over\s+([\d\.]+)\s+shots\b', r'\1 más de \2 tiros', m, flags=re.IGNORECASE)
    m = re.sub(r'\b([A-Za-z\s]+)\s+under\s+([\d\.]+)\s+shots\b', r'\1 menos de \2 tiros', m, flags=re.IGNORECASE)
    m = m.replace("shots", "tiros")
    m = m.replace("shots on target", "tiros a puerta")
    
    return m.strip()

def get_probability_benefit_relation(probability: float, odds: float) -> str:
    # probability is from 0.0 to 1.0 (e.g. 0.65) or 0.0 to 100.0 (e.g. 65.0)
    p = probability
    if p > 1.0:
        p = p / 100.0
        
    profit_level = "low"
    if odds < 1.65:
        profit_level = "low"
    elif odds <= 1.95:
        profit_level = "moderate"
    else:
        profit_level = "high"
        
    if p >= 0.70 and profit_level == "low":
        return "Apuesta conservadora con beneficio bajo"
    elif p >= 0.65 and profit_level == "moderate":
        return "Alta probabilidad y beneficio moderado"
    elif p >= 0.55 and profit_level == "high":
        return "Probabilidad buena con beneficio atractivo"
    elif p < 0.55 and profit_level == "high":
        return "Más riesgo, pero mayor beneficio potencial"
    else:
        if p >= 0.65:
            return "Alta probabilidad y beneficio moderado"
        elif profit_level == "high":
            return "Probabilidad buena con beneficio atractivo"
        else:
            return "Apuesta conservadora con beneficio bajo"

def classify_bet_type(market: str, combined_bet: bool) -> str:
    if combined_bet:
        return "Combinada"
    m = market.lower()
    if "goal" in m or "gol" in m or "score" in m:
        return "Goles"
    elif "corner" in m or "córner" in m or "corners" in m:
        return "Córners"
    elif "card" in m or "tarjeta" in m or "cards" in m:
        return "Tarjetas"
    elif "handicap" in m or "hándicap" in m or "asiático" in m or "asiatico" in m:
        return "Hándicap"
    elif "win" in m or "draw" in m or "1x2" in m or "empate" in m or "doble op" in m or "chance" in m or "no bet" in m or "gana" in m:
        return "Resultado"
    else:
        return "Otro"

def save_or_update_studied_match(match, competition, phase, betting_house, presets, custom_markets="", csv_data=None, recommendations=None):
    if not match:
        return
    load_studied_matches()
    existing_entry = None
    for entry in st.session_state.studied_matches:
        if entry.get("match", "").lower() == match.lower():
            existing_entry = entry
            break
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if existing_entry:
        existing_entry["last_updated"] = now_str
        existing_entry["competition"] = competition
        existing_entry["phase"] = phase
        existing_entry["betting_house"] = betting_house
        existing_entry["selected_market_presets"] = presets
        if custom_markets:
            existing_entry["custom_markets"] = custom_markets
        if csv_data is not None:
            existing_entry["last_csv"] = csv_data
        if recommendations is not None:
            existing_entry["last_recommendations"] = recommendations
    else:
        new_entry = {
            "match": match,
            "sport": "Fútbol",
            "date_created": now_str,
            "last_updated": now_str,
            "competition": competition,
            "phase": phase,
            "betting_house": betting_house,
            "selected_market_presets": presets,
            "custom_markets": custom_markets,
            "last_csv": csv_data or "",
            "last_recommendations": recommendations or []
        }
        st.session_state.studied_matches.append(new_entry)
    save_studied_matches()

def calculate_balance_metrics(portfolio_list):
    dinero_invertido = 0.0
    beneficio_obtenido = 0.0
    apuestas_pendientes = 0
    apuestas_cerradas = 0
    apuestas_ganadas = 0
    apuestas_perdidas = 0
    apuestas_nulas = 0
    
    for bet in portfolio_list:
        stake = float(bet.get("stake", 0.0))
        odds = float(bet.get("odds", 0.0))
        status = bet.get("status", "Pendiente")
        
        dinero_invertido += stake
        
        if status == "Ganada":
            profit = stake * (odds - 1.0)
            beneficio_obtenido += profit
            apuestas_ganadas += 1
            apuestas_cerradas += 1
        elif status == "Perdida":
            profit = -stake
            beneficio_obtenido += profit
            apuestas_perdidas += 1
            apuestas_cerradas += 1
        elif status == "Nula":
            profit = 0.0
            beneficio_obtenido += profit
            apuestas_nulas += 1
            apuestas_cerradas += 1
        else:
            apuestas_pendientes += 1
            
    saldo_total = beneficio_obtenido
    
    closed_stake = sum(float(b.get("stake", 0.0)) for b in portfolio_list if b.get("status") in ["Ganada", "Perdida", "Nula"])
    if closed_stake > 0:
        roi_cerrado = (beneficio_obtenido / closed_stake) * 100.0
    else:
        roi_cerrado = 0.0
        
    return {
        "dinero_invertido": dinero_invertido,
        "beneficio_obtenido": beneficio_obtenido,
        "saldo_total": saldo_total,
        "apuestas_pendientes": apuestas_pendientes,
        "apuestas_cerradas": apuestas_cerradas,
        "apuestas_ganadas": apuestas_ganadas,
        "apuestas_perdidas": apuestas_perdidas,
        "apuestas_nulas": apuestas_nulas,
        "roi_cerrado": roi_cerrado
    }

def prepare_chart_data(portfolio_list):
    closed_bets = [b for b in portfolio_list if b.get("status") in ["Ganada", "Perdida", "Nula"]]
    if not closed_bets:
        return pd.DataFrame()
        
    date_data = {}
    for b in closed_bets:
        dp = b.get("date_placed", "")
        if dp and len(dp) >= 10:
            date_str = dp[:10]
        else:
            date_str = datetime.date.today().strftime("%Y-%m-%d")
            
        status = b.get("status")
        stake = float(b.get("stake", 0.0))
        odds = float(b.get("odds", 0.0))
        profit = float(b.get("profit", 0.0))
        
        if date_str not in date_data:
            date_data[date_str] = {"ingresos": 0.0, "gastos": 0.0, "beneficio_dia": 0.0}
            
        if status == "Ganada":
            date_data[date_str]["ingresos"] += profit
        elif status == "Perdida":
            date_data[date_str]["gastos"] += stake
            
        date_data[date_str]["beneficio_dia"] += profit

    sorted_dates = sorted(date_data.keys())
    
    chart_rows = []
    cumulative_profit = 0.0
    
    if sorted_dates:
        try:
            first_date_dt = datetime.datetime.strptime(sorted_dates[0], "%Y-%m-%d")
            start_date_str = (first_date_dt - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        except Exception:
            start_date_str = "Inicio"
            
        chart_rows.append({
            "Fecha": start_date_str,
            "Ingresos": 0.0,
            "Gastos": 0.0,
            "Beneficio del día": 0.0,
            "Beneficio acumulado": 0.0
        })
        
    for d in sorted_dates:
        cumulative_profit += date_data[d]["beneficio_dia"]
        chart_rows.append({
            "Fecha": d,
            "Ingresos": date_data[d]["ingresos"],
            "Gastos": date_data[d]["gastos"],
            "Beneficio del día": date_data[d]["beneficio_dia"],
            "Beneficio acumulado": cumulative_profit
        })
        
    return pd.DataFrame(chart_rows)

def render_altair_chart(df):
    if df.empty:
        st.info("No hay datos de apuestas finalizadas para mostrar la evolución del saldo.")
        return
    try:
        chart = alt.Chart(df).mark_line(point=True, strokeWidth=3).encode(
            x=alt.X('Fecha:O', title='Fecha', sort=None),
            y=alt.Y('Beneficio acumulado:Q', title='Beneficio acumulado (€)'),
            color=alt.condition(
                alt.datum['Beneficio acumulado'] >= 0,
                alt.value('#00C853'),
                alt.value('#FF3B3B')
            ),
            tooltip=[
                alt.Tooltip('Fecha:N', title='Fecha'),
                alt.Tooltip('Ingresos:Q', title='Ingresos (€)', format='.2f'),
                alt.Tooltip('Gastos:Q', title='Gastos (€)', format='.2f'),
                alt.Tooltip('Beneficio del día:Q', title='Beneficio del día (€)', format='.2f'),
                alt.Tooltip('Beneficio acumulado:Q', title='Beneficio acumulado (€)', format='.2f')
            ]
        ).properties(
            width='container',
            height=350
        ).configure_view(
            strokeWidth=0
        ).configure_axis(
            grid=True,
            gridColor='#222222',
            labelColor='#a0aec0',
            titleColor='#ffffff'
        )
        st.altair_chart(chart, use_container_width=True)
    except Exception as e:
        st.line_chart(df.set_index("Fecha")[["Beneficio acumulado"]], y="Beneficio acumulado")

# Page configurations
st.set_page_config(
    page_title="CALCULADORA DE APUESTAS",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state keys safely at startup
if "current_section" not in st.session_state:
    st.session_state.current_section = "Inicio"
if "intro_seen" not in st.session_state:
    st.session_state.intro_seen = False
if "generated_prompt" not in st.session_state:
    st.session_state.generated_prompt = ""
if "result_prompt" not in st.session_state:
    st.session_state.result_prompt = ""
if "user_name" not in st.session_state:
    st.session_state.user_name = "Usuario"
if "portfolio" not in st.session_state:
    st.session_state.portfolio = []
if "favorites" not in st.session_state:
    st.session_state.favorites = []
if "favourites" not in st.session_state:
    st.session_state.favourites = []
if "studied_matches" not in st.session_state:
    st.session_state.studied_matches = []


# Custom Injectable CSS styling to achieve the requested red, black, and white professional trading theme
st.markdown("""
<style>
/* Dark base background for the entire dashboard */
.stApp {
    background-color: #080808 !important;
    color: #F5F5F5 !important;
}

/* Page titles and headers */
.big-title {
    font-size: 38px;
    font-weight: 800;
    color: #E30613;
    margin-bottom: 2px;
    text-transform: uppercase;
    letter-spacing: 2px;
}

.subtitle {
    font-size: 16px;
    color: #a0aec0;
    margin-bottom: 25px;
    font-weight: 400;
}

/* Layout section modules */
.module {
    background-color: #111111 !important;
    padding: 22px !important;
    border-radius: 12px !important;
    border: 1px solid #222222 !important;
    margin-bottom: 20px !important;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2) !important;
}

.formula {
    background-color: #111111;
    padding: 18px;
    border-radius: 10px;
    border-left: 4px solid #E30613;
    font-family: 'Courier New', monospace;
    font-size: 15px;
    color: #e2e8f0;
    margin: 15px 0;
}

/* Ensure all form labels are white and readable */
label, .stSlider label, .stTextInput label, .stNumberInput label, .stSelectbox label, .stTextArea label {
    color: #ffffff !important;
    font-weight: 600 !important;
    font-size: 14px !important;
}

/* Dark backgrounds for inputs, text areas and select boxes with white text and red borders */
input[type="text"], input[type="number"], textarea {
    background-color: #111111 !important;
    color: #F5F5F5 !important;
    border: 2px solid #E30613 !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 15px !important;
}

/* Placeholders inside inputs and textareas */
input::placeholder, textarea::placeholder {
    color: #718096 !important;
    opacity: 0.8 !important;
}

/* Selectbox container styling */
div[data-baseweb="select"] > div {
    background-color: #111111 !important;
    color: #F5F5F5 !important;
    border: 2px solid #E30613 !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}

/* Selected option text inside selectbox */
div[data-baseweb="select"] span {
    color: #F5F5F5 !important;
    font-weight: 600 !important;
}

/* Selectbox dropdown arrow */
div[data-baseweb="select"] svg {
    fill: #F5F5F5 !important;
}

/* Dropdown list popover styling */
div[data-baseweb="popover"] {
    background-color: #111111 !important;
    border: 1px solid #E30613 !important;
}

div[data-baseweb="popover"] li {
    background-color: #111111 !important;
    color: #F5F5F5 !important;
    font-weight: 600 !important;
}

div[data-baseweb="popover"] li:hover {
    background-color: #E30613 !important;
    color: #ffffff !important;
}

/* Tabs styles */
div[data-testid="stTabBar"] button {
    color: #a0aec0 !important;
    font-size: 16px !important;
    font-weight: 600 !important;
}

div[data-testid="stTabBar"] button[aria-selected="true"] {
    color: #E30613 !important;
    border-bottom-color: #E30613 !important;
}

/* Plus and minus buttons of Streamlit number inputs */
button[kind="secondary"] {
    background-color: #E30613 !important;
    color: #ffffff !important;
    border: 1px solid #ff4d4d !important;
}
button[kind="secondary"]:hover {
    background-color: #ff4d4d !important;
    color: #ffffff !important;
}

/* Styled Primary Buttons */
div.stButton > button {
    background-color: #E30613 !important;
    color: #ffffff !important;
    border: 2px solid #ff4d4d !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    padding: 0.6rem 2.5rem !important;
    transition: all 0.3s ease !important;
    width: 100% !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
}

div.stButton > button:hover {
    background-color: #ffffff !important;
    color: #E30613 !important;
    border-color: #ffffff !important;
    box-shadow: 0 0 15px rgba(227, 6, 19, 0.4) !important;
}

/* Adjust dataframe wrapper for dark-theme contrast and readability */
div[data-testid="stDataFrame"] {
    background-color: #111111 !important;
    border: 1px solid #222222 !important;
    border-radius: 8px !important;
}

/* Metric card text adjustments */
div[data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-weight: 800 !important;
}

div[data-testid="stMetricLabel"] {
    color: #a0aec0 !important;
    font-weight: 600 !important;
}

/* Home Navigation Card Grid styling */
.home-card div.stButton > button {
    background-color: #0b0b0b !important;
    color: #E30613 !important;
    border: 1px solid #E30613 !important;
    border-radius: 8px !important;
    font-size: 16px !important;
    font-weight: 700 !important;
    padding: 1rem !important;
    width: 100% !important;
    aspect-ratio: 1 / 1 !important;
    max-width: 220px !important;
    margin: 0 auto !important;
    text-align: center !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    transition: all 0.3s ease !important;
    white-space: normal !important;
    word-break: break-word !important;
}
.home-card div.stButton > button:hover {
    background-color: #E30613 !important;
    color: #ffffff !important;
    box-shadow: 0 0 15px rgba(227, 6, 19, 0.4) !important;
    transform: translateY(-2px) !important;
}

/* Top Right User Profile Styling */
div.element-container:has(.top-header-marker) {
    display: none !important;
}

div.element-container:has(.top-header-marker) + div.element-container {
    position: fixed !important;
    top: 15px !important;
    right: 20px !important;
    z-index: 999999 !important;
    width: auto !important;
}

div.element-container:has(.top-header-marker) + div.element-container div.stButton > button {
    background-color: #111111 !important;
    border: 1px solid #222222 !important;
    border-radius: 8px !important;
    padding: 6px 16px !important;
    font-size: 14px !important;
    font-weight: bold !important;
    box-shadow: 0 4px 10px rgba(0,0,0,0.5) !important;
    cursor: pointer !important;
    text-transform: none !important;
    letter-spacing: 0px !important;
    transition: all 0.3s ease !important;
    height: auto !important;
    min-height: auto !important;
    line-height: normal !important;
}

div.element-container:has(.top-header-marker) + div.element-container div.stButton > button::before {
    content: "Usuario | ";
    color: #a0aec0 !important;
    font-weight: bold !important;
    margin-right: 2px !important;
}

div.element-container:has(.top-header-marker) + div.element-container div.stButton > button:hover {
    border-color: #E30613 !important;
    color: #ffffff !important;
    box-shadow: 0 0 10px rgba(227,6,19,0.3) !important;
}

/* Metric / Insight Cards */
.metric-box {
    background-color: #111111;
    border: 1px solid #E30613;
    border-radius: 8px;
    padding: 15px;
    text-align: center;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
}
.metric-label {
    font-size: 11px;
    color: #a0aec0;
    font-weight: bold;
    letter-spacing: 1px;
}
.metric-value {
    font-size: 24px;
    font-weight: bold;
    color: #ffffff;
    margin-top: 5px;
}
.mini-metric-box {
    background-color: #111111;
    border: 1px solid #222222;
    border-radius: 6px;
    padding: 10px;
    text-align: center;
    font-size: 13px;
    color: #ffffff;
}
.insight-card {
    background-color: #111111;
    border: 1px solid #E30613;
    border-radius: 8px;
    padding: 18px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
}
.insight-header {
    font-size: 11px;
    color: #a0aec0;
    font-weight: bold;
    letter-spacing: 1px;
    text-transform: uppercase;
}
.insight-title {
    font-size: 20px;
    font-weight: bold;
    color: #E30613;
    margin-top: 5px;
    margin-bottom: 12px;
}
.insight-metric-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px 15px;
    font-size: 13px;
    color: #a0aec0;
}
.insight-metric-grid div b {
    color: #ffffff;
}

/* Sidebar styling overrides */
section[data-testid="stSidebar"] {
    background-color: #080808 !important;
    border-right: 1px solid #222222 !important;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label {
    background-color: #111111 !important;
    color: #F5F5F5 !important;
    border: 1px solid #222222 !important;
    border-radius: 6px !important;
    padding: 8px 12px !important;
    margin-bottom: 6px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    border-color: #E30613 !important;
    box-shadow: 0 0 10px rgba(227, 6, 19, 0.2) !important;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"] {
    border-color: #E30613 !important;
    background-color: #E30613 !important;
    color: #ffffff !important;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"] span {
    color: #ffffff !important;
}

/* Decision classes coloring */
.status-ok {
    color: #00ff88;
    font-weight: bold;
}

.status-warn {
    color: #ffcc00;
    font-weight: bold;
}

.status-bad {
    color: #ff3b30;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# 1.5. Dynamic sidebar visibility based on active section
if st.session_state.get("current_section", "Inicio") == "Inicio":
    st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        display: none !important;
    }
    [data-testid="collapsedControl"] {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 1. Page Intro Animation
if "intro_seen" not in st.session_state:
    st.markdown("""
    <div class="intro-container" style="
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        background-color: #000000;
        z-index: 999999;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    ">
        <style>
        .intro-title {
            font-family: sans-serif;
            font-size: 42px;
            font-weight: 900;
            color: #E30613;
            letter-spacing: 4px;
            text-transform: uppercase;
            margin-bottom: 20px;
            text-shadow: 0 0 20px rgba(227, 6, 19, 0.8);
            animation: glowSweep 1.5s ease-in-out infinite alternate;
        }
        .intro-line {
            width: 180px;
            height: 3px;
            background: linear-gradient(90deg, transparent, #E30613, transparent);
            box-shadow: 0 0 10px #E30613;
        }
        @keyframes glowSweep {
            from { text-shadow: 0 0 10px rgba(227, 6, 19, 0.5); }
            to { text-shadow: 0 0 25px rgba(227, 6, 19, 1); }
        }
        </style>
        <div class="intro-title">CALCULADORA DE APUESTAS</div>
        <div class="intro-line"></div>
    </div>
    """, unsafe_allow_html=True)
    time.sleep(1.8)
    st.session_state.intro_seen = True
    st.rerun()

# 2. Calculate global metrics for the header
portfolio = st.session_state.get("portfolio", [])
metrics_glob = calculate_balance_metrics(portfolio)

bal_val = metrics_glob["saldo_total"]
bal_sign = "+" if bal_val > 0 else ""
bal_color = "#00C853" if bal_val > 0 else ("#FF3B3B" if bal_val < 0 else "#ffffff")

# 3. Top Right User Box Layout (Clickable balance text positioned via CSS)
st.markdown('<div class="top-header-marker"></div>', unsafe_allow_html=True)
st.markdown(f"""
<style>
div.element-container:has(.top-header-marker) + div.element-container div.stButton > button {{
    color: {bal_color} !important;
}}
</style>
""", unsafe_allow_html=True)

if st.button(f"Saldo: {bal_sign}{bal_val:.2f} €", key="top_clickable_balance_btn"):
    st.session_state.current_section = "Evolución del saldo"
    st.rerun()

# 4. Main Title Section (Centered on Inicio, Left-aligned on others)
if st.session_state.current_section == "Inicio":
    st.markdown("""
    <div style="text-align: center; margin-top: 50px; margin-bottom: 40px;">
        <div class="big-title" style="font-size: 44px; margin-bottom: 10px;">CALCULADORA DE APUESTAS</div>
        <div class="subtitle" style="font-size: 18px; color: #a0aec0;">Plataforma de análisis, gestión y seguimiento de apuestas</div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown('<div class="big-title">CALCULADORA DE APUESTAS</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Plataforma de análisis, gestión y seguimiento de apuestas</div>', unsafe_allow_html=True)

# 4. Left Sidebar Navigation Menu
SECTIONS = [
    "Inicio",
    "Calculadora",
    "Favoritas",
    "Top cuotas",
    "Cartera",
    "Estadísticas del modelo",
    "Asistente manual",
    "Historial de partidos estudiados",
    "Evolución del saldo"
]

if "current_section" not in st.session_state:
    st.session_state.current_section = "Inicio"

try:
    sec_index = SECTIONS.index(st.session_state.current_section)
except ValueError:
    sec_index = 0

st.sidebar.markdown("""
<div style="display: flex; align-items: center; margin-bottom: 20px; margin-top: 10px;">
    <div style="margin-right: 12px; display: flex; flex-direction: column; justify-content: space-between; width: 18px; height: 12px;">
        <div style="width: 100%; height: 2px; background-color: #E30613;"></div>
        <div style="width: 100%; height: 2px; background-color: #E30613;"></div>
        <div style="width: 100%; height: 2px; background-color: #E30613;"></div>
    </div>
    <div style="font-size: 18px; font-weight: bold; color: #ffffff; text-transform: uppercase; letter-spacing: 1px;">Menú</div>
</div>
""", unsafe_allow_html=True)

selected_sidebar_sec = st.sidebar.radio(
    "Menú de navegación",
    SECTIONS,
    index=sec_index,
    label_visibility="collapsed",
    key="nav_sidebar_radio"
)

if selected_sidebar_sec != st.session_state.current_section:
    st.session_state.current_section = selected_sidebar_sec
    st.rerun()

section = st.session_state.current_section

def clean_match_name(text):
    if not text:
        return ""
    
    # Clean extra spaces
    text = " ".join(text.split())
    
    # Standardize separators
    import re
    # Replace " against " (case-insensitive) with " vs "
    text = re.sub(r'\s+against\s+', ' vs ', text, flags=re.IGNORECASE)
    # Replace " - " or "-" with " vs "
    text = re.sub(r'\s*-\s*', ' vs ', text)
    # Replace " v " or " V " with " vs "
    text = re.sub(r'\s+[vV]\s+', ' vs ', text)
    
    # If no "vs" (case-insensitive) exists, check if it's two words
    if not re.search(r'\bvs\b', text, re.IGNORECASE):
        words = text.split()
        if len(words) == 2:
            text = f"{words[0]} vs {words[1]}"
            
    # Dictionary to translate common Spanish team names
    translations = {
        "españa": "Spain",
        "cabo verde": "Cape Verde",
        "méxico": "Mexico",
        "mexico": "Mexico",
        "sudáfrica": "South Africa",
        "sudafrica": "South Africa",
        "estados unidos": "United States",
        "alemania": "Germany",
        "francia": "France",
        "inglaterra": "England",
        "argentina": "Argentina",
        "brasil": "Brazil",
        "portugal": "Portugal",
        "italia": "Italy",
        "marruecos": "Morocco",
        "japón": "Japan",
        "japon": "Japan",
        "corea del sur": "South Korea"
    }
    
    # Translate using word boundary substitutions
    for spanish, english in translations.items():
        pattern = r'\b' + re.escape(spanish) + r'\b'
        text = re.sub(pattern, english, text, flags=re.IGNORECASE)
        
    # Standardize casing for "vs" (ensure it is lower case "vs" with correct spacing)
    text = re.sub(r'\s+[vV][sS]\s+', ' vs ', text)
    
    return " ".join(text.split())

# ----------------------------------------------------
# SECCIÓN: INICIO
# ----------------------------------------------------
if section == "Inicio":
    col_h1, col_h2, col_h3, col_h4 = st.columns(4)
    with col_h1:
        st.markdown('<div class="home-card">', unsafe_allow_html=True)
        if st.button("Calculadora", key="h_btn_calc"):
            st.session_state.current_section = "Calculadora"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="home-card" style="margin-top:15px;">', unsafe_allow_html=True)
        if st.button("Favoritas", key="h_btn_fav"):
            st.session_state.current_section = "Favoritas"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col_h2:
        st.markdown('<div class="home-card">', unsafe_allow_html=True)
        if st.button("Top cuotas", key="h_btn_top"):
            st.session_state.current_section = "Top cuotas"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="home-card" style="margin-top:15px;">', unsafe_allow_html=True)
        if st.button("Cartera", key="h_btn_cart"):
            st.session_state.current_section = "Cartera"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col_h3:
        st.markdown('<div class="home-card">', unsafe_allow_html=True)
        if st.button("Estadísticas del modelo", key="h_btn_est"):
            st.session_state.current_section = "Estadísticas del modelo"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="home-card" style="margin-top:15px;">', unsafe_allow_html=True)
        if st.button("Asistente manual", key="h_btn_asis"):
            st.session_state.current_section = "Asistente manual"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col_h4:
        st.markdown('<div class="home-card">', unsafe_allow_html=True)
        if st.button("Historial de partidos estudiados", key="h_btn_hist"):
            st.session_state.current_section = "Historial de partidos estudiados"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="home-card" style="margin-top:15px;">', unsafe_allow_html=True)
        if st.button("Evolución del saldo", key="h_btn_evol"):
            st.session_state.current_section = "Evolución del saldo"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------------------------------
# SECCIÓN: CALCULADORA
# ----------------------------------------------------
elif section == "Calculadora":
    st.header("Calculadora")
    if "config_match" not in st.session_state:
        st.session_state.config_match = ""
    if "config_competition" not in st.session_state:
        st.session_state.config_competition = ""
    if "config_phase" not in st.session_state:
        st.session_state.config_phase = "Fase de grupos"
    if "config_betting_house" not in st.session_state:
        st.session_state.config_betting_house = ""
    if "config_total_stake" not in st.session_state:
        st.session_state.config_total_stake = 10.0
    if "config_num_picks" not in st.session_state:
        st.session_state.config_num_picks = 2
    if "config_stake_strategy" not in st.session_state:
        st.session_state.config_stake_strategy = "Principal + secundaria"
    if "config_allow_combined" not in st.session_state:
        st.session_state.config_allow_combined = True
    if "config_cuota_minima" not in st.session_state:
        st.session_state.config_cuota_minima = 1.50
    if "config_cuota_maxima" not in st.session_state:
        st.session_state.config_cuota_maxima = 2.50


    st.header("1. Generador de prompt de análisis")
    st.markdown("Rellena los datos del partido, pulsa GENERAR / ACTUALIZAR PROMPT, envía el prompt generado a tu asistente de IA y pega el CSV devuelto en la sección de Entrada CSV de mercados.")
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        prompt_match = st.text_input("Partido", placeholder="Ejemplo: España vs Cabo Verde", key="prompt_match_input")
        st.caption("Puedes escribirlo de forma normal, por ejemplo: España vs Cabo Verde, España - Cabo Verde o España Cabo Verde.")
        
        prompt_competition_choice = st.selectbox(
            "Competición",
            [
                "FIFA World Cup 2026",
                "UEFA Euro",
                "Copa América",
                "Africa Cup of Nations",
                "UEFA Champions League",
                "UEFA Europa League",
                "UEFA Conference League",
                "Premier League",
                "LaLiga",
                "Serie A",
                "Bundesliga",
                "Ligue 1",
                "Otro"
            ],
            key="prompt_comp_select"
        )
        if prompt_competition_choice == "Otro":
            prompt_competition = st.text_input(
                "Competición personalizada",
                placeholder="Ejemplo: Amistoso Internacional",
                key="prompt_comp_custom"
            )
        else:
            prompt_competition = prompt_competition_choice
            
        prompt_phase = st.selectbox("Fase", ["Fase de grupos", "Eliminatoria", "Semifinal", "Final"], key="prompt_phase_input")
    with col_p2:
        prompt_house_choice = st.selectbox(
            "Casa de apuestas",
            [
                "Winamax",
                "Bet365",
                "Codere",
                "Betfair",
                "Bwin",
                "Marathonbet",
                "1xBet",
                "Betway",
                "William Hill",
                "Pinnacle",
                "Otro"
            ],
            key="prompt_house_select"
        )
        if prompt_house_choice == "Otro":
            prompt_house = st.text_input(
                "Casa de apuestas personalizada",
                placeholder="Ejemplo: Sportium",
                key="prompt_house_custom"
            )
        else:
            prompt_house = prompt_house_choice

        prompt_presets = st.multiselect(
            "Tipo de análisis de mercados",
            [
                "Análisis completo",
                "Apuestas conservadoras / seguras",
                "Mercados principales de resultado",
                "Goles",
                "Córners",
                "Tarjetas",
                "Tiros",
                "Hándicaps",
                "Personalizado"
            ],
            default=["Análisis completo"],
            key="prompt_market_presets"
        )
        st.caption("Elige uno o varios análisis para un examen detallado del modelo (Goles, Córners, Tarjetas, Tiros, Hándicaps, etc.).")
        
        preset_mapping = {
            "Análisis completo": "1X2, double chance, draw no bet, goals, under/over 2.5, under/over 3.5, both teams to score, team goals, corners, team corners, cards, team cards, shots, shots on target, handicaps, Asian handicaps",
            "Apuestas conservadoras / seguras": "double chance, draw no bet, under/over 3.5 goals, team under/over goals, team corners, team cards, low-risk handicaps",
            "Mercados principales de resultado": "1X2, double chance, draw no bet, halftime/fulltime, team to score first, win to nil",
            "Goles": "goals, under/over 1.5, under/over 2.5, under/over 3.5, both teams to score, team goals, clean sheet, win to nil",
            "Córners": "total corners, under/over corners, team corners, corner handicap, first half corners",
            "Tarjetas": "total cards, team cards, most cards, player cards if lineups are available, cards handicap",
            "Tiros": "total shots, team shots, shots on target, player shots if lineups are available, player shots on target if lineups are available",
            "Hándicaps": "European handicaps, Asian handicaps, favorite handicap, underdog positive handicap, low-risk handicap lines"
        }
        
        markets_list = []
        for pr in prompt_presets:
            if pr in preset_mapping:
                for item in preset_mapping[pr].split(","):
                    item_clean = item.strip()
                    if item_clean and item_clean not in markets_list:
                        markets_list.append(item_clean)
                        
        if "Personalizado" in prompt_presets:
            prompt_markets_custom_text = st.text_area(
                "Mercados personalizados a analizar",
                placeholder="Ejemplo: Córners de España, tarjetas de Cabo Verde, más de 1.5 goles de España",
                height=125,
                key="prompt_markets_custom_input"
            )
            if prompt_markets_custom_text:
                for item in prompt_markets_custom_text.split(","):
                    item_clean = item.strip()
                    if item_clean and item_clean not in markets_list:
                        markets_list.append(item_clean)
                        
        prompt_markets = ", ".join(markets_list)
    
    if "generated_prompt" not in st.session_state:
        st.session_state.generated_prompt = ""

    if st.button("GENERAR / ACTUALIZAR PROMPT", use_container_width=True):
        cleaned_match = clean_match_name(prompt_match)
        
        phase_mapping = {
            "Fase de grupos": "Group",
            "Eliminatoria": "Knockout",
            "Semifinal": "Semifinal",
            "Final": "Final"
        }
        prompt_phase_eng = phase_mapping.get(prompt_phase, prompt_phase)
        
        prompt_text = f"""Please search current information about the football match "{cleaned_match}" in the "{prompt_competition}" ({prompt_phase_eng} phase).
Review odds, lineups, injuries, suspensions, recent form, FIFA ranking or Elo, tactical context, referee if available, corners, cards, goals and shots. Use "{prompt_house}" as the betting house preference if possible.

Based on your research and analysis, estimate probabilities for the following markets: {prompt_markets}

You must return ONLY a CSV with exactly these columns:
Market,Odds,Probability,Risk,Uncertainty,Type

CSV rules:
- Odds must be in decimal format.
- Probability must be a number from 0 to 100.
- Risk must be a number from 0 to 100.
- Uncertainty must be a number from 0 to 100.
- Type must be Low, Medium or High.
- Do not include explanations outside the CSV.
- Do not include markdown code fences.
- Do not include markets without odds.
- If data is missing, increase uncertainty.
- Do not force bets.
- Only include markets with realistic potential value.

Here is the model formula for context:
EV* = [(Estimated Probability − λ × Uncertainty − ρ × Risk) × Odds] − 1

Please be conservative with:
- finals,
- knockout matches,
- low odds favorites,
- aggressive handicaps,
- under bets based only on defensive style,
- cards totals without referee information."""
        st.session_state.generated_prompt = prompt_text
        st.session_state.generated_prompt_area = prompt_text
        
        # Store cleaned match in a separate session state key
        st.session_state.cleaned_match = cleaned_match
        
        # Connect AI Research Prompt Generator with Parameters & Configuration
        st.session_state.config_match = cleaned_match
        st.session_state.config_competition = prompt_competition
        st.session_state.config_phase = prompt_phase
        st.session_state.config_betting_house = prompt_house
        
        # Save studied match history entry
        save_or_update_studied_match(
            match=cleaned_match,
            competition=prompt_competition,
            phase=prompt_phase,
            betting_house=prompt_house,
            presets=prompt_presets,
            custom_markets=st.session_state.get("prompt_markets_custom_input", "")
        )

    st.text_area(
        "Prompt de análisis de IA generado",
        value=st.session_state.generated_prompt,
        height=350,
        key="generated_prompt_area"
    )
    
    # JavaScript copy-to-clipboard component
    import json
    import streamlit.components.v1 as components
    
    escaped_prompt = json.dumps(st.session_state.generated_prompt)
    
    copy_button_html = f"""
    <style>
    body {{
        margin: 0;
        padding: 0;
        background-color: transparent;
        overflow: hidden;
    }}
    button {{
        background-color: #e63946;
        color: #ffffff;
        border: 2px solid #ff6b6b;
        border-radius: 8px;
        font-weight: 700;
        padding: 0.6rem 2.5rem;
        transition: all 0.3s ease;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-family: sans-serif;
        cursor: pointer;
    }}
    button:hover {{
        background-color: #ffffff !important;
        color: #e63946 !important;
        border-color: #ffffff !important;
        box-shadow: 0 0 15px rgba(230, 57, 70, 0.4) !important;
    }}
    </style>
    <button id="copy-btn">COPIAR PROMPT</button>
    <div id="status" style="
        color: #00ff88;
        font-weight: bold;
        font-family: sans-serif;
        margin-top: 8px;
        font-size: 14px;
        text-align: center;
        display: none;
    ">Prompt copiado al portapapeles</div>
    
    <script>
    document.getElementById('copy-btn').addEventListener('click', function() {{
        const text = {escaped_prompt};
        if (!text) {{
            const status = document.getElementById('status');
            status.innerText = "No se ha generado ningún prompt aún";
            status.style.color = "#ff3b30";
            status.style.display = "block";
            setTimeout(() => {{ status.style.display = "none"; }}, 3000);
            return;
        }}
        
        if (navigator.clipboard && navigator.clipboard.writeText) {{
            navigator.clipboard.writeText(text).then(showSuccess).catch(fallbackCopy);
        }} else {{
            fallbackCopy();
        }}
        
        function fallbackCopy() {{
            try {{
                const el = document.createElement('textarea');
                el.value = text;
                el.setAttribute('readonly', '');
                el.style.position = 'absolute';
                el.style.left = '-9999px';
                document.body.appendChild(el);
                el.select();
                const success = document.execCommand('copy');
                document.body.removeChild(el);
                if (success) {{
                    showSuccess();
                }} else {{
                    showError();
                }}
            }} catch (err) {{
                showError();
            }}
        }}
        
        function showSuccess() {{
            const status = document.getElementById('status');
            status.innerText = "Prompt copiado al portapapeles";
            status.style.color = "#00ff88";
            status.style.display = "block";
            setTimeout(() => {{ status.style.display = "none"; }}, 3000);
        }}
        
        function showError() {{
            const status = document.getElementById('status');
            status.innerText = "Falló la copia. Por favor selecciona y copia manualmente.";
            status.style.color = "#ff3b30";
            status.style.display = "block";
            setTimeout(() => {{ status.style.display = "none"; }}, 5000);
        }}
    }});
    </script>
    """
    components.html(copy_button_html, height=75)
    
    st.markdown(
        '<p style="font-size: 13px; color: #a0aec0; margin-top: -10px; margin-bottom: 25px;">'
        '“Haz clic en el botón después de editar los detalles del partido. Luego copia el prompt generado y envíalo a tu asistente de IA.”'
        '</p>',
        unsafe_allow_html=True
    )
    st.markdown("---")

    st.header("2. Parámetros y configuración")

    # Inputs organized in 3 columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        match = st.text_input("Partido", placeholder="Ejemplo: España vs Cabo Verde", key="config_match")
        competition = st.text_input("Competición", placeholder="Ejemplo: FIFA World Cup 2026", key="config_competition")
        phase = st.selectbox("Fase", ["Fase de grupos", "Eliminatoria", "Semifinal", "Final"], key="config_phase")
        betting_house = st.text_input("Casa de apuestas", placeholder="Ejemplo: Winamax", key="config_betting_house")

    with col2:
        total_stake = st.number_input("Cantidad total a apostar (€)", min_value=1.0, value=st.session_state.config_total_stake, step=1.0)
        num_picks = 3
        strategy_options = ["60 / 25 / 15", "50 / 30 / 20", "70 / 20 / 10"]
            
        valid_defaults = []
        if "config_stake_strategies" in st.session_state:
            valid_defaults = [s for s in st.session_state.config_stake_strategies if s in strategy_options]
        if not valid_defaults:
            valid_defaults = [strategy_options[0]]
            
        selected_strategies = st.multiselect(
            "Estrategia de reparto",
            options=strategy_options,
            default=valid_defaults,
            key="config_stake_strategies"
        )

    with col3:
        reliability = st.selectbox("Fiabilidad de los datos", ["Alta", "Media", "Baja"], key="config_reliability")
        model_mode = st.selectbox("Modo del modelo", ["Conservador", "Equilibrado", "Agresivo"], key="config_model_mode")
        cuota_minima = st.number_input("Cuota mínima objetivo", min_value=1.01, value=st.session_state.config_cuota_minima, step=0.01)
        cuota_maxima = st.number_input("Cuota máxima objetivo", min_value=1.01, value=st.session_state.config_cuota_maxima, step=0.01)
        allow_combined = st.checkbox("Permitir combinadas", value=st.session_state.config_allow_combined)

    st.markdown("### Model Formula Identity")
    st.markdown(
        r"""
        <div class="formula">
        EV* = [(Estimated Probability − λ × Uncertainty − ρ × Risk) × Odds] − 1
        </div>
        """,
        unsafe_allow_html=True
    )

    st.header("3. Entrada CSV de mercados")
    st.markdown("""
    Pega tus mercados en formato CSV. El CSV debe contener exactamente estas columnas:
    `Market`, `Odds`, `Probability`, `Risk`, `Uncertainty`, `Type`
    """)

    # Default CSV example
    default_csv = """Market,Odds,Probability,Risk,Uncertainty,Type
Under 2.5 goals,1.80,66,8,8,Low
Spain win,2.10,48,18,16,Medium
Over 8.5 corners,1.85,61,12,10,Medium
France over 1.5 cards,1.90,60,15,12,Medium"""

    csv_input = st.text_area(
        "Pegar mercados en formato CSV",
        value=default_csv,
        height=180
    )

    # Process and Validate CSV
    valid_csv = False
    df_input = None

    if csv_input.strip() != "":
        try:
            df_input = pd.read_csv(StringIO(csv_input))
            # Clean whitespaces in column names
            df_input.columns = [c.strip() for c in df_input.columns]
            
            # Column verification
            required_columns = ["Market", "Odds", "Probability", "Risk", "Uncertainty", "Type"]
            missing_cols = [col for col in required_columns if col not in df_input.columns]
            
            if missing_cols:
                st.error(f"Error de validación: Al CSV le faltan las siguientes columnas requeridas: {', '.join(missing_cols)}")
            else:
                # Convert numeric values and check for errors
                df_input["Odds"] = pd.to_numeric(df_input["Odds"], errors='coerce')
                df_input["Probability"] = pd.to_numeric(df_input["Probability"], errors='coerce')
                df_input["Risk"] = pd.to_numeric(df_input["Risk"], errors='coerce')
                df_input["Uncertainty"] = pd.to_numeric(df_input["Uncertainty"], errors='coerce')

                if df_input[["Odds", "Probability", "Risk", "Uncertainty"]].isnull().any().any():
                    st.error("Error de validación: Algunos campos en las columnas numéricas (Odds, Probability, Risk, Uncertainty) no se pueden convertir a números.")
                else:
                    valid_csv = True
        except Exception as e:
            st.error(f"Error al analizar el archivo CSV: {str(e)}")

    st.markdown('<div id="resultados"></div>', unsafe_allow_html=True)
    st.header("Resultado final")

    # Ejecutar el modelo / Calcular apuestas
    if st.button("CALCULAR APUESTAS", use_container_width=True):
        if not valid_csv:
            st.error("No se pueden calcular las apuestas. Por favor, corrige los errores de validación del CSV anteriores.")
        else:
            # Contradiction filter
            def are_contradictory(m1: str, m2: str) -> bool:
                m1_l = m1.lower()
                m2_l = m2.lower()
                if "both teams to score" in m1_l and "both teams to score" in m2_l:
                    if ("yes" in m1_l and "no" in m2_l) or ("no" in m1_l and "yes" in m2_l):
                        return True
                if "win" in m1_l and "win" in m2_l:
                    w1 = m1_l.replace("win", "").strip()
                    w2 = m2_l.replace("win", "").strip()
                    if w1 != w2 and w1 and w2:
                        return True
                if "win to nil" in m1_l and "both teams to score" in m2_l and "yes" in m2_l:
                    return True
                if "win to nil" in m2_l and "both teams to score" in m1_l and "yes" in m1_l:
                    return True
                if ("over" in m1_l and "under" in m2_l) or ("under" in m1_l and "over" in m2_l):
                    r1 = m1_l.replace("over", "").replace("under", "").strip()
                    r2 = m2_l.replace("over", "").replace("under", "").strip()
                    if r1 == r2:
                        return True
                return False

            # Simple bet candidates
            candidates = []
            under_1_50_markets = []
            for _, row in df_input.iterrows():
                odds = float(row["Odds"])
                prob = float(row["Probability"]) / 100.0
                risk = float(row["Risk"]) / 100.0
                unc = float(row["Uncertainty"]) / 100.0
                risk_type = str(row["Type"]).strip()

                # Add simple candidates
                if (cuota_minima <= odds <= cuota_maxima and 
                    prob >= 0.45 and 
                    risk <= 0.35 and 
                    unc <= 0.35):
                    
                    candidates.append({
                        "combined_bet": False,
                        "legs": [{"market": row["Market"], "odds": odds, "probability": prob, "risk": risk, "uncertainty": unc, "type": risk_type}],
                        "market": row["Market"],
                        "odds": odds,
                        "probability": prob,
                        "risk": risk,
                        "uncertainty": unc,
                        "type": risk_type,
                        "safety_score": (prob * 100.0) - (risk * 40.0) - (unc * 40.0)
                    })
                
                # Collect candidates under 1.50 for combined bets
                if odds < 1.50 and prob >= 0.45 and risk <= 0.35 and unc <= 0.35:
                    under_1_50_markets.append({
                        "market": row["Market"],
                        "odds": odds,
                        "probability": prob,
                        "risk": risk,
                        "uncertainty": unc,
                        "type": risk_type
                    })

            # Combined bet candidates
            if allow_combined and len(under_1_50_markets) >= 2:
                for i in range(len(under_1_50_markets)):
                    for j in range(i + 1, len(under_1_50_markets)):
                        m1 = under_1_50_markets[i]
                        m2 = under_1_50_markets[j]

                        if are_contradictory(m1["market"], m2["market"]):
                            continue

                        c_odds = m1["odds"] * m2["odds"]
                        c_prob = m1["probability"] * m2["probability"]
                        c_risk = ((m1["risk"] + m2["risk"]) / 2.0) + 0.05
                        c_unc = ((m1["uncertainty"] + m2["uncertainty"]) / 2.0) + 0.05

                        if (cuota_minima <= c_odds <= cuota_maxima and 
                            c_prob >= 0.35 and 
                            c_risk <= 0.35 and 
                            c_unc <= 0.35):
                            
                            type_map = {"Low": 1, "Medium": 2, "High": 3}
                            inv_type_map = {1: "Low", 2: "Medium", 3: "High"}
                            t1 = type_map.get(m1["type"], 2)
                            t2 = type_map.get(m2["type"], 2)
                            c_type = inv_type_map[max(t1, t2)]

                            candidates.append({
                                "combined_bet": True,
                                "legs": [m1, m2],
                                "market": f"{m1['market']} + {m2['market']}",
                                "odds": c_odds,
                                "probability": c_prob,
                                "risk": c_risk,
                                "uncertainty": c_unc,
                                "type": c_type,
                                "safety_score": (c_prob * 100.0) - (c_risk * 40.0) - (c_unc * 40.0)
                            })

            # Sort and filter top recommendations
            def cand_sort_key(x):
                dist_1_80 = abs(x["odds"] - 1.80)
                return (-x["probability"], -x["safety_score"], x["risk"], x["uncertainty"], dist_1_80)

            candidates_sorted = sorted(candidates, key=cand_sort_key)

            selected_recommendations = []
            used_markets = set()
            for cand in candidates_sorted:
                cand_markets = {leg["market"] for leg in cand["legs"]}
                if not (cand_markets & used_markets):
                    selected_recommendations.append(cand)
                    used_markets.update(cand_markets)
                if len(selected_recommendations) >= num_picks:
                    break

            # Store in session state
            st.session_state.calculated_results = {
                "selected_recommendations": selected_recommendations,
                "match": match,
                "competition": competition,
                "betting_house": betting_house,
                "total_stake": total_stake,
                "num_picks": num_picks,
                "selected_strategies": selected_strategies
            }

            # Save studied match history entry with CSV and recommendations
            save_or_update_studied_match(
                match=match,
                competition=competition,
                phase=phase,
                betting_house=betting_house,
                presets=st.session_state.get("prompt_market_presets", ["Análisis completo"]),
                custom_markets=st.session_state.get("prompt_markets_custom_input", ""),
                csv_data=csv_input,
                recommendations=selected_recommendations
            )

            # Save latest markets for Top cuotas
            st.session_state.latest_markets = []
            for _, row in df_input.iterrows():
                st.session_state.latest_markets.append({
                    "Match": match,
                    "BettingHouse": betting_house,
                    "Market": str(row["Market"]),
                    "Odds": float(row["Odds"]),
                    "Probability": float(row["Probability"]),
                    "Risk": float(row["Risk"]),
                    "Uncertainty": float(row["Uncertainty"]),
                    "Type": str(row["Type"]).strip(),
                    "SafetyScore": float(row["Probability"]) - (float(row["Risk"]) * 0.5) - (float(row["Uncertainty"]) * 0.5)
                })

            # Auto-scroll script
            st.components.v1.html(
                """
                <script>
                try {
                    window.parent.location.hash = "resultados";
                } catch (e) {}
                try {
                    window.parent.document.getElementById("resultados").scrollIntoView({behavior: "smooth"});
                } catch (e) {}
                </script>
                """,
                height=0,
                width=0
            )

    # Render results if they exist in session state
    if "calculated_results" in st.session_state and st.session_state.calculated_results is not None:
        res = st.session_state.calculated_results
        selected_recommendations = res["selected_recommendations"]
        c_match = res["match"]
        c_competition = res["competition"]
        c_betting_house = res["betting_house"]
        c_total_stake = res["total_stake"]
        c_num_picks = res["num_picks"]
        selected_strategies = res["selected_strategies"]

        st.markdown("---")
        st.subheader("PLAN DE APUESTAS RECOMENDADO")

        M = len(selected_recommendations)
        if M == 0:
            st.warning("No se pudieron generar apuestas simples o combinadas seguras con los filtros requeridos en el rango de cuota objetivo de 1.50 a 2.50. Intenta cambiar los parámetros.")
        else:
            for strat_idx, strategy_str in enumerate(selected_strategies):
                st.markdown(f"""
                <div style="border-bottom: 2px solid #E30613; margin-top: 25px; margin-bottom: 15px; padding-bottom: 5px;">
                    <h3 style="color: #ffffff; margin: 0;">Reparto {strategy_str}</h3>
                </div>
                """, unsafe_allow_html=True)
                
                try:
                    pcts = sorted([float(p.strip()) / 100.0 for p in strategy_str.split("/")], reverse=True)
                except Exception:
                    pcts = [1.0 / M] * M
                    
                total_ret_opt = 0.0
                total_prof_opt = 0.0
                
                for idx, rec in enumerate(selected_recommendations):
                    role = "Apuesta principal" if idx == 0 else f"Apuesta secundaria"
                    if idx > 1:
                        role = f"Apuesta secundaria {idx}"
                        
                    pct_val = pcts[idx] if idx < len(pcts) else 0.0
                    stake_val = c_total_stake * pct_val
                    pot_return = stake_val * rec["odds"]
                    pot_profit = pot_return - stake_val
                    
                    total_ret_opt += pot_return
                    total_prof_opt += pot_profit
                    
                    # Translate market to Spanish
                    translated_market = translate_market_to_spanish(rec["market"])
                    
                    legs_html = ""
                    if rec["combined_bet"]:
                        role_text = "Apuesta combinada:"
                        legs_list = [f"<li>{translate_market_to_spanish(leg['market'])} (@{leg['odds']:.2f})</li>" for leg in rec["legs"]]
                        legs_html = f"<ol style='margin: 5px 0; padding-left: 20px; color: #a0aec0;'>{''.join(legs_list)}</ol>"
                    else:
                        role_text = f"{role}:"
                        legs_html = f"<div style='margin-bottom: 8px; font-weight: bold; color: #ffffff;'>{translated_market}</div>"

                    rel_text = get_probability_benefit_relation(rec["probability"], rec["odds"])

                    st.markdown(f"""
                    <div style="background-color: #111111; padding: 18px; border-radius: 10px; border-left: 5px solid #E30613; margin-bottom: 15px; border-top: 1px solid #222222; border-right: 1px solid #222222; border-bottom: 1px solid #222222;">
                        <div style="font-size: 15px; font-weight: bold; color: #E30613; margin-bottom: 5px; text-transform: uppercase;">{role_text}</div>
                        {legs_html}
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 10px; font-size: 14px; color: #a0aec0; margin-top: 10px;">
                            <div><b>Cuota:</b> <span style="color: #ffffff;">{rec['odds']:.2f}</span></div>
                            <div><b>Probabilidad de éxito:</b> <span style="color: #ffffff;">{rec['probability'] * 100.0 if rec['probability'] < 1.0 else rec['probability']:.1f}%</span></div>
                            <div><b>Importe apostado:</b> <span style="color: #ffffff; font-weight: bold;">{stake_val:.2f} €</span></div>
                            <div><b>Retorno potencial:</b> <span style="color: #ffffff;">{pot_return:.2f} €</span></div>
                            <div><b>Beneficio potencial:</b> <span style="color: #00C853; font-weight: bold;">{pot_profit:.2f} €</span></div>
                            <div style="grid-column: span 2;"><b>Relación:</b> <span style="color: #ffd400;">{rel_text}</span></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    is_saved = any(fav["market"] == rec["market"] and fav["match"] == c_match for fav in st.session_state.favorites)
                    if is_saved:
                        st.button("Guardada en favoritas", key=f"save_fav_{strat_idx}_{idx}", disabled=True)
                    else:
                        if st.button("Guardar en favoritas", key=f"save_fav_{strat_idx}_{idx}"):
                            new_fav = {
                                "id": f"{int(time.time())}_{strat_idx}_{idx}",
                                "date_saved": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "match": c_match,
                                "competition": c_competition,
                                "betting_house": c_betting_house,
                                "market": rec["market"],
                                "odds": float(rec["odds"]),
                                "estimated_probability": float(rec["probability"]),
                                "risk": float(rec["risk"]),
                                "uncertainty": float(rec["uncertainty"]),
                                "type": rec["type"],
                                "stake": float(stake_val),
                                "potential_return": float(pot_return),
                                "potential_profit": float(pot_profit),
                                "status": "Favorita",
                                "combined_bet": rec["combined_bet"],
                                "legs": rec["legs"],
                                "sport": "Fútbol"
                            }
                            st.session_state.favorites.append(new_fav)
                            save_favorites()
                            st.success(f"¡Apuesta guardada como favorita!")
                            st.rerun()

                st.markdown(f"""
                <div style="background-color: #111111; padding: 12px 18px; border-radius: 8px; border: 1px solid #E30613; margin-bottom: 25px; display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: bold; color: #ffffff;">Resumen Reparto:</span>
                    <span style="color: #a0aec0;">Importe total: <b style="color: #ffffff;">{c_total_stake:.2f} €</b></span>
                    <span style="color: #a0aec0;">Retorno potencial total: <b style="color: #ffffff;">{total_ret_opt:.2f} €</b></span>
                    <span style="color: #a0aec0;">Beneficio potencial total: <b style="color: #00C853;">{total_prof_opt:.2f} €</b></span>
                </div>
                """, unsafe_allow_html=True)

            # Final summary
            if M == 2:
                best_strat = "75 / 25"
                motive = "Permite asignar una cantidad mayor a la apuesta principal (más probable) mientras se mantiene una cobertura moderada en la apuesta secundaria."
            else: # M == 3
                best_strat = "60 / 25 / 15"
                motive = "Distribuye el capital de forma óptima en tres niveles de probabilidad, maximizando el retorno esperado sin sobreexponer el depósito."
            
            st.markdown(f"""
            <div style="background-color: #111111; padding: 20px; border-radius: 10px; border: 2px solid #ffd400; margin-top: 25px; margin-bottom: 20px;">
                <h3 style="color: #ffd400; margin: 0 0 10px 0;">RESULTADO FINAL</h3>
                <div style="font-size: 16px; color: #ffffff; margin-bottom: 5px;">
                    <b>Mejor reparto recomendado:</b> Reparto {best_strat}
                </div>
                <div style="font-size: 14px; color: #a0aec0;">
                    <b>Motivo:</b> {motive}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Final mini summary (Resumen final)
            st.markdown("""
            <div style="border-bottom: 2px solid #ffd400; margin-top: 35px; margin-bottom: 15px; padding-bottom: 5px;">
                <h3 style="color: #ffffff; margin: 0;">Resumen final</h3>
            </div>
            """, unsafe_allow_html=True)
            
            def mini_summary_sort_key(x):
                balance = x["probability"] * (x["odds"] - 1.0)
                return (-x["probability"], -x.get("safety_score", 0.0), -balance)
                
            mini_summary_bets = sorted(selected_recommendations, key=mini_summary_sort_key)
            for idx, rec in enumerate(mini_summary_bets[:3]):
                m_trans = translate_market_to_spanish(rec["market"])
                rel = get_probability_benefit_relation(rec["probability"], rec["odds"])
                # We can calculate potential profit for a standard 10 € stake
                stake_val = 10.0
                pot_profit = stake_val * (rec["odds"] - 1.0)
                
                # Setup legs if combined
                legs_html = ""
                if rec["combined_bet"]:
                    legs_list = [f"<li>{translate_market_to_spanish(leg['market'])} (@{leg['odds']:.2f})</li>" for leg in rec["legs"]]
                    legs_html = f"<ol style='margin: 5px 0; padding-left: 20px; color: #a0aec0;'>{''.join(legs_list)}</ol>"
                else:
                    legs_html = f"<div style='margin-bottom: 8px; font-weight: bold; color: #ffffff;'>{m_trans}</div>"
                
                st.markdown(f"""
                <div style="background-color: #111111; padding: 15px; border-radius: 8px; border-left: 4px solid #ffd400; margin-bottom: 12px; border-top: 1px solid #222222; border-right: 1px solid #222222; border-bottom: 1px solid #222222;">
                    {legs_html}
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 8px; font-size: 13px; color: #a0aec0; margin-top: 5px;">
                        <div><b>Cuota:</b> <span style="color: #ffffff;">{rec['odds']:.2f}</span></div>
                        <div><b>Probabilidad de éxito:</b> <span style="color: #ffffff;">{rec['probability'] * 100.0 if rec['probability'] < 1.0 else rec['probability']:.1f}%</span></div>
                        <div><b>Beneficio potencial (por cada 10 €):</b> <span style="color: #00C853; font-weight: bold;">{pot_profit:.2f} €</span></div>
                        <div style="grid-column: span 2;"><b>Relación:</b> <span style="color: #ffd400;">{rel}</span></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.caption(
            "Nota: La calculadora estima los valores esperados en base a ajustes estadísticos. Los rendimientos pasados no garantizan resultados futuros."
        )

# ----------------------------------------------------
# SECCIÓN: FAVORITAS
# ----------------------------------------------------
elif section == "Favoritas":
    st.header("Favoritas")
    if not st.session_state.favorites:
        st.info("No tienes apuestas guardadas como favoritas. Haz clic en 'Guardar en favoritas' en los resultados para agregar una.")
    else:
        for idx, fav in enumerate(st.session_state.favorites):
            fav_id = fav.get("id", f"fav_{idx}")
            m_trans = translate_market_to_spanish(fav["market"])
            
            legs_html = ""
            if fav.get("combined_bet"):
                legs_list = [f"<li>{translate_market_to_spanish(leg['market'])} (@{leg['odds']:.2f})</li>" for leg in fav.get("legs", [])]
                legs_html = f"<ol style='margin: 5px 0; padding-left: 20px; color: #a0aec0;'>{''.join(legs_list)}</ol>"
            else:
                legs_html = f"<div style='margin-bottom: 8px; font-weight: bold; color: #ffffff;'>{m_trans}</div>"
                
            fav_rel = get_probability_benefit_relation(fav["estimated_probability"], fav["odds"])
            st.markdown(f"""
            <div style="background-color: #111111; padding: 18px; border-radius: 10px 10px 0 0; border-left: 5px solid #ffd400; border-top: 1px solid #222222; border-right: 1px solid #222222; border-bottom: 1px solid #222222; margin-top: 15px;">
                <div style="display: flex; justify-content: space-between; font-size: 12px; color: #a0aec0; margin-bottom: 5px;">
                    <span>Guardada: {fav.get('date_saved', '')}</span>
                    <span style="color: #ffd400; font-weight: bold;">{fav.get('betting_house', '')}</span>
                </div>
                <div style="font-size: 15px; font-weight: bold; color: #ffffff; margin-bottom: 3px;">{fav.get('match', '')}</div>
                <div style="font-size: 13px; color: #a0aec0; margin-bottom: 8px;">{fav.get('competition', '')}</div>
                {legs_html}
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 10px; font-size: 13px; color: #a0aec0; margin-top: 10px;">
                    <div>Cuota: <span style="color: #ffffff;">{fav['odds']:.2f}</span></div>
                    <div>Probabilidad de éxito: <span style="color: #ffffff;">{fav['estimated_probability'] * 100.0 if fav['estimated_probability'] < 1.0 else fav['estimated_probability']:.1f}%</span></div>
                    <div>Importe apostado: <span style="color: #ffffff;">{fav['stake']:.2f} €</span></div>
                    <div>Retorno potencial: <span style="color: #ffffff;">{fav['potential_return']:.2f} €</span></div>
                    <div>Beneficio potencial: <span style="color: #00C853; font-weight: bold;">{fav['potential_profit']:.2f} €</span></div>
                    <div style="grid-column: span 2;"><b>Relación:</b> <span style="color: #ffd400;">{fav_rel}</span></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Action buttons
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                if st.button("Marcar como realizada", key=f"realize_fav_{fav_id}_{idx}"):
                    new_placed = {
                        "id": f"port_{int(time.time())}_{fav_id}",
                        "date_placed": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "match": fav["match"],
                        "competition": fav.get("competition", ""),
                        "betting_house": fav.get("betting_house", ""),
                        "market": fav["market"],
                        "odds": fav["odds"],
                        "stake": fav["stake"],
                        "status": "Pendiente",
                        "profit": 0.0,
                        "combined_bet": fav.get("combined_bet", False),
                        "legs": fav.get("legs", []),
                        "sport": fav.get("sport", "Fútbol")
                    }
                    if "portfolio" not in st.session_state:
                        st.session_state.portfolio = []
                    st.session_state.portfolio.append(new_placed)
                    save_portfolio()
                    
                    # Remove it from favorites
                    st.session_state.favorites.pop(idx)
                    save_favorites()
                    st.success("¡Apuesta marcada como realizada y movida a la Cartera!")
                    st.rerun()
            with col_b2:
                if st.button("Eliminar de favoritas", key=f"delete_fav_{fav_id}_{idx}"):
                    st.session_state.favorites.pop(idx)
                    save_favorites()
                    st.success("¡Apuesta eliminada de favoritas!")
                    st.rerun()

# ----------------------------------------------------
# SECCIÓN: TOP CUOTAS
# ----------------------------------------------------
elif section == "Top cuotas":
    st.header("Top cuotas")
    if "latest_markets" in st.session_state and st.session_state.latest_markets:
        markets_df_data = []
        for m in st.session_state.latest_markets:
            type_trans = {"Low": "Bajo", "Medium": "Medio", "High": "Alto"}.get(m["Type"], m["Type"])
            markets_df_data.append({
                "Partido": m["Match"],
                "Casa de apuestas": m["BettingHouse"],
                "Apuesta": translate_market_to_spanish(m["Market"]),
                "Cuota": float(m["Odds"]),
                "Probabilidad": f"{m['Probability']:.1f}%",
                "Riesgo": f"{m['Risk']:.1f}%",
                "Incertidumbre": f"{m['Uncertainty']:.1f}%",
                "Tipo": type_trans,
                "Seguridad": float(m["SafetyScore"])
            })
        df_display = pd.DataFrame(markets_df_data)
        df_display = df_display.sort_values(by="Seguridad", ascending=False)
        st.dataframe(df_display, use_container_width=True, hide_index=True)
    else:
        st.info("No se han cargado mercados aún. Sube un CSV y calcula las apuestas en la pestaña de Calculadora.")

# ----------------------------------------------------
# SECCIÓN: CARTERA
# ----------------------------------------------------
elif section == "Cartera":
    st.markdown('<div class="big-title">CARTERA</div>', unsafe_allow_html=True)
    
    if "portfolio" not in st.session_state:
        st.session_state.portfolio = []
        
    portfolio = st.session_state.portfolio
    
    # 1. Global Summary (unfiltered)
    metrics_glob = calculate_balance_metrics(portfolio)
    
    col_g1, col_g2, col_g3 = st.columns(3)
    with col_g1:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">DINERO INVERTIDO</div>
            <div class="metric-value">{metrics_glob["dinero_invertido"]:.2f} €</div>
        </div>
        """, unsafe_allow_html=True)
    with col_g2:
        prof_color = "#00C853" if metrics_glob["beneficio_obtenido"] >= 0 else "#FF3B3B"
        prof_sign = "+" if metrics_glob["beneficio_obtenido"] > 0 else ""
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">BENEFICIO OBTENIDO</div>
            <div class="metric-value" style="color: {prof_color};">{prof_sign}{metrics_glob["beneficio_obtenido"]:.2f} €</div>
        </div>
        """, unsafe_allow_html=True)
    with col_g3:
        roi_color = "#00C853" if metrics_glob["roi_cerrado"] >= 0 else "#FF3B3B"
        roi_sign = "+" if metrics_glob["roi_cerrado"] > 0 else ""
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">ROI CERRADO</div>
            <div class="metric-value" style="color: {roi_color};">{roi_sign}{metrics_glob["roi_cerrado"]:.2f}%</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_g4, col_g5, col_g6, col_g7, col_g8, col_g9 = st.columns(6)
    with col_g4:
        st.markdown(f'<div class="mini-metric-box"><b>Saldo total:</b><br>{metrics_glob["saldo_total"]:.2f} €</div>', unsafe_allow_html=True)
    with col_g5:
        st.markdown(f'<div class="mini-metric-box"><b>Pendientes:</b><br>{metrics_glob["apuestas_pendientes"]}</div>', unsafe_allow_html=True)
    with col_g6:
        st.markdown(f'<div class="mini-metric-box"><b>Cerradas:</b><br>{metrics_glob["apuestas_cerradas"]}</div>', unsafe_allow_html=True)
    with col_g7:
        st.markdown(f'<div class="mini-metric-box"><b>Ganadas:</b><br><span style="color:#00C853">{metrics_glob["apuestas_ganadas"]}</span></div>', unsafe_allow_html=True)
    with col_g8:
        st.markdown(f'<div class="mini-metric-box"><b>Perdidas:</b><br><span style="color:#FF3B3B">{metrics_glob["apuestas_perdidas"]}</span></div>', unsafe_allow_html=True)
    with col_g9:
        st.markdown(f'<div class="mini-metric-box"><b>Nulas:</b><br>{metrics_glob["apuestas_nulas"]}</div>', unsafe_allow_html=True)

    st.markdown("---")

    # 2. Smart Best Bet Types Insights
    st.subheader("Análisis inteligente de tipos de apuesta")
    bet_types = ["Resultado", "Goles", "Córners", "Tarjetas", "Hándicap", "Combinada", "Otro"]
    stats_by_type = {t: {
        "total_bets": 0,
        "closed_bets": 0,
        "wins": 0,
        "losses": 0,
        "win_rate": 0.0,
        "ROI": 0.0,
        "net_profit": 0.0,
        "total_stake": 0.0,
        "total_odds": 0.0,
        "average_odds": 0.0
    } for t in bet_types}

    for bet in portfolio:
        market = bet.get("market", "")
        is_combined = bet.get("combined_bet", False)
        b_type = classify_bet_type(market, is_combined)
        
        status = bet.get("status", "Pendiente")
        stake = float(bet.get("stake", 0.0))
        odds = float(bet.get("odds", 0.0))
        profit = float(bet.get("profit", 0.0))
        
        stats_by_type[b_type]["total_bets"] += 1
        stats_by_type[b_type]["total_odds"] += odds
        
        if status in ["Ganada", "Perdida", "Nula"]:
            stats_by_type[b_type]["closed_bets"] += 1
            stats_by_type[b_type]["total_stake"] += stake
            stats_by_type[b_type]["net_profit"] += profit
            if status == "Ganada":
                stats_by_type[b_type]["wins"] += 1
            elif status == "Perdida":
                stats_by_type[b_type]["losses"] += 1

    valid_types = []
    for t in bet_types:
        data = stats_by_type[t]
        if data["total_bets"] > 0:
            data["average_odds"] = data["total_odds"] / data["total_bets"]
        else:
            data["average_odds"] = 0.0
            
        if data["closed_bets"] > 0:
            data["win_rate"] = data["wins"] / data["closed_bets"]
            data["ROI"] = data["net_profit"] / data["total_stake"]
        else:
            data["win_rate"] = 0.0
            data["ROI"] = 0.0
            
        if data["closed_bets"] >= 3:
            data["weighted_accuracy"] = data["win_rate"] * min(data["closed_bets"] / 10.0, 1.0)
            data["weighted_profitability"] = data["ROI"] * min(data["closed_bets"] / 10.0, 1.0)
            valid_types.append((t, data))

    if len(valid_types) < 1:
        st.info("Todavía no hay suficientes datos para detectar tus mejores tipos de apuesta. Se requieren al menos 3 apuestas cerradas por tipo.")
    else:
        best_acc = sorted(valid_types, key=lambda x: (-x[1]["weighted_accuracy"], -x[1]["closed_bets"], -x[1]["ROI"]))[0]
        best_prof = sorted(valid_types, key=lambda x: (-x[1]["weighted_profitability"], -x[1]["net_profit"], -x[1]["closed_bets"]))[0]
        
        col_i1, col_i2 = st.columns(2)
        with col_i1:
            st.markdown(f"""
            <div class="insight-card">
                <div class="insight-header">TIPO DE APUESTA CON MAYOR ACIERTO</div>
                <div class="insight-title">{best_acc[0]}</div>
                <div class="insight-metric-grid">
                    <div><b>Apuestas:</b> {best_acc[1]["total_bets"]}</div>
                    <div><b>Cerradas:</b> {best_acc[1]["closed_bets"]}</div>
                    <div><b>Tasa acierto:</b> {best_acc[1]["win_rate"]*100:.1f}%</div>
                    <div><b>ROI:</b> {best_acc[1]["ROI"]*100:+.1f}%</div>
                    <div><b>Beneficio neto:</b> <span style="color:{'#00C853' if best_acc[1]['net_profit'] >= 0 else '#FF3B3B'}">{best_acc[1]["net_profit"]:+.2f} €</span></div>
                    <div><b>Cuota media:</b> {best_acc[1]["average_odds"]:.2f}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with col_i2:
            st.markdown(f"""
            <div class="insight-card">
                <div class="insight-header">TIPO DE APUESTA MÁS RENTABLE</div>
                <div class="insight-title">{best_prof[0]}</div>
                <div class="insight-metric-grid">
                    <div><b>Apuestas:</b> {best_prof[1]["total_bets"]}</div>
                    <div><b>Cerradas:</b> {best_prof[1]["closed_bets"]}</div>
                    <div><b>Tasa acierto:</b> {best_prof[1]["win_rate"]*100:.1f}%</div>
                    <div><b>ROI:</b> {best_prof[1]["ROI"]*100:+.1f}%</div>
                    <div><b>Beneficio neto:</b> <span style="color:{'#00C853' if best_prof[1]['net_profit'] >= 0 else '#FF3B3B'}">{best_prof[1]["net_profit"]:+.2f} €</span></div>
                    <div><b>Cuota media:</b> {best_prof[1]["average_odds"]:.2f}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # 3. Filtered Analysis Area
    st.subheader("Análisis filtrado")
    
    all_dates = []
    for b in portfolio:
        dp = b.get("date_placed", "")
        if dp and len(dp) >= 10:
            try:
                all_dates.append(datetime.datetime.strptime(dp[:10], "%Y-%m-%d").date())
            except Exception:
                pass
                
    default_start = datetime.date.today() - datetime.timedelta(days=30)
    default_end = datetime.date.today()
    min_date = min(all_dates) if all_dates else default_start
    max_date = max(all_dates) if all_dates else default_end
    
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        fecha_inicio = st.date_input("Fecha inicial", value=min_date, key="cart_fecha_inicio")
    with col_f2:
        fecha_fin = st.date_input("Fecha final", value=max_date, key="cart_fecha_fin")
        
    all_competitions = sorted(list(set(b.get("competition", "") for b in portfolio if b.get("competition"))))
    competition_options = ["Todos"] + all_competitions
    with col_f3:
        torneo_filtro = st.selectbox("Torneo / competición", options=competition_options, key="cart_torneo_filtro")
        
    # Apply filtering
    filtered_bets = []
    for b in portfolio:
        dp = b.get("date_placed", "")
        bet_date = None
        if dp and len(dp) >= 10:
            try:
                bet_date = datetime.datetime.strptime(dp[:10], "%Y-%m-%d").date()
            except Exception:
                pass
        if bet_date:
            if not (fecha_inicio <= bet_date <= fecha_fin):
                continue
        comp = b.get("competition", "")
        if torneo_filtro != "Todos":
            if comp != torneo_filtro:
                continue
        filtered_bets.append(b)
        
    metrics_filt = calculate_balance_metrics(filtered_bets)
    
    col_rf1, col_rf2, col_rf3, col_rf4 = st.columns(4)
    with col_rf1:
        st.markdown(f'<div class="mini-metric-box"><b>Invertido filtrado:</b><br>{metrics_filt["dinero_invertido"]:.2f} €</div>', unsafe_allow_html=True)
    with col_rf2:
        f_prof_color = "#00C853" if metrics_filt["beneficio_obtenido"] >= 0 else "#FF3B3B"
        f_prof_sign = "+" if metrics_filt["beneficio_obtenido"] > 0 else ""
        st.markdown(f'<div class="mini-metric-box"><b>Beneficio filtrado:</b><br><span style="color:{f_prof_color}">{f_prof_sign}{metrics_filt["beneficio_obtenido"]:.2f} €</span></div>', unsafe_allow_html=True)
    with col_rf3:
        st.markdown(f'<div class="mini-metric-box"><b>Apuestas filtradas:</b><br>{len(filtered_bets)} (Cerradas: {metrics_filt["apuestas_cerradas"]})</div>', unsafe_allow_html=True)
    with col_rf4:
        f_roi_color = "#00C853" if metrics_filt["roi_cerrado"] >= 0 else "#FF3B3B"
        f_roi_sign = "+" if metrics_filt["roi_cerrado"] > 0 else ""
        st.markdown(f'<div class="mini-metric-box"><b>ROI filtrado:</b><br><span style="color:{f_roi_color}">{f_roi_sign}{metrics_filt["roi_cerrado"]:.2f}%</span></div>', unsafe_allow_html=True)
        
    st.markdown("#### Evolución de saldo filtrado")
    df_filt_chart = prepare_chart_data(filtered_bets)
    if not df_filt_chart.empty:
        render_altair_chart(df_filt_chart)
    else:
        st.info("No hay datos suficientes para mostrar el gráfico de evolución filtrado.")

    st.markdown("---")

    # 4. List of Placed Bets (Realizadas)
    st.subheader("Historial de apuestas en cartera")
    if not portfolio:
        st.info("No tienes apuestas en tu cartera. Para añadir una apuesta, ve a la pestaña de 'Favoritas' y haz clic en 'Marcar como realizada'.")
    else:
        placed_bets = sorted(portfolio, key=lambda x: x.get("date_placed", ""), reverse=True)
        for idx, bet in enumerate(placed_bets):
            bet_id = bet.get("id", f"bet_{idx}")
            m_trans = translate_market_to_spanish(bet["market"])
            
            legs_html = ""
            if bet.get("combined_bet"):
                legs_list = [f"<li>{translate_market_to_spanish(leg['market'])} (@{leg['odds']:.2f})</li>" for leg in bet.get("legs", [])]
                legs_html = f"<ol style='margin: 5px 0; padding-left: 20px; color: #a0aec0;'>{''.join(legs_list)}</ol>"
            else:
                legs_html = f"<div style='margin-bottom: 8px; font-weight: bold; color: #ffffff;'>{m_trans}</div>"
                
            status_curr = bet.get("status", "Pendiente")
            if status_curr == "Ganada":
                profit_color = "#00C853"
                profit_prefix = "+"
            elif status_curr == "Perdida":
                profit_color = "#FF3B3B"
                profit_prefix = ""
            else:
                profit_color = "#a0aec0"
                profit_prefix = ""
                
            st.markdown(f"""
            <div style="background-color: #111111; padding: 18px; border-radius: 10px 10px 0 0; border-left: 5px solid {profit_color}; border-top: 1px solid #222222; border-right: 1px solid #222222; border-bottom: 1px solid #222222; margin-top: 15px;">
                <div style="display: flex; justify-content: space-between; font-size: 12px; color: #a0aec0; margin-bottom: 5px;">
                    <span>Realizada: {bet.get('date_placed', '')}</span>
                    <span style="color: #ffd400; font-weight: bold;">{bet.get('betting_house', '')}</span>
                </div>
                <div style="font-size: 15px; font-weight: bold; color: #ffffff; margin-bottom: 3px;">{bet.get('match', '')}</div>
                <div style="font-size: 13px; color: #a0aec0; margin-bottom: 8px;">{bet.get('competition', '')}</div>
                {legs_html}
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 10px; font-size: 13px; color: #a0aec0; margin-top: 10px;">
                    <div>Cuota: <span style="color: #ffffff;">{bet['odds']:.2f}</span></div>
                    <div>Importe apostado: <span style="color: #ffffff;">{bet['stake']:.2f} €</span></div>
                    <div>Retorno potencial: <span style="color: #ffffff;">{(bet['stake'] * bet['odds']):.2f} €</span></div>
                    <div>Resultado: <span style="color: {profit_color}; font-weight: bold;">{profit_prefix}{bet.get('profit', 0.0):.2f} €</span></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            ctrl_col1, ctrl_col2 = st.columns([3, 1])
            with ctrl_col1:
                status_options = ["Pendiente", "Ganada", "Perdida", "Nula"]
                try:
                    status_idx = status_options.index(status_curr)
                except ValueError:
                    status_idx = 0
                    
                new_status = st.selectbox(
                    "Estado de la apuesta",
                    status_options,
                    index=status_idx,
                    key=f"cart_status_select_{bet_id}_{idx}",
                    label_visibility="collapsed"
                )
                
                if new_status != status_curr:
                    for b in st.session_state.portfolio:
                        if b.get("id") == bet_id:
                            b["status"] = new_status
                            if new_status == "Ganada":
                                b["profit"] = b["stake"] * (b["odds"] - 1.0)
                            elif new_status == "Perdida":
                                b["profit"] = -b["stake"]
                            else:
                                b["profit"] = 0.0
                            break
                    save_portfolio()
                    st.rerun()
                    
            with ctrl_col2:
                if st.button("Eliminar", key=f"cart_delete_port_{bet_id}_{idx}"):
                    for b in st.session_state.portfolio:
                        if b.get("id") == bet_id:
                            st.session_state.portfolio.remove(b)
                            break
                    save_portfolio()
                    st.rerun()

# ----------------------------------------------------
# SECCIÓN: ESTADÍSTICAS DEL MODELO
# ----------------------------------------------------
elif section == "Estadísticas del modelo":
    st.header("Estadísticas del modelo")
    st.markdown("Análisis detallado de rendimiento histórico y métricas estadísticas del modelo basándose en tu Cartera.")
    
    if "portfolio" not in st.session_state or not st.session_state.portfolio:
        st.info("No hay datos suficientes para calcular estadísticas. Registra algunas apuestas en la Cartera para ver las estadísticas del modelo.")
    else:
        # Calculate statistics
        total_bets = len(st.session_state.portfolio)
        pending_bets = sum(1 for b in st.session_state.portfolio if b.get("status") == "Pendiente")
        closed_bets = sum(1 for b in st.session_state.portfolio if b.get("status") in ["Ganada", "Perdida", "Nula"])
        won_bets = sum(1 for b in st.session_state.portfolio if b.get("status") == "Ganada")
        lost_bets = sum(1 for b in st.session_state.portfolio if b.get("status") == "Perdida")
        void_bets = sum(1 for b in st.session_state.portfolio if b.get("status") == "Nula")
        
        total_stake = sum(b.get("stake", 0.0) for b in st.session_state.portfolio)
        total_closed_stake = sum(b.get("stake", 0.0) for b in st.session_state.portfolio if b.get("status") in ["Ganada", "Perdida", "Nula"])
        total_profit = sum(b.get("profit", 0.0) for b in st.session_state.portfolio)
        total_returned = sum((b.get("stake", 0.0) + b.get("profit", 0.0)) for b in st.session_state.portfolio if b.get("status") in ["Ganada", "Perdida", "Nula"])
        
        win_rate = (won_bets / closed_bets * 100.0) if closed_bets > 0 else 0.0
        roi = (total_profit / total_closed_stake * 100.0) if total_closed_stake > 0 else 0.0
        
        # Grid layout
        col_m1, col_m2 = st.columns(2)
        
        with col_m1:
            st.subheader("Resumen de actividad")
            st.markdown(f"""
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 20px;">
                <div style="background-color: #111111; padding: 15px; border-radius: 8px; border: 1px solid #222222; text-align: center;">
                    <div style="font-size: 12px; color: #a0aec0; text-transform: uppercase;">Apuestas registradas</div>
                    <div style="font-size: 28px; font-weight: bold; color: #ffffff; margin-top: 5px;">{total_bets}</div>
                </div>
                <div style="background-color: #111111; padding: 15px; border-radius: 8px; border: 1px solid #222222; text-align: center;">
                    <div style="font-size: 12px; color: #a0aec0; text-transform: uppercase;">Apuestas finalizadas</div>
                    <div style="font-size: 28px; font-weight: bold; color: #ffffff; margin-top: 5px;">{closed_bets}</div>
                </div>
                <div style="background-color: #111111; padding: 15px; border-radius: 8px; border: 1px solid #222222; text-align: center;">
                    <div style="font-size: 12px; color: #a0aec0; text-transform: uppercase;">Apuestas pendientes</div>
                    <div style="font-size: 28px; font-weight: bold; color: #ffd400; margin-top: 5px;">{pending_bets}</div>
                </div>
                <div style="background-color: #111111; padding: 15px; border-radius: 8px; border: 1px solid #222222; text-align: center;">
                    <div style="font-size: 12px; color: #a0aec0; text-transform: uppercase;">Tasa de acierto</div>
                    <div style="font-size: 28px; font-weight: bold; color: {'#00C853' if win_rate >= 50 else '#FF3B3B'}; margin-top: 5px;">{win_rate:.1f}%</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with col_m2:
            st.subheader("Rendimiento financiero")
            
            profit_color = "#00C853" if total_profit >= 0 else "#FF3B3B"
            roi_color = "#00C853" if roi >= 0 else "#FF3B3B"
            profit_sign = "+" if total_profit > 0 else ""
            roi_sign = "+" if roi > 0 else ""
            
            st.markdown(f"""
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 20px;">
                <div style="background-color: #111111; padding: 15px; border-radius: 8px; border: 1px solid #222222; text-align: center;">
                    <div style="font-size: 12px; color: #a0aec0; text-transform: uppercase;">Capital invertido</div>
                    <div style="font-size: 24px; font-weight: bold; color: #ffffff; margin-top: 5px;">{total_closed_stake:.2f} €</div>
                </div>
                <div style="background-color: #111111; padding: 15px; border-radius: 8px; border: 1px solid #222222; text-align: center;">
                    <div style="font-size: 12px; color: #a0aec0; text-transform: uppercase;">Capital retornado</div>
                    <div style="font-size: 24px; font-weight: bold; color: #ffffff; margin-top: 5px;">{total_returned:.2f} €</div>
                </div>
                <div style="background-color: #111111; padding: 15px; border-radius: 8px; border: 1px solid #222222; text-align: center; grid-column: span 2;">
                    <div style="display: flex; justify-content: space-around; align-items: center; height: 100%;">
                        <div>
                            <div style="font-size: 12px; color: #a0aec0; text-transform: uppercase;">Resultado neto</div>
                            <div style="font-size: 24px; font-weight: bold; color: {profit_color}; margin-top: 5px;">{profit_sign}{total_profit:.2f} €</div>
                        </div>
                        <div style="border-left: 1px solid #222222; height: 40px;"></div>
                        <div>
                            <div style="font-size: 12px; color: #a0aec0; text-transform: uppercase;">ROI total</div>
                            <div style="font-size: 24px; font-weight: bold; color: {roi_color}; margin-top: 5px;">{roi_sign}{roi:.2f}%</div>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        # Grouped tables
        comp_stats = {}
        house_stats = {}
        type_stats = {"Simple": {"bets": 0, "won": 0, "lost": 0, "stake": 0.0, "profit": 0.0},
                      "Combinada": {"bets": 0, "won": 0, "lost": 0, "stake": 0.0, "profit": 0.0}}
        
        for b in st.session_state.portfolio:
            comp = b.get("competition") or "Otros"
            house = b.get("betting_house") or "Otros"
            status = b.get("status")
            stake = b.get("stake", 0.0)
            profit = b.get("profit", 0.0)
            is_combined = b.get("combined_bet", False)
            b_type = "Combinada" if is_combined else "Simple"
            
            # Grouping competition
            if comp not in comp_stats:
                comp_stats[comp] = {"bets": 0, "won": 0, "lost": 0, "stake": 0.0, "profit": 0.0}
            comp_stats[comp]["bets"] += 1
            if status in ["Ganada", "Perdida", "Nula"]:
                comp_stats[comp]["stake"] += stake
                comp_stats[comp]["profit"] += profit
            if status == "Ganada":
                comp_stats[comp]["won"] += 1
            elif status == "Perdida":
                comp_stats[comp]["lost"] += 1
                
            # Grouping house
            if house not in house_stats:
                house_stats[house] = {"bets": 0, "won": 0, "lost": 0, "stake": 0.0, "profit": 0.0}
            house_stats[house]["bets"] += 1
            if status in ["Ganada", "Perdida", "Nula"]:
                house_stats[house]["stake"] += stake
                house_stats[house]["profit"] += profit
            if status == "Ganada":
                house_stats[house]["won"] += 1
            elif status == "Perdida":
                house_stats[house]["lost"] += 1
                
            # Grouping type
            type_stats[b_type]["bets"] += 1
            if status in ["Ganada", "Perdida", "Nula"]:
                type_stats[b_type]["stake"] += stake
                type_stats[b_type]["profit"] += profit
            if status == "Ganada":
                type_stats[b_type]["won"] += 1
            elif status == "Perdida":
                type_stats[b_type]["lost"] += 1
                
        st.markdown("---")
        st.subheader("Rendimiento por competición")
        comp_rows = []
        for comp, data in comp_stats.items():
            comp_roi = (data["profit"] / data["stake"] * 100.0) if data["stake"] > 0 else 0.0
            comp_rows.append({
                "Competición": comp,
                "Apuestas": data["bets"],
                "Ganadas": data["won"],
                "Perdidas": data["lost"],
                "Capital apostado": f"{data['stake']:.2f} €",
                "Beneficio neto": f"{data['profit']:+.2f} €",
                "ROI": f"{comp_roi:+.1f}%"
            })
        st.dataframe(pd.DataFrame(comp_rows), use_container_width=True, hide_index=True)
        
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.subheader("Rendimiento por casa de apuestas")
            house_rows = []
            for house, data in house_stats.items():
                house_roi = (data["profit"] / data["stake"] * 100.0) if data["stake"] > 0 else 0.0
                house_rows.append({
                    "Casa": house,
                    "Apuestas": data["bets"],
                    "Capital apostado": f"{data['stake']:.2f} €",
                    "Beneficio": f"{data['profit']:+.2f} €",
                    "ROI": f"{house_roi:+.1f}%"
                })
            st.dataframe(pd.DataFrame(house_rows), use_container_width=True, hide_index=True)
            
        with col_t2:
            st.subheader("Rendimiento por tipo de apuesta")
            type_rows = []
            for b_type, data in type_stats.items():
                type_roi = (data["profit"] / data["stake"] * 100.0) if data["stake"] > 0 else 0.0
                type_rows.append({
                    "Tipo": b_type,
                    "Apuestas": data["bets"],
                    "Capital apostado": f"{data['stake']:.2f} €",
                    "Beneficio": f"{data['profit']:+.2f} €",
                    "ROI": f"{type_roi:+.1f}%"
                })
            st.dataframe(pd.DataFrame(type_rows), use_container_width=True, hide_index=True)

elif section == "Asistente manual":
    st.markdown('<div class="big-title">ASISTENTE MANUAL</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background-color: #111111; padding: 20px; border-radius: 8px; border: 1px solid #E30613; margin-bottom: 25px; font-size: 14px; color: #ffffff;">
        El Asistente manual prepara automáticamente los textos que necesitas para analizar partidos o actualizar resultados. La aplicación genera el prompt exacto, tú lo envías a tu asistente de IA y después pegas el CSV recibido para actualizar la calculadora, la cartera y las estadísticas.
        <br><br>
        <b>Pasos a seguir:</b>
        <ol style="margin-left: 20px; margin-top: 5px;">
            <li>Genera el prompt del partido.</li>
            <li>Envía el prompt a tu asistente de IA.</li>
            <li>Pega el CSV devuelto en la aplicación.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("Generar prompt de análisis del partido")
    
    col_ap1, col_ap2 = st.columns(2)
    with col_ap1:
        am_match = st.text_input(
            "Partido", 
            value=st.session_state.get("prompt_match_input", ""), 
            placeholder="Ejemplo: España vs Cabo Verde", 
            key="am_match_input"
        )
        am_comp_select = st.selectbox(
            "Competición",
            [
                "FIFA World Cup 2026",
                "UEFA Euro",
                "Copa América",
                "Africa Cup of Nations",
                "UEFA Champions League",
                "UEFA Europa League",
                "UEFA Conference League",
                "Premier League",
                "LaLiga",
                "Serie A",
                "Bundesliga",
                "Ligue 1",
                "Otro"
            ],
            index=0 if st.session_state.get("prompt_comp_select") not in [
                "FIFA World Cup 2026", "UEFA Euro", "Copa América", "Africa Cup of Nations",
                "UEFA Champions League", "UEFA Europa League", "UEFA Conference League",
                "Premier League", "LaLiga", "Serie A", "Bundesliga", "Ligue 1", "Otro"
            ] else [
                "FIFA World Cup 2026", "UEFA Euro", "Copa América", "Africa Cup of Nations",
                "UEFA Champions League", "UEFA Europa League", "UEFA Conference League",
                "Premier League", "LaLiga", "Serie A", "Bundesliga", "Ligue 1", "Otro"
            ].index(st.session_state.get("prompt_comp_select")),
            key="am_comp_select_widget"
        )
        if am_comp_select == "Otro":
            am_competition = st.text_input(
                "Competición personalizada",
                value=st.session_state.get("prompt_comp_custom", ""),
                placeholder="Ejemplo: Amistoso Internacional",
                key="am_comp_custom"
            )
        else:
            am_competition = am_comp_select
            
        am_phase = st.selectbox(
            "Fase", 
            ["Fase de grupos", "Eliminatoria", "Semifinal", "Final"], 
            index=["Fase de grupos", "Eliminatoria", "Semifinal", "Final"].index(st.session_state.get("prompt_phase_input", "Fase de grupos")),
            key="am_phase_input"
        )
    with col_ap2:
        am_house_select = st.selectbox(
            "Casa de apuestas",
            [
                "Winamax",
                "Bet365",
                "Codere",
                "Betfair",
                "Bwin",
                "Marathonbet",
                "1xBet",
                "Betway",
                "William Hill",
                "Pinnacle",
                "Otro"
            ],
            index=0 if st.session_state.get("prompt_house_select") not in [
                "Winamax", "Bet365", "Codere", "Betfair", "Bwin", "Marathonbet",
                "1xBet", "Betway", "William Hill", "Pinnacle", "Otro"
            ] else [
                "Winamax", "Bet365", "Codere", "Betfair", "Bwin", "Marathonbet",
                "1xBet", "Betway", "William Hill", "Pinnacle", "Otro"
            ].index(st.session_state.get("prompt_house_select")),
            key="am_house_select_widget"
        )
        if am_house_select == "Otro":
            am_house = st.text_input(
                "Casa de apuestas personalizada",
                value=st.session_state.get("prompt_house_custom", ""),
                placeholder="Ejemplo: Sportium",
                key="am_house_custom"
            )
        else:
            am_house = am_house_select
        am_presets = st.multiselect(
            "Tipo de análisis de mercados",
            [
                "Análisis completo",
                "Apuestas conservadoras / seguras",
                "Mercados principales de resultado",
                "Goles",
                "Córners",
                "Tarjetas",
                "Tiros",
                "Hándicaps",
                "Personalizado"
            ],
            default=st.session_state.get("prompt_market_presets", ["Análisis completo"]),
            key="am_market_presets"
        )
        
    if "am_generated_analysis_prompt" not in st.session_state:
        st.session_state.am_generated_analysis_prompt = ""
        
    if st.button("GENERAR PROMPT DE ANÁLISIS", key="am_generate_analysis_btn", use_container_width=True):
        cleaned_match = clean_match_name(am_match)
        phase_mapping = {
            "Fase de grupos": "Group",
            "Eliminatoria": "Knockout",
            "Semifinal": "Semifinal",
            "Final": "Final"
        }
        am_phase_eng = phase_mapping.get(am_phase, am_phase)
        preset_mapping = {
            "Análisis completo": "1X2, double chance, draw no bet, goals, under/over 2.5, under/over 3.5, both teams to score, team goals, corners, team corners, cards, team cards, shots, shots on target, handicaps, Asian handicaps",
            "Apuestas conservadoras / seguras": "double chance, draw no bet, under/over 3.5 goals, team under/over goals, team corners, team cards, low-risk handicap lines",
            "Mercados principales de resultado": "1X2, double chance, draw no bet, halftime/fulltime, team to score first, win to nil",
            "Goles": "goals, under/over 1.5, under/over 2.5, under/over 3.5, both teams to score, team goals, clean sheet, win to nil",
            "Córners": "total corners, under/over corners, team corners, corner handicap, first half corners",
            "Tarjetas": "total cards, team cards, most cards, player cards if lineups are available, cards handicap",
            "Tiros": "total shots, team shots, shots on target, player shots if lineups are available, player shots on target if lineups are available",
            "Hándicaps": "European handicaps, Asian handicaps, favorite handicap, underdog positive handicap, low-risk handicap lines"
        }
        markets_list = []
        for pr in am_presets:
            if pr in preset_mapping:
                for item in preset_mapping[pr].split(","):
                    item_clean = item.strip()
                    if item_clean and item_clean not in markets_list:
                        markets_list.append(item_clean)
        if "Personalizado" in am_presets:
            custom_markets = st.session_state.get("prompt_markets_custom_input", "")
            if custom_markets:
                for item in custom_markets.split(","):
                    item_clean = item.strip()
                    if item_clean and item_clean not in markets_list:
                        markets_list.append(item_clean)
        am_markets = ", ".join(markets_list)
        prompt_text = f"""Please search current information about the football match "{cleaned_match}" in the "{am_competition}" ({am_phase_eng} phase).
Review odds, lineups, injuries, suspensions, recent form, FIFA ranking or Elo, tactical context, referee if available, corners, cards, goals and shots. Use "{am_house}" as the betting house preference if possible.

Based on your research and analysis, estimate probabilities for the following markets: {am_markets}

You must return ONLY a CSV with exactly these columns:
Market,Odds,Probability,Risk,Uncertainty,Type

CSV rules:
- Odds must be in decimal format.
- Probability must be a number from 0 to 100.
- Risk must be a number from 0 to 100.
- Uncertainty must be a number from 0 to 100.
- Type must be Low, Medium or High.
- Do not include explanations outside the CSV.
- Do not include markdown code fences.
- Do not include markets without odds.
- If data is missing, increase uncertainty.
- Do not force bets.
- Only include markets with realistic potential value.

Here is the model formula for context:
EV* = [(Estimated Probability − λ × Uncertainty − ρ × Risk) × Odds] − 1

Please be conservative with:
- finals,
- knockout matches,
- low odds favorites,
- aggressive handicaps,
- under bets based only on defensive style,
- cards totals without referee information."""
        st.session_state.am_generated_analysis_prompt = prompt_text
        save_or_update_studied_match(
            match=cleaned_match,
            competition=am_competition,
            phase=am_phase,
            betting_house=am_house,
            presets=am_presets,
            custom_markets=st.session_state.get("prompt_markets_custom_input", "")
        )
        
    st.text_area(
        "Prompt de análisis de IA",
        value=st.session_state.am_generated_analysis_prompt,
        height=250,
        key="am_analysis_prompt_area"
    )
    escaped_analysis_prompt = json.dumps(st.session_state.am_generated_analysis_prompt)
    copy_analysis_html = f"""
    <style>
    body {{ margin: 0; padding: 0; background-color: transparent; overflow: hidden; }}
    button {{
        background-color: #E30613; color: #ffffff; border: 2px solid #ff4d4d; border-radius: 8px;
        font-weight: 700; padding: 0.6rem 2.5rem; transition: all 0.3s ease; width: 100%;
        text-transform: uppercase; letter-spacing: 1px; font-family: sans-serif; cursor: pointer;
    }}
    button:hover {{ background-color: #ffffff !important; color: #E30613 !important; border-color: #ffffff !important; }}
    </style>
    <button id="copy-analysis-btn">COPIAR PROMPT DE ANÁLISIS</button>
    <div id="status-analysis" style="color: #00C853; font-weight: bold; font-family: sans-serif; margin-top: 8px; font-size: 14px; text-align: center; display: none;">Prompt copiado al portapapeles</div>
    <script>
    document.getElementById('copy-analysis-btn').addEventListener('click', function() {{
        const text = {escaped_analysis_prompt};
        if (!text) {{
            const status = document.getElementById('status-analysis');
            status.innerText = "No se ha generado ningún prompt aún";
            status.style.color = "#FF3B3B";
            status.style.display = "block";
            setTimeout(() => {{ status.style.display = "none"; }}, 3000);
            return;
        }}
        navigator.clipboard.writeText(text).then(() => {{
            const status = document.getElementById('status-analysis');
            status.innerText = "Prompt copiado al portapapeles";
            status.style.color = "#00C853";
            status.style.display = "block";
            setTimeout(() => {{ status.style.display = "none"; }}, 3000);
        }}).catch(() => {{
            const status = document.getElementById('status-analysis');
            status.innerText = "Fallo la copia. Por favor selecciona y copia manualmente.";
            status.style.color = "#FF3B3B";
            status.style.display = "block";
        }});
    }});
    </script>
    """
    st.components.v1.html(copy_analysis_html, height=75)
    
    st.markdown("---")
    st.subheader("Generar prompt para actualizar resultados pendientes")
    if "am_generated_results_prompt" not in st.session_state:
        st.session_state.am_generated_results_prompt = ""
    if st.button("GENERAR PROMPT DE RESULTADOS PENDIENTES", key="am_generate_results_btn", use_container_width=True):
        pending_bets = [b for b in st.session_state.get("portfolio", []) if b.get("status") == "Pendiente"]
        if not pending_bets:
            st.session_state.am_generated_results_prompt = "No hay apuestas pendientes en la Cartera para actualizar."
        else:
            bets_list_str = []
            for b in pending_bets:
                legs_str = ""
                if b.get("combined_bet"):
                    legs_str = " (Combined legs: " + ", ".join([f"{leg['market']} (@{leg['odds']:.2f})" for leg in b.get("legs", [])]) + ")"
                bets_list_str.append(
                    f"- BetID: {b['id']}\n"
                    f"  Match: {b['match']}\n"
                    f"  Competition: {b.get('competition', '')}\n"
                    f"  Betting house: {b.get('betting_house', '')}\n"
                    f"  Bet name: {b['market']}{legs_str}\n"
                    f"  Odds: {b['odds']:.2f}\n"
                    f"  Stake: {b['stake']:.2f} EUR\n"
                    f"  Date saved: {b.get('date_placed', '')}"
                )
            bets_formatted = "\n\n".join(bets_list_str)
            prompt_text = f"""Please verify the final results for the following football bets:

{bets_formatted}

Verify the final score of each match. Check goals, cards, corners, shots or handicaps if needed to determine if the bet won, lost, or was voided.

You must return ONLY a CSV with exactly these columns:
BetID,Status,FinalScore,Reason

CSV rules:
- Status must be exactly one of: Ganada, Perdida, Nula, Pendiente.
- If the match has not been played yet or the result is not final, return Pendiente.
- If the result cannot be verified, return Pendiente.
- FinalScore must be the match score (e.g. "Spain 3-0 Cape Verde") or relevant stat result.
- Reason must be a short explanation of the result verification (e.g. "Bet landed", "Under 2.5 goals failed").
- Do not include explanations outside the CSV.
- Do not include markdown code fences."""
            st.session_state.am_generated_results_prompt = prompt_text
            
    st.text_area(
        "Prompt de actualización de resultados",
        value=st.session_state.am_generated_results_prompt,
        height=250,
        key="am_results_prompt_area"
    )
    escaped_results_prompt = json.dumps(st.session_state.am_generated_results_prompt)
    copy_results_html = f"""
    <style>
    body {{ margin: 0; padding: 0; background-color: transparent; overflow: hidden; }}
    button {{
        background-color: #E30613; color: #ffffff; border: 2px solid #ff4d4d; border-radius: 8px;
        font-weight: 700; padding: 0.6rem 2.5rem; transition: all 0.3s ease; width: 100%;
        text-transform: uppercase; letter-spacing: 1px; font-family: sans-serif; cursor: pointer;
    }}
    button:hover {{ background-color: #ffffff !important; color: #E30613 !important; border-color: #ffffff !important; }}
    </style>
    <button id="copy-results-btn">COPIAR PROMPT DE RESULTADOS</button>
    <div id="status-results" style="color: #00C853; font-weight: bold; font-family: sans-serif; margin-top: 8px; font-size: 14px; text-align: center; display: none;">Prompt copiado al portapapeles</div>
    <script>
    document.getElementById('copy-results-btn').addEventListener('click', function() {{
        const text = {escaped_results_prompt};
        if (!text) {{
            const status = document.getElementById('status-results');
            status.innerText = "No se ha generado ningún prompt aún";
            status.style.color = "#FF3B3B";
            status.style.display = "block";
            setTimeout(() => {{ status.style.display = "none"; }}, 3000);
            return;
        }}
        navigator.clipboard.writeText(text).then(() => {{
            const status = document.getElementById('status-results');
            status.innerText = "Prompt copiado al portapapeles";
            status.style.color = "#00C853";
            status.style.display = "block";
            setTimeout(() => {{ status.style.display = "none"; }}, 3000);
        }}).catch(() => {{
            const status = document.getElementById('status-results');
            status.innerText = "Fallo la copia. Por favor selecciona y copia manualmente.";
            status.style.color = "#FF3B3B";
            status.style.display = "block";
        }});
    }});
    </script>
    """
    st.components.v1.html(copy_results_html, height=75)
    
    st.markdown("---")
    st.subheader("Actualizar cartera con CSV de resultados")
    csv_results_input = st.text_area(
        "Pegar CSV de resultados",
        placeholder="BetID,Status,FinalScore,Reason\nport_123456789_fav_123,Ganada,Spain 3-0 Cape Verde,Bet landed\nport_987654321_fav_456,Perdida,Belgium 1-1 Egypt,Bet did not land",
        height=150,
        key="am_csv_results_input"
    )
    if st.button("ACTUALIZAR CARTERA CON RESULTADOS", key="am_update_portfolio_btn", use_container_width=True):
        if not csv_results_input.strip():
            st.error("Por favor, pega el CSV de resultados antes de hacer clic en el botón.")
        else:
            try:
                df_results = pd.read_csv(StringIO(csv_results_input))
                df_results.columns = [c.strip() for c in df_results.columns]
                required_cols = ["BetID", "Status", "FinalScore", "Reason"]
                missing_cols = [col for col in required_cols if col not in df_results.columns]
                if missing_cols:
                    st.error(f"Error: Al CSV le faltan las columnas requeridas: {', '.join(missing_cols)}")
                else:
                    updated_count = 0
                    for _, row in df_results.iterrows():
                        bet_id = str(row["BetID"]).strip()
                        status = str(row["Status"]).strip()
                        final_score = str(row["FinalScore"]).strip()
                        reason = str(row["Reason"]).strip()
                        for b in st.session_state.portfolio:
                            if str(b.get("id")).strip() == bet_id:
                                if status in ["Ganada", "Perdida", "Nula", "Pendiente"]:
                                    b["status"] = status
                                    b["final_score"] = final_score
                                    b["reason"] = reason
                                    if status == "Ganada":
                                        b["profit"] = b["stake"] * (b["odds"] - 1.0)
                                    elif status == "Perdida":
                                        b["profit"] = -b["stake"]
                                    else:
                                        b["profit"] = 0.0
                                    updated_count += 1
                                break
                    if updated_count > 0:
                        save_portfolio()
                        st.success(f"Se han actualizado correctamente {updated_count} apuestas en la Cartera.")
                        st.rerun()
                    else:
                        st.warning("No se encontró ninguna apuesta con los BetIDs proporcionados en la Cartera o el formato es incorrecto.")
            except Exception as e:
                st.error(f"Error al procesar el CSV de resultados: {str(e)}")

# ----------------------------------------------------
# SECCIÓN: HISTORIAL DE PARTIDOS ESTUDIADOS
# ----------------------------------------------------
elif section == "Historial de partidos estudiados":
    st.markdown('<div class="big-title">HISTORIAL DE PARTIDOS ESTUDIADOS</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background-color: #111111; padding: 12px; border-radius: 6px; border: 1px solid #ffd400; margin-bottom: 20px; font-size: 13px; color: #ffffff;">
        <b>Nota de cuotas:</b> Las cuotas guardadas pertenecen al último análisis realizado. Para actualizar la información del partido, vuelve a generar el prompt y pega un nuevo CSV.
    </div>
    """, unsafe_allow_html=True)
    load_studied_matches()
    matches = st.session_state.studied_matches
    if not matches:
        st.info("Aún no has analizado ningún partido. Ve a la Calculadora y genera un prompt o calcula apuestas para registrarlos en el historial.")
    else:
        for idx, entry in enumerate(sorted(matches, key=lambda x: x.get("last_updated", ""), reverse=True)):
            match_name = entry.get("match", "")
            comp = entry.get("competition", "")
            house = entry.get("betting_house", "")
            last_up = entry.get("last_updated", "")
            presets_used = ", ".join(entry.get("selected_market_presets", ["Análisis completo"]))
            recs = entry.get("last_recommendations", [])
            recs_text = ""
            if recs:
                recs_list = []
                for r in recs[:2]:
                    m_trans = translate_market_to_spanish(r.get("market", ""))
                    recs_list.append(f"{m_trans} (@{r.get('odds', 0.0):.2f})")
                recs_text = " — ".join(recs_list)
            else:
                recs_text = "Sin recomendaciones previas"
                
            st.markdown(f"""
            <div style="background-color: #111111; padding: 18px; border-radius: 10px 10px 0 0; border-left: 5px solid #E30613; border-top: 1px solid #222222; border-right: 1px solid #222222; border-bottom: 1px solid #222222; margin-top: 15px;">
                <div style="display: flex; justify-content: space-between; font-size: 12px; color: #a0aec0; margin-bottom: 5px;">
                    <span>Último análisis: {last_up}</span>
                    <span style="color: #E30613; font-weight: bold;">{house}</span>
                </div>
                <div style="font-size: 16px; font-weight: bold; color: #ffffff; margin-bottom: 3px;">{match_name}</div>
                <div style="font-size: 13px; color: #a0aec0; margin-bottom: 8px;">{comp} ({entry.get('phase', 'Fase de grupos')})</div>
                <div style="font-size: 13px; color: #ffd400; margin-bottom: 8px;"><b>Presets de mercados:</b> {presets_used}</div>
                <div style="font-size: 13px; color: #00C853;"><b>Últimas recomendaciones:</b> {recs_text}</div>
            </div>
            """, unsafe_allow_html=True)
            
            col_b1, col_b2, col_b3, col_b4 = st.columns(4)
            with col_b1:
                if st.button("Cargar en calculadora", key=f"hist_load_{idx}"):
                    st.session_state.prompt_match_input = match_name
                    if comp in [
                        "FIFA World Cup 2026", "UEFA Euro", "Copa América", "Africa Cup of Nations",
                        "UEFA Champions League", "UEFA Europa League", "UEFA Conference League",
                        "Premier League", "LaLiga", "Serie A", "Bundesliga", "Ligue 1"
                    ]:
                        st.session_state.prompt_comp_select = comp
                    else:
                        st.session_state.prompt_comp_select = "Otro"
                        st.session_state.prompt_comp_custom = comp
                    st.session_state.prompt_phase_input = entry.get("phase", "Fase de grupos")
                    if house in [
                        "Winamax", "Bet365", "Codere", "Betfair", "Bwin", "Marathonbet",
                        "1xBet", "Betway", "William Hill", "Pinnacle"
                    ]:
                        st.session_state.prompt_house_select = house
                    else:
                        st.session_state.prompt_house_select = "Otro"
                        st.session_state.prompt_house_custom = house
                    st.session_state.prompt_market_presets = entry.get("selected_market_presets", ["Análisis completo"])
                    st.session_state.prompt_markets_custom_input = entry.get("custom_markets", "")
                    
                    st.session_state.config_match = match_name
                    st.session_state.config_competition = comp
                    st.session_state.config_phase = entry.get("phase", "Fase de grupos")
                    st.session_state.config_betting_house = house
                    
                    st.session_state.current_section = "Calculadora"
                    st.success("¡Partido cargado en la calculadora!")
                    st.rerun()
            with col_b2:
                if st.button("Volver a generar prompt", key=f"hist_prompt_{idx}"):
                    cleaned_m = clean_match_name(match_name)
                    presets = entry.get("selected_market_presets", ["Análisis completo"])
                    custom_m = entry.get("custom_markets", "")
                    phase = entry.get("phase", "Fase de grupos")
                    phase_mapping = {
                        "Fase de grupos": "Group",
                        "Eliminatoria": "Knockout",
                        "Semifinal": "Semifinal",
                        "Final": "Final"
                    }
                    p_eng = phase_mapping.get(phase, phase)
                    preset_mapping = {
                        "Análisis completo": "1X2, double chance, draw no bet, goals, under/over 2.5, under/over 3.5, both teams to score, team goals, corners, team corners, cards, team cards, shots, shots on target, handicaps, Asian handicaps",
                        "Apuestas conservadoras / seguras": "double chance, draw no bet, under/over 3.5 goals, team under/over goals, team corners, team cards, low-risk handicap lines",
                        "Mercados principales de resultado": "1X2, double chance, draw no bet, halftime/fulltime, team to score first, win to nil",
                        "Goles": "goals, under/over 1.5, under/over 2.5, under/over 3.5, both teams to score, team goals, clean sheet, win to nil",
                        "Córners": "total corners, under/over corners, team corners, corner handicap, first half corners",
                        "Tarjetas": "total cards, team cards, most cards, player cards if lineups are available, cards handicap",
                        "Tiros": "total shots, team shots, shots on target, player shots if lineups are available, player shots on target if lineups are available",
                        "Hándicaps": "European handicaps, Asian handicaps, favorite handicap, underdog positive handicap, low-risk handicap lines"
                    }
                    markets_list = []
                    for pr in presets:
                        if pr in preset_mapping:
                            for item in preset_mapping[pr].split(","):
                                item_clean = item.strip()
                                if item_clean and item_clean not in markets_list:
                                    markets_list.append(item_clean)
                    if custom_m:
                        for item in custom_m.split(","):
                            item_clean = item.strip()
                            if item_clean and item_clean not in markets_list:
                                markets_list.append(item_clean)
                    p_markets = ", ".join(markets_list)
                    fresh_prompt = f"""Please search current information about the football match "{cleaned_m}" in the "{comp}" ({p_eng} phase).
Use the most recent available odds and current match information. Do not reuse old odds.
Review updated odds, lineups, injuries, suspensions, recent form, FIFA ranking or Elo, tactical context, referee if available, corners, cards, goals and shots. Use "{house}" as the betting house preference if possible.

Based on your research and analysis, estimate probabilities for the following markets: {p_markets}

You must return ONLY a CSV with exactly these columns:
Market,Odds,Probability,Risk,Uncertainty,Type

CSV rules:
- Odds must be in decimal format.
- Probability must be a number from 0 to 100.
- Risk must be a number from 0 to 100.
- Uncertainty must be a number from 0 to 100.
- Type must be Low, Medium or High.
- Do not include explanations outside the CSV.
- Do not include markdown code fences.
- Do not include markets without odds.
- If data is missing, increase uncertainty.
- Do not force bets.
- Only include markets with realistic potential value.

Here is the model formula for context:
EV* = [(Estimated Probability − λ × Uncertainty − ρ × Risk) × Odds] − 1

Please be conservative with:
- finals,
- knockout matches,
- low odds favorites,
- aggressive handicaps,
- under bets based only on defensive style,
- cards totals without referee information."""
                    st.session_state.fresh_prompt_text = fresh_prompt
                    st.session_state.fresh_prompt_match = match_name
                    st.rerun()
            with col_b3:
                last_csv = entry.get("last_csv", "")
                if last_csv:
                    exp_csv = st.expander("Ver CSV guardado")
                    with exp_csv:
                        st.code(last_csv, language="csv")
                else:
                    st.button("Sin CSV guardado", key=f"hist_csv_none_{idx}", disabled=True)
            with col_b4:
                if st.button("Eliminar del historial", key=f"hist_delete_{idx}"):
                    st.session_state.studied_matches.remove(entry)
                    save_studied_matches()
                    st.success("¡Partido eliminado del historial!")
                    st.rerun()
                    
        if "fresh_prompt_text" in st.session_state and "fresh_prompt_match" in st.session_state:
            st.markdown("---")
            st.subheader(f"Prompt de análisis actualizado: {st.session_state.fresh_prompt_match}")
            st.text_area("Prompt (copia y envía a tu asistente de IA)", value=st.session_state.fresh_prompt_text, height=250, key="fresh_prompt_area")
            escaped_fresh_prompt = json.dumps(st.session_state.fresh_prompt_text)
            copy_fresh_html = f"""
            <style>
            body {{ margin: 0; padding: 0; background-color: transparent; overflow: hidden; }}
            button {{
                background-color: #E30613; color: #ffffff; border: 2px solid #ff4d4d; border-radius: 8px;
                font-weight: 700; padding: 0.6rem 2.5rem; transition: all 0.3s ease; width: 100%;
                text-transform: uppercase; letter-spacing: 1px; font-family: sans-serif; cursor: pointer;
            }}
            button:hover {{ background-color: #ffffff !important; color: #E30613 !important; border-color: #ffffff !important; }}
            </style>
            <button id="copy-fresh-btn">COPIAR PROMPT ACTUALIZADO</button>
            <div id="status-fresh" style="color: #00C853; font-weight: bold; font-family: sans-serif; margin-top: 8px; font-size: 14px; text-align: center; display: none;">Prompt copiado al portapapeles</div>
            <script>
            document.getElementById('copy-fresh-btn').addEventListener('click', function() {{
                const text = {escaped_fresh_prompt};
                navigator.clipboard.writeText(text).then(() => {{
                    const status = document.getElementById('status-fresh');
                    status.innerText = "Prompt copiado al portapapeles";
                    status.style.color = "#00C853";
                    status.style.display = "block";
                    setTimeout(() => {{ status.style.display = "none"; }}, 3000);
                }}).catch(() => {{
                    const status = document.getElementById('status-fresh');
                    status.innerText = "Fallo la copia. Por favor selecciona y copia manualmente.";
                    status.style.color = "#FF3B3B";
                    status.style.display = "block";
                }});
            }});
            </script>
            """
            st.components.v1.html(copy_fresh_html, height=75)

# ----------------------------------------------------
# SECCIÓN: EVOLUCIÓN DEL SALDO
# ----------------------------------------------------
elif section == "Evolución del saldo":
    st.markdown('<div class="big-title">EVOLUCIÓN DEL SALDO</div>', unsafe_allow_html=True)
    portfolio = st.session_state.get("portfolio", [])
    metrics_glob = calculate_balance_metrics(portfolio)
    col_e1, col_e2, col_e3, col_e4 = st.columns(4)
    with col_e1:
        e_saldo_color = "#00C853" if metrics_glob["saldo_total"] >= 0 else "#FF3B3B"
        e_saldo_sign = "+" if metrics_glob["saldo_total"] > 0 else ""
        st.markdown(f'<div class="mini-metric-box"><b>Saldo total:</b><br><span style="color:{e_saldo_color}; font-size:18px; font-weight:bold;">{e_saldo_sign}{metrics_glob["saldo_total"]:.2f} €</span></div>', unsafe_allow_html=True)
    with col_e2:
        st.markdown(f'<div class="mini-metric-box"><b>Beneficio total:</b><br><span style="color:{e_saldo_color}; font-size:18px; font-weight:bold;">{e_saldo_sign}{metrics_glob["beneficio_obtenido"]:.2f} €</span></div>', unsafe_allow_html=True)
    with col_e3:
        st.markdown(f'<div class="mini-metric-box"><b>Dinero invertido:</b><br><span style="font-size:18px; font-weight:bold;">{metrics_glob["dinero_invertido"]:.2f} €</span></div>', unsafe_allow_html=True)
    with col_e4:
        e_roi_color = "#00C853" if metrics_glob["roi_cerrado"] >= 0 else "#FF3B3B"
        e_roi_sign = "+" if metrics_glob["roi_cerrado"] > 0 else ""
        st.markdown(f'<div class="mini-metric-box"><b>ROI cerrado:</b><br><span style="color:{e_roi_color}; font-size:18px; font-weight:bold;">{e_roi_sign}{metrics_glob["roi_cerrado"]:.2f}%</span></div>', unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Evolución temporal del saldo")
    df_chart = prepare_chart_data(portfolio)
    if not df_chart.empty:
        render_altair_chart(df_chart)
    else:
        st.info("No hay datos de apuestas finalizadas en la Cartera para mostrar el gráfico de evolución.")
        
    st.markdown("<br>", unsafe_allow_html=True)
    exp1 = st.expander("Detalle por torneo")
    with exp1:
        comp_stats_evo = {}
        for b in portfolio:
            comp = b.get("competition") or "Otros"
            status = b.get("status", "Pendiente")
            stake = float(b.get("stake", 0.0))
            profit = float(b.get("profit", 0.0))
            if comp not in comp_stats_evo:
                comp_stats_evo[comp] = {"total_bets": 0, "closed_bets": 0, "wins": 0, "stake": 0.0, "profit": 0.0}
            comp_stats_evo[comp]["total_bets"] += 1
            if status in ["Ganada", "Perdida", "Nula"]:
                comp_stats_evo[comp]["closed_bets"] += 1
                comp_stats_evo[comp]["stake"] += stake
                comp_stats_evo[comp]["profit"] += profit
                if status == "Ganada":
                    comp_stats_evo[comp]["wins"] += 1
        if comp_stats_evo:
            comp_rows = []
            for comp, cdata in comp_stats_evo.items():
                c_roi = (cdata["profit"] / cdata["stake"] * 100.0) if cdata["stake"] > 0 else 0.0
                c_acc = (cdata["wins"] / cdata["closed_bets"] * 100.0) if cdata["closed_bets"] > 0 else 0.0
                comp_rows.append({
                    "Competición": comp,
                    "Apuestas": cdata["total_bets"],
                    "Invertido": f"{cdata['stake']:.2f} €",
                    "Beneficio": f"{cdata['profit']:+.2f} €",
                    "ROI": f"{c_roi:+.1f}%",
                    "Acierto": f"{c_acc:.1f}%"
                })
            st.dataframe(pd.DataFrame(comp_rows), use_container_width=True, hide_index=True)
        else:
            st.info("No hay datos suficientes para mostrar el desglose por torneo.")
            
    exp2 = st.expander("Detalle por tipo de apuesta")
    with exp2:
        bet_types = ["Resultado", "Goles", "Córners", "Tarjetas", "Hándicap", "Combinada", "Otro"]
        stats_by_type = {t: {
            "total_bets": 0,
            "closed_bets": 0,
            "wins": 0,
            "losses": 0,
            "win_rate": 0.0,
            "ROI": 0.0,
            "net_profit": 0.0,
            "total_stake": 0.0,
            "total_odds": 0.0,
            "average_odds": 0.0
        } for t in bet_types}
        for b in portfolio:
            market = b.get("market", "")
            is_combined = b.get("combined_bet", False)
            b_type = classify_bet_type(market, is_combined)
            status = b.get("status", "Pendiente")
            stake = float(b.get("stake", 0.0))
            odds = float(b.get("odds", 0.0))
            profit = float(b.get("profit", 0.0))
            stats_by_type[b_type]["total_bets"] += 1
            stats_by_type[b_type]["total_odds"] += odds
            if status in ["Ganada", "Perdida", "Nula"]:
                stats_by_type[b_type]["closed_bets"] += 1
                stats_by_type[b_type]["total_stake"] += stake
                stats_by_type[b_type]["net_profit"] += profit
                if status == "Ganada":
                    stats_by_type[b_type]["wins"] += 1
                elif status == "Perdida":
                    stats_by_type[b_type]["losses"] += 1
        type_rows = []
        for t in bet_types:
            tdata = stats_by_type[t]
            if tdata["total_bets"] > 0:
                tdata["average_odds"] = tdata["total_odds"] / tdata["total_bets"]
            if tdata["closed_bets"] > 0:
                tdata["win_rate"] = tdata["wins"] / tdata["closed_bets"]
                tdata["ROI"] = tdata["net_profit"] / tdata["total_stake"]
            t_roi = tdata["ROI"] * 100.0
            t_acc = tdata["win_rate"] * 100.0
            type_rows.append({
                "Tipo de apuesta": t,
                "Apuestas cerradas": tdata["closed_bets"],
                "Acierto": f"{t_acc:.1f}%",
                "Beneficio": f"{tdata['net_profit']:+.2f} €",
                "ROI": f"{t_roi:+.1f}%",
                "Cuota media": f"{tdata['average_odds']:.2f}"
            })
        st.dataframe(pd.DataFrame(type_rows), use_container_width=True, hide_index=True)
        
    exp3 = st.expander("Historial cronológico")
    with exp3:
        if portfolio:
            chrono_rows = []
            for b in sorted(portfolio, key=lambda x: x.get("date_placed", ""), reverse=True):
                chrono_rows.append({
                    "Fecha": b.get("date_placed", "")[:10] if b.get("date_placed") else "",
                    "Partido": b.get("match", ""),
                    "Competición": b.get("competition", ""),
                    "Casa de apuestas": b.get("betting_house", ""),
                    "Apuesta": translate_market_to_spanish(b.get("market", "")),
                    "Cuota": f"{float(b.get('odds', 0.0)):.2f}",
                    "Importe": f"{float(b.get('stake', 0.0)):.2f} €",
                    "Estado": b.get("status", "Pendiente"),
                    "Beneficio": f"{float(b.get('profit', 0.0)):+.2f} €"
                })
            st.dataframe(pd.DataFrame(chrono_rows), use_container_width=True, hide_index=True)
        else:
            st.info("No hay apuestas en la Cartera para mostrar en el historial.")
