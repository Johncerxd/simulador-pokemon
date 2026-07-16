import streamlit as st
import pandas as pd
from modelos import Pokemon
from estructuras import ListaEnlazada

# Configuración de página
st.set_page_config(page_title="Simulador Pokémon Pro", layout="wide")

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
    st.session_state.equipo = ListaEnlazada() #[cite: 2]
if 'log' not in st.session_state:
    st.session_state.log = []

# --- INTERFAZ ---
st.markdown('<div class="console-box">', unsafe_allow_html=True)
st.title("⚡ Simulador Pokémon Pro")

menu = st.sidebar.radio("SISTEMA DE CONTROL", 
                        ["Gestión de Equipo", "Búsqueda Avanzada", "Arena de Combate", "Exportación de Datos"])

# 1. GESTIÓN DE EQUIPO
if menu == "Gestión de Equipo":
    st.header("🎒 Registrar nuevo Pokémon")
    with st.form("nuevo_pokemon"):
        nombre = st.text_input("Nombre:")
        tipo = st.text_input("Tipo:")
        nivel = st.number_input("Nivel:", 1, 100)
        hp = st.number_input("HP:", 1, 999)
        if st.form_submit_button("Guardar"):
            nuevo = Pokemon(0, nombre, tipo, nivel, hp, hp, 10, 10, 10) #[cite: 3]
            st.session_state.equipo.insertar_final(nuevo) #[cite: 2]
            st.success(f"¡{nombre} añadido al equipo!")
            st.rerun()

    st.subheader("Tu Equipo Actual")
    elementos = st.session_state.equipo.obtener_todos() #[cite: 2]
    if elementos:
        data = [{"Nombre": p.nombre, "Tipo": p.tipo, "Nivel": p.nivel, "HP": p.hp} for p in elementos]
        st.table(pd.DataFrame(data))
    else:
        st.info("No hay Pokémon en el equipo todavía.")

# 2. BÚSQUEDA AVANZADA
elif menu == "Búsqueda Avanzada":
    st.header("🔍 Buscar Pokémon")
    query = st.text_input("Nombre a buscar:")
    if query:
        elementos = st.session_state.equipo.obtener_todos() #[cite: 2]
        resultados = [p for p in elementos if query.lower() in p.nombre.lower()]
        if resultados:
            for p in resultados: st.success(f"Encontrado: {p.nombre} (Tipo: {p.tipo})")
        else: st.error("No encontrado.")

# 3. ARENA DE COMBATE
elif menu == "Arena de Combate":
    st.header("⚔️ Registro de Combates")
    if st.button("Registrar Victoria"):
        st.session_state.log.append({"Accion": "Combate", "Resultado": "Victoria"})
        st.balloons()
        st.success("¡Victoria registrada!")

# 4. EXPORTACIÓN DE DATOS (UNIFICADO)
# 4. EXPORTACIÓN DE DATOS (VERSION SEGURA)
elif menu == "Exportación de Datos":
    st.header("💾 Exportar CSV de Aventura")
    
    # Obtenemos los elementos de forma segura
    lista_equipo = st.session_state.equipo.obtener_todos() #
    
    # Creamos las listas de forma separada para evitar errores
    equipo_data = []
    for p in lista_equipo:
        equipo_data.append({"Accion": "Registro", "Resultado": f"Pokémon: {p.nombre}"})
        
    combates_data = st.session_state.log
    todo_el_reporte = equipo_data + combates_data
    
    if todo_el_reporte:
        df = pd.DataFrame(todo_el_reporte)
        st.table(df)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Descargar Reporte Completo", csv, "reporte_aventura.csv", "text/csv")
    else:
        st.info("Aún no tienes registros de Pokémon ni de combates.")
