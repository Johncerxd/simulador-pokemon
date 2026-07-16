import streamlit as st
import pandas as pd
from modelos import Pokemon
from estructuras import ListaEnlazada

st.set_page_config(page_title="Simulador Pokémon Final", layout="wide")

# --- ESTILOS ---
st.markdown("""
<style>
.stApp { background-image: url('https://i.gifer.com/P4W4.gif'); background-size: cover; }
.main-box { background-color: rgba(0, 0, 0, 0.8); padding: 20px; border-radius: 15px; color: white; border: 2px solid #00f2ff; }
</style>
""", unsafe_allow_html=True)

# --- GESTIÓN DE ESTADO CON TUS CLASES ---
if 'equipo' not in st.session_state:
    st.session_state.equipo = ListaEnlazada()
if 'log' not in st.session_state:
    st.session_state.log = []

st.markdown('<div class="main-box">', unsafe_allow_html=True)
st.title("⚡ Simulador Pokémon Pro")

menu = st.sidebar.radio("Navegación", ["Arena", "Captura", "Gestión de Datos"])

# --- LÓGICA DE ARENA (USANDO MODELOS) ---
if menu == "Arena":
    st.subheader("⚔️ Registro de Combates")
    if st.button("Registrar Victoria"):
        st.session_state.log.append({"Accion": "Combate", "Resultado": "Victoria"})
        st.success("¡Victoria en Arena registrada!")

# --- LÓGICA DE CAPTURA (USANDO ESTRUCTURAS) ---
elif menu == "Captura":
    st.subheader("🎯 Capturar Pokémon")
    nombre = st.text_input("Nombre del Pokémon:")
    if st.button("Lanzar Pokéball"):
        nuevo_poke = Pokemon(1, nombre, "Normal", 5, 100, 100, 10, 10, 10)
        st.session_state.equipo.insertar_final(nuevo_poke) # Uso de tu ListaEnlazada
        st.session_state.log.append({"Accion": "Captura", "Resultado": nombre})
        st.balloons()
        st.success(f"¡{nombre} añadido a tu Lista Enlazada!")

# --- GESTIÓN DE DATOS ---
elif menu == "Gestión de Datos":
    st.subheader("📊 Estadísticas de tu Aventura")
    if st.session_state.log:
        df = pd.DataFrame(st.session_state.log)
        st.table(df)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Descargar Reporte CSV", csv, "aventura_pokemon.csv", "text/csv")
    else:
        st.info("Aún no tienes registros.")

st.markdown('</div>', unsafe_allow_html=True)
