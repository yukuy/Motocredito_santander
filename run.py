import os  
from app import app, db

# Crear tablas en la base de datos al iniciar la aplicación
with app.app_context():
    db.create_all()  # Crea las tablas al iniciar la aplicación
    print("Tablas creadas con éxito.")

if __name__ == "__main__":
    app.run(debug=True)

