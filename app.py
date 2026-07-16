import streamlit as st
import pandas as pd
from modelos import Pokemon
from estructuras import ListaEnlazada

# Configuración de página
st.set_page_config(page_title="Simulador Pokémon Final", layout="wide")

# --- ESTILOS TEMÁTICOS ---
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
        color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)

# Inicializar sesión con tus clases
if 'equipo' not in st.session_state:
    st.session_state.equipo = ListaEnlazada()
if 'log' not in st.session_state:
    st.session_state.log = []

# --- INTERFAZ ---
st.markdown('<div class="console-box">', unsafe_allow_html=True)
st.title("⚡ Simulador Pokémon Pro")

menu = st.sidebar.radio("SISTEMA DE CONTROL", 
                        ["Gestión de Equipo", "Búsqueda Avanzada", "Arena de Combate", "Exportación de Datos"])

# 1. GESTIÓN DE EQUIPO (INGRESAR POKÉMON)
if menu == "Gestión de Equipo":
    st.header("🎒 Registrar nuevo Pokémon")
    with st.form("nuevo_pokemon"):
        nombre = st.text_input("Nombre:")
        tipo = st.text_input("Tipo:")
        nivel = st.number_input("Nivel:", 1, 100)
        hp = st.number_input("HP:", 1, 999)
        if st.form_submit_button("Guardar"):
            nuevo = Pokemon(0, nombre, tipo, nivel, hp, hp, 10, 10, 10)[cite: 3]
            st.session_state.equipo.insertar_final(nuevo)[cite: 2]
            st.success(f"¡{nombre} añadido al equipo!")
            st.rerun()

    st.subheader("Tu Equipo Actual")
    data = [{"Nombre": p.nombre, "Tipo": p.tipo, "Nivel": p.nivel, "HP": p.hp} for p in st.session_state.equipo.obtener_todos()][cite: 2]
    st.table(pd.DataFrame(data))

# 2. BÚSQUEDA AVANZADA
elif menu == "Búsqueda Avanzada":
    st.header("🔍 Buscar Pokémon")
    query = st.text_input("Nombre a buscar:")
    if query:
        resultados = [p for p in st.session_state.equipo.obtener_todos() if query.lower() in p.nombre.lower()][cite: 2]
        if resultados:
            for p in resultados: st.success(f"Encontrado: {p.nombre} (Tipo: {p.tipo})")
        else: st.error("No encontrado.")

# 3. ARENA DE COMBATE
elif menu == "Arena de Combate":
    st.header("⚔️ Registro de Combates")
    if st.button("Registrar Victoria"):
        st.session_state.log.append({"Accion": "Combate", "Resultado": "Victoria"})
        st.balloons()

# 4. EXPORTACIÓN DE DATOS
elif menu == "Exportación de Datos":
    st.header("💾 Exportar CSV")
    if st.session_state.log:
        df = pd.DataFrame(st.session_state.log)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Descargar Reporte", csv, "reporte.csv", "text/csv")

st.markdown('</div>', unsafe_allow_html=True)
