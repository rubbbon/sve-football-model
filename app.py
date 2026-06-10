import streamlit as st
import pandas as pd
from io import StringIO
import os
import json
import time
import datetime
import re

# Favorites database file
FAVORITES_FILE = "favorites.json"
PORTFOLIO_FILE = "portfolio.json"

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

# Load databases at startup
load_favorites()
load_portfolio()

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

# Page configurations
st.set_page_config(
    page_title="CALCULADOR DE APUESTAS",
    page_icon="⚽",
    layout="wide"
)

# Custom Injectable CSS styling to achieve the requested red, black, and white professional trading theme
st.markdown("""
<style>
/* Dark base background for the entire dashboard */
.stApp {
    background-color: #0b0d10 !important;
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
    background-color: #12161a !important;
    padding: 22px !important;
    border-radius: 12px !important;
    border: 1px solid #262c35 !important;
    margin-bottom: 20px !important;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2) !important;
}

.formula {
    background-color: #12161a;
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
    background-color: #12161a !important;
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
    background-color: #12161a !important;
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
    background-color: #12161a !important;
    border: 1px solid #E30613 !important;
}

div[data-baseweb="popover"] li {
    background-color: #12161a !important;
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
    background-color: #12161a !important;
    border: 1px solid #262c35 !important;
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

# Main Title Section
st.markdown('<div class="big-title">CALCULADOR DE APUESTAS</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Motor de análisis estadístico de fútbol y calculadora de combinadas de valor</div>', unsafe_allow_html=True)

# Define Tabs
tab1, tab2, tab3, tab4 = st.tabs(["1. Calculadora", "2. Favoritas", "3. Top cuotas", "4. Cartera"])

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
# TAB 1: LIVE MODEL
# ----------------------------------------------------
with tab1:
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
    ">✓ Prompt copiado al portapapeles</div>
    
    <script>
    document.getElementById('copy-btn').addEventListener('click', function() {{
        const text = {escaped_prompt};
        if (!text) {{
            const status = document.getElementById('status');
            status.innerText = "✕ No se ha generado ningún prompt aún";
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
            status.innerText = "✓ Prompt copiado al portapapeles";
            status.style.color = "#00ff88";
            status.style.display = "block";
            setTimeout(() => {{ status.style.display = "none"; }}, 3000);
        }}
        
        function showError() {{
            const status = document.getElementById('status');
            status.innerText = "✕ Falló la copia. Por favor selecciona y copia manualmente.";
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
        num_picks = st.slider("Número de apuestas recomendadas", 2, 3, int(st.session_state.config_num_picks) if st.session_state.config_num_picks in [2, 3] else 2)
        
        if num_picks == 2:
            strategy_options = ["50 / 50", "60 / 40", "70 / 30", "75 / 25", "80 / 20"]
        else:
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
                    st.subheader("📋 Vista previa de mercados cargados")
                    st.dataframe(df_input, use_container_width=True)
        except Exception as e:
            st.error(f"Error al analizar el archivo CSV: {str(e)}")

    st.header("4. Resultados del modelo")

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
        st.subheader("🏆 PLAN DE APUESTAS RECOMENDADO")

        M = len(selected_recommendations)
        if M == 0:
            st.warning("No se pudieron generar apuestas simples o combinadas seguras con los filtros requeridos en el rango de cuota objetivo de 1.50 a 2.50. Intenta cambiar los parámetros.")
        else:
            for strat_idx, strategy_str in enumerate(selected_strategies):
                st.markdown(f"""
                <div style="border-bottom: 2px solid #E30613; margin-top: 25px; margin-bottom: 15px; padding-bottom: 5px;">
                    <h3 style="color: #ffffff; margin: 0;">Opción {strat_idx + 1} — Reparto {strategy_str}</h3>
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

                    st.markdown(f"""
                    <div style="background-color: #12161a; padding: 18px; border-radius: 10px; border-left: 5px solid #E30613; margin-bottom: 15px; border-top: 1px solid #262c35; border-right: 1px solid #262c35; border-bottom: 1px solid #262c35;">
                        <div style="font-size: 15px; font-weight: bold; color: #E30613; margin-bottom: 5px; text-transform: uppercase;">{role_text}</div>
                        {legs_html}
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 10px; font-size: 14px; color: #a0aec0; margin-top: 10px;">
                            <div><b>Cuota:</b> <span style="color: #ffffff;">{rec['odds']:.2f}</span></div>
                            <div><b>Probabilidad estimada:</b> <span style="color: #ffffff;">{rec['probability'] * 100.0 if rec['probability'] < 1.0 else rec['probability']:.1f}%</span></div>
                            <div><b>Importe:</b> <span style="color: #ffffff; font-weight: bold;">{stake_val:.2f} €</span></div>
                            <div><b>Retorno potencial:</b> <span style="color: #ffffff;">{pot_return:.2f} €</span></div>
                            <div><b>Beneficio potencial:</b> <span style="color: #00C853; font-weight: bold;">{pot_profit:.2f} €</span></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    is_saved = any(fav["market"] == rec["market"] and fav["match"] == c_match for fav in st.session_state.favorites)
                    if is_saved:
                        st.button("✓ Guardada en favoritas", key=f"save_fav_{strat_idx}_{idx}", disabled=True)
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
                                "legs": rec["legs"]
                            }
                            st.session_state.favorites.append(new_fav)
                            save_favorites()
                            st.success(f"¡Apuesta guardada como favorita!")
                            st.rerun()

                st.markdown(f"""
                <div style="background-color: #1a1e24; padding: 12px 18px; border-radius: 8px; border: 1px solid #E30613; margin-bottom: 25px; display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: bold; color: #ffffff;">Resumen Opción:</span>
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
            <div style="background-color: #12161a; padding: 20px; border-radius: 10px; border: 2px solid #ffd400; margin-top: 25px; margin-bottom: 20px;">
                <h3 style="color: #ffd400; margin: 0 0 10px 0;">RESULTADO FINAL</h3>
                <div style="font-size: 16px; color: #ffffff; margin-bottom: 5px;">
                    <b>Mejor opción recomendada:</b> {best_strat}
                </div>
                <div style="font-size: 14px; color: #a0aec0;">
                    <b>Motivo:</b> {motive}
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.caption(
            "Nota: La calculadora estima los valores esperados en base a ajustes estadísticos. Los rendimientos pasados no garantizan resultados futuros."
        )

# ----------------------------------------------------
# TAB 2: FAVORITAS
# ----------------------------------------------------
with tab2:
    st.header("2. Apuestas favoritas")
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
                
            st.markdown(f"""
            <div style="background-color: #12161a; padding: 18px; border-radius: 10px 10px 0 0; border-left: 5px solid #ffd400; border-top: 1px solid #262c35; border-right: 1px solid #262c35; border-bottom: 1px solid #262c35; margin-top: 15px;">
                <div style="display: flex; justify-content: space-between; font-size: 12px; color: #a0aec0; margin-bottom: 5px;">
                    <span>📅 Guardada: {fav.get('date_saved', '')}</span>
                    <span style="color: #ffd400; font-weight: bold;">{fav.get('betting_house', '')}</span>
                </div>
                <div style="font-size: 15px; font-weight: bold; color: #ffffff; margin-bottom: 3px;">{fav.get('match', '')}</div>
                <div style="font-size: 13px; color: #a0aec0; margin-bottom: 8px;">{fav.get('competition', '')}</div>
                {legs_html}
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 10px; font-size: 13px; color: #a0aec0; margin-top: 10px;">
                    <div>Cuota: <span style="color: #ffffff;">{fav['odds']:.2f}</span></div>
                    <div>Probabilidad: <span style="color: #ffffff;">{fav['estimated_probability'] * 100.0 if fav['estimated_probability'] < 1.0 else fav['estimated_probability']:.1f}%</span></div>
                    <div>Importe: <span style="color: #ffffff;">{fav['stake']:.2f} €</span></div>
                    <div>Retorno: <span style="color: #ffffff;">{fav['potential_return']:.2f} €</span></div>
                    <div>Beneficio: <span style="color: #00C853; font-weight: bold;">{fav['potential_profit']:.2f} €</span></div>
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
                        "legs": fav.get("legs", [])
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
# TAB 3: TOP CUOTAS
# ----------------------------------------------------
with tab3:
    st.header("3. Top cuotas de mercados analizados")
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
# TAB 4: CARTERA
# ----------------------------------------------------
with tab4:
    st.header("4. Cartera de apuestas")
    
    if "portfolio" not in st.session_state:
        st.session_state.portfolio = []
        
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.subheader("Historial de apuestas realizadas")
        if not st.session_state.portfolio:
            st.info("No tienes apuestas en tu cartera. Para añadir una apuesta, ve a la pestaña de 'Favoritas' y haz clic en 'Marcar como realizada'.")
        else:
            placed_bets = sorted(st.session_state.portfolio, key=lambda x: x.get("date_placed", ""), reverse=True)
            
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
                <div style="background-color: #12161a; padding: 18px; border-radius: 10px 10px 0 0; border-left: 5px solid {profit_color}; border-top: 1px solid #262c35; border-right: 1px solid #262c35; border-bottom: 1px solid #262c35; margin-top: 15px;">
                    <div style="display: flex; justify-content: space-between; font-size: 12px; color: #a0aec0; margin-bottom: 5px;">
                        <span>📅 Realizada: {bet.get('date_placed', '')}</span>
                        <span style="color: #ffd400; font-weight: bold;">{bet.get('betting_house', '')}</span>
                    </div>
                    <div style="font-size: 15px; font-weight: bold; color: #ffffff; margin-bottom: 3px;">{bet.get('match', '')}</div>
                    <div style="font-size: 13px; color: #a0aec0; margin-bottom: 8px;">{bet.get('competition', '')}</div>
                    {legs_html}
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 10px; font-size: 13px; color: #a0aec0; margin-top: 10px;">
                        <div>Cuota: <span style="color: #ffffff;">{bet['odds']:.2f}</span></div>
                        <div>Importe: <span style="color: #ffffff;">{bet['stake']:.2f} €</span></div>
                        <div>Retorno: <span style="color: #ffffff;">{(bet['stake'] * bet['odds']):.2f} €</span></div>
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
                        key=f"status_select_{bet_id}_{idx}",
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
                    if st.button("Eliminar", key=f"delete_port_{bet_id}_{idx}"):
                        for b in st.session_state.portfolio:
                            if b.get("id") == bet_id:
                                st.session_state.portfolio.remove(b)
                                break
                        save_portfolio()
                        st.rerun()
                        
    with col_right:
        st.subheader("Resumen de rendimiento")
        
        total_bets = len(st.session_state.portfolio)
        pending_bets = sum(1 for b in st.session_state.portfolio if b.get("status") == "Pendiente")
        closed_bets = sum(1 for b in st.session_state.portfolio if b.get("status") in ["Ganada", "Perdida", "Nula"])
        won_bets = sum(1 for b in st.session_state.portfolio if b.get("status") == "Ganada")
        lost_bets = sum(1 for b in st.session_state.portfolio if b.get("status") == "Perdida")
        
        saldo_total = sum(b.get("profit", 0.0) for b in st.session_state.portfolio)
        
        total_closed_stake = sum(b.get("stake", 0.0) for b in st.session_state.portfolio if b.get("status") in ["Ganada", "Perdida", "Nula"])
        total_closed_profit = sum(b.get("profit", 0.0) for b in st.session_state.portfolio if b.get("status") in ["Ganada", "Perdida", "Nula"])
        
        if total_closed_stake > 0:
            roi_cerrado = (total_closed_profit / total_closed_stake) * 100.0
        else:
            roi_cerrado = 0.0
            
        if saldo_total > 0:
            saldo_color = "#00C853"
            saldo_sign = "+"
        elif saldo_total < 0:
            saldo_color = "#FF3B3B"
            saldo_sign = ""
        else:
            saldo_color = "#ffffff"
            saldo_sign = ""
            
        st.markdown(f"""
        <div style="background-color: #12161a; padding: 25px; border-radius: 12px; border: 2px solid #262c35; text-align: center; margin-bottom: 20px;">
            <div style="font-size: 14px; font-weight: bold; color: #a0aec0; text-transform: uppercase; letter-spacing: 1px;">SALDO TOTAL</div>
            <div style="font-size: 38px; font-weight: 800; color: {saldo_color}; margin-top: 10px;">{saldo_sign}{saldo_total:.2f} €</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 15px;">
            <div style="background-color: #12161a; padding: 12px; border-radius: 8px; border: 1px solid #262c35; text-align: center;">
                <div style="font-size: 11px; color: #a0aec0; text-transform: uppercase;">Total Apuestas</div>
                <div style="font-size: 20px; font-weight: bold; color: #ffffff; margin-top: 2px;">{total_bets}</div>
            </div>
            <div style="background-color: #12161a; padding: 12px; border-radius: 8px; border: 1px solid #262c35; text-align: center;">
                <div style="font-size: 11px; color: #a0aec0; text-transform: uppercase;">Pendientes</div>
                <div style="font-size: 20px; font-weight: bold; color: #ffd400; margin-top: 2px;">{pending_bets}</div>
            </div>
            <div style="background-color: #12161a; padding: 12px; border-radius: 8px; border: 1px solid #262c35; text-align: center;">
                <div style="font-size: 11px; color: #a0aec0; text-transform: uppercase;">Ganadas</div>
                <div style="font-size: 20px; font-weight: bold; color: #00C853; margin-top: 2px;">{won_bets}</div>
            </div>
            <div style="background-color: #12161a; padding: 12px; border-radius: 8px; border: 1px solid #262c35; text-align: center;">
                <div style="font-size: 11px; color: #a0aec0; text-transform: uppercase;">Perdidas</div>
                <div style="font-size: 20px; font-weight: bold; color: #ff3b30; margin-top: 2px;">{lost_bets}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if roi_cerrado > 0:
            roi_color = "#00C853"
            roi_sign = "+"
        elif roi_cerrado < 0:
            roi_color = "#FF3B3B"
            roi_sign = ""
        else:
            roi_color = "#ffffff"
            roi_sign = ""
            
        st.markdown(f"""
        <div style="background-color: #12161a; padding: 15px; border-radius: 8px; border: 1px solid #262c35; text-align: center;">
            <div style="font-size: 12px; color: #a0aec0; text-transform: uppercase; letter-spacing: 0.5px;">ROI Cerrado</div>
            <div style="font-size: 24px; font-weight: bold; color: {roi_color}; margin-top: 5px;">{roi_sign}{roi_cerrado:.2f}%</div>
            <div style="font-size: 11px; color: #718096; margin-top: 5px;">Basado en {closed_bets} apuestas finalizadas (Inversión: {total_closed_stake:.2f} €)</div>
        </div>
        """, unsafe_allow_html=True)
