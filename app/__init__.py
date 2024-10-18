from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

# Inicializar la aplicación Flask
app = Flask(__name__)
app.config.from_object(config)



# Inicializar SQLAlche
db.init_app(app)

#configuracion de almacenamiento de cloudinary
config.init_cloudinary()
    
# Importar controladores y modelos
from app.rutas import control_user
from app.rutas.rutas_admin import contol_motos, comentarios, calificaciones, historial, creditos, usuario
from app.rutas.rutas_cliente import motos,  comentarios, calificaciones, creditos, historial

# Crear la base de datos y las tablas al ejecutar la aplicación
with app.app_context():
    db.create_all()  # Esto creará las tablas si aún no existen
    
    from app import db  # Importa db desde tu aplicación


