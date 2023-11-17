# Importar las Librerias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import streamlit as st
from tinydb import TinyDB, Query

# Nombres de archivos para la base de datos
usuarios_filename = TinyDB('usuarios.json')
partidos_filename = TinyDB('partidos.json')
jugadores_filename = TinyDB('jugadores.json')
equipos_filename = TinyDB('equipos.json')

# Inicializar la variable de sesión para el nombre de usuario
if 'username' not in st.session_state:
    st.session_state.username = None

def get_current_user():
    '''Obtiene el nombre de usuario actual después del inicio de sesión'''
    return st.session_state.username


def get_user_data(username):
    '''Función para cargar o crear un archivo CSV para el usuario actual
    '''
    user_data_filename = f"{username}_data.csv"
    if not os.path.exists(user_data_filename):
        # Si el archivo no existe, crea un DataFrame vacío
        return pd.DataFrame({'Fecha': [], 'Tipo': [], 'Categoría': [], 'Monto': []})
    else:
        # Si el archivo existe, carga los datos desde el archivo CSV
        return pd.read_csv(user_data_filename)


def registrar_usuario(username, password, first_name, last_name, email, confirm_password):
    '''Esta función usa la librería TinyDB para registrar un usuario en un archivo
    llamado usuarios_filename
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


def verificar_credenciales(username, password):
    '''Esta función recibe como argumento el username y el password y verifica que sean iguales para 
    permitir el ingreso al sistema
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
    username = get_current_user()
    partidos_user = partidos_filename.search(User.username == username)
    jugadores_user = jugadores_filename.search(User.username == username)
    equipos_user = equipos_filename.search(User.username == username)

    # Botones para registrar gasto, ingreso o ver registros
    st.title("DeporteStats Pro")

    # Opción de registro en la barra inferior
    st.sidebar.subheader("Registro")
    registro_opciones = ["Partido", "Jugador","Equipo"]
    registro_opcion = st.sidebar.selectbox("Seleccione una opción:", registro_opciones)

    #Registro de partido
    if registro_opcion == "Partido":
        st.subheader("Registro de Partido")
        fecha = st.date_input("Fecha del Partido")
        # Obtener los nombres de los equipos desde el DataFrame equipos_filename
        nombres_equipos = pd.DataFrame(equipos_filename.search(User.Usuario == username))

        try:
            #Boxes para ingresar informacion
            equipo_local = st.selectbox("Equipo Local", nombres_equipos['Equipo'])
            equipo_visitante = st.selectbox("Equipo Visitante", nombres_equipos["Equipo"])
            goles_local = st.number_input("Goles del Equipo Local", step=1)
            goles_visitante = st.number_input("Goles del Equipo Visitante", step=1)

            #Titulo de la seccion
            st.write("Datos de Partidos:")
            # Convierte los datos en un DataFrame de pandas
            df = pd.DataFrame(partidos_filename.search(User.Usuario == username))

            # Muestra el DataFrame en forma de tabla
            st.write(df)

            st.write("Gráfico de Goles por Partido:")
            goles = np.sum(df[['Goles Local', 'Goles Visitante']], axis=0)
            equipos = nombres_equipos["Equipo"]

            # Crear el gráfico de barras
            fig, ax = plt.subplots()
            ax.bar(equipos, goles)

            # Agregar etiquetas y título
            ax.set_xlabel('Equipos')
            ax.set_ylabel('Goles por Partido')
            ax.set_title('Goles por Partido de Cada Equipo')

            # Mostrar el gráfico en Streamlit
            st.pyplot(fig)
            
        except:
            
            st.warning('Aun no tienes equipos registrados')

        #Boton para registrar partido
        if st.button("Registrar Partido"):
            #Insertar partido al dataframe
            partidos_filename.insert({'Usuario': username ,'Fecha': str(fecha) , 'Equipo Local': str(equipo_local),
                                    'Equipo Visitante': str(equipo_visitante), 'Goles Local':goles_local , 
                                    'Goles Visitante':goles_visitante})
            #Mensaje de exito
            st.success("Partido registrado con éxito.")

    #Opcion de tegistro de Jugador
    elif registro_opcion == "Jugador":
        # Boxes para pedir informacion
        posicion_jugador = ['Arquero','Defensa','Mediocampista','Delantero']
        st.subheader("Registro de Jugador")
        nombre_jugador = st.text_input("Nombre del Jugador")
        posicion = st.selectbox('Posicion' , posicion_jugador )

        #Boton para registrar
        if st.button("Registrar Jugador"):
            jugadores_filename.insert({'Usuario':username,'Nombre del Jugador':str(nombre_jugador),
                                        'Posición':str(posicion)})
            st.success("Jugador registrado con éxito.")

        #Mustra los datos de los jugadores
        st.write("Datos de Jugadores:")
        jugadores = pd.DataFrame(jugadores_filename.search(User.Usuario == username))
        st.write(jugadores)

    #Opcion de Registro de Equipo
    elif registro_opcion == "Equipo":
        #Boxes para pedir informacion
        st.subheader("Registro de Equipo")
        nombre_equipo = st.text_input("Nombre del Equipo")
        ciudad = st.text_input("Ciudad del Equipo")
        
        #Boton para registrar equipos
        if st.button("Registrar Equipo"):
            try:
                equipos_filename.insert({'Usuario': username,'Equipo': nombre_equipo, 'Ciudad': ciudad})
                st.success("Equipo registrado con éxito.")
            except Exception as e:
                st.error(f"Error al registrar el equipo: {e}")

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
    
    # Seccion para registro de usuario
    elif menu_option == "Registro":
        st.write("Registro de Usuario")

        # Campos de registro
        first_name = st.text_input("Nombre del Usuario:")
        last_name = st.text_input("Apellidos del Usuario:")
        email = st.text_input("Correo electronico del Usuario:")
        new_username = st.text_input("Nuevo Nombre de Usuario:")
        new_password = st.text_input("Nueva Contraseña:", type = "password")
        confirm_password = st.text_input("Confirmar contraseña:", type = "password")

        # Crear dos columnas para los botones
        col1, col2 = st.columns(2)
        # Casilla de verificación para aceptar la política de datos personales
        # Inicializa la variable aceptar_politica
        
        # Variable de estado para rastrear si el usuario ha visto la política
        if 'politica_vista' not in st.session_state:
            st.session_state.politica_vista = False

        # Botón para abrir la ventana emergente en la segunda columna
        if col2.button("Ver Política de Tratamiento de Datos"):
            with open("politica_datos.txt", "r") as archivo:
                politica = archivo.read()
                with st.expander("Política de Tratamiento de Datos",expanded=True):
                    st.write(politica)
                    st.session_state.politica_vista = True
                # Casilla de verificación para aceptar la política
        aceptar_politica = st.checkbox("Acepta la política de datos personales")
        # Botón de registro de usuario en la primera columna
        if col1.button("Registrarse") and aceptar_politica and st.session_state.politica_vista:
            registration_successful, message = registrar_usuario(new_username, new_password, first_name, last_name, email, confirm_password)
            if registration_successful:
                st.success(message)
            else:
                st.error(message)

        if not aceptar_politica:
            st.warning("Por favor, acepta la política de datos personales antes de registrarte.")

        if not st.session_state.politica_vista:
            st.warning("Por favor, ve la política de datos personales antes de registrarte.")

