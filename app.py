import streamlit as st
import pandas as pd
from io import StringIO
import os
import json
import time
import datetime

# Favorites database file
FAVORITES_FILE = "favorites.json"

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

# Load favorites at startup
load_favorites()

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
    color: #f0f2f5 !important;
}

/* Page titles and headers */
.big-title {
    font-size: 38px;
    font-weight: 800;
    color: #e63946;
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
    border-left: 4px solid #e63946;
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

/* Red backgrounds for inputs, text areas and select boxes with black text */
input[type="text"], input[type="number"], textarea {
    background-color: #e63946 !important;
    color: #000000 !important;
    border: 2px solid #ff6b6b !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 15px !important;
}

/* Placeholders inside inputs and textareas */
input::placeholder, textarea::placeholder {
    color: #2d3748 !important;
    opacity: 0.8 !important;
}

/* Selectbox container styling */
div[data-baseweb="select"] > div {
    background-color: #e63946 !important;
    color: #000000 !important;
    border: 2px solid #ff6b6b !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}

/* Selected option text inside selectbox */
div[data-baseweb="select"] span {
    color: #000000 !important;
    font-weight: 600 !important;
}

/* Selectbox dropdown arrow */
div[data-baseweb="select"] svg {
    fill: #000000 !important;
}

/* Dropdown list popover styling */
div[data-baseweb="popover"] {
    background-color: #e63946 !important;
    border: 1px solid #ff6b6b !important;
}

div[data-baseweb="popover"] li {
    background-color: #e63946 !important;
    color: #000000 !important;
    font-weight: 600 !important;
}

div[data-baseweb="popover"] li:hover {
    background-color: #ff8585 !important;
    color: #000000 !important;
}

/* Tabs styles */
div[data-testid="stTabBar"] button {
    color: #a0aec0 !important;
    font-size: 16px !important;
    font-weight: 600 !important;
}

div[data-testid="stTabBar"] button[aria-selected="true"] {
    color: #e63946 !important;
    border-bottom-color: #e63946 !important;
}

/* Plus and minus buttons of Streamlit number inputs */
button[kind="secondary"] {
    background-color: #e63946 !important;
    color: #000000 !important;
    border: 1px solid #ff6b6b !important;
}
button[kind="secondary"]:hover {
    background-color: #ff8585 !important;
    color: #000000 !important;
}

/* Styled Primary Buttons */
div.stButton > button {
    background-color: #e63946 !important;
    color: #ffffff !important;
    border: 2px solid #ff6b6b !important;
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
    color: #e63946 !important;
    border-color: #ffffff !important;
    box-shadow: 0 0 15px rgba(230, 57, 70, 0.4) !important;
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
tab1, tab2, tab3 = st.tabs(["1. Calculadora", "2. Favoritas", "3. Top cuotas"])

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
    if "config_recommendation_style" not in st.session_state:
        st.session_state.config_recommendation_style = "Valor práctico"
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

        prompt_preset = st.selectbox(
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
            key="prompt_market_preset"
        )
        st.caption("Elige Análisis completo para un examen detallado del modelo, o selecciona un área específica como Goles, Córners, Tarjetas o Tiros.")
        
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
        
        if prompt_preset == "Personalizado":
            prompt_markets = st.text_area(
                "Mercados personalizados a analizar",
                placeholder="Ejemplo: Córners de España, tarjetas de Cabo Verde, más de 1.5 goles de España",
                height=125,
                key="prompt_markets_custom"
            )
        else:
            prompt_markets = preset_mapping[prompt_preset]
    
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
        bankroll = st.number_input("Depósito (€)", min_value=1.0, value=100.0, step=10.0)
        total_stake = st.number_input("Cantidad total a apostar (€)", min_value=1.0, value=st.session_state.config_total_stake, step=1.0)
        num_picks = st.slider("Número de apuestas recomendadas", 1, 5, int(st.session_state.config_num_picks))
        stake_strategy = st.selectbox(
            "Estrategia de reparto", 
            ["Reparto equilibrado", "Principal + secundaria", "Conservadora"], 
            index=["Reparto equilibrado", "Principal + secundaria", "Conservadora"].index(st.session_state.config_stake_strategy)
        )

    with col3:
        reliability = st.selectbox("Fiabilidad de los datos", ["Alta", "Media", "Baja"], key="config_reliability")
        model_mode = st.selectbox("Modo del modelo", ["Conservador", "Equilibrado", "Agresivo"], key="config_model_mode")
        recommendation_style = st.selectbox(
            "Estilo de recomendación",
            ["Valor práctico", "Valor estricto", "Seguridad conservadora"],
            key="config_recommendation_style"
        )
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
            # Map Spanish selectbox values to English for calculations
            model_mode_eng = {
                "Conservador": "Conservative",
                "Equilibrado": "Balanced",
                "Agresivo": "Aggressive"
            }.get(model_mode, "Balanced")

            phase_eng = {
                "Fase de grupos": "Group",
                "Eliminatoria": "Knockout",
                "Semifinal": "Semifinal",
                "Final": "Final"
            }.get(phase, "Group")

            reliability_eng = {
                "Alta": "High",
                "Media": "Medium",
                "Baja": "Low"
            }.get(reliability, "Medium")

            recommendation_style_eng = {
                "Valor práctico": "Practical Value",
                "Valor estricto": "Strict Value",
                "Seguridad conservadora": "Conservative Safety"
            }.get(recommendation_style, "Practical Value")

            # Model mode configuration parameters (lambda and rho)
            if model_mode_eng == "Conservative":
                lamb = 0.25
                rho = 0.25
            elif model_mode_eng == "Balanced":
                lamb = 0.18
                rho = 0.18
            else:  # Aggressive
                lamb = 0.12
                rho = 0.12

            # Phase-based minimum adjusted EV thresholds (theta)
            if phase_eng == "Group":
                theta = 0.04
            elif phase_eng == "Knockout":
                theta = 0.06
            elif phase_eng == "Semifinal":
                theta = 0.07
            else:  # Final
                theta = 0.08

            # Reliability adjustments
            if reliability_eng == "Medium":
                theta += 0.01
            elif reliability_eng == "Low":
                theta += 0.03

            results = []
            for _, row in df_input.iterrows():
                market = str(row["Market"])
                odds = float(row["Odds"])
                prob = float(row["Probability"]) / 100.0
                risk = float(row["Risk"]) / 100.0
                uncertainty = float(row["Uncertainty"]) / 100.0
                risk_type = str(row["Type"]).strip()

                # Model calculations
                implied_prob = 1.0 / odds
                edge = prob - implied_prob
                simple_ev = (prob * odds) - 1.0
                adj_prob = prob - (lamb * uncertainty) - (rho * risk)
                adj_ev = (adj_prob * odds) - 1.0

                # Scores
                safety_score = (prob * 100.0) - (risk * 50.0) - (uncertainty * 50.0)
                final_ranking_score = (adj_ev * 100.0) + (prob * 30.0) - (risk * 20.0) - (uncertainty * 20.0)

                # Classification logic
                if recommendation_style_eng == "Strict Value":
                    if odds >= cuota_minima and uncertainty < 0.35 and adj_ev > theta:
                        decision = "VALUE BET"
                    elif (
                        (prob >= 0.60 and risk <= 0.20 and uncertainty <= 0.25 and odds >= 1.25 and simple_ev > -0.08) or
                        (prob >= 0.70 and risk <= 0.18 and uncertainty <= 0.25 and odds >= 1.15) or
                        (adj_ev >= theta - 0.04 and prob >= 0.55 and uncertainty <= 0.25)
                    ):
                        decision = "SAFE PICK"
                    elif simple_ev > 0:
                        decision = "WATCHLIST"
                    else:
                        decision = "NO BET"

                elif recommendation_style_eng == "Practical Value":
                    is_strict_value = (odds >= cuota_minima and uncertainty < 0.35 and adj_ev > theta)
                    is_practical_value = (
                        (odds >= cuota_minima and uncertainty <= 0.25 and risk <= 0.25 and simple_ev >= 0.03 and adj_ev >= -0.03) or
                        (adj_ev > theta - 0.03 and simple_ev > 0 and prob >= 0.55 and uncertainty <= 0.25)
                    )
                    
                    if is_strict_value:
                        decision = "VALUE BET"
                    elif is_practical_value:
                        decision = "PRACTICAL VALUE"
                    elif (
                        (prob >= 0.60 and risk <= 0.20 and uncertainty <= 0.25 and odds >= 1.25 and simple_ev > -0.08) or
                        (prob >= 0.70 and risk <= 0.18 and uncertainty <= 0.25 and odds >= 1.15) or
                        (adj_ev >= theta - 0.04 and prob >= 0.55 and uncertainty <= 0.25)
                    ):
                        decision = "SAFE PICK"
                    elif simple_ev > 0:
                        decision = "WATCHLIST"
                    else:
                        decision = "NO BET"

                else:  # Conservative Safety
                    is_conservative_safe = (prob >= 0.65 and risk <= 0.22 and uncertainty <= 0.25 and odds >= 1.15)
                    is_strict_value = (odds >= cuota_minima and uncertainty < 0.35 and adj_ev > theta)
                    
                    if is_conservative_safe:
                        decision = "SAFE PICK"
                    elif is_strict_value:
                        decision = "VALUE BET"
                    elif simple_ev > 0:
                        decision = "WATCHLIST"
                    else:
                        decision = "NO BET"

                # Stake sizing
                if decision in ["VALUE BET", "PRACTICAL VALUE", "SAFE PICK"]:
                    risk_type_cap = risk_type.capitalize()
                    if risk_type_cap == "Low":
                        stake = bankroll * 0.015
                    elif risk_type_cap == "Medium":
                        stake = bankroll * 0.010
                    elif risk_type_cap == "High":
                        stake = bankroll * 0.005
                    else:
                        stake = bankroll * 0.010  # default fallback
                else:
                    stake = 0.0

                results.append({
                    "Market": market,
                    "Odds": odds,
                    "Estimated Probability": prob,
                    "Implied Probability": implied_prob,
                    "Edge": edge,
                    "Adjusted Probability": adj_prob,
                    "Simple EV": simple_ev,
                    "Adjusted EV": adj_ev,
                    "Risk Type": risk_type,
                    "Recommended Stake": stake,
                    "Decision": decision,
                    "Safety Score": safety_score,
                    "Final Ranking Score": final_ranking_score,
                    "Recommendation Style Used": recommendation_style
                })

            df_results = pd.DataFrame(results)

            # Build simple and combined bet recommendations (odds between cuota_minima and cuota_maxima)
            candidates = []
            n_rows = len(df_input)
            
            # Size 1 (Simple bets)
            for i in range(n_rows):
                row = df_input.iloc[i]
                odds = float(row["Odds"])
                prob = float(row["Probability"])
                risk = float(row["Risk"])
                unc = float(row["Uncertainty"])
                risk_type = str(row["Type"]).strip()
                
                if cuota_minima <= odds <= cuota_maxima:
                    candidates.append({
                        "combined_bet": False,
                        "legs": [{"market": row["Market"], "odds": odds, "probability": prob, "risk": risk, "uncertainty": unc, "type": risk_type}],
                        "market": row["Market"],
                        "odds": odds,
                        "probability": prob,
                        "risk": risk,
                        "uncertainty": unc,
                        "type": risk_type,
                        "safety_score": prob - (risk * 0.5) - (unc * 0.5)
                    })
            
            # Size 2 (Combined bets)
            if allow_combined:
                for i in range(n_rows):
                    for j in range(i + 1, n_rows):
                        row1 = df_input.iloc[i]
                        row2 = df_input.iloc[j]
                        
                        c_odds = float(row1["Odds"]) * float(row2["Odds"])
                        if cuota_minima <= c_odds <= cuota_maxima:
                            c_prob = (float(row1["Probability"]) / 100.0) * (float(row2["Probability"]) / 100.0) * 100.0
                            c_risk = max(float(row1["Risk"]), float(row2["Risk"]))
                            c_unc = max(float(row1["Uncertainty"]), float(row2["Uncertainty"]))
                            
                            type_map = {"Low": 1, "Medium": 2, "High": 3}
                            inv_type_map = {1: "Low", 2: "Medium", 3: "High"}
                            t1 = type_map.get(str(row1["Type"]).strip(), 2)
                            t2 = type_map.get(str(row2["Type"]).strip(), 2)
                            c_type = inv_type_map[max(t1, t2)]
                            
                            candidates.append({
                                "combined_bet": True,
                                "legs": [
                                    {"market": row1["Market"], "odds": float(row1["Odds"]), "probability": float(row1["Probability"]), "risk": float(row1["Risk"]), "uncertainty": float(row1["Uncertainty"]), "type": row1["Type"]},
                                    {"market": row2["Market"], "odds": float(row2["Odds"]), "probability": float(row2["Probability"]), "risk": float(row2["Risk"]), "uncertainty": float(row2["Uncertainty"]), "type": row2["Type"]}
                                ],
                                "market": f"{row1['Market']} + {row2['Market']}",
                                "odds": c_odds,
                                "probability": c_prob,
                                "risk": c_risk,
                                "uncertainty": c_unc,
                                "type": c_type,
                                "safety_score": c_prob - (c_risk * 0.5) - (c_unc * 0.5)
                            })
                            
                # Size 3 (Combined bets)
                for i in range(n_rows):
                    for j in range(i + 1, n_rows):
                        for k in range(j + 1, n_rows):
                            row1 = df_input.iloc[i]
                            row2 = df_input.iloc[j]
                            row3 = df_input.iloc[k]
                            
                            c_odds = float(row1["Odds"]) * float(row2["Odds"]) * float(row3["Odds"])
                            if cuota_minima <= c_odds <= cuota_maxima:
                                c_prob = (float(row1["Probability"]) / 100.0) * (float(row2["Probability"]) / 100.0) * (float(row3["Probability"]) / 100.0) * 100.0
                                c_risk = max(float(row1["Risk"]), float(row2["Risk"]), float(row3["Risk"]))
                                c_unc = max(float(row1["Uncertainty"]), float(row2["Uncertainty"]), float(row3["Uncertainty"]))
                                
                                type_map = {"Low": 1, "Medium": 2, "High": 3}
                                inv_type_map = {1: "Low", 2: "Medium", 3: "High"}
                                t1 = type_map.get(str(row1["Type"]).strip(), 2)
                                t2 = type_map.get(str(row2["Type"]).strip(), 2)
                                t3 = type_map.get(str(row3["Type"]).strip(), 2)
                                c_type = inv_type_map[max(t1, t2, t3)]
                                
                                candidates.append({
                                    "combined_bet": True,
                                    "legs": [
                                        {"market": row1["Market"], "odds": float(row1["Odds"]), "probability": float(row1["Probability"]), "risk": float(row1["Risk"]), "uncertainty": float(row1["Uncertainty"]), "type": row1["Type"]},
                                        {"market": row2["Market"], "odds": float(row2["Odds"]), "probability": float(row2["Probability"]), "risk": float(row2["Risk"]), "uncertainty": float(row2["Uncertainty"]), "type": row2["Type"]},
                                        {"market": row3["Market"], "odds": float(row3["Odds"]), "probability": float(row3["Probability"]), "risk": float(row3["Risk"]), "uncertainty": float(row3["Uncertainty"]), "type": row3["Type"]}
                                    ],
                                    "market": f"{row1['Market']} + {row2['Market']} + {row3['Market']}",
                                    "odds": c_odds,
                                    "probability": c_prob,
                                    "risk": c_risk,
                                    "uncertainty": c_unc,
                                    "type": c_type,
                                    "safety_score": c_prob - (c_risk * 0.5) - (c_unc * 0.5)
                                })
                                
            # Sort candidates by probability descending, safety score descending
            candidates_sorted = sorted(candidates, key=lambda x: (x["probability"], x["safety_score"], x["odds"]), reverse=True)
            
            selected_recommendations = []
            used_markets = set()
            for cand in candidates_sorted:
                cand_markets = {leg["market"] for leg in cand["legs"]}
                if not (cand_markets & used_markets):
                    selected_recommendations.append(cand)
                    used_markets.update(cand_markets)
                if len(selected_recommendations) >= num_picks:
                    break

            # Calculate stakes
            rec_stakes = []
            M = len(selected_recommendations)
            if M > 0:
                if M == 1:
                    rec_stakes = [total_stake]
                elif M == 2:
                    if stake_strategy == "Reparto equilibrado":
                        rec_stakes = [total_stake * 0.5, total_stake * 0.5]
                    elif stake_strategy == "Principal + secundaria":
                        rec_stakes = [total_stake * 0.75, total_stake * 0.25]
                    else:  # Conservadora
                        rec_stakes = [total_stake * 0.80, total_stake * 0.20]
                elif M == 3:
                    if stake_strategy == "Reparto equilibrado":
                        rec_stakes = [total_stake / 3.0, total_stake / 3.0, total_stake / 3.0]
                    elif stake_strategy == "Principal + secundaria":
                        rec_stakes = [total_stake * 0.60, total_stake * 0.25, total_stake * 0.15]
                    else:  # Conservadora
                        rec_stakes = [total_stake * 0.70, total_stake * 0.20, total_stake * 0.10]
                else:
                    if stake_strategy == "Reparto equilibrado":
                        rec_stakes = [total_stake / M] * M
                    elif stake_strategy == "Principal + secundaria":
                        rec_stakes = [total_stake * 0.50] + [total_stake * 0.50 / (M - 1)] * (M - 1)
                    else:  # Conservadora
                        rec_stakes = [total_stake * 0.60] + [total_stake * 0.40 / (M - 1)] * (M - 1)

            # Store in session state
            st.session_state.calculated_results = {
                "df_results": df_results,
                "selected_recommendations": selected_recommendations,
                "rec_stakes": rec_stakes,
                "match": match,
                "competition": competition,
                "betting_house": betting_house,
                "total_stake": total_stake,
                "num_picks": num_picks,
                "stake_strategy": stake_strategy
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
        df_results = res["df_results"]
        selected_recommendations = res["selected_recommendations"]
        rec_stakes = res["rec_stakes"]
        c_match = res["match"]
        c_competition = res["competition"]
        c_betting_house = res["betting_house"]
        c_total_stake = res["total_stake"]
        c_num_picks = res["num_picks"]
        c_stake_strategy = res["stake_strategy"]

        total_markets = len(df_results)
        value_bets = df_results[df_results["Decision"] == "VALUE BET"]
        practical_value_bets = df_results[df_results["Decision"] == "PRACTICAL VALUE"]
        safe_picks = df_results[df_results["Decision"] == "SAFE PICK"]
        watchlist_markets = df_results[df_results["Decision"] == "WATCHLIST"]
        no_bet_markets = df_results[df_results["Decision"] == "NO BET"]

        num_value_bets = len(value_bets)
        num_practical_value = len(practical_value_bets)
        num_safe_picks = len(safe_picks)
        num_watchlist = len(watchlist_markets)
        num_no_bets = len(no_bet_markets)

        best_adjusted_ev = df_results["Adjusted EV"].max() if total_markets > 0 else 0.0
        best_safety_score = df_results["Safety Score"].max() if total_markets > 0 else 0.0

        # Render Metrics in Spanish
        st.subheader("📈 Motor de probabilidades y métricas en vivo")
        
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.metric("Apuestas con valor", num_value_bets + num_practical_value)
            st.metric("Apuestas seguras", num_safe_picks)
        with col_m2:
            st.metric("Mercados a vigilar", num_watchlist)
            st.metric("No apostar", num_no_bets)
        with col_m3:
            st.metric("Mejor EV ajustado", f"{best_adjusted_ev * 100:.2f}%" if total_markets > 0 else "N/A")
            st.metric("Mejor Safety Score", f"{best_safety_score:.1f}" if total_markets > 0 else "N/A")

        st.progress(min(1.0, max(0.0, (num_value_bets + num_practical_value + num_safe_picks) / max(1, total_markets))))

        # Detailed Table in Spanish
        st.subheader("📋 Tabla detallada de cálculos")
        df_display = df_results.copy()
        df_display["Estimated Probability"] = df_display["Estimated Probability"].apply(lambda x: f"{x*100:.1f}%")
        df_display["Implied Probability"] = df_display["Implied Probability"].apply(lambda x: f"{x*100:.1f}%")
        df_display["Edge"] = df_display["Edge"].apply(lambda x: f"{x*100:.1f}%")
        df_display["Adjusted Probability"] = df_display["Adjusted Probability"].apply(lambda x: f"{x*100:.1f}%")
        df_display["Simple EV"] = df_display["Simple EV"].apply(lambda x: f"{x*100:.1f}%")
        df_display["Adjusted EV"] = df_display["Adjusted EV"].apply(lambda x: f"{x*100:.1f}%")
        df_display["Recommended Stake"] = df_display["Recommended Stake"].apply(lambda x: f"{x:.2f} €")
        df_display["Odds"] = df_display["Odds"].apply(lambda x: f"{x:.2f}")
        df_display["Safety Score"] = df_display["Safety Score"].apply(lambda x: f"{x:.1f}")
        df_display["Final Ranking Score"] = df_display["Final Ranking Score"].apply(lambda x: f"{x:.1f}")
        
        # Rename column headers
        df_display.rename(columns={
            "Market": "Mercado",
            "Odds": "Cuota",
            "Estimated Probability": "Probabilidad estimada",
            "Implied Probability": "Probabilidad implícita",
            "Edge": "Margen",
            "Adjusted Probability": "Probabilidad ajustada",
            "Simple EV": "EV simple",
            "Adjusted EV": "EV ajustado",
            "Risk Type": "Tipo de riesgo",
            "Recommended Stake": "Importe recomendado",
            "Decision": "Decisión",
            "Safety Score": "Puntuación de seguridad",
            "Final Ranking Score": "Puntuación de ranking"
        }, inplace=True)

        # Rename decision values for view
        decision_map_es = {
            "VALUE BET": "APUESTA CON VALOR ESTRICTO",
            "PRACTICAL VALUE": "APUESTA CON VALOR PRÁCTICO",
            "SAFE PICK": "APUESTA SEGURA",
            "WATCHLIST": "MERCADOS A VIGILAR",
            "NO BET": "NO APOSTAR"
        }
        df_display["Decisión"] = df_display["Decisión"].map(decision_map_es)
        
        st.dataframe(df_display, use_container_width=True)

        # Sort lists by Final Ranking Score descending
        value_bets_sorted = value_bets.sort_values(by="Final Ranking Score", ascending=False)
        practical_value_sorted = practical_value_bets.sort_values(by="Final Ranking Score", ascending=False)
        safe_picks_sorted = safe_picks.sort_values(by="Final Ranking Score", ascending=False)
        watchlist_sorted = watchlist_markets.sort_values(by="Final Ranking Score", ascending=False)

        # Traditional Model Output Section (Translated)
        st.markdown("---")
        st.subheader("🏆 RESULTADO DETALLADO DEL MODELO (EV)")
        
        if num_value_bets > 0:
            st.success(f"### APUESTA(S) CON VALOR ESTRICTO RECOMENDADA(S): {num_value_bets}")
            
            st.markdown("### APUESTAS CON VALOR ESTRICTO")
            for idx, row in value_bets_sorted.iterrows():
                st.markdown(f"""
                <div style="background-color: #12161a; padding: 18px; border-radius: 10px; border-left: 5px solid #e63946; margin-bottom: 15px; border-top: 1px solid #262c35; border-right: 1px solid #262c35; border-bottom: 1px solid #262c35;">
                    <h4 style="margin: 0 0 10px 0; color: #ffffff;">🎯 Mercado: <span style="color: #e63946;">{row['Market']}</span></h4>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 10px; font-size: 14px; color: #a0aec0;">
                        <div><b>Cuota:</b> <span style="color: #ffffff;">{row['Odds']:.2f}</span></div>
                        <div><b>Prob. estimada:</b> <span style="color: #ffffff;">{row['Estimated Probability']*100:.1f}%</span></div>
                        <div><b>Prob. implícita:</b> <span style="color: #ffffff;">{row['Implied Probability']*100:.1f}%</span></div>
                        <div><b>EV ajustado:</b> <span style="color: #00ff88; font-weight: bold;">{row['Adjusted EV']*100:.2f}%</span></div>
                        <div><b>Safety Score:</b> <span style="color: #ffffff;">{row['Safety Score']:.1f}</span></div>
                        <div><b>Ranking Score:</b> <span style="color: #ffffff;">{row['Final Ranking Score']:.1f}</span></div>
                        <div><b>Tipo de riesgo:</b> <span style="color: #ffffff;">{row['Risk Type']}</span></div>
                        <div><b>Importe:</b> <span style="color: #ffffff; font-weight: bold;">{row['Recommended Stake']:.2f} €</span></div>
                        <div><b>Decisión:</b> <span class="status-ok">VALOR ESTRICTO</span></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            if num_practical_value > 0:
                st.markdown("### APUESTAS CON VALOR PRÁCTICO")
                for idx, row in practical_value_sorted.iterrows():
                    st.markdown(f"""
                    <div style="background-color: #12161a; padding: 18px; border-radius: 10px; border-left: 5px solid #ff4d4d; margin-bottom: 15px; border-top: 1px solid #262c35; border-right: 1px solid #262c35; border-bottom: 1px solid #262c35;">
                        <h4 style="margin: 0 0 10px 0; color: #ffffff;">🎯 Mercado: <span style="color: #ff4d4d;">{row['Market']}</span></h4>
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 10px; font-size: 14px; color: #a0aec0;">
                            <div><b>Cuota:</b> <span style="color: #ffffff;">{row['Odds']:.2f}</span></div>
                            <div><b>Prob. estimada:</b> <span style="color: #ffffff;">{row['Estimated Probability']*100:.1f}%</span></div>
                            <div><b>Prob. implícita:</b> <span style="color: #ffffff;">{row['Implied Probability']*100:.1f}%</span></div>
                            <div><b>EV ajustado:</b> <span style="color: #ffcc00; font-weight: bold;">{row['Adjusted EV']*100:.2f}%</span></div>
                            <div><b>Safety Score:</b> <span style="color: #ffffff;">{row['Safety Score']:.1f}</span></div>
                            <div><b>Ranking Score:</b> <span style="color: #ffffff;">{row['Final Ranking Score']:.1f}</span></div>
                            <div><b>Tipo de riesgo:</b> <span style="color: #ffffff;">{row['Risk Type']}</span></div>
                            <div><b>Importe:</b> <span style="color: #ffffff; font-weight: bold;">{row['Recommended Stake']:.2f} €</span></div>
                            <div><b>Decisión:</b> <span style="color: #00ff88; font-weight: bold;">VALOR PRÁCTICO</span></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            if num_safe_picks > 0:
                st.markdown("### APUESTAS SEGURAS")
                for idx, row in safe_picks_sorted.iterrows():
                    st.markdown(f"""
                    <div style="background-color: #12161a; padding: 18px; border-radius: 10px; border-left: 5px solid #ffcc00; margin-bottom: 15px; border-top: 1px solid #262c35; border-right: 1px solid #262c35; border-bottom: 1px solid #262c35;">
                        <h4 style="margin: 0 0 10px 0; color: #ffffff;">🎯 Mercado: <span style="color: #ffcc00;">{row['Market']}</span></h4>
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 10px; font-size: 14px; color: #a0aec0;">
                            <div><b>Cuota:</b> <span style="color: #ffffff;">{row['Odds']:.2f}</span></div>
                            <div><b>Prob. estimada:</b> <span style="color: #ffffff;">{row['Estimated Probability']*100:.1f}%</span></div>
                            <div><b>Prob. implícita:</b> <span style="color: #ffffff;">{row['Implied Probability']*100:.1f}%</span></div>
                            <div><b>EV ajustado:</b> <span style="color: #ffcc00; font-weight: bold;">{row['Adjusted EV']*100:.2f}%</span></div>
                            <div><b>Safety Score:</b> <span style="color: #ffffff;">{row['Safety Score']:.1f}</span></div>
                            <div><b>Ranking Score:</b> <span style="color: #ffffff;">{row['Final Ranking Score']:.1f}</span></div>
                            <div><b>Tipo de riesgo:</b> <span style="color: #ffffff;">{row['Risk Type']}</span></div>
                            <div><b>Importe:</b> <span style="color: #ffffff; font-weight: bold;">{row['Recommended Stake']:.2f} €</span></div>
                            <div><b>Decisión:</b> <span class="status-warn">APUESTA SEGURA</span></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            if num_watchlist > 0:
                st.markdown("### MERCADOS A VIGILAR")
                for idx, row in watchlist_sorted.iterrows():
                    st.markdown(f"""
                    <div style="background-color: #12161a; padding: 18px; border-radius: 10px; border-left: 5px solid #a0aec0; margin-bottom: 15px; border-top: 1px solid #262c35; border-right: 1px solid #262c35; border-bottom: 1px solid #262c35;">
                        <h4 style="margin: 0 0 10px 0; color: #ffffff;">🎯 Mercado: <span style="color: #a0aec0;">{row['Market']}</span></h4>
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 10px; font-size: 14px; color: #a0aec0;">
                            <div><b>Cuota:</b> <span style="color: #ffffff;">{row['Odds']:.2f}</span></div>
                            <div><b>Prob. estimada:</b> <span style="color: #ffffff;">{row['Estimated Probability']*100:.1f}%</span></div>
                            <div><b>Prob. implícita:</b> <span style="color: #ffffff;">{row['Implied Probability']*100:.1f}%</span></div>
                            <div><b>EV ajustado:</b> <span style="color: #a0aec0; font-weight: bold;">{row['Adjusted EV']*100:.2f}%</span></div>
                            <div><b>Safety Score:</b> <span style="color: #ffffff;">{row['Safety Score']:.1f}</span></div>
                            <div><b>Ranking Score:</b> <span style="color: #ffffff;">{row['Final Ranking Score']:.1f}</span></div>
                            <div><b>Tipo de riesgo:</b> <span style="color: #ffffff;">{row['Risk Type']}</span></div>
                            <div><b>Importe:</b> <span style="color: #ffffff; font-weight: bold;">{row['Recommended Stake']:.2f} €</span></div>
                            <div><b>Decisión:</b> <span style="color: #a0aec0; font-weight: bold;">MERCADO A VIGILAR</span></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        elif num_practical_value > 0:
            st.warning("### NO SE ENCONTRARON APUESTAS CON VALOR ESTRICTO\n\nSin embargo, los siguientes mercados muestran un valor práctico positivo:")
            
            st.markdown("### APUESTAS CON VALOR PRÁCTICO")
            for idx, row in practical_value_sorted.iterrows():
                st.markdown(f"""
                <div style="background-color: #12161a; padding: 18px; border-radius: 10px; border-left: 5px solid #ff4d4d; margin-bottom: 15px; border-top: 1px solid #262c35; border-right: 1px solid #262c35; border-bottom: 1px solid #262c35;">
                    <h4 style="margin: 0 0 10px 0; color: #ffffff;">🎯 Mercado: <span style="color: #ff4d4d;">{row['Market']}</span></h4>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 10px; font-size: 14px; color: #a0aec0;">
                        <div><b>Cuota:</b> <span style="color: #ffffff;">{row['Odds']:.2f}</span></div>
                        <div><b>Prob. estimada:</b> <span style="color: #ffffff;">{row['Estimated Probability']*100:.1f}%</span></div>
                        <div><b>Prob. implícita:</b> <span style="color: #ffffff;">{row['Implied Probability']*100:.1f}%</span></div>
                        <div><b>EV ajustado:</b> <span style="color: #00ff88; font-weight: bold;">{row['Adjusted EV']*100:.2f}%</span></div>
                        <div><b>Safety Score:</b> <span style="color: #ffffff;">{row['Safety Score']:.1f}</span></div>
                        <div><b>Ranking Score:</b> <span style="color: #ffffff;">{row['Final Ranking Score']:.1f}</span></div>
                        <div><b>Tipo de riesgo:</b> <span style="color: #ffffff;">{row['Risk Type']}</span></div>
                        <div><b>Importe:</b> <span style="color: #ffffff; font-weight: bold;">{row['Recommended Stake']:.2f} €</span></div>
                        <div><b>Decisión:</b> <span style="color: #00ff88; font-weight: bold;">VALOR PRÁCTICO</span></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            if num_safe_picks > 0:
                st.markdown("### APUESTAS SEGURAS")
                for idx, row in safe_picks_sorted.iterrows():
                    st.markdown(f"""
                    <div style="background-color: #12161a; padding: 18px; border-radius: 10px; border-left: 5px solid #ffcc00; margin-bottom: 15px; border-top: 1px solid #262c35; border-right: 1px solid #262c35; border-bottom: 1px solid #262c35;">
                        <h4 style="margin: 0 0 10px 0; color: #ffffff;">🎯 Mercado: <span style="color: #ffcc00;">{row['Market']}</span></h4>
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 10px; font-size: 14px; color: #a0aec0;">
                            <div><b>Cuota:</b> <span style="color: #ffffff;">{row['Odds']:.2f}</span></div>
                            <div><b>Prob. estimada:</b> <span style="color: #ffffff;">{row['Estimated Probability']*100:.1f}%</span></div>
                            <div><b>Prob. implícita:</b> <span style="color: #ffffff;">{row['Implied Probability']*100:.1f}%</span></div>
                            <div><b>EV ajustado:</b> <span style="color: #ffcc00; font-weight: bold;">{row['Adjusted EV']*100:.2f}%</span></div>
                            <div><b>Safety Score:</b> <span style="color: #ffffff;">{row['Safety Score']:.1f}</span></div>
                            <div><b>Ranking Score:</b> <span style="color: #ffffff;">{row['Final Ranking Score']:.1f}</span></div>
                            <div><b>Tipo de riesgo:</b> <span style="color: #ffffff;">{row['Risk Type']}</span></div>
                            <div><b>Importe:</b> <span style="color: #ffffff; font-weight: bold;">{row['Recommended Stake']:.2f} €</span></div>
                            <div><b>Decisión:</b> <span class="status-warn">APUESTA SEGURA</span></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            if num_watchlist > 0:
                st.markdown("### MERCADOS A VIGILAR")
                for idx, row in watchlist_sorted.iterrows():
                    st.markdown(f"""
                    <div style="background-color: #12161a; padding: 18px; border-radius: 10px; border-left: 5px solid #a0aec0; margin-bottom: 15px; border-top: 1px solid #262c35; border-right: 1px solid #262c35; border-bottom: 1px solid #262c35;">
                        <h4 style="margin: 0 0 10px 0; color: #ffffff;">🎯 Mercado: <span style="color: #a0aec0;">{row['Market']}</span></h4>
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 10px; font-size: 14px; color: #a0aec0;">
                            <div><b>Cuota:</b> <span style="color: #ffffff;">{row['Odds']:.2f}</span></div>
                            <div><b>Prob. estimada:</b> <span style="color: #ffffff;">{row['Estimated Probability']*100:.1f}%</span></div>
                            <div><b>Prob. implícita:</b> <span style="color: #ffffff;">{row['Implied Probability']*100:.1f}%</span></div>
                            <div><b>EV ajustado:</b> <span style="color: #a0aec0; font-weight: bold;">{row['Adjusted EV']*100:.2f}%</span></div>
                            <div><b>Safety Score:</b> <span style="color: #ffffff;">{row['Safety Score']:.1f}</span></div>
                            <div><b>Ranking Score:</b> <span style="color: #ffffff;">{row['Final Ranking Score']:.1f}</span></div>
                            <div><b>Tipo de riesgo:</b> <span style="color: #ffffff;">{row['Risk Type']}</span></div>
                            <div><b>Importe:</b> <span style="color: #ffffff; font-weight: bold;">{row['Recommended Stake']:.2f} €</span></div>
                            <div><b>Decisión:</b> <span style="color: #a0aec0; font-weight: bold;">MERCADO A VIGILAR</span></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        elif num_safe_picks > 0:
            st.warning("### NO SE ENCONTRARON APUESTAS CON VALOR\n\nSin embargo, las alternativas más seguras disponibles son:")
            
            for idx, row in safe_picks_sorted.iterrows():
                st.markdown(f"""
                <div style="background-color: #12161a; padding: 18px; border-radius: 10px; border-left: 5px solid #ffcc00; margin-bottom: 15px; border-top: 1px solid #262c35; border-right: 1px solid #262c35; border-bottom: 1px solid #262c35;">
                    <h4 style="margin: 0 0 10px 0; color: #ffffff;">🎯 Mercado: <span style="color: #ffcc00;">{row['Market']}</span></h4>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 10px; font-size: 14px; color: #a0aec0;">
                        <div><b>Cuota:</b> <span style="color: #ffffff;">{row['Odds']:.2f}</span></div>
                        <div><b>Prob. estimada:</b> <span style="color: #ffffff;">{row['Estimated Probability']*100:.1f}%</span></div>
                        <div><b>Prob. implícita:</b> <span style="color: #ffffff;">{row['Implied Probability']*100:.1f}%</span></div>
                        <div><b>EV ajustado:</b> <span style="color: #ffcc00; font-weight: bold;">{row['Adjusted EV']*100:.2f}%</span></div>
                        <div><b>Safety Score:</b> <span style="color: #ffffff;">{row['Safety Score']:.1f}</span></div>
                        <div><b>Ranking Score:</b> <span style="color: #ffffff;">{row['Final Ranking Score']:.1f}</span></div>
                        <div><b>Tipo de riesgo:</b> <span style="color: #ffffff;">{row['Risk Type']}</span></div>
                        <div><b>Importe:</b> <span style="color: #ffffff; font-weight: bold;">{row['Recommended Stake']:.2f} €</span></div>
                        <div><b>Decisión:</b> <span class="status-warn">APUESTA SEGURA</span></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            if num_watchlist > 0:
                st.markdown("### MERCADOS A VIGILAR")
                for idx, row in watchlist_sorted.iterrows():
                    st.markdown(f"""
                    <div style="background-color: #12161a; padding: 18px; border-radius: 10px; border-left: 5px solid #a0aec0; margin-bottom: 15px; border-top: 1px solid #262c35; border-right: 1px solid #262c35; border-bottom: 1px solid #262c35;">
                        <h4 style="margin: 0 0 10px 0; color: #ffffff;">🎯 Mercado: <span style="color: #a0aec0;">{row['Market']}</span></h4>
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 10px; font-size: 14px; color: #a0aec0;">
                            <div><b>Cuota:</b> <span style="color: #ffffff;">{row['Odds']:.2f}</span></div>
                            <div><b>Prob. estimada:</b> <span style="color: #ffffff;">{row['Estimated Probability']*100:.1f}%</span></div>
                            <div><b>Prob. implícita:</b> <span style="color: #ffffff;">{row['Implied Probability']*100:.1f}%</span></div>
                            <div><b>EV ajustado:</b> <span style="color: #a0aec0; font-weight: bold;">{row['Adjusted EV']*100:.2f}%</span></div>
                            <div><b>Safety Score:</b> <span style="color: #ffffff;">{row['Safety Score']:.1f}</span></div>
                            <div><b>Ranking Score:</b> <span style="color: #ffffff;">{row['Final Ranking Score']:.1f}</span></div>
                            <div><b>Tipo de riesgo:</b> <span style="color: #ffffff;">{row['Risk Type']}</span></div>
                            <div><b>Importe:</b> <span style="color: #ffffff; font-weight: bold;">{row['Recommended Stake']:.2f} €</span></div>
                            <div><b>Decisión:</b> <span style="color: #a0aec0; font-weight: bold;">MERCADO A VIGILAR</span></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        else:
            st.warning("### DECISIÓN FINAL: NO APOSTAR\n\n**Razón:** Ningún mercado superó los filtros de valor o seguridad.")
            
            if num_watchlist > 0:
                st.markdown("### MERCADOS A VIGILAR")
                for idx, row in watchlist_sorted.iterrows():
                    st.markdown(f"""
                    <div style="background-color: #12161a; padding: 18px; border-radius: 10px; border-left: 5px solid #a0aec0; margin-bottom: 15px; border-top: 1px solid #262c35; border-right: 1px solid #262c35; border-bottom: 1px solid #262c35;">
                        <h4 style="margin: 0 0 10px 0; color: #ffffff;">🎯 Mercado: <span style="color: #a0aec0;">{row['Market']}</span></h4>
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 10px; font-size: 14px; color: #a0aec0;">
                            <div><b>Cuota:</b> <span style="color: #ffffff;">{row['Odds']:.2f}</span></div>
                            <div><b>Prob. estimada:</b> <span style="color: #ffffff;">{row['Estimated Probability']*100:.1f}%</span></div>
                            <div><b>Prob. implícita:</b> <span style="color: #ffffff;">{row['Implied Probability']*100:.1f}%</span></div>
                            <div><b>EV ajustado:</b> <span style="color: #a0aec0; font-weight: bold;">{row['Adjusted EV']*100:.2f}%</span></div>
                            <div><b>Safety Score:</b> <span style="color: #ffffff;">{row['Safety Score']:.1f}</span></div>
                            <div><b>Ranking Score:</b> <span style="color: #ffffff;">{row['Final Ranking Score']:.1f}</span></div>
                            <div><b>Tipo de riesgo:</b> <span style="color: #ffffff;">{row['Risk Type']}</span></div>
                            <div><b>Importe:</b> <span style="color: #ffffff; font-weight: bold;">{row['Recommended Stake']:.2f} €</span></div>
                            <div><b>Decisión:</b> <span style="color: #a0aec0; font-weight: bold;">MERCADO A VIGILAR</span></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # Staking / Combination Plan Results Display ("Plan de Apuestas Recomendado" / "Resultado Final")
        # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        st.markdown("---")
        st.subheader("🏆 PLAN DE APUESTAS RECOMENDADO (RESULTADO FINAL)")
        
        if len(selected_recommendations) == 0:
            st.warning("No se pudieron generar apuestas simples o combinadas seguras en el rango de cuota objetivo de 1.50 a 2.50. Intenta ampliar el rango de cuotas o cargar más datos.")
        else:
            st.markdown(f"**Mejor opción recomendada:** {c_stake_strategy}")
            
            for idx, rec in enumerate(selected_recommendations):
                role = "Apuesta principal" if idx == 0 else f"Apuesta secundaria"
                if idx > 1:
                    role = f"Apuesta secundaria {idx}"
                    
                stake_val = rec_stakes[idx]
                pot_return = stake_val * rec["odds"]
                pot_profit = pot_return - stake_val
                
                # Format legs string
                legs_html = ""
                if rec["combined_bet"]:
                    legs_details = "<br>".join([f"• {leg['market']} (@{leg['odds']:.2f})" for leg in rec["legs"]])
                    legs_html = f"<div style='font-size: 13px; color: #a0aec0; margin-top: 5px; margin-bottom: 5px;'><b>Selecciones combinadas:</b><br>{legs_details}</div>"
                
                st.markdown(f"""
                <div style="background-color: #12161a; padding: 18px; border-radius: 10px; border-left: 5px solid #ffcc00; margin-bottom: 15px; border-top: 1px solid #262c35; border-right: 1px solid #262c35; border-bottom: 1px solid #262c35;">
                    <h4 style="margin: 0 0 10px 0; color: #ffffff;">🎯 {role}: <span style="color: #ffcc00;">{rec['market']}</span></h4>
                    {legs_html}
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 10px; font-size: 14px; color: #a0aec0;">
                        <div><b>Cuota:</b> <span style="color: #ffffff;">{rec['odds']:.2f}</span></div>
                        <div><b>Probabilidad estimada:</b> <span style="color: #ffffff;">{rec['probability']:.1f}%</span></div>
                        <div><b>Riesgo:</b> <span style="color: #ffffff;">{rec['risk']:.1f}%</span></div>
                        <div><b>Incertidumbre:</b> <span style="color: #ffffff;">{rec['uncertainty']:.1f}%</span></div>
                        <div><b>Safety Score:</b> <span style="color: #ffffff;">{rec['safety_score']:.1f}</span></div>
                        <div><b>Importe:</b> <span style="color: #ffffff; font-weight: bold;">{stake_val:.2f} €</span></div>
                        <div><b>Retorno potencial:</b> <span style="color: #00ff88; font-weight: bold;">{pot_return:.2f} €</span></div>
                        <div><b>Beneficio potencial:</b> <span style="color: #00ff88; font-weight: bold;">{pot_profit:.2f} €</span></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Check if this favorite is already saved
                is_saved = any(fav["market"] == rec["market"] and fav["match"] == c_match for fav in st.session_state.favorites)
                
                if is_saved:
                    st.button("✓ Guardada en favoritas", key=f"save_fav_{idx}", disabled=True)
                else:
                    if st.button("Guardar en favoritas", key=f"save_fav_{idx}"):
                        new_fav = {
                            "id": f"{int(time.time())}_{idx}",
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
                            "status": "Pendiente",
                            "combined_bet": rec["combined_bet"],
                            "legs": rec["legs"]
                        }
                        st.session_state.favorites.append(new_fav)
                        save_favorites()
                        st.success(f"¡Apuesta guardada como favorita!")
                        st.rerun()

        st.caption(
            "Nota: La calculadora estima los valores esperados en base a ajustes estadísticos. Los rendimientos pasados no garantizan resultados futuros."
        )

# ----------------------------------------------------
# TAB 2: BACKTESTING
# ----------------------------------------------------
# ----------------------------------------------------
# TAB 2: FAVORITAS
# ----------------------------------------------------
with tab2:
    st.header("📋 Mis Apuestas Favoritas")
    
    # Calculate metrics for closed bets
    total_favs = len(st.session_state.favorites)
    pendientes = sum(1 for f in st.session_state.favorites if f["status"] == "Pendiente")
    ganadas = sum(1 for f in st.session_state.favorites if f["status"] == "Ganada")
    perdidas = sum(1 for f in st.session_state.favorites if f["status"] == "Perdida")
    nulas = sum(1 for f in st.session_state.favorites if f["status"] == "Nula")
    
    total_profit_closed = 0.0
    total_stake_closed = 0.0
    
    for f in st.session_state.favorites:
        st_val = float(f["stake"])
        od_val = float(f["odds"])
        status = f["status"]
        if status == "Ganada":
            total_profit_closed += st_val * (od_val - 1.0)
            total_stake_closed += st_val
        elif status == "Perdida":
            total_profit_closed -= st_val
            total_stake_closed += st_val
        elif status == "Nula":
            total_stake_closed += st_val
            
    roi_closed = (total_profit_closed / total_stake_closed * 100.0) if total_stake_closed > 0 else 0.0
    
    # Render metrics cards
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        st.metric("Apuestas guardadas", total_favs)
        st.metric("Pendientes", pendientes)
    with col_f2:
        st.metric("Ganadas", ganadas)
        st.metric("Perdidas", perdidas)
    with col_f3:
        st.metric("Beneficio total cerrado", f"{total_profit_closed:.2f} €", delta=f"{total_profit_closed:.2f} €")
        st.metric("ROI cerrado", f"{roi_closed:.2f}%")
        
    st.markdown("---")
    
    if total_favs == 0:
        st.info("No hay apuestas favoritas guardadas aún. Calcula apuestas y haz clic en 'Guardar en favoritas'.")
    else:
        # Loop through favorites and render them
        for idx, fav in enumerate(st.session_state.favorites):
            legs_str = ""
            if fav.get("combined_bet"):
                legs_str = " | **Piernas:** " + ", ".join([f"{leg['market']} (@{leg['odds']:.2f})" for leg in fav.get("legs", [])])
                
            # Render card
            st.markdown(f"""
            <div style="background-color: #12161a; padding: 15px; border-radius: 8px; border: 1px solid #262c35; margin-bottom: 15px;">
                <h4 style="margin: 0 0 5px 0; color: #ffffff;">🎯 Mercado: <span style="color: #ffcc00;">{fav['market']}</span></h4>
                <div style="font-size: 13px; color: #a0aec0; margin-bottom: 10px;">
                    <b>Partido:</b> {fav['match']} | <b>Competición:</b> {fav['competition']} | <b>Casa de apuestas:</b> {fav['betting_house']}{legs_str}
                </div>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 10px; font-size: 13px; color: #ffffff;">
                    <div><b>Cuota:</b> {fav['odds']:.2f}</div>
                    <div><b>Importe:</b> {fav['stake']:.2f} €</div>
                    <div><b>Probabilidad:</b> {fav['estimated_probability']:.1f}%</div>
                    <div><b>Retorno:</b> {fav['potential_return']:.2f} €</div>
                    <div><b>Beneficio:</b> {fav['potential_profit']:.2f} €</div>
                    <div><b>Estado actual:</b> <span style="color: #ff6b6b; font-weight: bold;">{fav['status']}</span></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Inline controls
            col_sel, col_del = st.columns([3, 1])
            with col_sel:
                status_options = ["Pendiente", "Ganada", "Perdida", "Nula"]
                current_idx = status_options.index(fav["status"]) if fav["status"] in status_options else 0
                new_status = st.selectbox(
                    f"Actualizar estado",
                    status_options,
                    index=current_idx,
                    key=f"status_fav_{fav['id']}_{idx}"
                )
                if new_status != fav["status"]:
                    fav["status"] = new_status
                    save_favorites()
                    st.rerun()
            with col_del:
                st.write("")
                st.write("")
                if st.button("Eliminar", key=f"delete_fav_{fav['id']}_{idx}", use_container_width=True):
                    st.session_state.favorites.pop(idx)
                    save_favorites()
                    st.rerun()
                    
        # Confirm delete all favorites
        st.markdown("---")
        if st.checkbox("Confirmar borrar todas las favoritas", key="confirm_delete_all_checkbox"):
            if st.button("BORRAR TODAS LAS FAVORITAS", use_container_width=True):
                st.session_state.favorites = []
                save_favorites()
                st.rerun()

# ----------------------------------------------------
# TAB 3: TOP CUOTAS
# ----------------------------------------------------
with tab3:
    st.header("🏆 Top cuotas")
    st.markdown("""
    Esta pestaña muestra los mejores mercados con cuotas superiores a 1.50 calculados en la pestaña Calculadora.
    Filtros automáticos aplicados:
    - Cuota >= 1.50
    - Probabilidad >= 45%
    - Riesgo <= 30%
    - Incertidumbre <= 30%
    """)
    
    if "latest_markets" not in st.session_state or not st.session_state.latest_markets:
        st.info("Por favor, introduce un CSV y haz clic en 'Calcular apuestas' en la pestaña Calculadora para generar datos de mercados.")
    else:
        top_candidates = []
        for m in st.session_state.latest_markets:
            if m["Odds"] >= 1.50 and m["Probability"] >= 45.0 and m["Risk"] <= 30.0 and m["Uncertainty"] <= 30.0:
                top_candidates.append(m)
                
        if not top_candidates:
            st.warning("No se encontraron mercados que cumplan con los filtros requeridos (Cuota >= 1.50, Probabilidad >= 45%, Riesgo <= 30%, Incertidumbre <= 30%).")
        else:
            # Sort:
            # 1. highest estimated probability (descending)
            # 2. highest Safety Score (descending)
            # 3. odds closest to the target range 1.50 - 2.50 (ascending distance)
            def top_sort_key(x):
                odds = x["Odds"]
                dist = 0.0
                if odds > 2.50:
                    dist = odds - 2.50
                return (-x["Probability"], -x["SafetyScore"], dist)
                
            sorted_top = sorted(top_candidates, key=top_sort_key)
            
            import urllib.parse
            for rank, item in enumerate(sorted_top, 1):
                query = f"{item['BettingHouse']} {item['Match']} {item['Market']}"
                encoded_query = urllib.parse.quote_plus(query)
                search_url = f"https://www.google.com/search?q={encoded_query}"
                
                st.markdown(f"""
                <div style="background-color: #12161a; padding: 15px; border-radius: 8px; border: 1px solid #262c35; margin-bottom: 12px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
                        <span style="background-color: #e63946; color: #ffffff; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">Ranking #{rank}</span>
                        <span style="font-size: 13px; color: #a0aec0;">Casa de apuestas: <b>{item['BettingHouse']}</b></span>
                    </div>
                    <h4 style="margin: 5px 0; color: #ffffff;">{item['Market']}</h4>
                    <div style="font-size: 13px; color: #a0aec0; margin-bottom: 8px;">
                        <b>Partido:</b> {item['Match']}
                    </div>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(110px, 1fr)); gap: 8px; font-size: 13px; color: #ffffff; margin-bottom: 10px;">
                        <div><b>Cuota:</b> {item['Odds']:.2f}</div>
                        <div><b>Probabilidad:</b> {item['Probability']:.1f}%</div>
                        <div><b>Riesgo:</b> {item['Risk']:.1f}%</div>
                        <div><b>Incertidumbre:</b> {item['Uncertainty']:.1f}%</div>
                        <div><b>Safety Score:</b> {item['SafetyScore']:.1f}</div>
                    </div>
                    <div style="font-size: 13px;">
                        <a href="{search_url}" target="_blank" style="color: #ff6b6b; font-weight: bold; text-decoration: none;">🔍 Buscar en casa de apuestas</a>
                    </div>
                </div>
                """, unsafe_allow_html=True)
