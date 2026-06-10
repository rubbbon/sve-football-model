import streamlit as st
import pandas as pd
from io import StringIO

# Page configurations
st.set_page_config(
    page_title="SVE — Statistical Value Engine",
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
st.markdown('<div class="big-title">SVE — STATISTICAL VALUE ENGINE</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Football expected value model & quantitative betting engine</div>', unsafe_allow_html=True)

# Define Tabs
tab1, tab2 = st.tabs(["📈 Live Model", "📊 Backtesting"])

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
        st.session_state.config_phase = "Group"
    if "config_betting_house" not in st.session_state:
        st.session_state.config_betting_house = ""
    if "config_recommendation_style" not in st.session_state:
        st.session_state.config_recommendation_style = "Practical Value"

    st.header("1. AI Research Prompt Generator")
    st.markdown("Fill in the match details, click GENERATE / UPDATE AI PROMPT, send the generated prompt to your AI assistant, then paste the returned CSV into the Market CSV Input section.")
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        prompt_match = st.text_input("Match", placeholder="Example: Spain vs Cape Verde", key="prompt_match_input")
        st.caption("You can write it normally, for example: Spain vs Cape Verde, Spain - Cape Verde, or Spain Cape Verde.")
        
        prompt_competition_choice = st.selectbox(
            "Competition",
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
                "Other"
            ],
            key="prompt_comp_select"
        )
        if prompt_competition_choice == "Other":
            prompt_competition = st.text_input(
                "Custom competition",
                placeholder="Example: International Friendly",
                key="prompt_comp_custom"
            )
        else:
            prompt_competition = prompt_competition_choice
            
        prompt_phase = st.selectbox("Phase", ["Group", "Knockout", "Semifinal", "Final"], key="prompt_phase_input")
    with col_p2:
        prompt_house_choice = st.selectbox(
            "Betting house preference",
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
                "Other"
            ],
            key="prompt_house_select"
        )
        if prompt_house_choice == "Other":
            prompt_house = st.text_input(
                "Custom betting house",
                placeholder="Example: Sportium",
                key="prompt_house_custom"
            )
        else:
            prompt_house = prompt_house_choice

        prompt_preset = st.selectbox(
            "Market analysis preset",
            [
                "Complete analysis",
                "Conservative / safe picks",
                "Main result markets",
                "Goals",
                "Corners",
                "Cards",
                "Shots",
                "Handicaps",
                "Custom"
            ],
            key="prompt_market_preset"
        )
        st.caption("Choose Complete analysis for a full model review, or select a specific area such as Goals, Corners, Cards or Shots.")
        
        preset_mapping = {
            "Complete analysis": "1X2, double chance, draw no bet, goals, under/over 2.5, under/over 3.5, both teams to score, team goals, corners, team corners, cards, team cards, shots, shots on target, handicaps, Asian handicaps",
            "Conservative / safe picks": "double chance, draw no bet, under/over 3.5 goals, team under/over goals, team corners, team cards, low-risk handicaps",
            "Main result markets": "1X2, double chance, draw no bet, halftime/fulltime, team to score first, win to nil",
            "Goals": "goals, under/over 1.5, under/over 2.5, under/over 3.5, both teams to score, team goals, clean sheet, win to nil",
            "Corners": "total corners, under/over corners, team corners, corner handicap, first half corners",
            "Cards": "total cards, team cards, most cards, player cards if lineups are available, cards handicap",
            "Shots": "total shots, team shots, shots on target, player shots if lineups are available, player shots on target if lineups are available",
            "Handicaps": "European handicaps, Asian handicaps, favorite handicap, underdog positive handicap, low-risk handicap lines"
        }
        
        if prompt_preset == "Custom":
            prompt_markets = st.text_area(
                "Custom markets to analyze",
                placeholder="Example: Spain corners, Cape Verde cards, Spain over 1.5 goals",
                height=125,
                key="prompt_markets_custom"
            )
        else:
            prompt_markets = preset_mapping[prompt_preset]
    
    if "generated_prompt" not in st.session_state:
        st.session_state.generated_prompt = ""

    if st.button("GENERATE / UPDATE AI PROMPT", use_container_width=True):
        cleaned_match = clean_match_name(prompt_match)
        
        prompt_text = f"""Please search current information about the football match "{cleaned_match}" in the "{prompt_competition}" ({prompt_phase} phase).
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
        "Generated AI Research Prompt",
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
    <button id="copy-btn">COPY AI PROMPT</button>
    <div id="status" style="
        color: #00ff88;
        font-weight: bold;
        font-family: sans-serif;
        margin-top: 8px;
        font-size: 14px;
        text-align: center;
        display: none;
    ">✓ Prompt copied to clipboard</div>
    
    <script>
    document.getElementById('copy-btn').addEventListener('click', function() {{
        const text = {escaped_prompt};
        if (!text) {{
            const status = document.getElementById('status');
            status.innerText = "✕ No prompt generated yet";
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
            status.innerText = "✓ Prompt copied to clipboard";
            status.style.color = "#00ff88";
            status.style.display = "block";
            setTimeout(() => {{ status.style.display = "none"; }}, 3000);
        }}
        
        function showError() {{
            const status = document.getElementById('status');
            status.innerText = "✕ Copy failed. Please select and copy manually.";
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
        '“Click the button after editing the match details. Then copy the generated prompt and send it to your AI assistant.”'
        '</p>',
        unsafe_allow_html=True
    )
    st.markdown("---")

    st.header("2. Parameters & Configuration")

    # Inputs organized in 3 columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        match = st.text_input("Match / Partido", placeholder="Example: Mexico vs South Africa", key="config_match")
        competition = st.text_input("Competition", placeholder="Example: FIFA World Cup 2026", key="config_competition")
        phase = st.selectbox("Phase", ["Group", "Knockout", "Semifinal", "Final"], key="config_phase")

    with col2:
        betting_house = st.text_input("Betting house", placeholder="Example: Winamax", key="config_betting_house")
        reliability = st.selectbox("Reliability", ["High", "Medium", "Low"], key="config_reliability")
        model_mode = st.selectbox("Model mode", ["Conservative", "Balanced", "Aggressive"], key="config_model_mode")
        recommendation_style = st.selectbox(
            "Recommendation Style",
            ["Practical Value", "Strict Value", "Conservative Safety"],
            key="config_recommendation_style"
        )

    with col3:
        bankroll = st.number_input("Bankroll (€)", min_value=1.0, value=100.0, step=10.0)
        max_picks = st.slider("Maximum recommended picks", 1, 10, 2)
        cuota_minima = st.number_input("Minimum acceptable odds", min_value=1.01, value=1.40, step=0.01)

    st.markdown("### Model Formula Identity")
    st.markdown(
        r"""
        <div class="formula">
        EV* = [(Estimated Probability − λ × Uncertainty − ρ × Risk) × Odds] − 1
        </div>
        """,
        unsafe_allow_html=True
    )

    st.header("3. Market CSV Input")
    st.markdown("""
    Paste your markets in CSV format. The CSV must contain exactly these columns:
    `Market`, `Odds`, `Probability`, `Risk`, `Uncertainty`, `Type`
    """)

    # Default CSV example
    default_csv = """Market,Odds,Probability,Risk,Uncertainty,Type
Under 2.5 goals,1.80,66,8,8,Low
Spain win,2.10,48,18,16,Medium
Over 8.5 corners,1.85,61,12,10,Medium
France over 1.5 cards,1.90,60,15,12,Medium"""

    csv_input = st.text_area(
        "Paste CSV Markets",
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
                st.error(f"Validation Error: The CSV is missing the following required columns: {', '.join(missing_cols)}")
            else:
                # Convert numeric values and check for errors
                df_input["Odds"] = pd.to_numeric(df_input["Odds"], errors='coerce')
                df_input["Probability"] = pd.to_numeric(df_input["Probability"], errors='coerce')
                df_input["Risk"] = pd.to_numeric(df_input["Risk"], errors='coerce')
                df_input["Uncertainty"] = pd.to_numeric(df_input["Uncertainty"], errors='coerce')

                if df_input[["Odds", "Probability", "Risk", "Uncertainty"]].isnull().any().any():
                    st.error("Validation Error: Some fields in numeric columns (Odds, Probability, Risk, Uncertainty) cannot be converted to numbers.")
                else:
                    valid_csv = True
                    st.subheader("📋 Markets Loaded Preview")
                    st.dataframe(df_input, use_container_width=True)
        except Exception as e:
            st.error(f"Error parsing CSV file: {str(e)}")

    st.header("4. Model Results")

    # Run the model
    if st.button("RUN VALUE MODEL", use_container_width=True):
        if not valid_csv:
            st.error("Cannot run the model. Please fix the CSV validation errors above.")
        else:
            # Model mode configuration parameters (lambda and rho)
            if model_mode == "Conservative":
                lamb = 0.25
                rho = 0.25
            elif model_mode == "Balanced":
                lamb = 0.18
                rho = 0.18
            else:  # Aggressive
                lamb = 0.12
                rho = 0.12

            # Phase-based minimum adjusted EV thresholds (theta)
            if phase == "Group":
                theta = 0.04
            elif phase == "Knockout":
                theta = 0.06
            elif phase == "Semifinal":
                theta = 0.07
            else:  # Final
                theta = 0.08

            # Reliability adjustments
            if reliability == "Medium":
                theta += 0.01
            elif reliability == "Low":
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
                if recommendation_style == "Strict Value":
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

                elif recommendation_style == "Practical Value":
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

            # Extract groups
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

            # Render Metrics
            st.subheader("📈 Probability Engine & Live Metrics")
            
            col_m1, col_m2, col_m3 = st.columns(3)
            with col_m1:
                # Count PRACTICAL VALUE together with VALUE BETS in the main dashboard
                st.metric("Value Bets", num_value_bets + num_practical_value)
                st.metric("Safe Picks", num_safe_picks)
            with col_m2:
                st.metric("Watchlist Markets", num_watchlist)
                st.metric("No Bet Markets", num_no_bets)
            with col_m3:
                st.metric("Best Adjusted EV", f"{best_adjusted_ev * 100:.2f}%" if total_markets > 0 else "N/A")
                st.metric("Best Safety Score", f"{best_safety_score:.1f}" if total_markets > 0 else "N/A")

            st.progress(min(1.0, max(0.0, (num_value_bets + num_practical_value + num_safe_picks) / max(1, total_markets))))

            # Formatted Results Table for general analysis
            st.subheader("📋 Detailed Calculation Table")
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
            
            st.dataframe(df_display, use_container_width=True)

            # Sort lists by Final Ranking Score descending
            value_bets_sorted = value_bets.sort_values(by="Final Ranking Score", ascending=False)
            practical_value_sorted = practical_value_bets.sort_values(by="Final Ranking Score", ascending=False)
            safe_picks_sorted = safe_picks.sort_values(by="Final Ranking Score", ascending=False)
            watchlist_sorted = watchlist_markets.sort_values(by="Final Ranking Score", ascending=False)

            # Final Model Output Section
            st.markdown("---")
            st.subheader("🏆 FINAL MODEL OUTPUT")
            
            if num_value_bets > 0:
                st.success(f"### FINAL DECISION: {num_value_bets} STRICT VALUE BET(S) RECOMMENDED")
                
                st.markdown("### STRICT VALUE BETS")
                for idx, row in value_bets_sorted.head(max_picks).iterrows():
                    st.markdown(f"""
                    <div style="background-color: #12161a; padding: 18px; border-radius: 10px; border-left: 5px solid #e63946; margin-bottom: 15px; border-top: 1px solid #262c35; border-right: 1px solid #262c35; border-bottom: 1px solid #262c35;">
                        <h4 style="margin: 0 0 10px 0; color: #ffffff;">🎯 Pick: <span style="color: #e63946;">{row['Market']}</span></h4>
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 10px; font-size: 14px; color: #a0aec0;">
                            <div><b>Odds:</b> <span style="color: #ffffff;">{row['Odds']:.2f}</span></div>
                            <div><b>Estimated Prob:</b> <span style="color: #ffffff;">{row['Estimated Probability']*100:.1f}%</span></div>
                            <div><b>Implied Prob:</b> <span style="color: #ffffff;">{row['Implied Probability']*100:.1f}%</span></div>
                            <div><b>Adjusted EV:</b> <span style="color: #00ff88; font-weight: bold;">{row['Adjusted EV']*100:.2f}%</span></div>
                            <div><b>Safety Score:</b> <span style="color: #ffffff;">{row['Safety Score']:.1f}</span></div>
                            <div><b>Ranking Score:</b> <span style="color: #ffffff;">{row['Final Ranking Score']:.1f}</span></div>
                            <div><b>Risk Type:</b> <span style="color: #ffffff;">{row['Risk Type']}</span></div>
                            <div><b>Recommended Stake:</b> <span style="color: #ffffff; font-weight: bold;">{row['Recommended Stake']:.2f} €</span></div>
                            <div><b>Decision:</b> <span class="status-ok">{row['Decision']}</span></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                if num_practical_value > 0:
                    st.markdown("### PRACTICAL VALUE BETS")
                    for idx, row in practical_value_sorted.iterrows():
                        st.markdown(f"""
                        <div style="background-color: #12161a; padding: 18px; border-radius: 10px; border-left: 5px solid #ff4d4d; margin-bottom: 15px; border-top: 1px solid #262c35; border-right: 1px solid #262c35; border-bottom: 1px solid #262c35;">
                            <h4 style="margin: 0 0 10px 0; color: #ffffff;">🎯 Pick: <span style="color: #ff4d4d;">{row['Market']}</span></h4>
                            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 10px; font-size: 14px; color: #a0aec0;">
                                <div><b>Odds:</b> <span style="color: #ffffff;">{row['Odds']:.2f}</span></div>
                                <div><b>Estimated Prob:</b> <span style="color: #ffffff;">{row['Estimated Probability']*100:.1f}%</span></div>
                                <div><b>Implied Prob:</b> <span style="color: #ffffff;">{row['Implied Probability']*100:.1f}%</span></div>
                                <div><b>Adjusted EV:</b> <span style="color: #ffcc00; font-weight: bold;">{row['Adjusted EV']*100:.2f}%</span></div>
                                <div><b>Safety Score:</b> <span style="color: #ffffff;">{row['Safety Score']:.1f}</span></div>
                                <div><b>Ranking Score:</b> <span style="color: #ffffff;">{row['Final Ranking Score']:.1f}</span></div>
                                <div><b>Risk Type:</b> <span style="color: #ffffff;">{row['Risk Type']}</span></div>
                                <div><b>Recommended Stake:</b> <span style="color: #ffffff; font-weight: bold;">{row['Recommended Stake']:.2f} €</span></div>
                                <div><b>Decision:</b> <span style="color: #00ff88; font-weight: bold;">{row['Decision']}</span></div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                if num_safe_picks > 0:
                    st.markdown("### SAFE PICKS")
                    for idx, row in safe_picks_sorted.iterrows():
                        st.markdown(f"""
                        <div style="background-color: #12161a; padding: 18px; border-radius: 10px; border-left: 5px solid #ffcc00; margin-bottom: 15px; border-top: 1px solid #262c35; border-right: 1px solid #262c35; border-bottom: 1px solid #262c35;">
                            <h4 style="margin: 0 0 10px 0; color: #ffffff;">🎯 Pick: <span style="color: #ffcc00;">{row['Market']}</span></h4>
                            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 10px; font-size: 14px; color: #a0aec0;">
                                <div><b>Odds:</b> <span style="color: #ffffff;">{row['Odds']:.2f}</span></div>
                                <div><b>Estimated Prob:</b> <span style="color: #ffffff;">{row['Estimated Probability']*100:.1f}%</span></div>
                                <div><b>Implied Prob:</b> <span style="color: #ffffff;">{row['Implied Probability']*100:.1f}%</span></div>
                                <div><b>Adjusted EV:</b> <span style="color: #ffcc00; font-weight: bold;">{row['Adjusted EV']*100:.2f}%</span></div>
                                <div><b>Safety Score:</b> <span style="color: #ffffff;">{row['Safety Score']:.1f}</span></div>
                                <div><b>Ranking Score:</b> <span style="color: #ffffff;">{row['Final Ranking Score']:.1f}</span></div>
                                <div><b>Risk Type:</b> <span style="color: #ffffff;">{row['Risk Type']}</span></div>
                                <div><b>Recommended Stake:</b> <span style="color: #ffffff; font-weight: bold;">{row['Recommended Stake']:.2f} €</span></div>
                                <div><b>Decision:</b> <span class="status-warn">{row['Decision']}</span></div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                if num_watchlist > 0:
                    st.markdown("### WATCHLIST")
                    for idx, row in watchlist_sorted.iterrows():
                        st.markdown(f"""
                        <div style="background-color: #12161a; padding: 18px; border-radius: 10px; border-left: 5px solid #a0aec0; margin-bottom: 15px; border-top: 1px solid #262c35; border-right: 1px solid #262c35; border-bottom: 1px solid #262c35;">
                            <h4 style="margin: 0 0 10px 0; color: #ffffff;">🎯 Pick: <span style="color: #a0aec0;">{row['Market']}</span></h4>
                            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 10px; font-size: 14px; color: #a0aec0;">
                                <div><b>Odds:</b> <span style="color: #ffffff;">{row['Odds']:.2f}</span></div>
                                <div><b>Estimated Prob:</b> <span style="color: #ffffff;">{row['Estimated Probability']*100:.1f}%</span></div>
                                <div><b>Implied Prob:</b> <span style="color: #ffffff;">{row['Implied Probability']*100:.1f}%</span></div>
                                <div><b>Adjusted EV:</b> <span style="color: #a0aec0; font-weight: bold;">{row['Adjusted EV']*100:.2f}%</span></div>
                                <div><b>Safety Score:</b> <span style="color: #ffffff;">{row['Safety Score']:.1f}</span></div>
                                <div><b>Ranking Score:</b> <span style="color: #ffffff;">{row['Final Ranking Score']:.1f}</span></div>
                                <div><b>Risk Type:</b> <span style="color: #ffffff;">{row['Risk Type']}</span></div>
                                <div><b>Recommended Stake:</b> <span style="color: #ffffff; font-weight: bold;">{row['Recommended Stake']:.2f} €</span></div>
                                <div><b>Decision:</b> <span style="color: #a0aec0; font-weight: bold;">{row['Decision']}</span></div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

            elif num_practical_value > 0:
                st.warning("### NO STRICT VALUE BET FOUND\n\nHowever, the following markets show practical positive value:")
                
                st.markdown("### PRACTICAL VALUE BETS")
                for idx, row in practical_value_sorted.head(max_picks).iterrows():
                    st.markdown(f"""
                    <div style="background-color: #12161a; padding: 18px; border-radius: 10px; border-left: 5px solid #ff4d4d; margin-bottom: 15px; border-top: 1px solid #262c35; border-right: 1px solid #262c35; border-bottom: 1px solid #262c35;">
                        <h4 style="margin: 0 0 10px 0; color: #ffffff;">🎯 Pick: <span style="color: #ff4d4d;">{row['Market']}</span></h4>
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 10px; font-size: 14px; color: #a0aec0;">
                            <div><b>Odds:</b> <span style="color: #ffffff;">{row['Odds']:.2f}</span></div>
                            <div><b>Estimated Prob:</b> <span style="color: #ffffff;">{row['Estimated Probability']*100:.1f}%</span></div>
                            <div><b>Implied Prob:</b> <span style="color: #ffffff;">{row['Implied Probability']*100:.1f}%</span></div>
                            <div><b>Adjusted EV:</b> <span style="color: #00ff88; font-weight: bold;">{row['Adjusted EV']*100:.2f}%</span></div>
                            <div><b>Safety Score:</b> <span style="color: #ffffff;">{row['Safety Score']:.1f}</span></div>
                            <div><b>Ranking Score:</b> <span style="color: #ffffff;">{row['Final Ranking Score']:.1f}</span></div>
                            <div><b>Risk Type:</b> <span style="color: #ffffff;">{row['Risk Type']}</span></div>
                            <div><b>Recommended Stake:</b> <span style="color: #ffffff; font-weight: bold;">{row['Recommended Stake']:.2f} €</span></div>
                            <div><b>Decision:</b> <span style="color: #00ff88; font-weight: bold;">{row['Decision']}</span></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                if num_safe_picks > 0:
                    st.markdown("### SAFE PICKS")
                    for idx, row in safe_picks_sorted.iterrows():
                        st.markdown(f"""
                        <div style="background-color: #12161a; padding: 18px; border-radius: 10px; border-left: 5px solid #ffcc00; margin-bottom: 15px; border-top: 1px solid #262c35; border-right: 1px solid #262c35; border-bottom: 1px solid #262c35;">
                            <h4 style="margin: 0 0 10px 0; color: #ffffff;">🎯 Pick: <span style="color: #ffcc00;">{row['Market']}</span></h4>
                            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 10px; font-size: 14px; color: #a0aec0;">
                                <div><b>Odds:</b> <span style="color: #ffffff;">{row['Odds']:.2f}</span></div>
                                <div><b>Estimated Prob:</b> <span style="color: #ffffff;">{row['Estimated Probability']*100:.1f}%</span></div>
                                <div><b>Implied Prob:</b> <span style="color: #ffffff;">{row['Implied Probability']*100:.1f}%</span></div>
                                <div><b>Adjusted EV:</b> <span style="color: #ffcc00; font-weight: bold;">{row['Adjusted EV']*100:.2f}%</span></div>
                                <div><b>Safety Score:</b> <span style="color: #ffffff;">{row['Safety Score']:.1f}</span></div>
                                <div><b>Ranking Score:</b> <span style="color: #ffffff;">{row['Final Ranking Score']:.1f}</span></div>
                                <div><b>Risk Type:</b> <span style="color: #ffffff;">{row['Risk Type']}</span></div>
                                <div><b>Recommended Stake:</b> <span style="color: #ffffff; font-weight: bold;">{row['Recommended Stake']:.2f} €</span></div>
                                <div><b>Decision:</b> <span class="status-warn">{row['Decision']}</span></div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                if num_watchlist > 0:
                    st.markdown("### WATCHLIST")
                    for idx, row in watchlist_sorted.iterrows():
                        st.markdown(f"""
                        <div style="background-color: #12161a; padding: 18px; border-radius: 10px; border-left: 5px solid #a0aec0; margin-bottom: 15px; border-top: 1px solid #262c35; border-right: 1px solid #262c35; border-bottom: 1px solid #262c35;">
                            <h4 style="margin: 0 0 10px 0; color: #ffffff;">🎯 Pick: <span style="color: #a0aec0;">{row['Market']}</span></h4>
                            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 10px; font-size: 14px; color: #a0aec0;">
                                <div><b>Odds:</b> <span style="color: #ffffff;">{row['Odds']:.2f}</span></div>
                                <div><b>Estimated Prob:</b> <span style="color: #ffffff;">{row['Estimated Probability']*100:.1f}%</span></div>
                                <div><b>Implied Prob:</b> <span style="color: #ffffff;">{row['Implied Probability']*100:.1f}%</span></div>
                                <div><b>Adjusted EV:</b> <span style="color: #a0aec0; font-weight: bold;">{row['Adjusted EV']*100:.2f}%</span></div>
                                <div><b>Safety Score:</b> <span style="color: #ffffff;">{row['Safety Score']:.1f}</span></div>
                                <div><b>Ranking Score:</b> <span style="color: #ffffff;">{row['Final Ranking Score']:.1f}</span></div>
                                <div><b>Risk Type:</b> <span style="color: #ffffff;">{row['Risk Type']}</span></div>
                                <div><b>Recommended Stake:</b> <span style="color: #ffffff; font-weight: bold;">{row['Recommended Stake']:.2f} €</span></div>
                                <div><b>Decision:</b> <span style="color: #a0aec0; font-weight: bold;">{row['Decision']}</span></div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            
            elif num_safe_picks > 0:
                st.warning("### NO VALUE BET FOUND\n\nHowever, the safest available alternatives are:")
                
                for idx, row in safe_picks_sorted.head(3).iterrows():
                    st.markdown(f"""
                    <div style="background-color: #12161a; padding: 18px; border-radius: 10px; border-left: 5px solid #ffcc00; margin-bottom: 15px; border-top: 1px solid #262c35; border-right: 1px solid #262c35; border-bottom: 1px solid #262c35;">
                        <h4 style="margin: 0 0 10px 0; color: #ffffff;">🎯 Pick: <span style="color: #ffcc00;">{row['Market']}</span></h4>
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 10px; font-size: 14px; color: #a0aec0;">
                            <div><b>Odds:</b> <span style="color: #ffffff;">{row['Odds']:.2f}</span></div>
                            <div><b>Estimated Prob:</b> <span style="color: #ffffff;">{row['Estimated Probability']*100:.1f}%</span></div>
                            <div><b>Implied Prob:</b> <span style="color: #ffffff;">{row['Implied Probability']*100:.1f}%</span></div>
                            <div><b>Adjusted EV:</b> <span style="color: #ffcc00; font-weight: bold;">{row['Adjusted EV']*100:.2f}%</span></div>
                            <div><b>Safety Score:</b> <span style="color: #ffffff;">{row['Safety Score']:.1f}</span></div>
                            <div><b>Ranking Score:</b> <span style="color: #ffffff;">{row['Final Ranking Score']:.1f}</span></div>
                            <div><b>Risk Type:</b> <span style="color: #ffffff;">{row['Risk Type']}</span></div>
                            <div><b>Recommended Stake:</b> <span style="color: #ffffff; font-weight: bold;">{row['Recommended Stake']:.2f} €</span></div>
                            <div><b>Decision:</b> <span class="status-warn">{row['Decision']}</span></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                if num_watchlist > 0:
                    st.markdown("### WATCHLIST")
                    for idx, row in watchlist_sorted.iterrows():
                        st.markdown(f"""
                        <div style="background-color: #12161a; padding: 18px; border-radius: 10px; border-left: 5px solid #a0aec0; margin-bottom: 15px; border-top: 1px solid #262c35; border-right: 1px solid #262c35; border-bottom: 1px solid #262c35;">
                            <h4 style="margin: 0 0 10px 0; color: #ffffff;">🎯 Pick: <span style="color: #a0aec0;">{row['Market']}</span></h4>
                            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 10px; font-size: 14px; color: #a0aec0;">
                                <div><b>Odds:</b> <span style="color: #ffffff;">{row['Odds']:.2f}</span></div>
                                <div><b>Estimated Prob:</b> <span style="color: #ffffff;">{row['Estimated Probability']*100:.1f}%</span></div>
                                <div><b>Implied Prob:</b> <span style="color: #ffffff;">{row['Implied Probability']*100:.1f}%</span></div>
                                <div><b>Adjusted EV:</b> <span style="color: #a0aec0; font-weight: bold;">{row['Adjusted EV']*100:.2f}%</span></div>
                                <div><b>Safety Score:</b> <span style="color: #ffffff;">{row['Safety Score']:.1f}</span></div>
                                <div><b>Ranking Score:</b> <span style="color: #ffffff;">{row['Final Ranking Score']:.1f}</span></div>
                                <div><b>Risk Type:</b> <span style="color: #ffffff;">{row['Risk Type']}</span></div>
                                <div><b>Recommended Stake:</b> <span style="color: #ffffff; font-weight: bold;">{row['Recommended Stake']:.2f} €</span></div>
                                <div><b>Decision:</b> <span style="color: #a0aec0; font-weight: bold;">{row['Decision']}</span></div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            
            else:
                st.warning("### FINAL DECISION: NO BET\n\n**Reason:** No market passed the value or safety filters.")
                
                if num_watchlist > 0:
                    st.markdown("### WATCHLIST")
                    for idx, row in watchlist_sorted.iterrows():
                        st.markdown(f"""
                        <div style="background-color: #12161a; padding: 18px; border-radius: 10px; border-left: 5px solid #a0aec0; margin-bottom: 15px; border-top: 1px solid #262c35; border-right: 1px solid #262c35; border-bottom: 1px solid #262c35;">
                            <h4 style="margin: 0 0 10px 0; color: #ffffff;">🎯 Pick: <span style="color: #a0aec0;">{row['Market']}</span></h4>
                            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 10px; font-size: 14px; color: #a0aec0;">
                                <div><b>Odds:</b> <span style="color: #ffffff;">{row['Odds']:.2f}</span></div>
                                <div><b>Estimated Prob:</b> <span style="color: #ffffff;">{row['Estimated Probability']*100:.1f}%</span></div>
                                <div><b>Implied Prob:</b> <span style="color: #ffffff;">{row['Implied Probability']*100:.1f}%</span></div>
                                <div><b>Adjusted EV:</b> <span style="color: #a0aec0; font-weight: bold;">{row['Adjusted EV']*100:.2f}%</span></div>
                                <div><b>Safety Score:</b> <span style="color: #ffffff;">{row['Safety Score']:.1f}</span></div>
                                <div><b>Ranking Score:</b> <span style="color: #ffffff;">{row['Final Ranking Score']:.1f}</span></div>
                                <div><b>Risk Type:</b> <span style="color: #ffffff;">{row['Risk Type']}</span></div>
                                <div><b>Recommended Stake:</b> <span style="color: #ffffff; font-weight: bold;">{row['Recommended Stake']:.2f} €</span></div>
                                <div><b>Decision:</b> <span style="color: #a0aec0; font-weight: bold;">{row['Decision']}</span></div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            
            st.caption(
                "Notice: SVE calculates expected values based on statistical adjustments. Past performance does not guarantee future results."
            )

# ----------------------------------------------------
# TAB 2: BACKTESTING
# ----------------------------------------------------
with tab2:
    st.header("📊 Model Backtesting Suite")
    st.markdown("""
    Evaluate historical performance metrics of your betting selections by pasting your historical records.
    The CSV must contain exactly these columns:
    `Match`, `Market`, `Odds`, `Stake`, `Result`
    """)

    # Backtesting Default CSV
    backtest_example = """Match,Market,Odds,Stake,Result
Germany Scotland,Germany -1,1.75,1,Win
Hungary Switzerland,Both teams to score,1.85,1,Win
Belgium Slovakia,Belgium win,1.45,1,Loss"""

    backtest_input = st.text_area(
        "Paste Historical Picks (CSV)",
        value=backtest_example,
        height=180
    )

    valid_bt_csv = False
    df_bt_input = None

    if backtest_input.strip() != "":
        try:
            df_bt_input = pd.read_csv(StringIO(backtest_input))
            df_bt_input.columns = [c.strip() for c in df_bt_input.columns]
            
            required_bt_cols = ["Match", "Market", "Odds", "Stake", "Result"]
            missing_bt_cols = [c for c in required_bt_cols if c not in df_bt_input.columns]
            
            if missing_bt_cols:
                st.error(f"Validation Error: Backtesting CSV is missing columns: {', '.join(missing_bt_cols)}")
            else:
                # Type Conversion
                df_bt_input["Odds"] = pd.to_numeric(df_bt_input["Odds"], errors='coerce')
                df_bt_input["Stake"] = pd.to_numeric(df_bt_input["Stake"], errors='coerce')
                
                if df_bt_input[["Odds", "Stake"]].isnull().any().any():
                    st.error("Validation Error: Numeric columns (Odds, Stake) contain invalid non-numeric values.")
                else:
                    valid_bt_csv = True
                    st.subheader("📋 Historical Picks Preview")
                    st.dataframe(df_bt_input, use_container_width=True)
        except Exception as e:
            st.error(f"Error parsing Backtesting CSV: {str(e)}")

    if st.button("RUN BACKTEST ANALYTICS", use_container_width=True):
        if not valid_bt_csv:
            st.error("Cannot run backtest analysis. Please fix the CSV validation errors above.")
        else:
            # Process profitability
            bt_results = []
            total_picks = len(df_bt_input)
            wins = 0
            losses = 0
            pushes = 0
            total_stake = 0.0
            net_profit = 0.0
            odds_sum = 0.0
            
            for _, row in df_bt_input.iterrows():
                match = str(row["Match"])
                market = str(row["Market"])
                odds = float(row["Odds"])
                stake = float(row["Stake"])
                result = str(row["Result"]).strip().capitalize()
                
                # Profit Logic
                if result == "Win":
                    profit = stake * (odds - 1.0)
                    wins += 1
                elif result == "Loss":
                    profit = -stake
                    losses += 1
                elif result == "Push":
                    profit = 0.0
                    pushes += 1
                else:
                    profit = 0.0  # Fallback for unrecognized result types
                    
                total_stake += stake
                net_profit += profit
                odds_sum += odds
                
                bt_results.append({
                    "Match": match,
                    "Market": market,
                    "Odds": odds,
                    "Stake": stake,
                    "Result": result,
                    "Profit/Loss (€)": round(profit, 2)
                })
                
            df_bt_results = pd.DataFrame(bt_results)
            
            # Aggregate calculations
            win_rate = (wins / total_picks) if total_picks > 0 else 0.0
            win_rate_excl_push = (wins / (wins + losses)) if (wins + losses) > 0 else 0.0
            roi = (net_profit / total_stake * 100) if total_stake > 0 else 0.0
            avg_odds = (odds_sum / total_picks) if total_picks > 0 else 0.0
            
            # Display Backtest Analytics
            st.subheader("📈 Performance Metrics")
            
            col_b1, col_b2, col_b3, col_b4 = st.columns(4)
            with col_b1:
                st.metric("Total Picks", total_picks)
                st.metric("Average Odds", f"{avg_odds:.2f}")
            with col_b2:
                st.metric("Record (W-L-P)", f"{wins} - {losses} - {pushes}")
                st.metric("Win Rate", f"{win_rate * 100:.1f}%")
            with col_b3:
                st.metric("Total Stake Used", f"{total_stake:.2f} €")
                st.metric("Net Profit/Loss", f"{net_profit:.2f} €", delta=f"{net_profit:.2f} €")
            with col_b4:
                st.metric("ROI", f"{roi:.2f}%")
                st.metric("Win Rate (excl. Pushes)", f"{win_rate_excl_push * 100:.1f}%")
                
            st.subheader("📋 Backtest Execution Details")
            st.dataframe(df_bt_results, use_container_width=True)
