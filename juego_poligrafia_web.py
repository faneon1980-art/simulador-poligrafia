# juego_poligrafia_web.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Simulador de Poligrafía", layout="wide")

# -------------------------------
# Funciones generadoras de señales
# -------------------------------

def generar_eda(evento):
    duracion = 30
    fs = 20
    t = np.linspace(0, duracion, duracion * fs)
    eda = 0.4 + np.random.normal(0, 0.01, len(t))

    if evento == "Reacción relevante":
        latencia = 3 * fs
        duracion_scr = 10 * fs
        scr_t = np.arange(duracion_scr)
        scr = 0.6 * (scr_t / fs) * np.exp(-scr_t / (3 * fs))
        eda[latencia:latencia + duracion_scr] += scr

    elif evento == "Ansiedad basal":
        eda += 0.05 * np.sin(0.3 * t)

    elif evento == "Artefacto":
        eda += np.random.normal(0, 0.12, len(t))

    elif evento == "Contramedida":
        eda += 0.15 * np.sin(2 * t)

    return t, eda

def generar_cardio(evento):
    duracion = 30
    fs = 20
    t = np.linspace(0, duracion, duracion * fs)
    cardio = 72 + np.random.normal(0, 0.8, len(t))

    if evento == "Reacción relevante":
        cardio += 4 * np.exp(-0.15 * (t - 5)) * (t > 5)

    elif evento == "Ansiedad basal":
        cardio += 2

    elif evento == "Artefacto":
        cardio += np.random.normal(0, 5, len(t))

    elif evento == "Contramedida":
        cardio += 5 * np.sin(3 * t)

    return t, cardio

# -------------------------------
# Interfaz Streamlit
# -------------------------------

st.title("Simulador de Poligrafía")

# Explicación de reacciones
st.header("Aprende sobre las reacciones")
st.markdown("""
- **EDA (Electrodermal Activity / Conductancia de la piel)**: Línea verde.  
  Reacción relevante: inicia en homeostasis, sube curva hasta un pico y desciende a homeostasis.  
- **Cardio (Frecuencia cardiaca)**: Línea roja.  
  Reacción relevante: aumento gradual y sostenido, no brusco.
""")

# Mostrar ejemplo
st.subheader("Ejemplo de reacciones")
eventos = ["Ansiedad basal", "Reacción relevante", "Artefacto", "Contramedida"]
for evento in eventos:
    t, eda = generar_eda(evento)
    _, cardio = generar_cardio(evento)
    fig, ax = plt.subplots(figsize=(8,3))
    ax.plot(t, eda, color='green', label='EDA')
    ax.plot(t, cardio, color='red', label='Cardio')
    ax.set_title(evento)
    ax.set_xlabel("Tiempo (s)")
    ax.set_ylabel("Amplitud")
    ax.legend()
    st.pyplot(fig)

st.header("Evaluación")
opcion = st.selectbox("¿A qué crees que se debe la reacción?", eventos)
if st.button("Enviar respuesta"):
    if opcion == "Reacción relevante":
        st.success("Correcto ✅")
    else:
        st.error("Incorrecto ❌")
