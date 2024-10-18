from flask import render_template, request, redirect, url_for, flash, session
from app import app
from app.modelos.models import Motos, Usuario, db
import cloudinary.uploader
import os


@app.route('/motos')
def motos():
    # Obtener el ID del usuario actual desde la sesión
    user_id = session.get('user_id')
    if user_id is None:
        flash('No estás autenticado. Por favor, inicia sesión.')
        return redirect(url_for('login'))

    # Filtrar motos por el ID del usuario
    motos = Motos.query.filter_by(usuario_id=user_id).all()
    return render_template('admin/listar_motos.html', motos=motos)

#ruta para el registro segun la secion 
@app.route('/add_moto', methods=['GET', 'POST'])
def add_moto():
    # Verificar si la sesión es válida
    if 'user_id' not in session:
        flash('Debes iniciar sesión para registrar.', 'warning')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        cantidad = request.form.get('cantidad')
        precio = request.form.get('precio')
        foto = None
        descripcion = request.form.get('descripcion') 
        marca = request.form.get('marca') 
        cilindrada =request.form.get('cilindrada')
        usuario_id = session['user_id']
        
        if 'foto' in request.files:
            foto_file = request.files['foto']
            if foto_file.filename != '':
                # Subir la imagen a Cloudinary
                upload_result = cloudinary.uploader.upload(foto_file)
                # Guardar la URL de la imagen subida
                foto = upload_result['secure_url']
            
        # Crear la nueva moto
        nueva_moto = Motos(nombre=nombre, cantidad=int(cantidad), precio=int(precio), 
                           foto=foto, descripcion=descripcion, marca=marca,
                           cilindrada=int(cilindrada), usuario_id=usuario_id)
        db.session.add(nueva_moto)
        db.session.commit()
        flash('Moto agregada exitosamente.')
        return redirect(url_for('motos'))

    
    return render_template('admin/registrar_moto.html')

# Ruta para editar los campos
@app.route('/edit_motos/edit/<int:id>', methods=['GET', 'POST'])
def edit_moto(id):
    motos = Motos.query.get(id)
    
    if not motos:
        flash('Moto no encontrada.')
        return redirect(url_for('motos'))
    
    # Verificar si el usuario actual es el dueño de la moto
    if motos.usuario_id != session.get('user_id'):
        flash('No tienes permiso para editar esta moto.', 'danger')
        return redirect(url_for('motos'))

    if request.method == 'POST':
        motos.nombre = request.form.get('nombre')
        motos.cantidad = request.form.get('cantidad')
        motos.precio = request.form.get('precio')
        motos.descripcion = request.form.get('descripcion')
        motos.marca = request.form.get('marca')
        motos.cilindrada = request.form.get('cilindrada')
        
        if not motos.nombre or not motos.cantidad or not motos.precio or not motos.descripcion or not motos.marca or not motos.cilindrada:
            flash('Todos los campos son requeridos.')
            return redirect(url_for('edit_moto', id=id))
        
        # Manejar la carga de la foto
        if 'foto' in request.files:
            foto_file = request.files['foto']
            if foto_file.filename != '':                
                # Subir la nueva imagen a Cloudinary
                upload_result = cloudinary.uploader.upload(foto_file)
                # Guardar la nueva URL de la imagen en la base de datos
                foto = upload_result['secure_url']
                motos.foto = foto  # Actualizar el campo foto en la base de datos

        db.session.commit()
        flash('Moto actualizada exitosamente.')
        return redirect(url_for('motos'))

    
    
    return render_template('admin/editar_moto.html', motos=motos)

# Eliminar un registro
@app.route('/delete_moto/delete/<int:id>', methods=['GET', 'POST'])
def delete_moto(id):
    # Obtener la moto a eliminar
    motos = Motos.query.get(id)
    # Verificar si la moto existe
    if not motos:
        flash('Moto no encontrada.', 'danger')
        return redirect(url_for('motos'))
    # Verificar si el usuario de la sesión es el que registró la moto
    if motos.usuario_id != session.get('user_id'):
        flash('No tienes permiso para eliminar esta moto.', 'danger')
        return redirect(url_for('motos'))
    # Eliminar lawoto si la verificación fue exitosa
    db.session.delete(motos)
    db.session.commit()
    flash('Moto eliminada correctamente.', 'success')
    
    return redirect(url_for('motos'))

#rutas para el catalogo
@app.route('/catalogo')
def catalogo():
    moto = Motos.query.all()
    return render_template('admin/catalogo.html', moto=moto)