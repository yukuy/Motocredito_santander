from flask import render_template, request, redirect, url_for, flash, session
from app import app
from app.modelos.models import Usuario, db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer
import cloudinary.uploader
import os

#logo del perfil
@app.route('/perfil/<int:user_id>')
def perfil_usuario(user_id):
    usuario = Usuario.query.get(user_id)
   
    return render_template('perfil.html', usuario=usuario, datetime=datetime)

# Ruta para editar perfil
@app.route('/editar_perfil/<int:user_id>', methods=['GET', 'POST'])
def editar_perfil(user_id):
    usuario = Usuario.query.get(user_id)
    
    if request.method == 'POST':
        usuario.nombre = request.form['nombre']
        usuario.correo = request.form['correo']
        usuario.telefono = request.form['telefono']
        foto = None
        
        nueva_clave = request.form['clave']
        if nueva_clave:
            usuario.clave = generate_password_hash(nueva_clave)

        # Manejar la carga de la foto
        if 'foto' in request.files:
            foto_file = request.files['foto']
            if foto_file.filename != '':                
                # Subir la nueva imagen a Cloudinary
                upload_result = cloudinary.uploader.upload(foto_file)
                # Guardar la nueva URL de la imagen en la base de datos
                foto = upload_result['secure_url']
                usuario.foto = foto  # Actualizar el campo foto en la base de datos

        # Guardar cambios en la base de datos
        db.session.commit()
        flash('Datos actualizados correctamente.', 'success')
        
        # Redirigir al perfil del usuario después de actualizar
        return redirect(url_for('perfil_usuario', user_id=user_id))  # Ajusta según tu ruta del perfil

    return render_template('editar_perfil.html', usuario=usuario)
        