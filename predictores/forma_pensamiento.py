##############################################################
# MICD – Predictor de Forma de Pensamiento
# ------------------------------------------------------------
# Este script carga el modelo entrenado en nivel 3.5 y realiza
# una predicción basada en un nuevo input simbólico o subjetivo.
##############################################################

import joblib
import os
import pandas as pd

######### 📁 Cargar modelo entrenado #########

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
RUTA_MODELO = os.path.join(BASE_DIR, "modelos/modelo_entrenado.pkl")

if not os.path.exists(RUTA_MODELO):
    print("❌ Modelo no entrenado aún. Ejecuta primero el script de entrenamiento.")
    exit()

modelo = joblib.load(RUTA_MODELO)
print("✅ Modelo cargado correctamente.")

######### 📝 Simulación de nuevo input #########

# Esto es un placeholder manual para cuando tengas UI o nuevos datos reales
nuevo_registro = {
    "tipo_procesamiento": "racional",
    "forma_pensamiento": "narrativa",
    "comentario": "Hoy estuve muy presente en todo",
    "simbolo_o_imagen": "fuego",
    "tension_cognitiva": 5,
    "flexibilidad_mental": 7
}


# Convertir a DataFrame de una fila
X_nuevo = pd.DataFrame([nuevo_registro])
print("\\n🧾 Datos utilizados para la predicción:")
print(X_nuevo)

######### 🔮 Predicción #########

pred = modelo.predict(X_nuevo)[0]
print(f"\n🧠 Nivel de conciencia estimado: {pred:.2f} (0–10)")
