# 🧠 MICD – Estado Actual del Proyecto (v2.0)

Esta es la versión **2.0** del proyecto MICD (Modelo Integral de Conciencia y Desarrollo). El sistema ha sido reestructurado, consolidado y alineado con una única fuente de datos para todos los niveles.

---

## ✅ ESTRUCTURA GENERAL DEL PROYECTO

```
neurocoach-ia/
├── niveles/
│   ├── nivel1_registro_conciencia/
│   ├── nivel2_ml_personalizado/
│   ├── nivel3_5_forma_pensamiento/
│   ├── nivel4_simbolos_subconscientes/
│   ├── nivel5_metaobservacion/
│   ├── nivel7_motivacion/
│
├── data/
│   └── nivel1/
│       └── registro_conciencia.csv
│
├── modelos/
│   └── modelo_entrenado.pkl
│
├── predictores/
│   ├── forma_pensamiento.py
│   └── motivacion.py
│
├── outputs/
│   └── coach_ia/
├── archivos_antiguos/
```

---

## ✅ AVANCE POR NIVEL

### 🟩 Nivel 1 – Registro de Conciencia
- `registro_conciencia.csv` consolidado y actualizado ✔️
- `analisis_datos.py` revisado y alineado ✔️

### 🟩 Nivel 2 – ML Personalizado
- `pipeline_entrenamiento.py` consolidado ✔️
- Entrena y guarda `modelo_entrenado.pkl` ✔️

### 🟩 Nivel 3.5 – Forma del Pensamiento
- `entrenamiento_modelo.py` eliminado (redundante) ✔️
- `forma_pensamiento.py` adaptado al nuevo pipeline ✔️

### 🟩 Nivel 7 – Motivación Interna
- `motivacion.py` funcionando con input simbólico y realista ✔️

---

## 🧠 Consolidación técnica

- Modelo unificado (`modelo_entrenado.pkl`)
- Scripts conectados al mismo CSV base
- Predictores conectados correctamente a los modelos
- Rutas dinámicas y defensivas aplicadas

---

## 📌 Próximos pasos

- Iniciar UI o flujo de carga desde Streamlit o CLI
- Crear estructura para Nivel 4 (símbolos) y Nivel 5 (metaobservación)
- Entrenar modelos alternativos por variable objetivo (`estado_emocional`, etc.)

---

> Versión: **v2.0**
> Última actualización: abril 2025