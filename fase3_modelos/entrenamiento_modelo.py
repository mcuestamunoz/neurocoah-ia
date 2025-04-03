import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

# --- CARGA DE DATOS ---
RUTA_CSV = os.path.abspath('../neurocoach-ia/data/registro_experimento.csv')
df = pd.read_csv(RUTA_CSV)
df = df.dropna(subset=[
    'energia_0_10', 'fatiga_mental_0_10',
    'control_pensamiento_0_10', 'conciencia_presente_0_10']) # Solo eliminamos filas donde las columnas numéricas críticas estén vacías

# --- FEATURE ENGINEERING ---
df['Datetime'] = pd.to_datetime(df['timestamp'])
df['Dia_Semana'] = df['Datetime'].dt.day_name()
df['Hora_Num'] = df['Datetime'].dt.hour
df['Comentario_longitud'] = df['nota_libre'].apply(lambda x: len(str(x)))

# --- VARIABLES DE ENTRADA Y SALIDA ---
# Seleccionamos las variables de entrada (X) y salida (y)
X = df[['energia_0_10', 'fatiga_mental_0_10', 'control_pensamiento_0_10', 
        'conciencia_presente_0_10', 'tipo_pensamiento', 'simbolo_o_imagen', 
        'input_tipo', 'input_intensidad', 'contenido_estudiado', 'Dia_Semana', 
        'Hora_Num', 'Comentario_longitud']]

# La variable objetivo: aprendizaje espontáneo
y = df['conciencia_presente_0_10'].astype(float)  # Asegúrate de que esté en formato numérico

# --- PREPROCESAMIENTO ---
# Definimos las columnas categóricas y numéricas
categorical_cols = ['tipo_pensamiento', 'simbolo_o_imagen', 'input_tipo', 'input_intensidad', 'contenido_estudiado', 'Dia_Semana']
numerical_cols = ['energia_0_10', 'fatiga_mental_0_10', 'control_pensamiento_0_10', 'conciencia_presente_0_10',
                  'Hora_Num', 'Comentario_longitud']

# Preprocesamos los datos: codificamos las columnas categóricas y mantenemos las numéricas
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
    ],
    remainder='passthrough'  # Mantén las columnas numéricas tal cual
)

# --- PIPELINE ---
# Usamos un pipeline que incluye el preprocesador y el modelo de RandomForest
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('model', RandomForestRegressor(n_estimators=100, random_state=42))
])

# --- ENTRENAMIENTO ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
pipeline.fit(X_train, y_train)

# --- EVALUACIÓN ---
y_pred = pipeline.predict(X_test)
print("\n🔍 Evaluación del Modelo")
print(f"MAE: {mean_absolute_error(y_test, y_pred):.2f}")
print(f"R²: {r2_score(y_test, y_pred):.2f}")

# --- EXPORTACIÓN DEL MODELO ---
export_path = os.path.abspath(os.path.join('../neurocoach-ia/data/modelo_predictivo.pkl'))
joblib.dump(pipeline, export_path)
print(f"✅ Modelo exportado como: {export_path}")
