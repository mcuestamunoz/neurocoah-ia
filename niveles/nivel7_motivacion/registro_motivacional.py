import os
import csv
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
RUTA_CSV = os.path.join(BASE_DIR, "data/nivel7/motivacion.csv")
os.makedirs(os.path.dirname(RUTA_CSV), exist_ok=True)

CAMPOS = [
    "fecha", "hora",
    "motivacion_subyacente",
    "tipo_energia",  # mental, emocional, física
    "alineacion_motivacion_tarea"  # escala 0–10
]

def registrar_motivacion():
    registro = {
        "fecha": datetime.now().strftime("%Y-%m-%d"),
        "hora": datetime.now().strftime("%H:%M:%S"),
        "motivacion_subyacente": input("⚡ Motivación subyacente (ej. validación, curiosidad, seguridad): "),
        "tipo_energia": input("💥 Tipo de energía dominante hoy: "),
        "alineacion_motivacion_tarea": input("🎯 ¿Qué tanto tu motivación coincidió con tus tareas? (0-10): ")
    }

    archivo_nuevo = not os.path.exists(RUTA_CSV)
    with open(RUTA_CSV, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=CAMPOS)
        if archivo_nuevo:
            writer.writeheader()
        writer.writerow(registro)

    print("✅ Registro motivacional guardado.")

if __name__ == "__main__":
    registrar_motivacion()
