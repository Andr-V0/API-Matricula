from utils.db import db

def insert_user_type():
    try:
        # Verificar si el tipo de usuario ya existe
        if db.tipos_usuarios.find_one({"codigo": "EST"}):
            print("El tipo de usuario 'EST' ya existe en la base de datos.")
            return

        # Insertar el nuevo tipo de usuario
        db.tipos_usuarios.insert_one({
            "codigo": "EST",
            "nombre": "Estudiante" 
        })
        print("El tipo de usuario 'EST' ha sido insertado correctamente.")

    except Exception as e:
        print(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    insert_user_type()
