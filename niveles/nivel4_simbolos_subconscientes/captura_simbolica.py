import os
import csv
from datetime import datetime

# 📁 Guardar en ruta estructurada
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
RUTA_CSV = os.path.join(BASE_DIR, "data/nivel4/simbolos.csv")
os.makedirs(os.path.dirname(RUTA_CSV), exist_ok=True)

CAMPOS = [
    "fecha", "hora",
    "flash_visual",
    "emocion_asociada",
    "asociacion_espontanea",
    "intensidad",  # escala 0–10
]

def registrar_simbolo():
    simbolo = {
        "fecha": datetime.now().strftime("%Y-%m-%d"),
        "hora": datetime.now().strftime("%H:%M:%S"),
        "flash_visual": input("🔮 Flash o símbolo del día: "),
        "emocion_asociada": input("💓 Emoción asociada: "),
        "asociacion_espontanea": input("🌀 ¿Qué te evocó?: "),
        "intensidad": input("🔥 Intensidad del símbolo (0-10): ")
    }

    archivo_nuevo = not os.path.exists(RUTA_CSV)
    with open(RUTA_CSV, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=CAMPOS)
        if archivo_nuevo:
            writer.writeheader()
        writer.writerow(simbolo)

    print("✅ Símbolo registrado correctamente.")

if __name__ == "__main__":
    registrar_simbolo()
