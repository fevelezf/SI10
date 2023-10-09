import streamlit as st
import pandas as pd
from github import Github

# Tu token de acceso personal de GitHub (generado en tu cuenta de GitHub)
access_token = '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'

# Nombre de tu repositorio y archivo CSV
repo_name = 'fevelezf/SI10'
file_name = 'usuarios.csv'

# Crear una instancia de la clase Github con tu token de acceso
g = Github(access_token)

# Obtener el contenido del archivo CSV desde el repositorio
try:
    repo = g.get_repo(repo_name)
    file_content = repo.get_contents(file_name)
    usuarios_df = pd.read_csv(file_content.decoded_content)
except:
    usuarios_df = pd.DataFrame(columns=["Usuario", "Clave"])

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
        if nuevo_usuario in usuarios_df["Usuario"].values:
            st.warning("El usuario ya existe. Elije otro nombre de usuario.")
        else:
            # Añadir un nuevo registro al DataFrame
            nuevo_registro = pd.DataFrame({"Usuario": [nuevo_usuario], "Clave": [nueva_clave]})
            usuarios_df = pd.concat([usuarios_df, nuevo_registro], ignore_index=True)

            # Convertir el DataFrame a un archivo CSV en memoria
            csv_data = usuarios_df.to_csv(index=False)

            # Actualizar el archivo CSV en el repositorio de GitHub
            repo.update_file(file_name, "Actualización de usuarios", csv_data, file_content.sha)

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
