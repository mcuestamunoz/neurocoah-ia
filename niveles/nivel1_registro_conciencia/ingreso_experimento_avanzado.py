import csv
from datetime import datetime
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "registro_experimento_avanzado.csv")

FASES_APRENDIZAJE = ["Preactivación", "Codificación", "Consolidación", "Integración"]
FASES_ATENCIONALES = ["Alpha-flotante", "Theta-inmersivo", "Gamma-enfocado"]
DOPAMINA = ["Baja", "Media", "Alta"]
ENTROPIA = ["Ordenado", "Intermedio", "Caótico creativo"]

def seleccionar_opcion(lista, titulo):
    print(f"\nSelecciona {titulo}:")
    for i, item in enumerate(lista, 1):
        print(f"{i}. {item}")
    idx = input("→ Número de opción: ")
    if idx.isdigit() and 1 <= int(idx) <= len(lista):
        return lista[int(idx) - 1]
    return ""

def get_num_input(pregunta):
    while True:
        val = input(pregunta)
        if val.isdigit() and 0 <= int(val) <= 10:
            return int(val)
        print("⚠️ Ingresa un número del 0 al 10.")

print("\n🧬 Registro de Experimento Cognitivo Avanzado")

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
fase_aprendizaje = seleccionar_opcion(FASES_APRENDIZAJE, "Fase de Aprendizaje")
fase_atencional = seleccionar_opcion(FASES_ATENCIONALES, "Estado Atencional")
dopamina = seleccionar_opcion(DOPAMINA, "Nivel Dopaminérgico Estimado")
entropia = seleccionar_opcion(ENTROPIA, "Entropía Mental")

claridad = get_num_input("Claridad mental (0-10): ")
ruido = get_num_input("Ruido mental (0-10): ")
significado = get_num_input("Nivel de significado emocional (0-10): ")

simbolo = input("Símbolo o imagen emergente: ").strip()
retencion = input("¿Qué recordaste espontáneamente más tarde?: ").strip()
reflexion = input("Nota libre / Insight del momento: ").strip()

fila = [
    timestamp, fase_aprendizaje, fase_atencional, dopamina, entropia,
    claridad, ruido, significado, simbolo, retencion, reflexion
]

file_exists = os.path.exists(DATA_PATH)
with open(DATA_PATH, 'a', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    if not file_exists:
        writer.writerow([
            "timestamp", "fase_aprendizaje", "fase_atencional", "nivel_dopaminico_estimado",
            "entropia_mental", "claridad_mental_0_10", "ruido_mental_0_10",
            "nivel_significado_0_10", "simbolo_emergente", "retencion_spontanea", "nota_libre"
        ])
    writer.writerow(fila)

print("✅ Registro avanzado guardado.")
