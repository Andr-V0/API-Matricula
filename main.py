from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from routes import auth, tipos_usuario, pac, asignatura, matricula, pipelines, user
from utils.db import db
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "*" 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_db_client():
    # Verifica y crea el tipo de usuario "EST"
    if not db.tipos_usuarios.find_one({"codigo": "EST"}):
        db.tipos_usuarios.insert_one({"codigo": "EST", "nombre": "Estudiante"})
        print("Tipo de usuario 'EST' creado.")

    # Verifica y crea el tipo de usuario "PROF"
    if not db.tipos_usuarios.find_one({"codigo": "PROF"}):
        db.tipos_usuarios.insert_one({"codigo": "PROF", "nombre": "Profesor"})
        print("Tipo de usuario 'PROF' creado.")

    # Verifica y crea el tipo de usuario "ADM"
    if not db.tipos_usuarios.find_one({"codigo": "ADM"}):
        db.tipos_usuarios.insert_one({"codigo": "ADM", "nombre": "Administrador"})
        print("Tipo de usuario 'ADM' creado.")

@app.on_event("shutdown")
def shutdown_db_client():
    pass



app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(tipos_usuario.router, prefix="/api", tags=["tipos_usuario"])
app.include_router(pac.router, prefix="/api", tags=["pac"])
app.include_router(asignatura.router, prefix="/api", tags=["asignatura"])
app.include_router(matricula.router, prefix="/api", tags=["matricula"])
app.include_router(pipelines.router, prefix="/api", tags=["pipelines"])
app.include_router(user.router, prefix="/api", tags=["user"])
