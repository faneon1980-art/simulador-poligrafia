import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random

st.set_page_config(page_title="Simulador Integral de Poligrafía", layout="centered")

# ---------------------------
# Control de fases
# ---------------------------
if "fase" not in st.session_state:
    st.session_state.fase = "explicacion"

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
    elif evento == "Ansiedad basal":
        y += 2
    elif evento == "Artefacto":
        y += np.random.normal(0, 4, 200)
    elif evento == "Contramedida":
        y += np.sin(8 * x) * 5

    return x, y

# ---------------------------
# Ejemplos didácticos
# ---------------------------
ejemplos = [
    ("Ansiedad basal",
     "Microcurvas constantes en EDA, sin picos claros. Cardio estable o levemente elevado."),
    ("Reacción relevante",
     "Pico abrupto de EDA asociado temporalmente a la pregunta. Aumento claro del Cardio."),
    ("Artefacto",
     "Trazos irregulares y caóticos. No guardan coherencia temporal."),
    ("Contramedida",
     "Patrones repetitivos forzados en EDA y oscilaciones rítmicas en Cardio.")
]

# =====================================================
# FASE 1 – EXPLICACIÓN CON GRÁFICOS
# =====================================================
if st.session_state.fase == "explicacion":

    st.title("📘 Fundamentos de Reacciones Poligráficas")
    st.markdown("### Ejemplos gráficos de patrones fisiológicos")

    for evento, descripcion in ejemplos:
        st.subheader(evento)

        x1, eda = generar_eda(evento)
        x2, cardio = generar_cardio(evento)

        fig, ax = plt.subplots()
        ax.plot(x1, eda, color="green")
        ax.set_title("EDA")
        st.pyplot(fig)

        fig2, ax2 = plt.subplots()
        ax2.plot(x2, cardio, color="red")
        ax2.set_title("Cardio")
        st.pyplot(fig2)

        st.markdown(f"🧠 **Interpretación:** {descripcion}")
        st.divider()

    if st.button("➡️ Ir a evaluación"):
        st.session_state.fase = "evaluacion"
        st.rerun()

# =====================================================
# FASE 2 – EVALUACIÓN
# =====================================================
if st.session_state.fase == "evaluacion":

    eventos = [
        "Reacción relevante",
        "Ansiedad basal",
        "Artefacto",
        "Contramedida"
    ]

    if "evento" not in st.session_state:
        st.session_state.evento = random.choice(eventos)

    evento = st.session_state.evento

    st.title("🧠 Evaluación del Análisis Poligráfico")

    x1, eda = generar_eda(evento)
    x2, cardio = generar_cardio(evento)

    fig, ax = plt.subplots()
    ax.plot(x1, eda, color="green")
    ax.set_title("EDA")
    st.pyplot(fig)

    fig2, ax2 = plt.subplots()
    ax2.plot(x2, cardio, color="red")
    ax2.set_title("Cardio")
    st.pyplot(fig2)

    st.subheader("Análisis del poligrafista")

    causa = st.selectbox(
        "¿A qué atribuye la reacción?",
        [
            "Reacción relevante",
            "Ansiedad basal",
            "Artefacto",
            "Contramedida",
            "No concluyente"
        ]
    )

    justificacion = st.text_area("Justifique técnicamente su análisis")

    if st.button("Evaluar"):
        if justificacion.strip() == "":
            st.warning("Debe justificar su respuesta.")
        else:
            st.markdown(f"**Evento real:** {evento}")
            if causa == evento:
                st.success("✔ Interpretación correcta")
            else:
                st.error("✖ Interpretación incorrecta")

    if st.button("🔄 Nuevo caso"):
        st.session_state.evento = random.choice(eventos)
        st.rerun()
