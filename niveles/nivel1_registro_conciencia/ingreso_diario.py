import csv
from datetime import datetime
import os

# Ruta del archivo donde se guardarán los registros
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
ARCHIVO_CSV = os.path.join(BASE_DIR, "data/nivel1/registro_diario.csv")
os.makedirs(os.path.dirname(ARCHIVO_CSV), exist_ok=True)

# Campos que se van a registrar
campos = [
    "fecha",
    "hora",
    "nivel_energia",
    "estado_emocional",
    "tipo_tarea",
    "resultado",
    "forma_pensamiento",
    "tipo_procesamiento",
    "tension_cognitiva",
    "flexibilidad_mental",
    "estrategia_afrontamiento",
    "dialogo_interno"
]

def obtener_datos_usuario():
    print("🧠 Registro Diario de Conciencia")
    datos = {
        "fecha": datetime.now().strftime("%Y-%m-%d"),
        "hora": datetime.now().strftime("%H:%M:%S"),
        "nivel_energia": input("Nivel de energía (1-10): "),
        "estado_emocional": input("Estado emocional (ej: tranquilo, ansioso): "),
        "tipo_tarea": input("Tipo de tarea realizada: "),
        "resultado": input("Resultado (ej: completada, a medias): "),
        "forma_pensamiento": input("Forma del pensamiento (visual, narrativa...): "),
        "tipo_procesamiento": input("Tipo de procesamiento (emocional, racional...): "),
        "tension_cognitiva": input("Tensión cognitiva (0-10): "),
        "flexibilidad_mental": input("Flexibilidad mental (0-10): "),
        "estrategia_afrontamiento": input("Estrategia de afrontamiento: "),
        "dialogo_interno": input("Diálogo interno (apoyo, juicio, dispersión...): "),
    }
    return datos

def guardar_en_csv(datos):
    archivo_nuevo = not os.path.exists(ARCHIVO_CSV)

    with open(ARCHIVO_CSV, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        if archivo_nuevo:
            writer.writeheader()
        writer.writerow(datos)
    print("✅ Registro guardado correctamente.")

if __name__ == "__main__":
    datos = obtener_datos_usuario()
    guardar_en_csv(datos)
