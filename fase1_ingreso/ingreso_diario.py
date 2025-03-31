import os
import csv
import subprocess
from datetime import datetime

# --- CONFIGURACIÓN ---
RUTA_CSV = os.path.abspath('../neurocoach-ia/registro_cognitivo.csv')
RUTA_ANALISIS = os.path.abspath('../neurocoach-ia/fase2_analisis/analisis_datos.py')

# --- FUNCIONES DE ENTRADA ---
def input_numerico(mensaje, minimo=1, maximo=10):
    while True:
        valor = input(f"{mensaje} ({minimo}-{maximo}): ").strip()
        if valor.isdigit() and minimo <= int(valor) <= maximo:
            return valor
        else:
            print("❌ Valor no válido. Intenta de nuevo.")

def capturar_datos():
    print("\n🧠 Ingreso de datos para el Neurocoach:")
    def input_fecha():
        hoy = datetime.now().strftime("%Y-%m-%d")
        entrada = input(f"Fecha del registro [Enter para usar {hoy}]: ").strip()
        if entrada == "":
            return hoy
        try:
            datetime.strptime(entrada, "%Y-%m-%d")
            return entrada
        except ValueError:
            print("❌ Formato inválido. Usa AAAA-MM-DD.")
            return input_fecha()
    def input_hora():
        ahora = datetime.now().strftime("%H:%M")
        entrada = input(f"Hora del registro [Enter para usar {ahora}]: ").strip()
        if entrada == "":
            return ahora
        try:
            datetime.strptime(entrada, "%H:%M")
            return entrada
        except ValueError:
            print("❌ Formato inválido. Usa HH:MM en 24h.")
            return input_hora()
        
    fecha = input_fecha()
    hora = input_hora()
    energia = input_numerico("Nivel de energía")
    estado_animo = input_numerico("Estado de ánimo")
    tarea = input("¿Qué tarea realizaste?: ").strip()
    tipo_tarea = input("Tipo de tarea (Ejercicio, Rutina, Trabajo...): ").strip()
    resultado = input_numerico("Resultado percibido")
    comentarios = input("Comentarios del día: ").strip()
    punto_clave = input("Punto clave (si hubo alguno): ").strip()

    return [fecha, hora, energia, estado_animo, tarea, tipo_tarea, resultado, comentarios, punto_clave]

# --- GUARDAR EN CSV ---
def guardar_registro(datos):
    existe = os.path.isfile(RUTA_CSV)
    with open(RUTA_CSV, 'a', newline='') as archivo:
        escritor = csv.writer(archivo)
        if not existe:
            escritor.writerow(['Fecha', 'Hora', 'Energia', 'Estado_Animo', 'Tarea', 'Tipo_tarea', 'Resultado', 'Comentarios', 'Punto clave'])
        escritor.writerow(datos)
    print("✅ Registro guardado correctamente.")

# --- LANZAR ANÁLISIS ---
def ejecutar_analisis():
    if not os.path.exists(RUTA_ANALISIS):
        print(f"⚠️ Script de análisis no encontrado en: {RUTA_ANALISIS}")
        return
    print("📈 Ejecutando análisis de datos...\n")
    subprocess.run(['python3', RUTA_ANALISIS])

# --- MAIN FLOW ---
if __name__ == "__main__":
    datos = capturar_datos()
    guardar_registro(datos)

    respuesta = input("\n¿Deseas ejecutar el análisis de datos ahora? (s/n): ").strip().lower()
    if respuesta == 's':
        ejecutar_analisis()
