import streamlit as st
from modelos import Pokemon, Entrenador
from estructuras import ListaEnlazada, Cola

st.set_page_config(page_title="Simulador Pokémon", layout="wide")

if 'equipo' not in st.session_state:
    st.session_state.equipo = ListaEnlazada()
    st.session_state.equipo.insertar_final(Pokemon(1, "Pikachu", "Electrico", 5, 100, 100, 20, 10, 50))

st.title("🎮 Simulador Pokémon Online")

col1, col2 = st.columns(2)

with col1:
    st.header("Tu Equipo")
    for p in st.session_state.equipo.obtener_todos():
        st.write(f"### {p.nombre}")
        st.progress(p.hp / p.hp_maximo)
        st.write(f"HP: {p.hp}/{p.hp_maximo} | Nivel: {p.nivel}")

with col2:
    st.header("Acciones")
    if st.button("Curar Equipo"):
        for p in st.session_state.equipo.obtener_todos():
            p.restaurar_hp()
        st.success("¡Curado!")
        st.rerun()
