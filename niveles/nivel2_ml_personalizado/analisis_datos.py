import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ✅ Ruta dinámica del CSV
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
RUTA_CSV = os.path.join(BASE_DIR, "data/nivel1/registro_diario.csv")

def cargar_datos():
    if not os.path.exists(RUTA_CSV):
        print("❌ No se encontró el archivo de registros.")
        return None
    df = pd.read_csv(RUTA_CSV)
    df['fecha'] = pd.to_datetime(df['fecha'])
    return df

def estadisticas_basicas(df):
    print("\n📊 Estadísticas numéricas:")
    print(df.describe())

    print("\n🎭 Valores únicos por columna:")
    for col in df.columns:
        print(f"{col}: {df[col].nunique()}")

def graficar_energia(df):
    df.sort_values("fecha", inplace=True)
    plt.figure(figsize=(10, 4))
    plt.plot(df['fecha'], df['nivel_energia'], marker='o', linestyle='-')
    plt.title("Evolución del Nivel de Energía")
    plt.xlabel("Fecha")
    plt.ylabel("Nivel de Energía")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def graficar_formas_pensamiento(df):
    conteo = df['forma_pensamiento'].value_counts()
    plt.figure(figsize=(6, 4))
    conteo.plot(kind='bar', color='orange')
    plt.title("Frecuencia de Formas de Pensamiento")
    plt.xlabel("Forma del pensamiento")
    plt.ylabel("Frecuencia")
    plt.tight_layout()
    plt.show()

def boxplot_tension_tarea(df):
    plt.figure(figsize=(8, 5))
    sns.boxplot(data=df, x='tipo_tarea', y='tension_cognitiva')
    plt.title("Tensión Cognitiva por Tipo de Tarea")
    plt.xlabel("Tipo de tarea")
    plt.ylabel("Tensión cognitiva")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def mapa_correlaciones(df):
    cols_num = ['nivel_energia', 'tension_cognitiva', 'flexibilidad_mental']
    corr = df[cols_num].corr()
    plt.figure(figsize=(6, 4))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title("Mapa de Correlaciones")
    plt.tight_layout()
    plt.show()

def main():
    df = cargar_datos()
    if df is None:
        return

    # Asegurar conversión numérica por si acaso
    df['nivel_energia'] = pd.to_numeric(df['nivel_energia'], errors='coerce')
    df['tension_cognitiva'] = pd.to_numeric(df['tension_cognitiva'], errors='coerce')
    df['flexibilidad_mental'] = pd.to_numeric(df['flexibilidad_mental'], errors='coerce')

    estadisticas_basicas(df)
    graficar_energia(df)
    graficar_formas_pensamiento(df)
    boxplot_tension_tarea(df)
    mapa_correlaciones(df)

if __name__ == "__main__":
    main()
