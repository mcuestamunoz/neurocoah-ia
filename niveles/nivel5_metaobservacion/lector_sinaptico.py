import pandas as pd
import os
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder, StandardScaler
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime

# --- Configuración ---
load_dotenv()
OpenAI.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

CSV_PATH = os.path.abspath("../data/registro_experimento_avanzado.csv")

# --- Carga de datos ---
df = pd.read_csv(CSV_PATH)
df = df.dropna(subset=["claridad_mental_0_10", "ruido_mental_0_10", "nivel_significado_0_10"])

# --- Preprocesamiento ---
label_cols = ["fase_aprendizaje", "fase_atencional", "nivel_dopaminico_estimado", "entropia_mental"]
encoders = {col: LabelEncoder().fit(df[col]) for col in label_cols}
for col, encoder in encoders.items():
    df[col + "_enc"] = encoder.transform(df[col])

features = [
    "fase_aprendizaje_enc", "fase_atencional_enc", "nivel_dopaminico_estimado_enc",
    "entropia_mental_enc", "claridad_mental_0_10", "ruido_mental_0_10", "nivel_significado_0_10"
]

X = StandardScaler().fit_transform(df[features])

# --- Clustering cognitivo ---
kmeans = KMeans(n_clusters=3, random_state=42, n_init='auto')
df["perfil_mental"] = kmeans.fit_predict(X)

# --- Resumen semántico ---
ultimo = df.iloc[-1]
simbolo = ultimo["simbolo_emergente"]
perfil = int(ultimo["perfil_mental"])
retencion = ultimo.get("retencion_spontanea", "sin datos")
nota = ultimo.get("nota_libre", "")

# --- Mensaje a GPT ---
prompt = f"""
Actúa como un lector de sinapsis personalizado.

Estoy diseñando una IA que detecta estados cognitivos internos para acelerar el aprendizaje. El último registro presenta:

- Fase de aprendizaje: {ultimo["fase_aprendizaje"]}
- Estado atencional: {ultimo["fase_atencional"]}
- Nivel dopaminérgico estimado: {ultimo["nivel_dopaminico_estimado"]}
- Entropía mental: {ultimo["entropia_mental"]}
- Claridad mental: {ultimo["claridad_mental_0_10"]}
- Ruido mental: {ultimo["ruido_mental_0_10"]}
- Nivel de significado emocional: {ultimo["nivel_significado_0_10"]}
- Símbolo emergente: {simbolo}
- Retención espontánea: {retencion}
- Insight libre: {nota}
- Perfil mental detectado (cluster #{perfil})

Genera una lectura sináptica de este estado: incluye una interpretación simbólica, una sugerencia de acción y una pregunta de autoexploración.
"""

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Eres una IA especializada en interpretar patrones cognitivos y simbólicos para guiar el aprendizaje acelerado."},
        {"role": "user", "content": prompt}
    ]
)

respuesta = response.choices[0].message.content
print("\n🧠 Lectura sináptica del día:")
print(respuesta)

# Guardar log
fecha = datetime.now().strftime("%Y-%m-%d_%H-%M")
log_path = os.path.abspath(f"../data/log_lector_sinaptico_{fecha}.txt")
with open(log_path, "w", encoding="utf-8") as f:
    f.write("🧠 LECTURA SINÁPTICA DEL DÍA\n\n")
    f.write(respuesta)

print(f"\n📝 Log guardado en: {log_path}")
