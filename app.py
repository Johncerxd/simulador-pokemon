import streamlit as st
from modelos import Pokemon
from estructuras import ListaEnlazada

st.set_page_config(page_title="Simulador Pokémon Pro", layout="wide")

# Inicialización de estado
if 'equipo' not in st.session_state:
    st.session_state.equipo = ListaEnlazada()
    st.session_state.equipo.insertar_final(Pokemon(1, "Pikachu", "Electrico", 5, 100, 100, 20, 10, 50))

# --- MENÚ AVANZADO (SIDEBAR) ---
with st.sidebar:
    st.title("⚙️ Panel de Control")
    st.markdown("---")
    menu = st.radio("Navegación", ["Combate", "Gestionar Equipo", "Estadísticas"])
    st.markdown("---")
    if st.button("🔄 Reiniciar Simulación"):
        st.session_state.equipo = ListaEnlazada()
        st.rerun()

# --- LÓGICA DE NAVEGACIÓN ---
if menu == "Combate":
    st.title("⚔️ Arena de Batalla")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Tu Equipo")
        for p in st.session_state.equipo.obtener_todos():
            st.metric(label=p.nombre, value=f"{p.hp} HP", delta=f"Nivel {p.nivel}")
            st.progress(p.hp / p.hp_maximo)

elif menu == "Gestionar Equipo":
    st.title("🎒 Gestión de Pokémon")
    st.info("Aquí puedes administrar tus criaturas.")
    if st.button("✨ Curar todo el equipo"):
        for p in st.session_state.equipo.obtener_todos():
            p.restaurar_hp()
        st.success("¡Salud restaurada!")
        st.rerun()

elif menu == "Estadísticas":
    st.title("📊 Análisis de Datos")
    st.bar_chart({p.nombre: p.hp for p in st.session_state.equipo.obtener_todos()})
