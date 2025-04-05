# niveles/nivel3_5_forma_pensamiento/entrenamiento_modelo.py

import pandas as pd
import os

# Cargar CSV desde nueva ruta del proyecto
csv_path = os.path.abspath('../../data/nivel1/registro_diario.csv')
df = pd.read_csv(csv_path)

# Campos necesarios según roadmap v3 - Nivel 3.5
campos_requeridos = [
    'forma_pensamiento',
    'tipo_procesamiento',
    'tension_cognitiva',
    'flexibilidad_mental',
    'estrategia_afrontamiento',
    'dialogo_interno',
    'tipo_tarea',
    'resultado'
]

# Validación: columnas presentes
df = df[[col for col in campos_requeridos if col in df.columns]].dropna()

# Análisis exploratorio básico
print("▶️ Formas de pensamiento registradas:")
print(df['forma_pensamiento'].value_counts())

print("\n▶️ Tipos de procesamiento:")
print(df['tipo_procesamiento'].value_counts())

print("\n▶️ Promedios:")
print("Tensión cognitiva:", df['tension_cognitiva'].mean())
print("Flexibilidad mental:", df['flexibilidad_mental'].mean())

# Exportar resultado limpio para otros niveles o dashboard
output_path = os.path.abspath('../../outputs/coach_ia/nivel3_5_forma_clean.csv')
df.to_csv(output_path, index=False)

print(f"\n✅ Datos procesados exportados a: {output_path}")

