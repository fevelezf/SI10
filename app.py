import streamlit as st
import pandas as pd
import os

# Cargar o crear un DataFrame para almacenar usuarios y contraseñas
usuarios_csv = "usuarios.csv"
if not os.path.exists(usuarios_csv):
    usuarios_df = pd.DataFrame(columns=["Usuario", "Clave"])
else:
    usuarios_df = pd.read_csv(usuarios_csv)

# Iniciar sesión
def iniciar_sesion():
    st.subheader("Iniciar Sesión")
    usuario = st.text_input("Usuario")
    clave = st.text_input("Clave", type="password")

    if st.button("Iniciar Sesión"):
        if usuarios_df.empty:
            st.error("No hay usuarios registrados. Por favor, regístrate primero.")
            return False

        if usuario in usuarios_df["Usuario"].values and usuarios_df.loc[usuarios_df["Usuario"] == usuario, "Clave"].values[0] == clave:
            st.success("Inicio de sesión exitoso.")
            return True
        else:
            st.error("Usuario o clave incorrectos.")
            return False
    return False

# Registro de nuevos usuarios
def registrar_usuario():
    global usuarios_df  # Declarar usuarios_df como una variable global
    st.subheader("Registrarse")
    nuevo_usuario = st.text_input("Nuevo Usuario")
    nueva_clave = st.text_input("Nueva Clave", type="password")

    if st.button("Registrarse"):
        if nuevo_usuario:
            if nuevo_usuario in usuarios_df["Usuario"].values:
                st.warning("El usuario ya existe. Elije otro nombre de usuario.")
            else:
                nuevo_registro = pd.DataFrame({"Usuario": [nuevo_usuario], "Clave": [nueva_clave]})
                usuarios_df = pd.concat([usuarios_df, nuevo_registro], ignore_index=True)
                usuarios_df.to_csv(usuarios_csv, index=False)  # Guardar el DataFrame en el archivo CSV
                st.success("Registro exitoso. Ahora puedes iniciar sesión.")

# Comprobar si el usuario ha iniciado sesión o desea registrarse
if not iniciar_sesion():
    registrar_usuario()
else:
    st.title("DeporteStats Pro")

    # Opción de registro
    st.subheader("Registro")
    registro_opcion = st.radio("Seleccione una opción:", ["Partido", "Jugador"])

    if registro_opcion == "Partido":
        st.subheader("Registro de Partido")
        fecha = st.date_input("Fecha del Partido")
        equipo_local = st.text_input("Equipo Local")
        equipo_visitante = st.text_input("Equipo Visitante")
        goles_local = st.number_input("Goles del Equipo Local")
        goles_visitante = st.number_input("Goles del Equipo Visitante")

        if st.button("Registrar Partido"):
            partido = pd.Series([fecha, equipo_local, equipo_visitante, goles_local, goles_visitante], index=partidos_df.columns)
            partidos_df = partidos_df.append(partido, ignore_index=True)
            st.success("Partido registrado con éxito.")

    elif registro_opcion == "Jugador":
        st.subheader("Registro de Jugador")
        nombre_jugador = st.text_input("Nombre del Jugador")
        posicion = st.text_input("Posición del Jugador")

        if st.button("Registrar Jugador"):
            jugador = pd.Series([nombre_jugador, posicion], index=jugadores_df.columns)
            jugadores_df = jugadores_df.append(jugador, ignore_index=True)
            st.success("Jugador registrado con éxito.")

    # Visualización y análisis de datos
    st.subheader("Análisis de Datos")

    # Puedes realizar análisis y visualizaciones aquí utilizando Pandas, Numpy y Matplotlib

    # Visualización de los DataFrames
    st.write("Datos de Partidos:")
    st.write(partidos_df)

    st.write("Datos de Jugadores:")
    st.write(jugadores_df)

    st.write("Gráfico de Goles por Partido:")
    if not partidos_df.empty:
        goles_por_partido = partidos_df.groupby("Fecha")[["Goles Local", "Goles Visitante"]].sum()
        st.line_chart(goles_por_partido)

    st.write("Gráfico de Posiciones de Jugadores:")
    if not jugadores_df.empty:
        posiciones = jugadores_df["Posición"].value_counts()
        st.bar_chart(posiciones)
