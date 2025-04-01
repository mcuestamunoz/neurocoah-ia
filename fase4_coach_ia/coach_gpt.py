# 🧠 Coach Cognitivo con GPT – Neurocoach IA

import pandas as pd
import openai
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# --- CARGAR CLAVE DESDE .env ---
load_dotenv()  # 👉 Carga variables del .env
openai.api_key = os.getenv("OPENAI_API_KEY")

# --- CARGA Y FILTRADO DE DATOS ---
ruta_csv = os.path.abspath(os.path.join('..', 'data', 'registro_cognitivo.csv'))
df = pd.read_csv(ruta_csv)
df['Datetime'] = pd.to_datetime(df['Fecha'] + ' ' + df['Hora'])

# Últimos 7 días
una_semana = datetime.now() - timedelta(days=7)
df_semana = df[df['Datetime'] >= una_semana]

# --- ANÁLISIS AUTOMÁTICO ---
energia_prom = df_semana['Energia'].mean()
animo_prom = df_semana['Estado_Animo'].mean()
resultado_prom = df_semana['Resultado'].mean()
tarea_mas_frecuente = df_semana['Tipo_tarea'].mode()[0] if not df_semana.empty else "No disponible"
dia_mas_fuerte = df_semana['Datetime'].dt.day_name().mode()[0] if not df_semana.empty else "No disponible"

resumen_analisis = f"""
Resumen de los últimos 7 días:
- Energía media: {energia_prom:.2f}
- Estado de ánimo medio: {animo_prom:.2f}
- Resultado percibido medio: {resultado_prom:.2f}
- Tipo de tarea más frecuente: {tarea_mas_frecuente}
- Día con mayor actividad: {dia_mas_fuerte}
"""

# --- PROMPT PARA GPT ---
prompt = f"""
Eres un coach cognitivo. Basado en el siguiente resumen semanal, ofrece:
1. Un consejo personalizado.
2. Una observación sobre los patrones.
3. Una pregunta poderosa para reflexión.

{resumen_analisis}
"""

# --- LLAMADA A GPT ---
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Eres un coach cognitivo experto en productividad y bienestar."},
        {"role": "user", "content": prompt}
    ]
)

respuesta = response.choices[0].message.content
print("\n🧠 Análisis del Coach IA")
print(respuesta)
