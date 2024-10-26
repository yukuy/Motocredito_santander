from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy


# Inicializar SQLAlchemy
db = SQLAlchemy()

# Crear la aplicación Flask
app = Flask(__name__)
app.config.from_object(config)

# Inicializar SQLAlchemy con la aplicación
db.init_app(app)

# Configuración de Cloudinary (si está implementado en config)
config.init_cloudinary()  # Asegúrate de que esta función esté en tu archivo de config

# Importar controladores y modelos
from app.rutas import control_user
from app.rutas.rutas_admin import contol_motos, comentarios as admin_comentarios, calificaciones as admin_calificaciones, historial as admin_historial, creditos as admin_creditos, usuario as admin_usuario
from app.rutas.rutas_cliente import motos, comentarios as cliente_comentarios, calificaciones as cliente_calificaciones, creditos as cliente_creditos, historial as cliente_historial

# Crear la base de datos y las tablas si no existen
with app.app_context():
    db.create_all()
