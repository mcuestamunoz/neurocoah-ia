import streamlit as st

st.set_page_config(page_title="🧠 Neurocoach Dashboard", layout="centered")

import pandas as pd
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from openai import OpenAI
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Cargar entorno
load_dotenv()
OpenAI.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("🧠 Neurocoach Dashboard")

CSV_BASIC = os.path.abspath("../data/registro_experimento.csv")
CSV_AVANZADO = os.path.abspath("../data/registro_experimento_avanzado.csv")

tab1, tab2, tab3 = st.tabs(["🧠 Coach Cognitivo GPT", "🧬 Lector Sináptico", "📊 Visualización Cognitiva"])

# === COACH GPT ===
with tab1:
    st.subheader("📘 Resumen Cognitivo")
    try:
        df = pd.read_csv(CSV_BASIC)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df_week = df[df["timestamp"] >= datetime.now() - timedelta(days=7)]

        if df_week.empty:
            st.warning("No hay registros esta semana.")
        else:
            energia = df_week['energia_0_10'].mean()
            fatiga = df_week['fatiga_mental_0_10'].mean()
            control = df_week['control_pensamiento_0_10'].mean()
            conciencia = df_week['conciencia_presente_0_10'].mean()
            fase = df_week['fase_mental'].mode()[0]
            pensamiento = df_week['tipo_pensamiento'].mode()[0]

            resumen = f"""
            - Energía promedio: {energia:.2f}
            - Fatiga mental: {fatiga:.2f}
            - Control: {control:.2f}
            - Conciencia: {conciencia:.2f}
            - Fase mental: {fase}
            - Pensamiento: {pensamiento}
            """

            st.code(resumen)

            if st.button("📤 Pedir consejo a GPT"):
                with st.spinner("Consultando al coach..."):
                    prompt = f"""
Actúa como un coach cognitivo experto.

Resumen semanal:
{resumen}

1. Observa el patrón general.
2. Sugiere una estrategia de aprendizaje óptima.
3. Haz una pregunta introspectiva.
"""
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "Eres un mentor en neuroaprendizaje."},
                            {"role": "user", "content": prompt}
                        ]
                    )
                    st.success(response.choices[0].message.content)

    except Exception as e:
        st.error(f"⚠️ Error en Tab 1: {e}")

# === LECTOR SINÁPTICO ===
with tab2:
    st.subheader("🧬 Interpretación Simbólica")

    try:
        df2 = pd.read_csv(CSV_AVANZADO)
        df2 = df2.dropna(subset=["claridad_mental_0_10", "ruido_mental_0_10", "nivel_significado_0_10"])

        if df2.empty:
            st.warning("⚠️ No hay datos suficientes en el CSV avanzado.")
        else:
            # Encode vars
            for col in ["fase_aprendizaje", "fase_atencional", "nivel_dopaminico_estimado", "entropia_mental"]:
                df2[col + "_enc"] = LabelEncoder().fit_transform(df2[col])

            features = [
                "fase_aprendizaje_enc", "fase_atencional_enc", "nivel_dopaminico_estimado_enc",
                "entropia_mental_enc", "claridad_mental_0_10", "ruido_mental_0_10", "nivel_significado_0_10"
            ]
            X = StandardScaler().fit_transform(df2[features])
            df2["perfil_mental"] = KMeans(n_clusters=3, random_state=42, n_init='auto').fit_predict(X)

            ultimo = df2.iloc[-1]
            prompt = f"""
Lee este estado cognitivo:

- Fase: {ultimo['fase_aprendizaje']}
- Atención: {ultimo['fase_atencional']}
- Dopamina: {ultimo['nivel_dopaminico_estimado']}
- Entropía: {ultimo['entropia_mental']}
- Claridad: {ultimo['claridad_mental_0_10']}
- Ruido: {ultimo['ruido_mental_0_10']}
- Significado: {ultimo['nivel_significado_0_10']}
- Símbolo: {ultimo['simbolo_emergente']}
- Retención: {ultimo['retencion_spontanea']}
- Nota libre: {ultimo['nota_libre']}

Devuelve:
1. Lectura simbólica del estado.
2. Sugerencia para hoy.
3. Pregunta de exploración.
"""

            if st.button("🧠 Interpretar sinapsis"):
                with st.spinner("Descifrando..."):
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "Eres una IA sináptica que analiza patrones mentales."},
                            {"role": "user", "content": prompt}
                        ]
                    )
                    st.success(response.choices[0].message.content)

    except Exception as e:
        st.error(f"⚠️ Error en Tab 2: {e}")

with tab3:
    st.subheader("📈 Evolución de estados mentales")

    try:
        df = pd.read_csv(CSV_BASIC)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.sort_values("timestamp")

        metrics = [
            "energia_0_10",
            "fatiga_mental_0_10",
            "control_pensamiento_0_10",
            "conciencia_presente_0_10"
        ]

        st.markdown("Selecciona métricas para visualizar:")
        seleccionadas = st.multiselect("🧠 Métricas", metrics, default=metrics)

        if seleccionadas:
            st.line_chart(df.set_index("timestamp")[seleccionadas])
        else:
            st.info("Selecciona al menos una métrica para visualizarla.")

    except Exception as e:
        st.error(f"⚠️ Error en Tab 3: {e}")
