import mysql.connector
from utils.mailer import verificacion

from repositories.usuarios_repo import (
    get_user,
    verificar_usuario,
    crear_usuario,
    editar_usuario,
    listar_usuarios,
    borrar_usuario
)

# crear usuario
def crear_usuario_service(data):

    if not data.get("email") or not data.get("username") or not data.get("password"):
        raise ValueError("email, name y password son obligatorios")

    if len(data["password"]) < 6:
        raise ValueError("La contraseña debe tener mínimo 6 caracteres")


    try:
        new_id,  verify_token = crear_usuario(data)
        verificacion(data["email"], verify_token)
        return {"id": new_id, "message": "Si el correo existe, se habra mandado una verificacion a este."}
    
    except Exception as e:
        raise ValueError(f"No se pudo enviar el correo: {e}")
    
    except mysql.connector.IntegrityError as e:
        if "email" in str(e).lower():
            raise ValueError("Ese email ya está registrado")
        elif "username" in str(e).lower():
            raise ValueError("Ese username ya existe")
        else:
            raise ValueError("Error en la base de datos")

    except Exception as e:
        raise ValueError("Error interno inesperado al crear usuario")

#verificar usuario
def verificar_token_service(token):
    user = get_user(token)
    if not user:
        raise ValueError("Token inválido o cuenta ya activada")
    
    activated = verificar_usuario(token)
    if not activated:
        raise ValueError("No se pudo activar el usuario")

    return user

# editar usuario
def editar_usuario_service(id, data):

    if not data:
        raise ValueError("No hay datos para actualizar")

    if "username" in data and data["username"].strip() == "":
        raise ValueError("Por favor pone un nombre de usuario")

    if "full_name" in data and data["full_name"].strip() == "":
        raise ValueError("Por favor pone un nombre completo")

    updated = editar_usuario(id, data)

    if not updated:
        raise ValueError("Nada para actualizar")

    return True


# listar usuarios + búsqueda opcional
def listar_usuarios_service(busqueda=None):
    return listar_usuarios(busqueda)


# borrar usuario
def borrar_usuario_service(id):
    return borrar_usuario(id)