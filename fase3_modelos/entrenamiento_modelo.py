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
RUTA_CSV = os.path.abspath('../neurocoach-ia/data/registro_cognitivo.csv')
df = pd.read_csv(RUTA_CSV)
df = df.dropna()

# --- FEATURE ENGINEERING ---
df['Datetime'] = pd.to_datetime(df['Fecha'] + ' ' + df['Hora'])
df['Dia_Semana'] = df['Datetime'].dt.day_name()
df['Hora_Num'] = df['Datetime'].dt.hour
df['Punto_clave_bin'] = df['Punto clave'].apply(lambda x: 0 if pd.isna(x) or x.strip() == '' else 1)
df['Comentario_longitud'] = df['Comentarios'].apply(lambda x: len(str(x)))

# --- VARIABLES DE ENTRADA Y SALIDA ---
X = df[['Energia', 'Estado_Animo', 'Hora_Num', 'Punto_clave_bin', 'Comentario_longitud', 'Tipo_tarea', 'Dia_Semana']]
y = df['Resultado'].astype(float)

# --- PREPROCESAMIENTO ---
categorical_cols = ['Tipo_tarea', 'Dia_Semana']
numerical_cols = ['Energia', 'Estado_Animo', 'Hora_Num', 'Punto_clave_bin', 'Comentario_longitud']

preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
    ],
    remainder='passthrough'  # deja las columnas numéricas tal cual
)

# --- PIPELINE ---
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
