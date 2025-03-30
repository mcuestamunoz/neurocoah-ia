import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# === Configuración de rutas ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, '..', 'registro_cognitivo.csv')
GRAFICOS_DIR = os.path.join(BASE_DIR, 'graficos')
INSIGHTS_DIR = os.path.join(BASE_DIR, 'insights')

os.makedirs(GRAFICOS_DIR, exist_ok=True)
os.makedirs(INSIGHTS_DIR, exist_ok=True)

# === Cargar y preparar datos ===
df = pd.read_csv(CSV_PATH)
df['Datetime'] = pd.to_datetime(df['Fecha'] + ' ' + df['Hora'])
df = df.sort_values(by="Datetime")
df['Dia_Semana'] = df['Datetime'].dt.day_name()

# === Graficar evolución energía y estado de ánimo ===
plt.figure(figsize=(10, 5))
plt.plot(df['Datetime'], df['Energia'], label='Energía', marker='o')
plt.plot(df['Datetime'], df['Estado_Animo'], label='Estado Ánimo', marker='s')
plt.gcf().autofmt_xdate()
plt.title('Evolución de Energía y Estado de Ánimo')
plt.xlabel('Fecha y Hora')
plt.ylabel('Nivel (escala 1-10)')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(GRAFICOS_DIR, 'evolucion_energia_estado.png'))
plt.close()

# === Mapa de calor de correlaciones ===
correlaciones = df[['Energia', 'Estado_Animo', 'Resultado']].corr()
plt.figure(figsize=(8, 6))
sns.heatmap(correlaciones, annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Mapa de calor de correlaciones")
plt.tight_layout()
plt.savefig(os.path.join(GRAFICOS_DIR, 'mapa_calor_correlaciones.png'))
plt.close()

# === Evolución de todas las variables ===
plt.figure(figsize=(12, 6))
sns.lineplot(data=df, x='Datetime', y='Energia', label='Energía')
sns.lineplot(data=df, x='Datetime', y='Estado_Animo', label='Estado de Ánimo')
sns.lineplot(data=df, x='Datetime', y='Resultado', label='Resultado')
plt.title('Evolución temporal de variables cognitivas')
plt.xlabel('Fecha y hora')
plt.ylabel('Valor')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(GRAFICOS_DIR, 'evolucion_completa.png'))
plt.close()

# === Promedios por día de la semana ===
promedios = df.groupby("Dia_Semana")[["Energia", "Estado_Animo", "Resultado"]].mean().reset_index()
orden_dias = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
promedios["Dia_Semana"] = pd.Categorical(promedios["Dia_Semana"], categories=orden_dias, ordered=True)
promedios = promedios.sort_values("Dia_Semana")
promedios_melt = promedios.melt(id_vars="Dia_Semana", var_name="Variable", value_name="Promedio")
plt.figure(figsize=(10, 6))
sns.barplot(data=promedios_melt, x="Dia_Semana", y="Promedio", hue="Variable")
plt.title("Promedio por Día de la Semana")
plt.ylabel("Promedio (escala 1-10)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(GRAFICOS_DIR, 'promedios_dia_semana.png'))
plt.close()

# === Promedios por Tarea ===
promedios_tarea = df.groupby('Tarea')[['Energia', 'Estado_Animo', 'Resultado']].mean()
promedios_tarea_reset = promedios_tarea.reset_index().melt(id_vars='Tarea', var_name='Variable', value_name='Promedio')
plt.figure(figsize=(12, 6))
sns.barplot(data=promedios_tarea_reset, x='Tarea', y='Promedio', hue='Variable')
plt.title("Promedio por Tarea")
plt.ylabel("Promedio (escala 1-10)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(GRAFICOS_DIR, 'promedios_por_tarea.png'))
plt.close()

# === Promedios por Tipo de Tarea ===
promedios_tipo = df.groupby('Tipo_tarea')[['Energia', 'Estado_Animo', 'Resultado']].mean()
promedios_tipo_reset = promedios_tipo.reset_index().melt(id_vars='Tipo_tarea', var_name='Variable', value_name='Promedio')
plt.figure(figsize=(10, 6))
sns.barplot(data=promedios_tipo_reset, x='Tipo_tarea', y='Promedio', hue='Variable')
plt.title("Promedio por Tipo de Tarea")
plt.ylabel("Promedio (escala 1-10)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(GRAFICOS_DIR, 'promedios_por_tipo_tarea.png'))
plt.close()

# === Puntos clave por tarea ===
agrupados = df.groupby('Tarea')['Punto clave'].unique()
insights_path = os.path.join(INSIGHTS_DIR, 'puntos_clave.txt')
with open(insights_path, 'w') as f:
    f.write("\n🧠 Puntos clave por Tarea:\n\n")
    for tarea, puntos in agrupados.items():
        f.write(f"🏷️ {tarea}:\n")
        for punto in puntos:
            if pd.notna(punto) and punto.strip():
                f.write(f"   - {punto}\n")
        f.write("-" * 40 + "\n")
