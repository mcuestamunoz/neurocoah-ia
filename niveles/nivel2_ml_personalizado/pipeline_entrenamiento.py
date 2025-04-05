##########################################################
# 🧠 MICD - Pipeline de Entrenamiento Personalizado
# --------------------------------------------------------
# Este script entrena un modelo flexible para predecir
# distintos aspectos cognitivos del usuario a partir de
# sus registros diarios (Nivel 2 del MICD).
##########################################################

import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import (
    r2_score,
    accuracy_score,
    confusion_matrix,
    classification_report
)

######### 🔧 CONFIGURACIÓN FLEXIBLE #########

# Variable que quieres predecir (cambia según tu foco de análisis)
VARIABLE_OBJETIVO = "nivel_energia"  
# Ejemplos alternativos:
# "estado_emocional", "forma_pensamiento", "tipo_procesamiento"

# Lista de columnas que usarás como input (features)
FEATURES = [
    "forma_pensamiento",
    "tipo_procesamiento",
    "tension_cognitiva",
    "flexibilidad_mental",
    "estrategia_afrontamiento",
    "dialogo_interno"
]

######### 📥 CARGA DE DATOS #########

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
RUTA_CSV = os.path.join(BASE_DIR, "data/nivel1/registro_diario.csv")

def cargar_datos():
    df = pd.read_csv(RUTA_CSV)
    df = df.dropna(subset=[VARIABLE_OBJETIVO] + FEATURES)
    return df

######### ⚙️ PREPROCESAMIENTO #########

def construir_pipeline(X, y):
    # Detectar tipos de variables
    cat_features = X.select_dtypes(include='object').columns.tolist()
    num_features = X.select_dtypes(exclude='object').columns.tolist()

    # Crear transformaciones
    transformer = ColumnTransformer(transformers=[
        ('num', StandardScaler(), num_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), cat_features)
    ])

    # Modelo según tipo de variable objetivo
    if y.dtype == 'object' or y.nunique() <= 5:
        modelo = LogisticRegression(max_iter=1000)
        es_clasificacion = True
    else:
        modelo = LinearRegression()
        es_clasificacion = False

    # Pipeline de procesamiento + entrenamiento
    pipeline = Pipeline(steps=[
        ('preprocesamiento', transformer),
        ('modelo', modelo)
    ])
    
    return pipeline, es_clasificacion

######### 🧠 ENTRENAMIENTO Y EVALUACIÓN #########

def entrenar_y_evaluar(df):
    X = df[FEATURES]
    y = df[VARIABLE_OBJETIVO]

    pipeline, es_clasificacion = construir_pipeline(X, y)

    # Separar datos
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Entrenar
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)

    # Resultados
    if es_clasificacion:
        print("\n✅ MODELO DE CLASIFICACIÓN")
        print("Accuracy:", accuracy_score(y_test, y_pred))
        print("Reporte:\n", classification_report(y_test, y_pred))
        print("Matriz de confusión:\n", confusion_matrix(y_test, y_pred))
    else:
        print("\n✅ MODELO DE REGRESIÓN")
        print("R²:", r2_score(y_test, y_pred))

######### 🚀 EJECUCIÓN #########

if __name__ == "__main__":
    df = cargar_datos()
    entrenar_y_evaluar(df)
