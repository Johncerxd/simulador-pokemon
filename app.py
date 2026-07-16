import streamlit as st
import pandas as pd

# --- CLASES ---
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

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Simulador Pokémon Pro", layout="wide")

# CSS para fondos de tablas y cajas
st.markdown("""
    <style>
    .stApp { background: url('https://wallpapercave.com/dwp1x/wp12939364.jpg') no-repeat center center fixed; background-size: cover; }
    .console-box { background-color: rgba(20, 25, 30, 0.9); padding: 30px; border-radius: 15px; border: 3px solid #00f2ff; color: #ffffff; }
    /* Fondo sólido para tablas y datos */
    [data-testid="stTable"], [data-testid="stDataFrame"] { background-color: rgba(20, 25, 30, 0.95) !important; padding: 10px; border-radius: 10px; }
    .stTable table { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- ESTADO ---
if 'equipo' not in st.session_state: st.session_state.equipo = ListaEnlazada()
if 'log' not in st.session_state: st.session_state.log = []
if 'pagina' not in st.session_state: st.session_state.pagina = "Gestión de Equipo"

# --- MENÚ ---
with st.sidebar:
    if st.button("1. Ver Equipo Pokémon"): st.session_state.pagina = "Gestión de Equipo"
    if st.button("2. Capturar Pokémon"): st.session_state.pagina = "Captura"
    if st.button("7. Ver Historial"): st.session_state.pagina = "Exportación"

# --- LÓGICA PRINCIPAL ---
st.markdown('<div class="console-box">', unsafe_allow_html=True)

if st.session_state.pagina == "Gestión de Equipo":
    st.header("🎒 Tu Equipo")
    
    # BUSCADOR INTERACTIVO
    elementos = st.session_state.equipo.obtener_todos()
    df_equipo = pd.DataFrame([{"Nombre": p.nombre, "Tipo": p.tipo, "Nivel": p.nivel, "HP": p.hp} for p in elementos])
    
    if not df_equipo.empty:
        col1, col2, col3 = st.columns(3)
        busqueda = col1.text_input("🔍 Buscar por Nombre")
        tipo_filtro = col2.selectbox("🏷️ Filtrar por Tipo", ["Todos"] + list(df_equipo["Tipo"].unique()))
        hp_filtro = col3.slider("❤️ HP Mínimo", int(df_equipo["HP"].min()), int(df_equipo["HP"].max()))
        
        # Aplicar filtros
        df_filtrado = df_equipo[df_equipo["Nombre"].str.contains(busqueda, case=False)]
        if tipo_filtro != "Todos": df_filtrado = df_filtrado[df_filtrado["Tipo"] == tipo_filtro]
        df_filtrado = df_filtrado[df_filtrado["HP"] >= hp_filtro]
        
        st.table(df_filtrado)
    else: st.info("Equipo vacío.")

elif st.session_state.pagina == "Captura":
    with st.form("cap"):
        n = st.text_input("Nombre"); t = st.text_input("Tipo")
        hp = st.number_input("HP", 1, 999)
        if st.form_submit_button("Lanzar"):
            st.session_state.equipo.insertar_final(Pokemon(n, t, 5, hp))
            st.rerun()

elif st.session_state.pagina == "Exportación":
    st.header("💾 Historial")
    datos = [{"Accion": "Registro", "Resultado": f"Pokémon: {p.nombre}"} for p in st.session_state.equipo.obtener_todos()]
    st.table(pd.DataFrame(datos + st.session_state.log))

st.markdown('</div>', unsafe_allow_html=True)
