from flask import render_template, request, session
from app import app
from app.modelos.models import Motos, Usuario, MotoFotos, db
import json
import os
from sqlalchemy.exc import SQLAlchemyError

def leer_historial(user_id):
    filepath = f'historial_{user_id}.json'
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []

def guardar_historial(user_id, query):
    filepath = f'historial_{user_id}.json'
    historial_busqueda = leer_historial(user_id)
    
    if query not in historial_busqueda:
        historial_busqueda.append(query)
        if len(historial_busqueda) > 10:
            historial_busqueda.pop(0)
        with open(filepath, 'w') as f:
            json.dump(historial_busqueda, f)

from sqlalchemy import cast, String

@app.route('/buscar_motos', methods=['GET'])
def buscar_motos():
    query = request.args.get('query')
    user_id = session.get('user_id')  # Obtén el ID del usuario de la sesión

    if query and user_id:
        # Realizar la búsqueda en la base de datos
        motos = Motos.query.filter(
            (Motos.nombre.ilike(f'%{query}%')) | 
            (Motos.marca.ilike(f'%{query}%')) |
            (cast(Motos.cilindrada, String).ilike(f'%{query}%'))  # Conversión a String sin advertencias
        ).all()

        # Obtener el historial de búsqueda desde el archivo específico del usuario
        historial_busqueda = leer_historial(user_id)

        # Agregar la nueva búsqueda al historial si no está ya presente
        if query not in historial_busqueda:
            historial_busqueda.append(query)
            # Limitar el tamaño del historial a 10 entradas
            if len(historial_busqueda) > 10:
                historial_busqueda.pop(0)
            guardar_historial(user_id, query)  # Asegúrate de pasar el user_id también al guardar

        # Obtener las fotos para cada moto
        fotos = {moto.id: MotoFotos.query.filter_by(moto_id=moto.id).all() for moto in motos}

    else:
        motos = []
        fotos = {}

    return render_template('admin/resultados.html', motos=motos, fotos=fotos, user_nombre=session.get('user_nombre'))


@app.route('/historial')
def historial():
    user_id = session.get('user_id')
    historial_busqueda = leer_historial(user_id) if user_id else []
    return render_template('admin/historial.html', historial_busqueda=historial_busqueda)