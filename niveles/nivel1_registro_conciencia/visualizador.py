import pandas as pd
import matplotlib.pyplot as plt
import os

# ✅ RUTA INTELIGENTE
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
RUTA_CSV = os.path.join(BASE_DIR, "data/nivel1/registro_diario.csv")

def cargar_datos():
    if not os.path.exists(RUTA_CSV):
        print("❌ No se encontró el archivo de registros.")
        return None
    return pd.read_csv(RUTA_CSV)

def graficar_nivel_energia(df):
    df['fecha'] = pd.to_datetime(df['fecha'])
    df.sort_values('fecha', inplace=True)

    plt.figure(figsize=(10, 4))
    plt.plot(df['fecha'], df['nivel_energia'], marker='o', linestyle='-')
    plt.title('Evolución del Nivel de Energía')
    plt.xlabel('Fecha')
    plt.ylabel('Nivel de Energía')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def contar_formas_pensamiento(df):
    conteo = df['forma_pensamiento'].value_counts()
    plt.figure(figsize=(6, 4))
    conteo.plot(kind='bar', color='skyblue')
    plt.title('Frecuencia de Formas de Pensamiento')
    plt.xlabel('Forma')
    plt.ylabel('Cantidad')
    plt.tight_layout()
    plt.show()

def boxplot_tension_por_tarea(df):
    plt.figure(figsize=(8, 5))
    df.boxplot(column='tension_cognitiva', by='tipo_tarea', grid=False)
    plt.title('Tensión Cognitiva por Tipo de Tarea')
    plt.suptitle('')
    plt.xlabel('Tipo de Tarea')
    plt.ylabel('Tensión Cognitiva')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def main():
    df = cargar_datos()
    if df is None:
        return

    try:
        df['nivel_energia'] = pd.to_numeric(df['nivel_energia'])
        df['tension_cognitiva'] = pd.to_numeric(df['tension_cognitiva'])
    except Exception as e:
        print("⚠️ Error al convertir datos numéricos:", e)
        return

    graficar_nivel_energia(df)
    contar_formas_pensamiento(df)
    boxplot_tension_por_tarea(df)

if __name__ == "__main__":
    main()
