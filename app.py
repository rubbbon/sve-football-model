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

# ----------------------------------------------------
# TAB 1: LIVE MODEL
# ----------------------------------------------------
with tab1:
    st.header("1. Parameters & Configurations")

    # Inputs organized in 3 columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        match = st.text_input("Match", "Spain vs France")
        competition = st.text_input("Competition", "Euro")
        phase = st.selectbox("Phase", ["Group", "Knockout", "Semifinal", "Final"])

    with col2:
        betting_house = st.text_input("Betting house", "Winamax")
        reliability = st.selectbox("Reliability", ["High", "Medium", "Low"])
        model_mode = st.selectbox("Model mode", ["Balanced", "Conservative", "Aggressive"])

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

    st.header("2. Markets Input")
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

    st.header("3. Execution of Value Model")

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

            # Calculate metrics for each market
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

                # Classification logic
                if odds < cuota_minima:
                    decision = "NO BET: ODDS TOO LOW"
                elif uncertainty >= 0.35:
                    decision = "NO BET: HIGH UNCERTAINTY"
                elif adj_ev > theta:
                    decision = "BET"
                elif simple_ev > 0:
                    decision = "PROBABLE BUT NOT ENOUGH VALUE"
                else:
                    decision = "NO BET"

                # Stake sizing
                if decision == "BET":
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
                    "Decision": decision
                })

            df_results = pd.DataFrame(results)

            # Sort and select recommended picks
            betting_picks_all = df_results[df_results["Decision"] == "BET"].sort_values(by="Adjusted EV", ascending=False)
            recommended_picks_count = len(betting_picks_all)
            picks_to_bet = betting_picks_all.head(max_picks)

            # Compute Dashboard Metrics
            total_markets = len(df_results)
            picks_count = len(picks_to_bet)
            best_adjusted_ev = df_results["Adjusted EV"].max() if total_markets > 0 else 0.0
            total_stake = picks_to_bet["Recommended Stake"].sum()
            avg_odds = df_results["Odds"].mean() if total_markets > 0 else 0.0
            
            # Expected profit estimate: sum(stake * adjusted EV) only for BET markets.
            expected_profit = (picks_to_bet["Recommended Stake"] * picks_to_bet["Adjusted EV"]).sum()

            # Render Metrics
            st.subheader("📈 Probability Engine & Live Metrics")
            
            col_m1, col_m2, col_m3 = st.columns(3)
            with col_m1:
                st.metric("Total Markets Analyzed", total_markets)
                st.metric("Total Stake", f"{total_stake:.2f} €")
            with col_m2:
                st.metric("Recommended Picks", f"{picks_count} (out of {recommended_picks_count} BETs)")
                st.metric("Average Odds", f"{avg_odds:.2f}")
            with col_m3:
                st.metric("Best Adjusted EV", f"{best_adjusted_ev * 100:.2f}%" if total_markets > 0 else "N/A")
                st.metric("Expected Profit Estimate", f"{expected_profit:.2f} €")

            st.progress(min(1.0, max(0.0, recommended_picks_count / max(1, total_markets))))

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
            
            st.dataframe(df_display, use_container_width=True)

            # Final Model Output Section
            st.markdown("---")
            st.subheader("🏆 FINAL MODEL OUTPUT")
            
            if recommended_picks_count == 0:
                st.warning("### FINAL DECISION: NO BET\n\n**Reason:** No market passed the risk-adjusted expected value threshold.")
            else:
                st.success(f"### FINAL DECISION: {picks_count} RECOMMENDED PICK(S)")
                for idx, row in picks_to_bet.iterrows():
                    st.markdown(f"""
                    <div style="background-color: #12161a; padding: 18px; border-radius: 10px; border-left: 5px solid #e63946; margin-bottom: 15px; border-top: 1px solid #262c35; border-right: 1px solid #262c35; border-bottom: 1px solid #262c35;">
                        <h4 style="margin: 0 0 10px 0; color: #ffffff;">🎯 Pick: <span style="color: #e63946;">{row['Market']}</span></h4>
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 10px; font-size: 14px; color: #a0aec0;">
                            <div><b>Odds:</b> <span style="color: #ffffff;">{row['Odds']:.2f}</span></div>
                            <div><b>Estimated Prob:</b> <span style="color: #ffffff;">{row['Estimated Probability']*100:.1f}%</span></div>
                            <div><b>Implied Prob:</b> <span style="color: #ffffff;">{row['Implied Probability']*100:.1f}%</span></div>
                            <div><b>Adjusted EV:</b> <span style="color: #00ff88; font-weight: bold;">{row['Adjusted EV']*100:.2f}%</span></div>
                            <div><b>Risk Type:</b> <span style="color: #ffffff;">{row['Risk Type']}</span></div>
                            <div><b>Recommended Stake:</b> <span style="color: #ffffff; font-weight: bold;">{row['Recommended Stake']:.2f} €</span></div>
                            <div><b>Decision:</b> <span class="status-ok">{row['Decision']}</span></div>
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
