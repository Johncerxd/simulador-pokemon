import streamlit as st
import pandas as pd
from modelos import Pokemon
from estructuras import ListaEnlazada

st.set_page_config(page_title="Simulador Pokémon Pro", layout="wide")

# --- FONDO DE PANTALLA ÉPICO ---
st.markdown("""
    <style>
    .stApp {
        background: url('https://wallpapercave.com/wp/wp2567439.jpg') no-repeat center center fixed;
        background-size: cover;
    }
    .console-box {
        background-color: rgba(20, 25, 30, 0.9);
        padding: 30px;
        border-radius: 15px;
        border: 3px solid #ffcb05;
        box-shadow: 0 0 20px rgba(255, 203, 5, 0.5);
        color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)

# Inicializar sesión
if 'equipo' not in st.session_state:
    st.session_state.equipo = ListaEnlazada()
    # Precarga de datos de ejemplo
    st.session_state.equipo.insertar_final(Pokemon(1, "Pikachu", "Electrico", 5, 100, 100, 20, 10, 50))
    st.session_state.equipo.insertar_final(Pokemon(2, "Charizard", "Fuego", 50, 200, 200, 100, 80, 90))

# --- MENÚ AVANZADO ---
with st.sidebar:
    st.title("📟 POKÉ-DEX TERMINAL")
    menu = st.radio("SISTEMA DE CONTROL", 
                    ["Gestión de Equipo", "Búsqueda Avanzada", "Arena de Combate", "Exportación de Datos"])

st.markdown('<div class="console-box">', unsafe_allow_html=True)

if menu == "Búsqueda Avanzada":
    st.header("🔍 Búsqueda de Pokémon")
    query = st.text_input("Ingresa el nombre del Pokémon:")
    
    if query:
        # Lógica de búsqueda en tu ListaEnlazada
        resultados = [p for p in st.session_state.equipo.obtener_todos() if query.lower() in p.nombre.lower()]
        if resultados:
            for p in resultados:
                st.success(f"✅ Encontrado: {p.nombre} | Tipo: {p.tipo} | Nivel: {p.nivel}")
        else:
            st.error("❌ Pokémon no encontrado en tu lista.")

elif menu == "Gestión de Equipo":
    st.header("🎒 Tu Equipo Pokémon")
    data = [{"Nombre": p.nombre, "Tipo": p.tipo, "Nivel": p.nivel, "HP": p.hp} for p in st.session_state.equipo.obtener_todos()]
    st.table(pd.DataFrame(data))

elif menu == "Exportación de Datos":
    st.header("💾 Exportar a CSV")
    if st.button("Generar reporte final"):
        df = pd.DataFrame([{"Nombre": p.nombre, "Tipo": p.tipo} for p in st.session_state.equipo.obtener_todos()])
        st.download_button("Descargar CSV", df.to_csv(index=False), "equipo.csv", "text/csv")

st.markdown('</div>', unsafe_allow_html=True)
