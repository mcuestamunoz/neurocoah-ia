import streamlit as st
import pandas as pd
from datetime import datetime
import os
import subprocess


# --- TÍTULO ---
st.title("🧠 Registro Diario – Neurocoach IA")

# --- FORMULARIO ---
energia = st.slider("Nivel de Energía", 0, 10, 5)
animo = st.slider("Estado de Ánimo", 0, 10, 5)
resultado = st.slider("Resultado Percibido", 0, 10, 5)
tipo_tarea = st.selectbox("Tipo de Tarea", ["Rutina", "Proyecto", "Creativa", "Física", "Estudio", "Trabajo", "Otra"])
comentario = st.text_area("Comentarios o Reflexiones")
punto_clave = st.text_input("¿Hubo algún punto clave hoy?")

# --- BOTÓN DE GUARDAR ---
if st.button("Guardar Registro"):
    now = datetime.now()
    nueva_fila = {
        "Fecha": now.strftime("%Y-%m-%d"),
        "Hora": now.strftime("%H:%M"),
        "Energia": energia,
        "Estado_Animo": animo,
        "Resultado": resultado,
        "Tipo_tarea": tipo_tarea,
        "Comentarios": comentario,
        "Punto clave": punto_clave
    }

    csv_path = os.path.abspath(os.path.join('../neurocoach-ia/data/registro_cognitivo.csv'))
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)
    else:
        df = pd.DataFrame([nueva_fila])

    df.to_csv(csv_path, index=False)
    st.success("✅ Registro guardado con éxito")

    # --- EJECUTAR FASE 2 Y 3 AUTOMÁTICAMENTE ---
    entrenamiento_script = os.path.abspath(os.path.join('../neurocoach-ia/fase3_modelos/entrenamiento_modelo.py'))
    resultado = subprocess.run(["python", entrenamiento_script], capture_output=True, text=True)

    if resultado.returncode == 0:
        st.success("📈 Modelo actualizado automáticamente")
    else:
        st.error("❌ Error al actualizar el modelo")
        st.text_area("Error", resultado.stderr, height=300)

    # --- MOSTRAR RESUMEN DE FASE 2 ---
    st.subheader("📊 Resumen semanal (últimos 7 días)")
    df['Datetime'] = pd.to_datetime(df['Fecha'] + ' ' + df['Hora'])
    ultima_semana = datetime.now() - timedelta(days=7)
    df_semana = df[df['Datetime'] >= ultima_semana]

    if not df_semana.empty:
        energia_prom = df_semana['Energia'].mean()
        animo_prom = df_semana['Estado_Animo'].mean()
        resultado_prom = df_semana['Resultado'].mean()
        tarea_mas_frecuente = df_semana['Tipo_tarea'].mode()[0]
        dia_mas_fuerte = df_semana['Datetime'].dt.day_name().mode()[0]

        st.markdown(f"""
        - Energía media: **{energia_prom:.2f}**
        - Estado de ánimo medio: **{animo_prom:.2f}**
        - Resultado percibido medio: **{resultado_prom:.2f}**
        - Tarea más frecuente: **{tarea_mas_frecuente}**
        - Día con más actividad: **{dia_mas_fuerte}**
        """)

        # --- EXPORTAR RESUMEN SEMANAL COMO TXT ---
        resumen = f"""
        Resumen semanal generado el {now.strftime('%Y-%m-%d %H:%M')}\n
        Energía media: {energia_prom:.2f}
        Estado de ánimo medio: {animo_prom:.2f}
        Resultado percibido medio: {resultado_prom:.2f}
        Tipo de tarea más frecuente: {tarea_mas_frecuente}
        Día con mayor actividad: {dia_mas_fuerte}
        """

        log_dir = os.path.abspath(os.path.join('../neurocoach-ia/fase4_coach_ia/logs'))
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, f"resumen_{now.strftime('%Y-%m-%d')}.txt")
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(resumen)

        st.success(f"📝 Resumen semanal exportado a: {log_path}")
    else:
        st.info("No hay suficientes datos para mostrar el análisis semanal.")
    # 🔁 Aquí podríamos lanzar automáticamente el pipeline completo
    # flujo_completo()
