import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="SVE - Statistical Value Engine",
    page_icon="⚽",
    layout="wide"
)

st.markdown("""
<style>

.stApp {

    background-color: #0E1117;

    color: white;

}

.big-title {

    font-size: 44px;

    font-weight: 900;

    color: #00FF9C;

    margin-bottom: 0px;

}

.subtitle {

    font-size: 18px;

    color: #C9D1D9;

    margin-bottom: 20px;

}

.module {

    background-color: #161B22;

    padding: 18px;

    border-radius: 14px;

    border: 1px solid #30363D;

    margin-bottom: 12px;

}

.formula {

    background-color: #161B22;

    padding: 20px;

    border-radius: 14px;

    border-left: 5px solid #00FF9C;

    font-size: 18px;

    color: #E6EDF3;

}

.small-text {

    color: #8B949E;

    font-size: 14px;

}

.status-ok {

    color: #00FF9C;

    font-weight: bold;

}

.status-warn {

    color: #FFD166;

    font-weight: bold;

}

.status-bad {

    color: #FF5C5C;

    font-weight: bold;

}

/* Texto de etiquetas de inputs */

label, .stTextInput label, .stNumberInput label, .stSelectbox label, .stSlider label {

    color: white !important;

}

/* Texto general */

.stMarkdown, .stText, p, span, div {

    color: white;

}

/* Texto de ayuda y captions */

small, .stCaption, [data-testid="stCaptionContainer"] {

    color: #C9D1D9 !important;

}

/* Texto dentro de inputs */

input, textarea {

    color: white !important;

}

/* Selectbox */

div[data-baseweb="select"] > div {

    color: white !important;

}
/* Etiquetas de los campos */
label, .stTextInput label, .stNumberInput label, .stSelectbox label, .stSlider label, .stTextArea label {
    color: white !important;
    font-weight: 600 !important;
}

/* Recuadros de texto */
.stTextInput input {
    background-color: #E63946 !important;
    color: black !important;
    border: 2px solid #FF6B6B !important;
    border-radius: 10px !important;
}

/* Recuadros numéricos */
.stNumberInput input {
    background-color: #E63946 !important;
    color: black !important;
    border: 2px solid #FF6B6B !important;
    border-radius: 10px !important;
}

/* Recuadro grande para CSV */
.stTextArea textarea {
    background-color: #E63946 !important;
    color: black !important;
    border: 2px solid #FF6B6B !important;
    border-radius: 10px !important;
}

/* Placeholder dentro de inputs */
.stTextInput input::placeholder,
.stNumberInput input::placeholder,
.stTextArea textarea::placeholder {
    color: black !important;
    opacity: 0.7 !important;
}

/* Selectbox cerrado */
div[data-baseweb="select"] > div {
    background-color: #E63946 !important;
    color: black !important;
    border: 2px solid #FF6B6B !important;
    border-radius: 10px !important;
}

/* Texto dentro del selectbox */
div[data-baseweb="select"] span {
    color: black !important;
}

/* Flecha del selectbox */
div[data-baseweb="select"] svg {
    fill: black !important;
}

/* Opciones desplegadas del selectbox */
div[data-baseweb="popover"] {
    background-color: #E63946 !important;
}

div[data-baseweb="popover"] li {
    background-color: #E63946 !important;
    color: black !important;
}

/* Sliders */
.stSlider label {
    color: white !important;
}

/* Botones + y - de number input */
button[kind="secondary"] {
    background-color: #E63946 !important;
    color: black !important;
    border: 1px solid #FF6B6B !important;
}
</style>

""", unsafe_allow_html=True)

st.divider()

st.header("1. Datos del partido")

col1, col2, col3 = st.columns(3)

with col1:
    partido = st.text_input("Partido", "España vs Francia")
    competicion = st.text_input("Competición", "Mundial")
    fase = st.selectbox("Fase", ["Grupo", "Eliminatoria", "Semifinal", "Final"])

with col2:
    casa = st.text_input("Casa de apuestas", "Winamax")
    fiabilidad = st.selectbox("Fiabilidad del análisis", ["Alta", "Media", "Baja"])
    modo = st.selectbox("Modo del modelo", ["Conservador", "Equilibrado", "Agresivo"])

with col3:
    bankroll = st.number_input("Bankroll simulado (€)", min_value=1.0, value=100.0, step=10.0)
    max_picks = st.slider("Máximo de picks recomendados", 1, 5, 2)
    cuota_minima = st.number_input("Cuota mínima aceptable", min_value=1.01, value=1.40, step=0.01)

st.divider()

st.header("2. Mercados a analizar")

st.markdown("""
Puedes introducir los mercados de dos formas:

1. Pegando una tabla en bloque.
2. Usando el ejemplo y cambiando los datos.

Formato obligatorio:

Mercado,Cuota,Probabilidad,Riesgo,Incertidumbre,Tipo
""")

ejemplo_csv = """Mercado,Cuota,Probabilidad,Riesgo,Incertidumbre,Tipo
Under 2.5 goles,1.80,66,8,8,Bajo
España gana,2.10,48,18,16,Medio
Más de 8.5 córners,1.85,61,12,10,Medio
Francia over 1.5 tarjetas,1.90,60,15,12,Medio"""

markets_text = st.text_area(
    "Pega aquí los mercados en formato CSV",
    value=ejemplo_csv,
    height=220
)

markets = []

try:
    from io import StringIO

    df_input = pd.read_csv(StringIO(markets_text))

    columnas_necesarias = ["Mercado", "Cuota", "Probabilidad", "Riesgo", "Incertidumbre", "Tipo"]

    if all(col in df_input.columns for col in columnas_necesarias):
        st.success("Mercados cargados correctamente.")

        st.dataframe(df_input, use_container_width=True)

        for _, row in df_input.iterrows():
            markets.append({
                "Mercado": str(row["Mercado"]),
                "Cuota": float(row["Cuota"]),
                "Probabilidad estimada": float(row["Probabilidad"]) / 100,
                "Riesgo": float(row["Riesgo"]) / 100,
                "Incertidumbre": float(row["Incertidumbre"]) / 100,
                "Tipo de riesgo": str(row["Tipo"])
            })

    else:
        st.error("Faltan columnas. Usa exactamente: Mercado, Cuota, Probabilidad, Riesgo, Incertidumbre, Tipo")

except Exception as e:
    st.error("Error al leer los mercados. Revisa que el formato sea correcto.")
    st.code(str(e))

st.header("3. Ejecución del modelo")

if st.button("RUN VALUE MODEL", use_container_width=True):

    if not markets:
        st.error("No hay mercados válidos para analizar.")

    else:
        if fase == "Final":
            theta = 0.08
        elif fase in ["Eliminatoria", "Semifinal"]:
            theta = 0.06
        else:
            theta = 0.04

        if fiabilidad == "Baja":
            theta += 0.03
        elif fiabilidad == "Media":
            theta += 0.01

        if modo == "Conservador":
            lamb = 0.45
            rho = 0.45
        elif modo == "Equilibrado":
            lamb = 0.35
            rho = 0.35
        else:
            lamb = 0.25
            rho = 0.25

        results = []

        for m in markets:
            cuota = m["Cuota"]
            p = m["Probabilidad estimada"]
            riesgo = m["Riesgo"]
            incertidumbre = m["Incertidumbre"]

            prob_implicita = 1 / cuota
            ev_simple = (p * cuota) - 1
            p_ajustada = max(0, p - lamb * incertidumbre - rho * riesgo)
            ev_ajustado = (p_ajustada * cuota) - 1
            edge = p - prob_implicita

            if cuota < cuota_minima:
                decision = "NO APOSTAR: cuota demasiado baja"
            elif incertidumbre >= 0.35:
                decision = "NO APOSTAR: incertidumbre alta"
            elif ev_ajustado > theta:
                decision = "APOSTAR"
            elif ev_simple > 0 and ev_ajustado <= theta:
                decision = "PROBABLE, PERO SIN VALOR SUFICIENTE"
            else:
                decision = "NO APOSTAR"

            if decision == "APOSTAR":
                if m["Tipo de riesgo"] == "Bajo":
                    stake = bankroll * 0.015
                elif m["Tipo de riesgo"] == "Medio":
                    stake = bankroll * 0.01
                else:
                    stake = bankroll * 0.005
            else:
                stake = 0

            results.append({
                "Mercado": m["Mercado"],
                "Cuota": round(cuota, 2),
                "P estimada": f"{p*100:.1f}%",
                "P implícita": f"{prob_implicita*100:.1f}%",
                "Edge": f"{edge*100:.1f}%",
                "P ajustada": f"{p_ajustada*100:.1f}%",
                "EV simple": f"{ev_simple*100:.1f}%",
                "EV ajustado": f"{ev_ajustado*100:.1f}%",
                "Riesgo": m["Tipo de riesgo"],
                "Stake recomendado (€)": round(stake, 2),
                "Decisión": decision
            })

        df = pd.DataFrame(results)

        def ev_to_float(x):
            return float(x.replace("%", ""))

        df["EV_num"] = df["EV ajustado"].apply(ev_to_float)
        df = df.sort_values(by="EV_num", ascending=False).drop(columns=["EV_num"])

        st.subheader("4. Probability Engine")

        col_a, col_b, col_c, col_d = st.columns(4)

        total_mercados = len(df)
        picks = len(df[df["Decisión"] == "APOSTAR"])
        mejor_ev = df["EV ajustado"].iloc[0]
        stake_total = df["Stake recomendado (€)"].sum()

        with col_a:
            st.metric("Mercados analizados", total_mercados)
        with col_b:
            st.metric("Picks recomendados", picks)
        with col_c:
            st.metric("Mejor EV ajustado", mejor_ev)
        with col_d:
            st.metric("Stake total", f"{stake_total:.2f} €")

        st.progress(min(1.0, max(0.0, picks / max(1, total_mercados))))

        st.subheader("5. Tabla de mercados")

        st.dataframe(df, use_container_width=True)

        st.divider()

        st.subheader("6. Output final")

        picks_df = df[df["Decisión"] == "APOSTAR"].head(max_picks)

        if picks_df.empty:
            st.warning("DECISIÓN FINAL: NO APOSTAR. No hay valor ajustado suficiente.")
        else:
            for idx, row in picks_df.iterrows():
                st.success(
                    f"Pick recomendado: {row['Mercado']} | "
                    f"Cuota: {row['Cuota']} | "
                    f"EV ajustado: {row['EV ajustado']} | "
                    f"Stake: {row['Stake recomendado (€)']} €"
                )

        st.caption(
            "El modelo calcula valor esperado ajustado al riesgo según los datos introducidos. "
            "No garantiza beneficios."
        )
