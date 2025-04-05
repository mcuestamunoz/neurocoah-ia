import pandas as pd
from datetime import datetime
import os

# Ruta al CSV actualizado
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "registro_experimento.csv")

# Cargar datos
df = pd.read_csv(DATA_PATH)
df['timestamp'] = pd.to_datetime(df['timestamp'])
hoy = datetime.now().strftime("%Y-%m-%d")
df['fecha'] = df['timestamp'].dt.strftime("%Y-%m-%d")
df_hoy = df[df['fecha'] == hoy]

print(f"\n📅 Registros del día {hoy}")
print("-" * 50)

if df_hoy.empty:
    print("⚠️ No hay registros para hoy.")
else:
    # Promedios de indicadores numéricos
    for col in ['energia_0_10', 'fatiga_mental_0_10', 'control_pensamiento_0_10', 'conciencia_presente_0_10']:
        promedio = pd.to_numeric(df_hoy[col], errors='coerce').mean()
        print(f"🔹 {col.replace('_', ' ').capitalize()}: {promedio:.2f}")

    # Más comunes
    def mostrar_mas_comun(nombre_col):
        print(f"\n📌 {nombre_col.replace('_', ' ').capitalize()} más común:")
        print(df_hoy[nombre_col].value_counts().head(3))

    mostrar_mas_comun('fase_mental')
    mostrar_mas_comun('tipo_pensamiento')

    # Símbolos
    if 'simbolo_o_imagen' in df_hoy.columns:
        simbolos = df_hoy['simbolo_o_imagen'].dropna().unique()
        print("\n🔣 Símbolos mentales del día:")
        for s in simbolos:
            print(f"- {s}")

    # Palabras repetitivas
    if 'palabra_repetitiva' in df_hoy.columns:
        palabras = df_hoy['palabra_repetitiva'].dropna().unique()
        print("\n🔁 Palabras o frases repetitivas:")
        for p in palabras:
            print(f"- {p}")

    # Aprendizaje espontáneo
    if 'aprendizaje_espontaneo' in df_hoy.columns:
        print("\n🧠 Aprendizaje espontáneo reportado:")
        for a in df_hoy['aprendizaje_espontaneo'].dropna():
            print(f"- {a}")

    # Resistencia detectada
    if 'resistencia_detectada' in df_hoy.columns:
        print("\n⚡ Resistencia detectada:")
        for r in df_hoy['resistencia_detectada'].dropna():
            print(f"- {r}")

    # Nota libre
    if 'nota_libre' in df_hoy.columns:
        print("\n🗯️ Comentarios introspectivos:")
        for c in df_hoy['nota_libre'].dropna():
            print(f"- {c}")
