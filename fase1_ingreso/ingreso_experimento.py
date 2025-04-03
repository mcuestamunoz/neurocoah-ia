import csv
from datetime import datetime
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "registro_experimento.csv")

FASES_MENTALES = [
    "Flow", "Visualización", "Fatiga mental", "Alta concentración", 
    "Mala calidad del sueño", "Adormecido lúcido", "Confusión creativa"
]

TIPOS_PENSAMIENTO = [
    "Lógico", "Analítico", "Narrativo", "Visual", "Intuitivo", 
    "Imágenes", "Asociativo", "Caótico organizado"
]

INPUT_TIPOS = ["Audio", "Lectura", "Video", "Mixto", "Sin estímulo"]

def get_numeric_input(pregunta):
    while True:
        val = input(pregunta)
        if val.isdigit() and 0 <= int(val) <= 10:
            return int(val)
        print("⚠️ Por favor, ingresa un número entre 0 y 10.")

def seleccionar_opcion(lista, titulo):
    print(f"\nSelecciona {titulo}:")
    for i, item in enumerate(lista, 1):
        print(f"{i}. {item}")
    idx = input("→ Número de opción: ")
    if idx.isdigit() and 1 <= int(idx) <= len(lista):
        return lista[int(idx) - 1]
    return ""

print("\n🧠 Registro cognitivo enriquecido")
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
energia = get_numeric_input("Nivel de energía (0-10): ")
fatiga = get_numeric_input("Nivel de fatiga mental (0-10): ")
estado_fisico = input("Sensación corporal o estado físico: ").strip()
estado_mental = input("¿Cómo describirías tu estado mental?: ").strip()
fase_mental = seleccionar_opcion(FASES_MENTALES, "Fase Mental")
control_mental = get_numeric_input("¿Qué tanto controlaste tus pensamientos? (0-10): ")
conciencia_presente = get_numeric_input("Conciencia en el presente (0-10): ")
tipo_pensamiento = seleccionar_opcion(TIPOS_PENSAMIENTO, "Tipo de Pensamiento")
simbolo = input("Símbolo o imagen mental del día: ").strip()
palabra = input("¿Qué palabra o frase se repitió mentalmente?: ").strip()
input_tipo = seleccionar_opcion(INPUT_TIPOS, "Tipo de input")
input_intensidad = input("¿Cómo fue la intensidad del input (ligero, moderado, intenso)?: ").strip()
contenido = input("¿Qué contenido o tema estudiaste?: ").strip()
aprendizaje = input("¿Qué aprendiste de forma espontánea hoy?: ").strip()
resistencia = input("¿Detectaste algún tipo de resistencia mental o emocional?: ").strip()
nota = input("Comentario libre o reflexión del momento: ").strip()

fila = [
    timestamp, energia, fatiga, estado_fisico, estado_mental, fase_mental,
    control_mental, conciencia_presente, tipo_pensamiento, simbolo, palabra,
    input_tipo, input_intensidad, contenido, aprendizaje, resistencia, nota
]

file_exists = os.path.exists(DATA_PATH)
with open(DATA_PATH, 'a', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    if not file_exists:
        writer.writerow([
            "timestamp", "energia_0_10", "fatiga_mental_0_10", "estado_fisico", "estado_mental",
            "fase_mental", "control_pensamiento_0_10", "conciencia_presente_0_10", "tipo_pensamiento",
            "simbolo_o_imagen", "palabra_repetitiva", "input_tipo", "input_intensidad",
            "contenido_estudiado", "aprendizaje_espontaneo", "resistencia_detectada", "nota_libre"
        ])
    writer.writerow(fila)

print("✅ Registro cognitivo guardado con éxito.")
print("🔍 Guardando en:", DATA_PATH)

