from flask import render_template, redirect, url_for, request, flash, session
from app import app
from datetime import datetime
from app.modelos.models import Motos, MotoFotos, Comentarios, Usuario, db

# Ruta para los comentarios
@app.route('/add_comentario/<int:moto_id>', methods=['POST'])
def add_comentario(moto_id):
    # Verificar si el usuario está autenticado
    if 'user_id' not in session:
        flash('Debes iniciar sesión para comentar.', 'warning')
        return redirect(url_for('login'))

    comentario = request.form.get('comentario')
    if not comentario:
        flash('El comentario no puede estar vacío.', 'error')
        return redirect(url_for('info_motos', moto_id=moto_id))

    # Obtener el ID del usuario desde la sesión
    user_id = session['user_id']

    # Crear y guardar el nuevo comentario
    nuevo_comentario = Comentarios(comentario=comentario, idUsuario=user_id, idMotos=moto_id)
    db.session.add(nuevo_comentario)
    db.session.commit()

    flash('Comentario agregado exitosamente!', 'success')
    return redirect(url_for('ver_comentarios', moto_id=moto_id))

#ruta para ver y poder agregar nuevos comentarios y ver las caracteristicas de cada moto
@app.route('/ver_comentarios/<int:moto_id>', methods=['GET'])
def ver_comentarios(moto_id):
    if 'user_id' not in session:
        flash('Debes iniciar sesión para ver y agregar comentarios.', 'warning')
        return redirect(url_for('login')) 

    # Obtener la moto
    moto = Motos.query.get_or_404(moto_id)
    
    # Obtener las fotos de la moto
    fotos = MotoFotos.query.filter_by(moto_id=moto.id).all()
    
    # Obtener los comentarios asociados a la moto
    comentarios = Comentarios.query.filter_by(idMotos=moto_id).all()
    
    # Obtener el usuario que registró la moto (vendedor)
    vendedor = Usuario.query.get_or_404(moto.usuario_id)

    return render_template('admin/info_motos.html', moto=moto, fotos=fotos, comentarios=comentarios, 
                           vendedor=vendedor, datetime=datetime)
