#import pandas as pd

# Crear DataFrames para almacenar datos de partidos y jugadores
'''partidos_df = pd.DataFrame(columns=["Fecha", "Equipo Local", "Equipo Visitante", "Goles Local", "Goles Visitante"])
jugadores_df = pd.DataFrame(columns=["Nombre", "Posición"])'''

# Crear un diccionario para almacenar usuarios y contraseñas (solo como ejemplo, no es seguro en producción)
usuarios = {}

# Iniciar sesión
def iniciar_sesion():
    print("Iniciar Sesión")
    usuario = input("Usuario: ")
    clave = input("Clave: ")

    if usuario in usuarios and usuarios[usuario] == clave:
        print("Inicio de sesión exitoso.")
        return True
    else:
        print("Usuario o clave incorrectos.")
        return False

# Registro de nuevos usuarios
def registrar_usuario():
    print("Registrarse")
    nuevo_usuario = input("Nuevo Usuario: ")
    nueva_clave = input("Nueva Clave: ")

    if nuevo_usuario in usuarios:
        print("El usuario ya existe. Elije otro nombre de usuario.")
    else:
        usuarios[nuevo_usuario] = nueva_clave
        print("Registro exitoso. Ahora puedes iniciar sesión.")

# Comprobar si el usuario ha iniciado sesión o desea registrarse
while True:
    opcion = input("¿Deseas iniciar sesión (I) o registrarte (R)? ").strip().lower()
    
    if opcion == "i":
        if iniciar_sesion():
            break
    elif opcion == "r":
        registrar_usuario()
    else:
        print("Opción no válida. Por favor, elige 'I' para iniciar sesión o 'R' para registrarte.")