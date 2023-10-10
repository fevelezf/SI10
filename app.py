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
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Cargar el archivo CSV con los usuarios
usuarios_df = pd.read_csv('usuarios.csv')

# Inicializar la variable de sesión para el nombre de usuario
if 'username' not in st.session_state:
    st.session_state.username = None

# Obtener el nombre de usuario actual después del inicio de sesión
def get_current_user():
    return st.session_state.username

# Función para cargar o crear un archivo CSV para el usuario actual
def get_user_data(username):
    user_data_filename = f"{username}_data.csv"
    if not os.path.exists(user_data_filename):
        # Si el archivo no existe, crea un DataFrame vacío
        return pd.DataFrame({'Fecha': [], 'Tipo': [], 'Categoría': [], 'Monto': []})
    else:
        # Si el archivo existe, carga los datos desde el archivo CSV
        return pd.read_csv(user_data_filename)

# Función para registrar un nuevo usuario
def registrar_usuario(username, password):
    global usuarios_df

    # Verificar si el usuario ya existe
    if username in usuarios_df['Username'].values:
        return False, "El usuario ya existe. Por favor, elija otro nombre de usuario."

    # Agregar el nuevo usuario al DataFrame
    nuevo_usuario = pd.DataFrame({'Username': [username], 'Password': [password]})
    usuarios_df = pd.concat([usuarios_df, nuevo_usuario], ignore_index=True)

    # Guardar el DataFrame actualizado en el archivo CSV
    usuarios_df.to_csv('usuarios.csv', index=False)

    return True, "Registro exitoso. Ahora puede iniciar sesión."

def verificar_credenciales(username, password):
    # Lee el archivo CSV de usuarios
    try:
        usuarios_df = pd.read_csv('usuarios.csv')
    except FileNotFoundError:
        return False, "No se encontraron usuarios registrados."

    # Verifica las credenciales
    if (usuarios_df['Username'] == username).any() and (usuarios_df['Password'] == password).any():
        return True, "Inicio de sesión exitoso."
    else:
        return False, "Credenciales incorrectas. Por favor, verifique su nombre de usuario y contraseña."
    

# Título de la aplicación
st.title("EQUIPO")

# Menú desplegable en la barra lateral
menu_option = st.sidebar.selectbox("Menú", ["Inicio", "Registro", "Cerrar Sesión"])  

# Si el usuario elige "Cerrar Sesión", restablecer la variable de sesión a None
if menu_option == "Cerrar Sesión":
    st.session_state.username = None
    st.success("Sesión cerrada con éxito. Por favor, inicie sesión nuevamente.")

# Si el usuario ya ha iniciado sesión, mostrar los botones
if get_current_user() is not None:
    st.write(f"Bienvenido, {get_current_user()}!")

    # Botones para registrar gasto, ingreso o ver registros
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
else:
    # Inicio de sesión
    if menu_option == "Inicio":
        st.write("Bienvenido al inicio de la aplicación.")

        # Campos de inicio de sesión
        username = st.text_input("Nombre de Usuario:")
        password = st.text_input("Contraseña:", type="password")

        if st.button("Iniciar Sesión"):
            login_successful, message = verificar_credenciales(username, password)
            if login_successful:
                st.success(message)
                st.session_state.username = username  # Almacenar el nombre de usuario en la sesión
            else:
                st.error(message)
    elif menu_option == "Registro":
        st.write("Registro de Usuario")

        # Campos de registro
        new_username = st.text_input("Nuevo Nombre de Usuario:")
        new_password = st.text_input("Nueva Contraseña:", type="password")

        if st.button("Registrarse"):
            registration_successful, message = registrar_usuario(new_username, new_password)
            if registration_successful:
                st.success(message)
            else:
                st.error(message)
    elif menu_option == "Salir":
        st.balloons()
        st.stop()
        #ho