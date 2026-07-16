import streamlit as st
import pandas as pd
import os
import random

try:
    from estructuras import ListaEnlazada, Cola
    from modelos import Pokemon, Entrenador
except ImportError as e:
    st.error(f"Error al importar módulos: {e}. Asegúrate de que 'estructuras.py' y 'modelos.py' estén en el mismo directorio.")
    st.stop()

st.set_page_config(page_title="Simulador Pokémon Pro", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460);
    }
    .console-box {
        background-color: rgba(20, 25, 30, 0.92);
        padding: 30px;
        border-radius: 15px;
        border: 3px solid #00f2ff;
        color: #ffffff;
    }
    .stat-card {
        background-color: rgba(0, 0, 0, 0.6);
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        border: 1px solid #00f2ff;
    }
    .stTable, [data-testid="stTable"] {
        background-color: rgba(20, 25, 30, 0.95) !important;
        padding: 10px;
        border-radius: 10px;
        color: white !important;
    }
    .stTable table, [data-testid="stTable"] table {
        color: white !important;
    }
    .stAlert {
        background-color: rgba(0,0,0,0.7) !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

ARCHIVO_EQUIPO = "equipo.csv"
ARCHIVO_ENTRENADORES = "entrenadores.csv"
ARCHIVO_HISTORIAL = "historial.csv"

def generar_codigo():
    if st.session_state.equipo.cabeza is None:
        return 1
    codigos = [p.codigo for p in st.session_state.equipo.obtener_todos()]
    return max(codigos) + 1 if codigos else 1

def estadisticas_equipo():
    elementos = st.session_state.equipo.obtener_todos()
    if not elementos:
        return 0, 0, 0
    n = len(elementos)
    hp_total = sum(p.hp for p in elementos)
    nivel_total = sum(p.nivel for p in elementos)
    return n, hp_total / n, nivel_total / n

def calcular_danio(atacante, defensor):
    danio = atacante.ataque - defensor.defensa
    return max(1, danio)

def registrar_accion(accion):
    st.session_state.historial_acciones.append(accion)

def deshacer_accion():
    if st.session_state.historial_acciones:
        return st.session_state.historial_acciones.pop()
    return None

def guardar_partida():
    elementos = st.session_state.equipo.obtener_todos()
    if elementos:
        df_equipo = pd.DataFrame([{
            'codigo': p.codigo,
            'nombre': p.nombre,
            'tipo': p.tipo,
            'nivel': p.nivel,
            'hp_maximo': p.hp_maximo,
            'hp': p.hp,
            'ataque': p.ataque,
            'defensa': p.defensa,
            'velocidad': p.velocidad
        } for p in elementos])
        df_equipo.to_csv(ARCHIVO_EQUIPO, index=False)
    else:
        if os.path.exists(ARCHIVO_EQUIPO):
            os.remove(ARCHIVO_EQUIPO)

    entrenadores = st.session_state.cola_entrenadores.elementos
    if entrenadores:
        df_ent = pd.DataFrame([{
            'nombre': e.nombre,
            'gimnasio': e.gimnasio,
            'pokemon_principal': e.pokemon_principal.nombre if e.pokemon_principal else '',
            'recompensa': e.recompensa
        } for e in entrenadores])
        df_ent.to_csv(ARCHIVO_ENTRENADORES, index=False)
    else:
        if os.path.exists(ARCHIVO_ENTRENADORES):
            os.remove(ARCHIVO_ENTRENADORES)

    if st.session_state.historial_acciones:
        df_hist = pd.DataFrame(st.session_state.historial_acciones, columns=['accion'])
        df_hist.to_csv(ARCHIVO_HISTORIAL, index=False)
    else:
        if os.path.exists(ARCHIVO_HISTORIAL):
            os.remove(ARCHIVO_HISTORIAL)

    st.success("Partida guardada correctamente.")

def cargar_partida():
    if os.path.exists(ARCHIVO_EQUIPO):
        df = pd.read_csv(ARCHIVO_EQUIPO)
        for _, row in df.iterrows():
            p = Pokemon(
                codigo=int(row['codigo']),
                nombre=row['nombre'],
                tipo=row['tipo'],
                nivel=int(row['nivel']),
                hp_maximo=int(row['hp_maximo']),
                hp=int(row['hp']),
                ataque=int(row['ataque']),
                defensa=int(row['defensa']),
                velocidad=int(row['velocidad'])
            )
            st.session_state.equipo.insertar_final(p)

    if os.path.exists(ARCHIVO_ENTRENADORES):
        df = pd.read_csv(ARCHIVO_ENTRENADORES)
        for _, row in df.iterrows():
            p_dummy = Pokemon(0, row['pokemon_principal'], 'Normal', 1, 10, 10, 5, 5, 5)
            e = Entrenador(row['nombre'], row['gimnasio'], p_dummy, row['recompensa'])
            st.session_state.cola_entrenadores.encolar(e)

    if os.path.exists(ARCHIVO_HISTORIAL):
        df = pd.read_csv(ARCHIVO_HISTORIAL)
        st.session_state.historial_acciones = df['accion'].tolist()

def iniciar_combate_salvaje():
    tipos = ['Fuego', 'Agua', 'Planta', 'Electrico', 'Psiquico', 'Roca', 'Tierra']
    nombres = ['Pikachu', 'Charmander', 'Squirtle', 'Bulbasaur', 'Eevee', 'Mewtwo', 'Gengar']
    nivel = random.randint(1, 30)
    hp = random.randint(30, 100)
    ataque = random.randint(5, 20)
    defensa = random.randint(5, 15)
    velocidad = random.randint(5, 20)
    pokemon = Pokemon(
        codigo=0,
        nombre=random.choice(nombres),
        tipo=random.choice(tipos),
        nivel=nivel,
        hp_maximo=hp,
        hp=hp,
        ataque=ataque,
        defensa=defensa,
        velocidad=velocidad
    )
    st.session_state.oponente_actual = pokemon
    st.session_state.combate_activo = True
    st.session_state.mensaje_combate = f"¡Apareció un {pokemon.nombre} salvaje!"
    registrar_accion(f"Inicio combate contra {pokemon.nombre}")

def iniciar_combate_gimnasio():
    if st.session_state.cola_entrenadores.esta_vacia():
        st.session_state.mensaje_combate = "No hay más entrenadores en la cola."
        return
    entrenador = st.session_state.cola_entrenadores.desencolar()
    st.session_state.oponente_actual = entrenador.pokemon_principal
    st.session_state.combate_activo = True
    st.session_state.mensaje_combate = f"¡Te enfrentas al entrenador {entrenador.nombre} del gimnasio {entrenador.gimnasio}!"
    registrar_accion(f"Inicio combate contra entrenador {entrenador.nombre}")

def realizar_ataque(jugador, oponente):
    danio = calcular_danio(jugador, oponente)
    oponente.recibir_danio(danio)
    msg = f"¡{jugador.nombre} ataca a {oponente.nombre} y causa {danio} de daño!"
    if oponente.esta_debilitado():
        msg += f" ¡{oponente.nombre} se debilitó!"
        st.session_state.combate_activo = False
    registrar_accion(f"Ataque: {jugador.nombre} -> {oponente.nombre} ({danio} dmg)")
    return msg

def huir():
    st.session_state.combate_activo = False
    st.session_state.oponente_actual = None
    msg = "Has huido del combate."
    registrar_accion("Huir del combate")
    return msg

if 'equipo' not in st.session_state:
    st.session_state.equipo = ListaEnlazada()
if 'cola_entrenadores' not in st.session_state:
    st.session_state.cola_entrenadores = Cola()
if 'historial_acciones' not in st.session_state:
    st.session_state.historial_acciones = []
if 'pagina' not in st.session_state:
    st.session_state.pagina = "Inicio"
if 'combate_activo' not in st.session_state:
    st.session_state.combate_activo = False
if 'oponente_actual' not in st.session_state:
    st.session_state.oponente_actual = None
if 'pokemon_jugador_actual' not in st.session_state:
    st.session_state.pokemon_jugador_actual = None
if 'mensaje_combate' not in st.session_state:
    st.session_state.mensaje_combate = ""
if 'turno' not in st.session_state:
    st.session_state.turno = 0
if 'datos_cargados' not in st.session_state:
    cargar_partida()
    st.session_state.datos_cargados = True

with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/9/98/International_Pok%C3%A9mon_logo.svg", width=200)
    st.markdown("---")
    opciones = [
        "Inicio",
        "Gestion de Equipo",
        "Combate",
        "Busqueda y Ordenamiento",
        "Historial",
        "Persistencia"
    ]
    for op in opciones:
        if st.button(op, use_container_width=True):
            st.session_state.pagina = op
            st.rerun()

st.markdown('<div class="console-box">', unsafe_allow_html=True)

if st.session_state.pagina == "Inicio":
    st.header("🏠 Bienvenido al Simulador Pokemon Pro")
    st.markdown("""
    Este sistema te permite gestionar tu equipo Pokemon, enfrentarte a oponentes salvajes
    y desafiar a entrenadores de gimnasio, todo utilizando estructuras de datos como
    listas enlazadas, colas y pilas.
    """)
    col1, col2, col3 = st.columns(3)
    cantidad, prom_hp, prom_nivel = estadisticas_equipo()
    col1.metric("Cantidad de Pokemon", cantidad)
    col2.metric("HP promedio", f"{prom_hp:.1f}")
    col3.metric("Nivel promedio", f"{prom_nivel:.1f}")

    if cantidad > 0:
        with st.expander("Ver equipo completo"):
            df = pd.DataFrame([{
                "Codigo": p.codigo,
                "Nombre": p.nombre,
                "Tipo": p.tipo,
                "Nivel": p.nivel,
                "HP": p.hp,
                "Ataque": p.ataque,
                "Defensa": p.defensa,
                "Velocidad": p.velocidad
            } for p in st.session_state.equipo.obtener_todos()])
            st.dataframe(df, use_container_width=True)
    else:
        st.info("Tu equipo esta vacio. Captura algunos Pokemon en 'Gestion de Equipo'.")

elif st.session_state.pagina == "Gestion de Equipo":
    st.header("🎒 Gestion de Equipo")

    elementos = st.session_state.equipo.obtener_todos()
    if elementos:
        df_equipo = pd.DataFrame([{
            "Codigo": p.codigo,
            "Nombre": p.nombre,
            "Tipo": p.tipo,
            "Nivel": p.nivel,
            "HP": p.hp,
            "Ataque": p.ataque,
            "Defensa": p.defensa,
            "Velocidad": p.velocidad
        } for p in elementos])

        col1, col2 = st.columns(2)
        busqueda = col1.text_input("🔍 Buscar por Nombre")
        tipo_filtro = col2.selectbox("🏷️ Filtrar por Tipo", ["Todos"] + list(df_equipo["Tipo"].unique()))

        nivel_min, nivel_max = int(df_equipo["Nivel"].min()), int(df_equipo["Nivel"].max())
        nivel_rango = st.slider("📊 Rango de Nivel", nivel_min, nivel_max+1, (nivel_min, nivel_max+1))
        hp_min, hp_max = int(df_equipo["HP"].min()), int(df_equipo["HP"].max())
        hp_rango = st.slider("❤️ Rango de HP", hp_min, hp_max+1, (hp_min, hp_max+1))

        df_filtrado = df_equipo[
            (df_equipo["Nombre"].str.contains(busqueda, case=False)) &
            (df_equipo["Nivel"] >= nivel_rango[0]) & (df_equipo["Nivel"] <= nivel_rango[1]) &
            (df_equipo["HP"] >= hp_rango[0]) & (df_equipo["HP"] <= hp_rango[1])
        ]
        if tipo_filtro != "Todos":
            df_filtrado = df_filtrado[df_filtrado["Tipo"] == tipo_filtro]

        st.dataframe(df_filtrado, use_container_width=True)

        cant, prom_hp, prom_niv = estadisticas_equipo()
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Pokemon", cant)
        col2.metric("HP Promedio", f"{prom_hp:.1f}")
        col3.metric("Nivel Promedio", f"{prom_niv:.1f}")

        st.subheader("🗑️ Liberar Pokemon")
        codigo_liberar = st.number_input("Ingresa el codigo del Pokemon a liberar", min_value=1, step=1)
        if st.button("Liberar"):
            encontrado = False
            actual = st.session_state.equipo.cabeza
            prev = None
            while actual:
                if actual.dato.codigo == codigo_liberar:
                    if prev:
                        prev.siguiente = actual.siguiente
                    else:
                        st.session_state.equipo.cabeza = actual.siguiente
                    encontrado = True
                    st.success(f"Pokemon con codigo {codigo_liberar} liberado.")
                    registrar_accion(f"Liberado Pokemon codigo {codigo_liberar}")
                    st.rerun()
                    break
                prev = actual
                actual = actual.siguiente
            if not encontrado:
                st.error("No se encontro un Pokemon con ese codigo.")
    else:
        st.info("Equipo vacio. Captura Pokemon usando el formulario de abajo.")

    with st.expander("➕ Capturar nuevo Pokemon", expanded=False):
        with st.form("captura_form"):
            col1, col2 = st.columns(2)
            nombre = col1.text_input("Nombre")
            tipo = col2.text_input("Tipo")
            nivel = col1.number_input("Nivel", 1, 100, 5)
            hp = col2.number_input("HP", 1, 999, 50)
            ataque = col1.number_input("Ataque", 1, 100, 10)
            defensa = col2.number_input("Defensa", 1, 100, 10)
            velocidad = col1.number_input("Velocidad", 1, 100, 10)
            if st.form_submit_button("Capturar"):
                if nombre and tipo:
                    codigo = generar_codigo()
                    nuevo = Pokemon(codigo, nombre, tipo, nivel, hp, hp, ataque, defensa, velocidad)
                    st.session_state.equipo.insertar_final(nuevo)
                    registrar_accion(f"Capturado {nombre} (codigo {codigo})")
                    st.success(f"¡{nombre} capturado con exito!")
                    st.rerun()
                else:
                    st.error("Nombre y tipo son obligatorios.")

elif st.session_state.pagina == "Combate":
    st.header("⚔️ Combate")

    elementos = st.session_state.equipo.obtener_todos()
    if not elementos:
        st.warning("No tienes Pokemon en tu equipo. Captura algunos primero.")
    else:
        nombres = [f"{p.nombre} (HP: {p.hp}/{p.hp_maximo})" for p in elementos]
        opcion = st.selectbox("Selecciona tu Pokemon", range(len(elementos)), format_func=lambda i: nombres[i])
        pokemon_jugador = elementos[opcion]
        st.session_state.pokemon_jugador_actual = pokemon_jugador

        if st.session_state.combate_activo and st.session_state.oponente_actual:
            oponente = st.session_state.oponente_actual
            st.subheader("Estado del combate")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Tu Pokemon:** {pokemon_jugador.nombre} (HP: {pokemon_jugador.hp}/{pokemon_jugador.hp_maximo})")
            with col2:
                st.markdown(f"**Oponente:** {oponente.nombre} (HP: {oponente.hp}/{oponente.hp_maximo})")
            st.info(st.session_state.mensaje_combate)

            col1, col2, col3 = st.columns(3)
            if col1.button("⚡ Atacar"):
                if pokemon_jugador.hp <= 0:
                    st.error("Tu Pokemon esta debilitado. No puede atacar.")
                else:
                    msg = realizar_ataque(pokemon_jugador, oponente)
                    st.session_state.mensaje_combate = msg
                    if oponente.esta_debilitado():
                        st.success(f"¡Ganaste el combate contra {oponente.nombre}!")
                        st.session_state.combate_activo = False
                    else:
                        danio_op = calcular_danio(oponente, pokemon_jugador)
                        pokemon_jugador.recibir_danio(danio_op)
                        st.session_state.mensaje_combate += f" {oponente.nombre} contraataca y causa {danio_op} de daño."
                        if pokemon_jugador.esta_debilitado():
                            st.session_state.mensaje_combate += f" ¡{pokemon_jugador.nombre} se debilito!"
                            st.session_state.combate_activo = False
                    st.rerun()

            if col2.button("💊 Curar (restaurar HP)"):
                if pokemon_jugador.hp < pokemon_jugador.hp_maximo:
                    pokemon_jugador.restaurar_hp()
                    st.session_state.mensaje_combate = f"{pokemon_jugador.nombre} restauró todo su HP."
                    registrar_accion(f"Curar {pokemon_jugador.nombre}")
                    danio_op = calcular_danio(oponente, pokemon_jugador)
                    pokemon_jugador.recibir_danio(danio_op)
                    st.session_state.mensaje_combate += f" {oponente.nombre} ataca y causa {danio_op} de daño."
                    if pokemon_jugador.esta_debilitado():
                        st.session_state.mensaje_combate += f" ¡{pokemon_jugador.nombre} se debilito!"
                        st.session_state.combate_activo = False
                    st.rerun()
                else:
                    st.warning("Tu Pokemon ya tiene HP completo.")

            if col3.button("🏃 Huir"):
                st.session_state.mensaje_combate = huir()
                st.rerun()

            if st.button("↩️ Deshacer ultima accion (historial)"):
                accion = deshacer_accion()
                if accion:
                    st.success(f"Accion deshecha: {accion}")
                else:
                    st.info("No hay acciones para deshacer.")
        else:
            st.subheader("Iniciar un nuevo combate")
            col1, col2 = st.columns(2)
            if col1.button("🐾 Pokemon Salvaje"):
                if pokemon_jugador.hp > 0:
                    iniciar_combate_salvaje()
                    st.rerun()
                else:
                    st.error("Tu Pokemon esta debilitado. Curalo primero.")
            if col2.button("🏅 Entrenador de Gimnasio"):
                if pokemon_jugador.hp > 0:
                    iniciar_combate_gimnasio()
                    st.rerun()
                else:
                    st.error("Tu Pokemon esta debilitado. Curalo primero.")

            entrenadores = st.session_state.cola_entrenadores.elementos
            if entrenadores:
                with st.expander("Entrenadores en espera"):
                    df_ent = pd.DataFrame([{
                        "Nombre": e.nombre,
                        "Gimnasio": e.gimnasio,
                        "Pokemon principal": e.pokemon_principal.nombre,
                        "Recompensa": e.recompensa
                    } for e in entrenadores])
                    st.dataframe(df_ent)
            else:
                st.info("No hay entrenadores en cola. Puedes agregar algunos desde 'Persistencia'.")

elif st.session_state.pagina == "Busqueda y Ordenamiento":
    st.header("🔍 Busqueda y Ordenamiento")

    elementos = st.session_state.equipo.obtener_todos()
    if not elementos:
        st.warning("Equipo vacio. Captura Pokemon primero.")
    else:
        st.subheader("Buscar Pokemon")
        criterio = st.radio("Buscar por:", ["Codigo", "Nombre"])
        if criterio == "Codigo":
            codigo_bus = st.number_input("Codigo", min_value=1, step=1)
            if st.button("Buscar"):
                encontrado = None
                for p in elementos:
                    if p.codigo == codigo_bus:
                        encontrado = p
                        break
                if encontrado:
                    st.success(f"Pokemon encontrado: {encontrado.nombre} (codigo {encontrado.codigo})")
                    df = pd.DataFrame([{
                        "Codigo": encontrado.codigo,
                        "Nombre": encontrado.nombre,
                        "Tipo": encontrado.tipo,
                        "Nivel": encontrado.nivel,
                        "HP": encontrado.hp,
                        "Ataque": encontrado.ataque,
                        "Defensa": encontrado.defensa,
                        "Velocidad": encontrado.velocidad
                    }])
                    st.dataframe(df)
                else:
                    st.error("No se encontro Pokemon con ese codigo.")
        else:
            nombre_bus = st.text_input("Nombre (puede ser parcial)")
            if st.button("Buscar"):
                resultados = [p for p in elementos if nombre_bus.lower() in p.nombre.lower()]
                if resultados:
                    st.success(f"Se encontraron {len(resultados)} Pokemon:")
                    df = pd.DataFrame([{
                        "Codigo": p.codigo,
                        "Nombre": p.nombre,
                        "Tipo": p.tipo,
                        "Nivel": p.nivel,
                        "HP": p.hp,
                        "Ataque": p.ataque,
                        "Defensa": p.defensa,
                        "Velocidad": p.velocidad
                    } for p in resultados])
                    st.dataframe(df)
                else:
                    st.error("No se encontraron coincidencias.")

        st.subheader("Ordenar equipo")
        col1, col2 = st.columns(2)
        criterio_ord = col1.selectbox("Criterio", ["HP (ascendente)", "HP (descendente)", "Ataque (ascendente)", "Ataque (descendente)"])
        algoritmo = col2.selectbox("Algoritmo", ["Burbuja", "Insercion"])

        if st.button("Ordenar"):
            lista_ordenar = elementos.copy()
            n = len(lista_ordenar)

            if criterio_ord == "HP (ascendente)":
                key = lambda p: p.hp
                reverse = False
            elif criterio_ord == "HP (descendente)":
                key = lambda p: p.hp
                reverse = True
            elif criterio_ord == "Ataque (ascendente)":
                key = lambda p: p.ataque
                reverse = False
            else:
                key = lambda p: p.ataque
                reverse = True

            if algoritmo == "Burbuja":
                for i in range(n-1):
                    for j in range(0, n-i-1):
                        if (key(lista_ordenar[j]) > key(lista_ordenar[j+1])) if not reverse else (key(lista_ordenar[j]) < key(lista_ordenar[j+1])):
                            lista_ordenar[j], lista_ordenar[j+1] = lista_ordenar[j+1], lista_ordenar[j]
            else:
                for i in range(1, n):
                    actual = lista_ordenar[i]
                    j = i-1
                    if not reverse:
                        while j >= 0 and key(lista_ordenar[j]) > key(actual):
                            lista_ordenar[j+1] = lista_ordenar[j]
                            j -= 1
                    else:
                        while j >= 0 and key(lista_ordenar[j]) < key(actual):
                            lista_ordenar[j+1] = lista_ordenar[j]
                            j -= 1
                    lista_ordenar[j+1] = actual

            st.success("Equipo ordenado:")
            df_ord = pd.DataFrame([{
                "Codigo": p.codigo,
                "Nombre": p.nombre,
                "Tipo": p.tipo,
                "Nivel": p.nivel,
                "HP": p.hp,
                "Ataque": p.ataque,
                "Defensa": p.defensa,
                "Velocidad": p.velocidad
            } for p in lista_ordenar])
            st.dataframe(df_ord, use_container_width=True)

            if st.button("Aplicar este orden al equipo"):
                nueva_lista = ListaEnlazada()
                for p in lista_ordenar:
                    nueva_lista.insertar_final(p)
                st.session_state.equipo = nueva_lista
                st.success("Equipo actualizado con el nuevo orden.")
                registrar_accion("Equipo reordenado")
                st.rerun()

elif st.session_state.pagina == "Historial":
    st.header("📜 Historial de Acciones")

    if st.session_state.historial_acciones:
        df_hist = pd.DataFrame(st.session_state.historial_acciones, columns=["Accion"])
        st.dataframe(df_hist, use_container_width=True)

        if st.button("🗑️ Limpiar historial"):
            st.session_state.historial_acciones.clear()
            st.success("Historial limpiado.")
            st.rerun()

        if st.button("↩️ Deshacer ultima accion"):
            accion = deshacer_accion()
            if accion:
                st.success(f"Ultima accion deshecha: {accion}")
                st.rerun()
            else:
                st.info("No hay acciones para deshacer.")
    else:
        st.info("Aun no se han registrado acciones.")

elif st.session_state.pagina == "Persistencia":
    st.header("💾 Persistencia de Datos")

    col1, col2 = st.columns(2)
    if col1.button("💿 Guardar partida"):
        guardar_partida()

    if col2.button("📂 Cargar partida"):
        st.session_state.equipo = ListaEnlazada()
        st.session_state.cola_entrenadores = Cola()
        st.session_state.historial_acciones = []
        cargar_partida()
        st.success("Partida cargada correctamente.")
        st.rerun()

    st.markdown("---")
    st.subheader("Agregar entrenadores a la cola (para combate de gimnasio)")
    with st.form("agregar_entrenador"):
        nombre = st.text_input("Nombre del entrenador")
        gimnasio = st.text_input("Gimnasio")
        pok_nombre = st.text_input("Pokemon principal (nombre)")
        recompensa = st.text_input("Recompensa")
        if st.form_submit_button("Agregar entrenador"):
            if nombre and gimnasio and pok_nombre:
                p_dummy = Pokemon(0, pok_nombre, "Normal", 1, 30, 30, 10, 10, 10)
                entrenador = Entrenador(nombre, gimnasio, p_dummy, recompensa)
                st.session_state.cola_entrenadores.encolar(entrenador)
                st.success(f"Entrenador {nombre} agregado a la cola.")
                registrar_accion(f"Agregado entrenador {nombre}")
                st.rerun()
            else:
                st.error("Todos los campos son obligatorios.")

    entrenadores = st.session_state.cola_entrenadores.elementos
    if entrenadores:
        with st.expander("Ver entrenadores en cola"):
            df_ent = pd.DataFrame([{
                "Nombre": e.nombre,
                "Gimnasio": e.gimnasio,
                "Pokemon": e.pokemon_principal.nombre,
                "Recompensa": e.recompensa
            } for e in entrenadores])
            st.dataframe(df_ent)

st.markdown('</div>', unsafe_allow_html=True)
