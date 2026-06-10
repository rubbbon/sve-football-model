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
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-title">SVE — Statistical Value Engine</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Football Market Expected Value Model</div>', unsafe_allow_html=True)

st.markdown("""
<div class="formula">
<b>Modelo matemático:</b><br><br>
EV* = [(P estimada − λ × Incertidumbre − ρ × Riesgo) × Cuota] − 1
<br><br>
<b>Regla:</b> apostar solo si el valor esperado ajustado supera el umbral mínimo exigido.
</div>
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
Introduce los mercados manualmente.  
Ejemplos: **España gana**, **Más de 8.5 córners**, **Francia más tarjetas**, **Under 2.5 goles**, **Ambos marcan: sí**.
""")

num_markets = st.slider("Número de mercados", 1, 10, 4)

markets = []

for i in range(num_markets):
    st.markdown(f"### Mercado {i+1}")
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        mercado = st.text_input(
            f"Nombre del mercado {i+1}",
            f"Mercado {i+1}",
            key=f"mercado_{i}"
        )
        cuota = st.number_input(
            f"Cuota {i+1}",
            min_value=1.01,
            value=1.80,
            step=0.01,
            key=f"cuota_{i}"
        )

    with c2:
        prob_estimada = st.slider(
            f"Probabilidad estimada (%) {i+1}",
            1,
            99,
            55,
            key=f"prob_{i}"
        )
        riesgo = st.slider(
            f"Riesgo (%) {i+1}",
            0,
            60,
            10,
            key=f"riesgo_{i}"
        )

    with c3:
        incertidumbre = st.slider(
            f"Incertidumbre (%) {i+1}",
            0,
            60,
            10,
            key=f"incertidumbre_{i}"
        )
        tipo_riesgo = st.selectbox(
            f"Tipo de riesgo {i+1}",
            ["Bajo", "Medio", "Alto"],
            key=f"tipo_{i}"
        )

    with c4:
        mercado_valido = st.checkbox(
            f"Incluir mercado {i+1}",
            value=True,
            key=f"valid_{i}"
        )

    if mercado_valido:
        markets.append({
            "Mercado": mercado,
            "Cuota": cuota,
            "Probabilidad estimada": prob_estimada / 100,
            "Riesgo": riesgo / 100,
            "Incertidumbre": incertidumbre / 100,
            "Tipo de riesgo": tipo_riesgo
        })

st.divider()

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
