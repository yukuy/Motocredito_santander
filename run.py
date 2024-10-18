import os  
from app import app, db

# Crear tablas en la base de datos al iniciar la aplicación
with app.app_context():
    db.create_all()  # Crea las tablas al iniciar la aplicación
    print("Tablas creadas con éxito.")

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))  # Obtener el puerto de la variable de entorno PORT
    app.run(host='0.0.0.0', port=port)  # Cambiar a '0.0.0.0' para permitir conexiones externas

