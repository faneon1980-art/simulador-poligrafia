import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random

st.set_page_config(page_title="Simulador Integral de Poligrafía", layout="centered")

# ---------------------------
# Generadores fisiológicos
# ---------------------------
def generar_eda(evento):
    x = np.linspace(0, 10, 200)
    y = 0.3 + np.random.normal(0, 0.02, 200)

    if evento == "Reacción relevante":
        y[90:110] += np.linspace(0, 0.6, 20)
    elif evento == "Ansiedad basal":
        y += 0.1 * np.sin(3 * x)
    elif evento == "Artefacto":
        y += np.random.normal(0, 0.15, 200)
    elif evento == "Contramedida":
        y += 0.2 * np.sin(6 * x)

    return x, y

def generar_cardio(evento):
    x = np.linspace(0, 10, 200)
    y = 70 + np.random.normal(0, 1, 200)

    if evento == "Reacción relevante":
        y[90:120] += 10
    elif evento == "Fatiga":
        y -= 5
    elif evento == "Contramedida":
        y += np.sin(8 * x) * 5

    return x, y

# ---------------------------
# Juego
# ---------------------------
eventos = [
    "Reacción relevante",
    "Ansiedad basal",
    "Artefacto",
    "Contramedida",
    "Respuesta orientadora",
    "Fatiga"
]

if "evento" not in st.session_state:
    st.session_state.evento = random.choice(eventos)

evento = st.session_state.evento

st.title("🧠 Simulador Integral de Poligrafía")

st.subheader("Observe las señales fisiológicas")

x1, eda = generar_eda(evento)
x2, cardio = generar_cardio(evento)

fig, ax = plt.subplots()
ax.plot(x1, eda)
ax.set_title("EDA")
st.pyplot(fig)

fig2, ax2 = plt.subplots()
ax2.plot(x2, cardio)
ax2.set_title("Cardio (FC)")
st.pyplot(fig2)

st.subheader("Análisis del examinador")

eda_resp = st.radio("¿Observa reacción EDA?", ["Sí", "No"])
cardio_resp = st.radio("¿Cómo describe el Cardio?", [
    "Aumento FC", "Disminución", "Inestable", "Sin cambio"
])

causa = st.selectbox(
    "¿A qué atribuye la reacción?",
    [
        "Reacción relevante",
        "Ansiedad basal",
        "Artefacto",
        "Contramedida",
        "Respuesta orientadora",
        "No concluyente"
    ]
)

justificacion = st.text_area("Justifique su análisis (obligatorio)")

if st.button("Evaluar análisis"):
    if justificacion.strip() == "":
        st.warning("Debe justificar su respuesta.")
    else:
        st.success("Evaluación completada")
        st.markdown(f"**Evento real:** {evento}")
        if causa == evento:
            st.success("✔ Interpretación correcta")
        else:
            st.error("✖ Interpretación incorrecta")
