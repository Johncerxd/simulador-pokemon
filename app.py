import streamlit as st
import pandas as pd

# 1. DEFINICIÓN DE CLASES (Debe ir primero)
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
    def __init__(self, nombre, tipo, nivel, hp):
        self.nombre = nombre
        self.tipo = tipo
        self.nivel = nivel
        self.hp = hp

# 2. CONFIGURACIÓN E INICIALIZACIÓN DE ESTADO
st.set_page_config(page_title="Simulador Pokémon Pro", layout="wide")

# Inicializamos el estado solo si no existe
if 'equipo' not in st.session_state:
    st.session_state.equipo = ListaEnlazada()
if 'log' not in st.session_state:
    st.session_state.log = []
if 'pagina' not in st.session_state:
    st.session_state.pagina = "Gestión de Equipo"

# 3. INTERFAZ Y ESTILOS
st.markdown("""
    <style>
    .stApp { background: url('https://wallpapercave.com/dwp1x/wp12939364.jpg') no-repeat center center fixed; background-size: cover; }
    .console-box { background-color: rgba(20, 25, 30, 0.9); padding: 30px; border-radius: 15px; border: 3px solid #00f2ff; color: #ffffff; }
    .menu-title { color: #00f2ff; font-weight: bold; text-align: center; font-size: 20px; font-family: monospace; }
    .stButton>button { width: 100%; background-color: transparent; color: #00f2ff; border: 1px solid #00f2ff; text-align: left; font-family: monospace; }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<div class="menu-title">--- MENÚ PRINCIPAL ---</div>', unsafe_allow_html=True)
    if st.button("1. Ver Equipo Pokémon"): st.session_state.pagina = "Gestión de Equipo"
    if st.button("2. Capturar Pokémon"): st.session_state.pagina = "Captura"
    if st.button("7. Ver Historial"): st.session_state.pagina = "Exportación"
    if st.button("6. Arena de Combate"): st.session_state.pagina = "Arena"

# 4. LÓGICA DE NAVEGACIÓN
st.markdown('<div class="console-box">', unsafe_allow_html=True)

if st.session_state.pagina == "Gestión de Equipo":
    st.header("🎒 Tu Equipo")
    # Acceso seguro a los datos
    elementos = st.session_state.equipo.obtener_todos()
    if elementos:
        data = [{"Nombre": p.nombre, "Tipo": p.tipo, "Nivel": p.nivel, "HP": p.hp} for p in elementos]
        st.table(pd.DataFrame(data))
    else: st.info("Equipo vacío.")

elif st.session_state.pagina == "Captura":
    st.header("🎯 Capturar Pokémon")
    with st.form("cap"):
        n = st.text_input("Nombre"); t = st.text_input("Tipo")
        if st.form_submit_button("Lanzar Pokéball"):
            st.session_state.equipo.insertar_final(Pokemon(n, t, 5, 100))
            st.success("¡Atrapado!"); st.rerun()

elif st.session_state.pagina == "Arena":
    st.header("⚔️ Arena")
    if st.button("Registrar Victoria"):
        st.session_state.log.append({"Accion": "Combate", "Resultado": "Victoria"})
        st.success("¡Victoria!")

elif st.session_state.pagina == "Exportación":
    st.header("💾 Historial")
    # Concatenación segura
    datos_pokemon = [{"Accion": "Registro", "Resultado": f"Pokémon: {p.nombre}"} for p in st.session_state.equipo.obtener_todos()]
    df = pd.DataFrame(datos_pokemon + st.session_state.log)
    if not df.empty: st.table(df)
    else: st.info("No hay datos.")

st.markdown('</div>', unsafe_allow_html=True)
