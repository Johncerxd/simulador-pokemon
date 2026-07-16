import streamlit as st
import requests
from streamlit_lottie import st_lottie
import plotly.express as px
import pandas as pd

# Configuración inicial
st.set_page_config(page_title="Simulador Pokémon Pro", layout="wide")

# Función para cargar animaciones Lottie (Pokeball girando)
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200: return None
    return r.json()

lottie_poke = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_6u84k2.json")

# --- INTERFAZ GRÁFICA ---
st.markdown("<h1 style='text-align: center; color: #ff0000;'>⚡ Simulador Pokémon Pro ⚡</h1>", unsafe_allow_html=True)

col_anim, col_menu = st.columns([1, 2])

with col_anim:
    if lottie_poke:
        st_lottie(lottie_poke, height=200, key="pokeball")

with col_menu:
    # Menú mejorado con selectbox animado
    opcion = st.selectbox("Selecciona una acción del sistema:", [
        "Ver Equipo Pokémon",
        "Capturar Pokémon",
        "Ver Estadísticas de Poder",
        "Guardar y Salir"
    ])

# --- LÓGICA CON ANIMACIONES Y GRÁFICOS ---
if opcion == "Ver Estadísticas de Poder":
    st.subheader("📊 Gráfico de Rendimiento")
    # Datos de ejemplo (puedes reemplazar con los de tu equipo)
    data = pd.DataFrame({
        'Pokémon': ['Pikachu', 'Bulbasaur', 'Charmander'],
        'Poder': [85, 70, 90]
    })
    fig = px.bar(data, x='Pokémon', y='Poder', color='Poder', 
                 color_continuous_scale='Viridis', template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

elif opcion == "Capturar Pokémon":
    with st.form("cap"):
        nombre = st.text_input("Nombre del Pokémon:")
        if st.form_submit_button("¡Lanzar Pokéball!"):
            with st.spinner('Capturando...'):
                st.balloons() # Animación de globos al capturar
                st.success(f"¡{nombre} fue capturado exitosamente!")
