import streamlit as st
import pandas as pd
import os
import joblib
from datetime import datetime, timedelta
from dotenv import load_dotenv
from openai import OpenAI

# --- CONFIGURACIÓN INICIAL ---
load_dotenv()
OpenAI.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="🧠 NeuroCoach IA", layout="centered")
st.title("🧠 Análisis Cognitivo Semanal + GPT Coach")

# --- CARGA DE DATOS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.abspath('../data/registro_experimento.csv')
MODELO_PATH = os.path.abspath('../data/modelo_predictivo.pkl')

try:
    df = pd.read_csv(CSV_PATH)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
except Exception as e:
    st.error(f"⚠️ Error cargando CSV: {e}")
    st.stop()

# --- FILTRO TEMPORAL ---
una_semana = datetime.now() - timedelta(days=7)
df_semana = df[df["timestamp"] >= una_semana]

if df_semana.empty:
    st.warning("No hay datos de los últimos 7 días.")
    st.stop()

# --- MÉTRICAS ---
energia = df_semana['energia_0_10'].mean()
fatiga = df_semana['fatiga_mental_0_10'].mean()
control = df_semana['control_pensamiento_0_10'].mean()
conciencia = df_semana['conciencia_presente_0_10'].mean()
fase = df_semana['fase_mental'].mode()[0]
pensamiento = df_semana['tipo_pensamiento'].mode()[0]
simbolos = ", ".join(df_semana['simbolo_o_imagen'].dropna().unique())
palabras = ", ".join(df_semana['palabra_repetitiva'].dropna().unique())

# --- MODELO (opcional) ---
try:
    modelo = joblib.load(MODELO_PATH)
    entrada = pd.DataFrame([{
        'energia_0_10': energia,
        'fatiga_mental_0_10': fatiga,
        'control_pensamiento_0_10': control,
        'conciencia_presente_0_10': conciencia,
        'tipo_pensamiento': pensamiento,
        'simbolo_o_imagen': simbolos.split(",")[0] if simbolos else "ninguno",
        'input_tipo': df_semana['input_tipo'].mode()[0],
        'input_intensidad': df_semana['input_intensidad'].mode()[0],
        'contenido_estudiado': df_semana['contenido_estudiado'].mode()[0],
        'Dia_Semana': datetime.now().strftime("%A"),
        'Hora_Num': datetime.now().hour,
        'Comentario_longitud': df_semana['nota_libre'].apply(lambda x: len(str(x))).mean()
    }])
    pred = modelo.predict(entrada)[0]
    prediccion_str = f"📈 Predicción del estado mental esperado: {pred:.2f}"
except Exception as e:
    prediccion_str = f"⚠️ No se pudo calcular predicción: {e}"

# --- RESUMEN COGNITIVO ---
resumen = f"""
- Energía: {energia:.2f}
- Fatiga mental: {fatiga:.2f}
- Control del pensamiento: {control:.2f}
- Conciencia presente: {conciencia:.2f}
- Fase mental más frecuente: {fase}
- Tipo de pensamiento predominante: {pensamiento}
- Símbolos mentales: {simbolos}
- Palabras repetidas: {palabras}
- {prediccion_str}
"""

with st.expander("🔍 Resumen Cognitivo de la Semana"):
    st.markdown(resumen)

# --- PREGUNTA A GPT ---
if st.button("🧠 Pedir consejo al Coach IA"):
    with st.spinner("Consultando a GPT..."):

        prompt = f"""
Eres un coach cognitivo experto. Basado en este resumen mental semanal:

{resumen}

Genera:
1. Una observación sobre los patrones mentales.
2. Un consejo para mejorar la próxima semana.
3. Una pregunta poderosa para autoexploración.
"""
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un coach cognitivo que guía en autoconocimiento, foco y bienestar mental."},
                {"role": "user", "content": prompt}
            ]
        )

        feedback = response.choices[0].message.content
        st.markdown("### 🧠 Feedback del Coach")
        st.success(feedback)

        # Guardar log opcional
        fecha = datetime.now().strftime("%Y-%m-%d")
        log_path = os.path.join("logs", f"log_{fecha}.txt")
        os.makedirs("logs", exist_ok=True)
        with open(log_path, "w", encoding="utf-8") as f:
            f.write("🧠 Resumen Cognitivo:\n")
            f.write(resumen)
            f.write("\n\n💬 Respuesta GPT:\n")
            f.write(feedback)
        st.caption(f"📁 Log guardado en: `{log_path}`")
