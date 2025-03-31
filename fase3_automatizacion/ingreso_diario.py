import os
import csv
from datetime import datetime

ruta_csv = os.path.abspath('../registro_cognitivo.csv')

# 1. Entrada del usuario
fecha = datetime.now().strftime("%Y-%m-%d")
hora = datetime.now().strftime("%H:%M")
energia = input("Nivel de energía (1-10): ")
estado_animo = input("Estado de ánimo (1-10): ")
tarea = input("¿Qué tarea realizaste?: ")
tipo_tarea = input("Tipo de tarea (Ejercicio, Rutina, Trabajo...): ")
resultado = input("Resultado percibido (1-10): ")
comentarios = input("Comentarios del día: ")
punto_clave = input("Punto clave (si hubo alguno): ")

# 2. Guardar en CSV
existe_archivo = os.path.isfile(ruta_csv)
with open(ruta_csv, 'a', newline='') as archivo:
    escritor = csv.writer(archivo)
    if not existe_archivo:
        escritor.writerow(['Fecha', 'Hora', 'Energia', 'Estado_Animo', 'Tarea', 'Tipo_tarea', 'Resultado', 'Comentarios', 'Punto clave'])
    escritor.writerow([fecha, hora, energia, estado_animo, tarea, tipo_tarea, resultado, comentarios, punto_clave])

print("\n✅ Registro guardado correctamente.")

# 3. Preguntar si ejecutar análisis
respuesta = input("\n¿Deseas ejecutar el análisis de datos ahora? (s/n): ").strip().lower()
if respuesta == 's':
    import subprocess
    ruta_analisis = '/Users/marccuestamunoz/repos/neurocoach-ia/fase2_analisis/analisis_datos.py'
    subprocess.run(['python3', ruta_analisis])

