import streamlit as st
import pandas as pd

# --- CLASES DEFINIDAS INTERNAMENTE PARA EVITAR ERRORES DE RUTA ---
class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

class ListaEnlazada:
    def __init__(self):
        self.cabeza = None
    def insertar_final(self, dato):
        nuevo = Nodo(dato)
        if not self.cabeza: self.cabeza = nuevo
        else:
            temp = self.cabeza
            while temp.siguiente: temp = temp.siguiente
            temp.siguiente = nuevo
    def obtener_todos(self):
        elementos = []
        temp = self.cabeza
        while temp:
            elementos.append(temp.dato)
            temp = temp.siguiente
        return elementos

class Pokemon:
    def __init__(self, codigo, nombre, tipo, nivel, hp_maximo, hp, ataque, defensa, velocidad):
        self.codigo = codigo
        self.nombre = nombre
        self.tipo = tipo
        self.nivel = nivel
        self.hp = hp

# --- CONFIGURACIÓN Y ESTILO ---
st.set_page_config(page_title="Simulador Pokémon Pro", layout="wide")

st.markdown("""
    <style>
    .stApp { background: url('https://wallpapercave.com/dwp1x/wp12939364.jpg') no-repeat center center fixed; background-size: cover; }
    .console-box { background-color: rgba(20, 25, 30, 0.9); padding: 30px; border-radius: 15px; border: 3px solid #ffcb05; color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZACIÓN ---
if 'equipo' not in st.session_state:
    st.session_state.equipo = ListaEnlazada()
if 'log' not in st.session_state:
    st.session_state.log = []

# --- INTERFAZ ---
st.markdown('<div class="console-box">', unsafe_allow_html=True)
st.title("⚡ Simulador Pokémon Pro")

menu = st.sidebar.radio("SISTEMA DE CONTROL", ["Gestión de Equipo", "Búsqueda Avanzada", "Arena de Combate", "Exportación de Datos"])

if menu == "Gestión de Equipo":
    st.header("🎒 Registrar nuevo Pokémon")
    with st.form("nuevo_pokemon"):
        nombre = st.text_input("Nombre:")
        tipo = st.text_input("Tipo:")
        nivel = st.number_input("Nivel:", 1, 100)
        hp = st.number_input("HP:", 1, 999)
        if st.form_submit_button("Guardar"):
            nuevo = Pokemon(0, nombre, tipo, nivel, hp, hp, 10, 10, 10)
            st.session_state.equipo.insertar_final(nuevo)
            st.success(f"¡{nombre} añadido!")
            st.rerun()

    st.subheader("Tu Equipo Actual")
    elementos = st.session_state.equipo.obtener_todos()
    if elementos:
        data = [{"Nombre": p.nombre, "Tipo": p.tipo, "Nivel": p.nivel, "HP": p.hp} for p in elementos]
        st.table(pd.DataFrame(data))

elif menu == "Búsqueda Avanzada":
    st.header("🔍 Buscar Pokémon")
    query = st.text_input("Nombre a buscar:")
    if query:
        resultados = [p for p in st.session_state.equipo.obtener_todos() if query.lower() in p.nombre.lower()]
        for p in resultados: st.success(f"Encontrado: {p.nombre}")

elif menu == "Arena de Combate":
    st.header("⚔️ Registro de Combates")
    if st.button("Registrar Victoria"):
        st.session_state.log.append({"Accion": "Combate", "Resultado": "Victoria"})
        st.balloons()

elif menu == "Exportación de Datos":
    st.header("💾 Exportar CSV")
    equipo_list = [{"Accion": "Registro", "Resultado": f"Pokémon: {p.nombre}"} for p in st.session_state.equipo.obtener_todos()]
    df = pd.DataFrame(equipo_list + st.session_state.log)
    if not df.empty:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Descargar Reporte", csv, "reporte.csv", "text/csv")
    else:
        st.info("No hay datos.")

st.markdown('</div>', unsafe_allow_html=True)
