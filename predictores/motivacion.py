##############################################################
# MICD – Predictor Motivacional (Nivel 7)
# ------------------------------------------------------------
# Este script carga un modelo futuro entrenado para detectar
# el tipo de motivación interna y su impacto en el rendimiento.
##############################################################

import joblib
import os
import pandas as pd

######### 📁 Cargar modelo entrenado #########

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
RUTA_MODELO = os.path.join(BASE_DIR, "modelos/modelo_entrenado.pkl")

if not os.path.exists(RUTA_MODELO):
    print("❌ Modelo motivacional no encontrado. Aún no entrenado.")
    exit()

modelo = joblib.load(RUTA_MODELO)
print("✅ Modelo motivacional cargado correctamente.")

######### 📝 Simulación de nuevo input #########

nuevo_registro = {
    "forma_pensamiento": "visual",
    "tipo_procesamiento": "emocional",
    "comentario": "He sentido claridad mental y foco.",
    "simbolo_o_imagen": "fuego",
    "tension_cognitiva": 4,
    "flexibilidad_mental": 6,
    "estrategia_afrontamiento": "reformulación",
    "dialogo_interno": "autoapoyo"
}

X_nuevo = pd.DataFrame([nuevo_registro])
print("\\n🧾 Datos utilizados para la predicción:")
print(X_nuevo)

######### 🔮 Predicción #########

pred = modelo.predict(X_nuevo)[0]
print(f"\n🔋 Nivel estimado de motivación efectiva: {pred:.2f}")
