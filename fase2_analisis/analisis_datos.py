import os
import pandas as pd
import matplotlib.pyplot as plt

## Bloque 1: Carga y orden de datos

ruta_csv = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'registro_cognitivo.csv'))

df = pd.read_csv(ruta_csv)
df['Datetime'] = pd.to_datetime(df['Fecha'] + ' ' + df['Hora'])
df = df.sort_values(by="Datetime")

df['Dia_Semana'] = df['Datetime'].dt.day_name()  # ← Esta es la línea clave

print(df[['Fecha', 'Hora', 'Dia_Semana']].head())


## Bloque 2: Graficar evolución de energía y estado de ánimo

plt.figure(figsize=(10, 5))
plt.plot(df['Datetime'], df['Energia'], label='Energía', marker='o')
plt.plot(df['Datetime'], df['Estado_Animo'], label='Estado Ánimo', marker='s')
plt.gcf().autofmt_xdate()  # Rotación más suave de las fechas (opcional)
plt.title('Evolución de Energía y Estado de Ánimo')
plt.xlabel('Fecha y Hora')
plt.ylabel('Nivel (escala 1-10)')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

import seaborn as sns

# Bloque 3: Mapa de calor de las correlaciones

correlaciones = df[['Energia', 'Estado_Animo', 'Resultado']].corr()

plt.figure(figsize=(8, 6))
sns.heatmap(correlaciones, annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Mapa de calor de correlaciones")
plt.show()

# Bloque 4: Graficar evolución

plt.figure(figsize=(12,6))
sns.lineplot(data=df, x='Datetime', y='Energia', label='Energía')
sns.lineplot(data=df, x='Datetime', y='Estado_Animo', label='Estado de Ánimo')
sns.lineplot(data=df, x='Datetime', y='Resultado', label='Resultado')

plt.title('📈 Evolución temporal de tus variables cognitivas')
plt.xlabel('Fecha y hora')
plt.ylabel('Valor')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()

## Bloque 5: Variación variables según dia de la semana
# Agrupar y visualizar promedios por día de la semana
plt.figure(figsize=(10, 6))
promedios = df.groupby("Dia_Semana")[["Energia", "Estado_Animo", "Resultado"]].mean().reset_index()

# Orden de los días de la semana (opcional para visual más natural)
orden_dias = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
promedios["Dia_Semana"] = pd.Categorical(promedios["Dia_Semana"], categories=orden_dias, ordered=True)
promedios = promedios.sort_values("Dia_Semana")

# Plot
promedios_melt = promedios.melt(id_vars="Dia_Semana", value_vars=["Energia", "Estado_Animo", "Resultado"],
                                 var_name="Variable", value_name="Promedio")

sns.barplot(data=promedios_melt, x="Dia_Semana", y="Promedio", hue="Variable")
plt.title("Promedio de Energía, Estado de Ánimo y Resultado por Día de la Semana")
plt.ylabel("Promedio (escala 1-10)")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()

## Bloque 6: Agrupar por tarea y graficar. 
promedios_tarea = df.groupby('Tarea')[['Energia', 'Estado_Animo', 'Resultado']].mean()

# Reinicio de índices para graficar con seaborn
promedios_tarea_reset = promedios_tarea.reset_index().melt(id_vars='Tarea', var_name='Variable', value_name='Promedio')

plt.figure(figsize=(12, 6))
sns.barplot(data=promedios_tarea_reset, x='Tarea', y='Promedio', hue='Variable')
plt.title("Promedio de Energía, Estado de Ánimo y Resultado por Tarea")
plt.ylabel("Promedio (escala 1-10)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Mostrar puntos clave agrupados por Tarea
agrupados = df.groupby('Tarea')['Punto clave'].unique()

print("\n🧠 Puntos clave por Tarea:\n")
for tarea, puntos in agrupados.items():
    print(f"🏷️ {tarea}:")
    for punto in puntos:
        if pd.notna(punto) and punto.strip():  # Evita vacíos
            print(f"   - {punto}")
    print("-" * 40)

# Bloque 7: Promedios por Tipo de Tarea
promedios_tipo = df.groupby('Tipo_tarea')[['Energia', 'Estado_Animo', 'Resultado']].mean()

promedios_tipo_reset = promedios_tipo.reset_index().melt(id_vars='Tipo_tarea', var_name='Variable', value_name='Promedio')

plt.figure(figsize=(10, 6))
sns.barplot(data=promedios_tipo_reset, x='Tipo_tarea', y='Promedio', hue='Variable')
plt.title("Promedio por Tipo de Tarea")
plt.ylabel("Promedio (escala 1-10)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
