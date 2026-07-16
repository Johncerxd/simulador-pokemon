import streamlit as st
import pandas as pd

# Configuración de página
st.set_page_config(page_title="Simulador Pokémon Final", layout="wide")

# --- ESTILOS TEMÁTICOS (FONDO Y CAJAS) ---
st.markdown("""
<style>
.stApp {
    background-image: url('https://i.gifer.com/P4W4.gif');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}
.main-box {
    background-color: rgba(0, 0, 0, 0.7);
    padding: 20px;
    border-radius: 15px;
    color: white;
    border: 2px solid #00f2ff;
}
</style>
""", unsafe_allow_html=True)

# Inicializar sesión
if 'data' not in st.session_state:
    st.session_state.data = []

st.markdown('<div class="main-box">', unsafe_allow_html=True)
st.title("⚡ Simulador Pokémon - Proyecto Final ⚡")

menu = st.sidebar.radio("Navegación", ["Arena de Combate", "Centro de Captura", "Gestión de Datos"])

if menu == "Arena de Combate":
    st.subheader("⚔️ Registro de Combates")
    if st.button("Registrar Victoria"):
        st.session_state.data.append({"Accion": "Combate", "Resultado": "Victoria"})
        st.success("¡Victoria registrada!")

elif menu == "Centro de Captura":
    st.subheader("🎯 Capturar Pokémon")
    poke = st.text_input("Nombre del Pokémon:")
    if st.button("Lanzar Pokéball"):
        st.session_state.data.append({"Accion": "Captura", "Resultado": poke})
        st.balloons()
        st.success(f"¡{poke} capturado!")

elif menu == "Gestión de Datos":
    st.subheader("📊 Tus Estadísticas")
    if st.session_state.data:
        df = pd.DataFrame(st.session_state.data)
        st.table(df)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Descargar CSV", csv, "pokemon_data.csv", "text/csv")
    else:
        st.info("Aún no tienes registros.")

st.markdown('</div>', unsafe_allow_html=True)
