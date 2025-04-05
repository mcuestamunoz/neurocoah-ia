import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

#########################
# CONFIGURACIÓN
#########################

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
RUTA_CSV = os.path.join(BASE_DIR, "data/nivel1/registro_conciencia.csv")
RUTA_MODELO = os.path.join(BASE_DIR, "modelos/modelo_entrenado.pkl")
os.makedirs(os.path.dirname(RUTA_MODELO), exist_ok=True)

# Cambia esta línea para probar otras variables objetivo
VARIABLE_OBJETIVO = "conciencia_presente_0_10"  # o "nivel_energia", etc.

# Features según variable objetivo
FEATURES_CONFIG = {
    "nivel_energia": [
        "forma_pensamiento", "tipo_procesamiento", "tension_cognitiva",
        "flexibilidad_mental", "estrategia_afrontamiento", "dialogo_interno"
    ],
    "conciencia_presente_0_10": [
        "tipo_procesamiento", "forma_pensamiento", "comentario", "simbolo_o_imagen",
        "tension_cognitiva", "flexibilidad_mental"
    ]
}

FEATURES = FEATURES_CONFIG.get(VARIABLE_OBJETIVO)
if FEATURES is None:
    raise ValueError(f"No se han definido FEATURES para la variable '{VARIABLE_OBJETIVO}'.")

#########################
# CARGA Y PREPROCESAMIENTO
#########################

def cargar_datos():
    if not os.path.exists(RUTA_CSV):
        print("❌ No se encontró el archivo de datos.")
        return None
    df = pd.read_csv(RUTA_CSV)
    df = df.dropna(subset=FEATURES + [VARIABLE_OBJETIVO])
    return df

def construir_pipeline(X):
    cat_features = X.select_dtypes(include='object').columns.tolist()
    num_features = X.select_dtypes(exclude='object').columns.tolist()

    preprocessor = ColumnTransformer(transformers=[
        ('num', 'passthrough', num_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), cat_features)
    ])

    modelo = RandomForestRegressor(n_estimators=100, random_state=42)

    pipeline = Pipeline(steps=[
        ('preprocesamiento', preprocessor),
        ('modelo', modelo)
    ])
    return pipeline

#########################
# ENTRENAMIENTO
#########################

def entrenar_y_evaluar(df):
    if len(df) < 5:
        print(f"⚠️ Muy pocos registros ({len(df)}). Se requieren al menos 5.")
        return

    X = df[FEATURES]
    y = df[VARIABLE_OBJETIVO]

    pipeline = construir_pipeline(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)

    print("\n📈 Resultados del modelo:")
    print("MAE:", mean_absolute_error(y_test, y_pred))
    print("R²:", r2_score(y_test, y_pred))

    joblib.dump(pipeline, RUTA_MODELO)
    print(f"✅ Modelo guardado en: {RUTA_MODELO}")

#########################
# MAIN
#########################

def main():
    df = cargar_datos()
    if df is not None:
        entrenar_y_evaluar(df)

if __name__ == "__main__":
    main()