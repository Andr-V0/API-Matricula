import firebase_admin
from firebase_admin import credentials, auth
from pathlib import Path

# Construir la ruta al fichero de credenciales de forma dinámica
# 1. Obtener la ruta del fichero actual (firebase.py)
# 2. Navegar al directorio padre (utils/)
# 3. Navegar al directorio padre superior (Proyecto2/)
# 4. Unir con la ruta a 'secrests/secrests.json'
cred_path = Path(__file__).parent.parent / "secrests" / "secrests.json"

cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)

def create_firebase_user(email, password):
    return auth.create_user(email=email, password=password)

def get_firebase_user_by_email(email):
    return auth.get_user_by_email(email)
