import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random

st.set_page_config(page_title="Simulador de Poligrafía", layout="centered")

st.title("🧠 Simulador Didáctico de Poligrafía")
st.write("Analiza el trazo EDA y selecciona la interpretación correcta.")

# -------------------------------
# Generador de señales EDA
# -------------------------------
def generar_eda(tipo):
    x = np.linspace(0, 10, 200)

    if tipo == "Ansiedad basal":
        y = 0.2 * np.sin(3 * x) + 0.3 + np.random.normal(0, 0.02, 200)

    elif tipo == "Reacción relevante":
        y = 0.2 * np.sin(2 * x) + 0.3
        y[90:110] += np.linspace(0, 0.6, 20)

    elif tipo == "Movimiento / artefacto":
        y = 0.3 + np.random.normal(0, 0.15, 200)

    elif tipo == "Contramedida":
        y = 0.25 * np.sin(6 * x) + 0.35

    return x, y

tipos = [
    "Ansiedad basal",
    "Reacción relevante",
    "Movimiento / artefacto",
    "Contramedida"
]

if "tipo_actual" not in st.session_state:
    st.session_state.tipo_actual = random.choice(tipos)
    st.session_state.puntaje = 0
    st.session_state.intentos = 0

x, y = generar_eda(st.session_state.tipo_actual)

fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_title("Respuesta Electrodermal (EDA)")
ax.set_xlabel("Tiempo")
ax.set_ylabel("Conductancia")
ax.grid(True)

st.pyplot(fig)

respuesta = st.radio(
    "Selecciona la interpretación correcta:",
    tipos
)

if st.button("Responder"):
    st.session_state.intentos += 1

    if respuesta == st.session_state.tipo_actual:
        st.session_state.puntaje += 1
        st.success("Interpretación correcta.")
    else:
        st.error(
            f"Incorrecto. La respuesta correcta era: {st.session_state.tipo_actual}"
        )

    st.session_state.tipo_actual = random.choice(tipos)
    st.experimental_rerun()

st.info(
    f"Puntaje: {st.session_state.puntaje} / {st.session_state.intentos}"
)

