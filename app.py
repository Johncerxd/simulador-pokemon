import streamlit as st
import pandas as pd
import io

# Inicializar estado si no existe
if 'historial_combates' not in st.session_state:
    st.session_state.historial_combates = []

# --- MENÚ DE NAVEGACIÓN ---
menu = st.sidebar.selectbox("Selecciona una sección", ["Combate", "Captura", "Estadísticas"])

if menu == "Combate":
    st.title("⚔️ Arena")
    if st.button("Registrar Combate Ganado"):
        st.session_state.historial_combates.append({"Accion": "Combate", "Resultado": "Victoria"})
        st.success("¡Combate registrado!")

elif menu == "Captura":
    st.title("🎯 Captura")
    nombre_poke = st.text_input("Nombre del Pokémon")
    if st.button("Capturar"):
        st.session_state.historial_combates.append({"Accion": "Captura", "Resultado": nombre_poke})
        st.balloons()

elif menu == "Estadísticas":
    st.title("📊 Exportar Datos")
    if st.session_state.historial_combates:
        df = pd.DataFrame(st.session_state.historial_combates)
        st.table(df)
        
        # Lógica de Exportación CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar Estadísticas en CSV",
            data=csv,
            file_name='historial_pokemon.csv',
            mime='text/csv',
        )
    else:
        st.info("No hay datos para exportar.")
