import streamlit as st
import pandas as pd
import numpy as np
import os

# Cargar el archivo CSV con los usuarios, partidos y jugadores si existen
usuarios_filename = 'usuarios.csv'
partidos_filename = 'partidos.csv'
jugadores_filename = 'jugadores.csv'
equipos_filename = 'equipos.csv'

if os.path.exists(partidos_filename):
    partidos_df = pd.read_csv(partidos_filename)
else:
    partidos_df = pd.DataFrame(columns=['Fecha', 'Equipo Local', 'Equipo Visitante', 'Goles Local', 'Goles Visitante'])

if os.path.exists(jugadores_filename):
    jugadores_df = pd.read_csv(jugadores_filename)
else:
    jugadores_df = pd.DataFrame(columns=['Nombre del Jugador', 'Posición'])

if os.path.exists(usuarios_filename ):
    usuarios_df = pd.read_csv(usuarios_filename )
else:
    usuarios_df = pd.DataFrame(columns=['Username','Password'])

if os.path.exists(equipos_filename ):
    equipos_df = pd.read_csv(equipos_filename )
else:
    equipos_df = pd.DataFrame(columns=['Equipo','Ciudad'])

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
    usuarios_df.to_csv('usuarios.csv', index=False)  # Guardar en el archivo CSV

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
st.title("Nuestra Liga")

# Menú desplegable en la barra lateral
menu_option = st.sidebar.selectbox("Menú", ["Inicio", "Registro", "Cerrar Sesión"])  

# Si el usuario elige "Cerrar Sesión", restablecer la variable de sesión a None
if menu_option == "Cerrar Sesión":
    st.session_state.username = None
    st.success("Sesión cerrada con éxito. Por favor, inicie sesión nuevamente.")

# Si el usuario ya ha iniciado sesión, mostrar los botones
if get_current_user() is not None:
    st.write(f"Bienvenido, {get_current_user()}!")

    # Obtener los datos del usuario actual
    user_data = get_user_data(get_current_user())

    # Botones para registrar gasto, ingreso o ver registros
    st.title("DeporteStats Pro")

    # Opción de registro en la barra inferior
    st.sidebar.subheader("Registro")
    registro_opciones = ["Partido", "Jugador","Equipo"]
    registro_opcion = st.sidebar.selectbox("Seleccione una opción:", registro_opciones)

    if registro_opcion == "Partido":
        st.subheader("Registro de Partido")
        fecha = st.date_input("Fecha del Partido")
        # Obtener los nombres de los equipos desde el DataFrame equipos_df
        equipos = list(equipos_df['Equipo'])
        equipo_local = st.selectbox("Equipo Local", equipos)
        equipo_visitante = st.selectbox("Equipo Visitante", equipos)
        goles_local = st.number_input("Goles del Equipo Local", step=1)
        goles_visitante = st.number_input("Goles del Equipo Visitante", step=1)

        if st.button("Registrar Partido"):
            partido = pd.DataFrame({'Fecha':[fecha], 'Equipo Local':[equipo_local], 'Equipo Visitante':[equipo_visitante], 'Goles Local':[goles_local ], 'Goles Visitante':[goles_visitante]})
            partidos_df = pd.concat([partidos_df,partido], ignore_index=True)
            # Guardar el DataFrame actualizado en el archivo CSV
            partidos_df.to_csv('partidos.csv', index=False)  # Guardar en el archivo CSV
            st.success("Partido registrado con éxito.")

        st.write("Datos de Partidos:")
        st.write(partidos_df)


        st.write("Gráfico de Goles por Partido:")
        if not partidos_df.empty:
            goles_por_partido = partidos_df.groupby("Fecha")[["Goles Local", "Goles Visitante"]].sum()
            st.line_chart(goles_por_partido)

    elif registro_opcion == "Jugador":
        st.subheader("Registro de Jugador")
        nombre_jugador = st.text_input("Nombre del Jugador")
        posicion = st.text_input("Posición del Jugador")

        if st.button("Registrar Jugador"):
            jugador = pd.DataFrame({'Nombre del Jugador':[nombre_jugador], 'Posición':[posicion]})
            jugadores_df = pd.concat([jugadores_df,jugador], ignore_index=True)
            # Guardar el DataFrame actualizado en el archivo CSV
            jugadores_df.to_csv('jugadores.csv', index=False)  # Guardar en el archivo CSV
            st.success("Partido registrado con éxito.")

        st.write("Datos de Jugadores:")
        st.write(jugadores_df)

        st.write("Gráfico de Posiciones de Jugadores:")
        if not jugadores_df.empty:
            posiciones = jugadores_df["Posición"].value_counts()
            st.bar_chart(posiciones)

        elif registro_opcion == "Equipo":
            st.subheader("Registro de Equipo")
            nombre_equipo = st.text_input("Nombre del Equipo")
            ciudad = st.text_input("Ciudad del Equipo")

            if st.button("Registrar Equipo"):
                equipo = pd.DataFrame({'Equipo': [nombre_equipo], 'Ciudad': [ciudad]})
                equipos_df = pd.concat([equipos_df, equipo], ignore_index=True)
                # Guardar el DataFrame actualizado en el archivo CSV
                equipos_df.to_csv('equipos.csv', index=False)  # Guardar en el archivo CSV
                st.success("Equipo registrado con éxito.")

    # Guardar los datos del usuario actual de vuelta al archivo CSV
    user_data.to_csv(f"{get_current_user()}_data.csv", index=False)

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
                st.session_state.username = username  # Almacenar el nombre de usuario en la sesión
                st.success(message)
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

