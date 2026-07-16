import streamlit as st
from modelos import Pokemon
from estructuras import ListaEnlazada

st.set_page_config(page_title="Menú Pokémon", layout="centered")

# --- ESTILOS ---
st.markdown("""
    <style>
    .menu-box {
        border: 2px solid #00f2ff;
        padding: 20px;
        border-radius: 10px;
        background-color: #1a1a1a;
    }
    </style>
    """, unsafe_allow_html=True)

# --- MENÚ PRINCIPAL ---
st.markdown('<div class="menu-box">', unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: #e6ff00;'>MENÚ PRINCIPAL</h2>", unsafe_allow_html=True)

opcion = st.radio("Selecciona una acción:", [
    "1. Ver Equipo Pokémon",
    "2. Capturar Pokémon",
    "3. Liberar Pokémon",
    "4. Ordenar Equipo",
    "5. Ver Gimnasios Disponibles",
    "6. Desafiar Líder de Gimnasio",
    "7. Ver Historial de Combate",
    "8. Estado del Entrenador",
    "9. Guardar y Salir"
])
st.markdown('</div>', unsafe_allow_html=True)

# --- LÓGICA DE INGRESO ---
if st.button("Ejecutar Acción"):
    if "1." in opcion:
        st.write("Cargando equipo...")
    elif "2." in opcion:
        with st.form("capturar_form"):
            nombre = st.text_input("Nombre del Pokémon a capturar:")
            if st.form_submit_button("Lanzar Pokéball"):
                st.success(f"¡Has capturado a {nombre}!")
    elif "9." in opcion:
        st.warning("Guardando progreso... ¡Hasta pronto!")
