import streamlit as st
import pandas as pd
import numpy as np
import os
from tinydb import TinyDB, Query

usuarios_filename = TinyDB('usuarios.json')
partidos_filename = TinyDB('partidos.json')
jugadores_filename = TinyDB('jugadores.json')
equipos_filename = TinyDB('equipos.json')

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
    

def csv(dataframe,user):
    data = dataframe[dataframe['Username'] == user]
    return data




# Función para registrar un nuevo usuario
def registrar_usuario(username, password, first_name, last_name, email, confirm_password):
    '''Esta funcion usa la libreria tinydb para registrar un usuario en un archivo llamado
    usuarios_filename
    '''
    User = Query()
    # Verifica si el usuario ya existe en la base de datos
    if usuarios_filename.search(User.username == username):
        return False, "El usuario ya existe. Por favor, elija otro nombre de usuario."

    # Verifica si las contraseñas coinciden
    if password != confirm_password:
        return False, "Las contraseñas no coinciden. Por favor, vuelva a intentar."

    # Agrega el nuevo usuario a la base de datos
    usuarios_filename.insert({'username': username, 'password': password, 'first_name': first_name, 'last_name': last_name, 'email': email})

    return True, "Registro exitoso. Ahora puede iniciar sesión."


# Función para verificar credenciales
def verificar_credenciales(username, password):
    '''Esta funcion recibe como argumento el username y el password y verifica que
    sean inguales para permitir el ingreso al sistema
    '''
    User = Query()
    # Busca el usuario en la base de datos
    user = usuarios_filename.get((User.username == username) & (User.password == password))
    if user:
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
    User = Query()
    # Obtener los datos del usuario actual
    username = get_current_user
    partidos_user = user_data = partidos_filename.search(User.username == username)
    jugadores_user = csv(jugadores_df, get_current_user())
    equipos_user = equipos_df[equipos_df['Username'] == get_current_user()]
    print(equipos_user)

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
        equipo_local = st.selectbox("Equipo Local", equipos_user["Equipo"])
        equipo_visitante = st.selectbox("Equipo Visitante", equipos_user["Equipo"])
        goles_local = st.number_input("Goles del Equipo Local", step=1)
        goles_visitante = st.number_input("Goles del Equipo Visitante", step=1)

        if st.button("Registrar Partido"):
            partido = pd.DataFrame({'Usuario':[user_data],'Fecha':[fecha], 'Equipo Local':[equipo_local], 'Equipo Visitante':[equipo_visitante], 'Goles Local':[goles_local ], 'Goles Visitante':[goles_visitante]})
            partidos_df = pd.concat([partidos_df,partido], ignore_index=True)
            # Guardar el DataFrame actualizado en el archivo CSV
            partidos_df.to_csv('partidos.csv', index=False)  # Guardar en el archivo CSV
            st.success("Partido registrado con éxito.")

        st.write("Datos de Partidos:")
        st.write(csv(partidos_df,get_current_user()))


        st.write("Gráfico de Goles por Partido:")
        if not csv(partidos_df,get_current_user()).empty:
            goles_por_partido = csv(partidos_df,get_current_user()).groupby("Fecha")[["Goles Local", "Goles Visitante"]].sum()
            st.line_chart(goles_por_partido)

    elif registro_opcion == "Jugador":
        st.subheader("Registro de Jugador")
        nombre_jugador = st.text_input("Nombre del Jugador")
        posicion = st.text_input("Posición del Jugador")

        if st.button("Registrar Jugador"):
            jugador = pd.DataFrame({'Usuario':[user_data],'Nombre del Jugador':[nombre_jugador], 'Posición':[posicion]})
            jugadores_df = pd.concat([jugadores_df,jugador], ignore_index=True)
            # Guardar el DataFrame actualizado en el archivo CSV
            jugadores_df.to_csv('jugadores.csv', index=False)  # Guardar en el archivo CSV
            st.success("Partido registrado con éxito.")

        st.write("Datos de Jugadores:")
        st.write(jugadores_user)

        st.write("Gráfico de Posiciones de Jugadores:")
        if not jugadores_user.empty:
            posiciones = jugadores_user["Posición"].value_counts()
            st.bar_chart(posiciones)

    elif registro_opcion == "Equipo":
        st.subheader("Registro de Equipo")
        nombre_equipo = st.text_input("Nombre del Equipo")
        ciudad = st.text_input("Ciudad del Equipo")

        if st.button("Registrar Equipo"):
            equipo = pd.DataFrame({'Usuario':[user_data],'Equipo': [nombre_equipo], 'Ciudad': [ciudad]})
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

