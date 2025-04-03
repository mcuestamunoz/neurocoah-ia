# 🧠 Coach Cognitivo con GPT – Neurocoach IA (versión mejorada)

import pandas as pd
from openai import OpenAI
import os
import joblib
from datetime import datetime, timedelta
from dotenv import load_dotenv

# --- CONFIGURACIÓN Y CLAVES ---
load_dotenv()
OpenAI.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- RUTAS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.abspath('../neurocoach-ia/data/registro_experimento.csv')
MODELO_PATH = os.path.abspath('../neurocoach-ia/data/modelo_predictivo.pkl')
LOG_DIR = os.path.abspath(os.path.join('..', 'fase4_coach_ia', 'logs'))
os.makedirs(LOG_DIR, exist_ok=True)

# --- CARGA Y FILTRO DE DATOS (últimos 7 días) ---
df = pd.read_csv(CSV_PATH)
df['timestamp'] = pd.to_datetime(df['timestamp'])
una_semana = datetime.now() - timedelta(days=7)
df_semana = df[df['timestamp'] >= una_semana]

if df_semana.empty:
    print("⚠️ No hay datos de los últimos 7 días.")
    exit()

# --- ANÁLISIS COGNITIVO ---
energia_prom = df_semana['energia_0_10'].mean()
fatiga_prom = df_semana['fatiga_mental_0_10'].mean()
control_prom = df_semana['control_pensamiento_0_10'].mean()
conciencia_prom = df_semana['conciencia_presente_0_10'].mean()

fase_mas_frecuente = df_semana['fase_mental'].mode()[0]
pensamiento_mas_frecuente = df_semana['tipo_pensamiento'].mode()[0]
simbolos = ", ".join(df_semana['simbolo_o_imagen'].dropna().unique().tolist())
palabras = ", ".join(df_semana['palabra_repetitiva'].dropna().unique().tolist())

# --- PREDICCIÓN DEL MODELO ---
try:
    modelo = joblib.load(MODELO_PATH)
    entrada = pd.DataFrame([{
        'energia_0_10': energia_prom,
        'fatiga_mental_0_10': fatiga_prom,
        'control_pensamiento_0_10': control_prom,
        'conciencia_presente_0_10': conciencia_prom,
        'tipo_pensamiento': pensamiento_mas_frecuente,
        'simbolo_o_imagen': df_semana['simbolo_o_imagen'].dropna().values[0] if not df_semana['simbolo_o_imagen'].dropna().empty else "ninguno",
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
    prediccion_str = f"⚠️ No se pudo calcular la predicción: {str(e)}"

# --- RESUMEN PARA GPT ---
resumen = f"""
🧠 Resumen Cognitivo de los últimos 7 días:

- Energía promedio: {energia_prom:.2f}
- Fatiga mental: {fatiga_prom:.2f}
- Control del pensamiento: {control_prom:.2f}
- Conciencia presente: {conciencia_prom:.2f}
- Fase mental más frecuente: {fase_mas_frecuente}
- Tipo de pensamiento predominante: {pensamiento_mas_frecuente}
- Símbolos mentales reportados: {simbolos}
- Palabras o frases repetitivas: {palabras}
- {prediccion_str}
"""

# --- PROMPT DE COACH GPT ---
prompt = f"""
Actúa como un coach cognitivo experto en productividad mental y autoconocimiento.

Basado en el siguiente resumen cognitivo semanal, realiza:
1. Una observación sobre los patrones mentales y emocionales.
2. Un consejo personalizado para optimizar la próxima semana.
3. Una pregunta poderosa para la autoexploración.

{resumen}
"""

# --- LLAMADA A GPT ---
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Eres un coach cognitivo que ayuda a las personas a entender cómo piensan y aprenden mejor."},
        {"role": "user", "content": prompt}
    ]
)
respuesta = response.choices[0].message.content

# --- RESULTADO ---
print("\n🧠 Análisis del Coach IA")
print(respuesta)

# --- GUARDAR LOG ---
fecha_hoy = datetime.now().strftime("%Y-%m-%d")
log_path = os.path.join(LOG_DIR, f"log_{fecha_hoy}.txt")
with open(log_path, "w", encoding="utf-8") as f:
    f.write("🧠 Resumen Cognitivo:\n")
    f.write(resumen)
    f.write("\n\n💬 Respuesta de GPT:\n")
    f.write(respuesta)

print(f"\n📝 Log guardado en: {log_path}")


