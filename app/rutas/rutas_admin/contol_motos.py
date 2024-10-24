from flask import render_template, request, redirect, url_for, flash, session
from app import app
from app.modelos.models import Motos, MotoFotos, Usuario, db
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

    # Para cada moto, obtenemos su primera imagen
    for moto in motos:
        primera_foto = MotoFotos.query.filter_by(moto_id=moto.id).first()
        if primera_foto:  # Verificamos que no sea None
            moto.foto_principal = primera_foto.foto_url
        else:
            moto.foto_principal = 'ruta/a/imagen/predeterminada.jpg'  # Cambia esto a la ruta de una imagen predeterminada

    return render_template('admin/listar_motos.html', motos=motos)


#ruta para el registro segun la secion 
@app.route('/add_moto', methods=['GET', 'POST'])
def add_moto():
    if 'user_id' not in session:
        flash('Debes iniciar sesión para registrar.', 'warning')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        cantidad = request.form.get('cantidad')
        precio = request.form.get('precio')
        descripcion = request.form.get('descripcion') 
        marca = request.form.get('marca') 
        cilindrada = request.form.get('cilindrada')
        usuario_id = session['user_id']
        
        # Crear la nueva moto
        nueva_moto = Motos(nombre=nombre, cantidad=int(cantidad), precio=int(precio), 
                           descripcion=descripcion, marca=marca, cilindrada=int(cilindrada), usuario_id=usuario_id)
        db.session.add(nueva_moto)
        db.session.commit()

        # Guardar múltiples fotos
        if 'fotos' in request.files:
            fotos_files = request.files.getlist('fotos')  # Obtener lista de archivos
            for foto_file in fotos_files:
                if foto_file.filename != '':
                    # Subir la imagen a Cloudinary o donde lo estés almacenando
                    upload_result = cloudinary.uploader.upload(foto_file)
                    foto_url = upload_result['secure_url']
                    
                    # Guardar la URL de la imagen en la base de datos
                    nueva_foto = MotoFotos(moto_id=nueva_moto.id, foto_url=foto_url)
                    db.session.add(nueva_foto)
                    
            db.session.commit()
        
        flash('Moto agregada exitosamente.')
        return redirect(url_for('motos'))

    return render_template('admin/registrar_moto.html')


# Ruta para editar los campos# Ruta para editar los campos
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
        # Actualizar los campos de la moto
        motos.nombre = request.form.get('nombre')
        motos.cantidad = request.form.get('cantidad')
        motos.precio = request.form.get('precio')
        motos.descripcion = request.form.get('descripcion')
        motos.marca = request.form.get('marca')
        motos.cilindrada = request.form.get('cilindrada')
        
        # Validar que todos los campos requeridos estén llenos
        if not motos.nombre or not motos.cantidad or not motos.precio or not motos.descripcion or not motos.marca or not motos.cilindrada:
            flash('Todos los campos son requeridos.')
            return redirect(url_for('edit_moto', id=id))

        # Manejar la eliminación de fotos antiguas y la carga de nuevas fotos
        if 'fotos' in request.files:
            fotos_files = request.files.getlist('fotos')  # Obtener lista de archivos

            # Eliminar fotos anteriores si se están subiendo nuevas
            if fotos_files and any(foto_file.filename != '' for foto_file in fotos_files):
                # Obtener las fotos anteriores
                fotos_anteriores = MotoFotos.query.filter_by(moto_id=motos.id).all()

                # Eliminar cada foto del sistema y base de datos
                for foto in fotos_anteriores:
                    # Si estás usando Cloudinary o un servicio externo, aquí podrías eliminar la imagen del servicio:
                    # cloudinary.uploader.destroy(foto.cloudinary_id) (si guardas los IDs de Cloudinary)
                    
                    # Eliminar de la base de datos
                    db.session.delete(foto)
                
                # Subir nuevas imágenes
                for foto_file in fotos_files:
                    if foto_file.filename != '':
                        # Subir la nueva imagen
                        upload_result = cloudinary.uploader.upload(foto_file)
                        foto_url = upload_result['secure_url']
                        
                        # Guardar la nueva URL de la imagen en la base de datos
                        nueva_foto = MotoFotos(moto_id=motos.id, foto_url=foto_url)
                        db.session.add(nueva_foto)

        # Guardar cambios en la moto y en las fotos
        db.session.commit()
        flash('Moto actualizada exitosamente.')
        return redirect(url_for('motos'))

    return render_template('admin/editar_moto.html', motos=motos)


# Eliminar un registro
@app.route('/delete_moto/delete/<int:id>', methods=['GET', 'POST'])
def delete_moto(id):
    # Obtener la moto a eliminar
    moto = Motos.query.get(id)
    
    # Verificar si la moto existe
    if not moto:
        flash('Moto no encontrada.', 'danger')
        return redirect(url_for('motos'))
    
    # Verificar si el usuario de la sesión es el que registró la moto
    if moto.usuario_id != session.get('user_id'):
        flash('No tienes permiso para eliminar esta moto.', 'danger')
        return redirect(url_for('motos'))
    
    # Obtener las fotos de la moto
    fotos = MotoFotos.query.filter_by(moto_id=moto.id).all()
    
    # Eliminar las fotos relacionadas con la moto (Cloudinary URLs)
    for foto in fotos:
        # Eliminar la imagen de Cloudinary utilizando la API
        public_id = foto.foto_url.split('/')[-1].split('.')[0]  # Extraer el public_id de la URL
        try:
            cloudinary.uploader.destroy(public_id)  # Elimina la imagen de Cloudinary
        except Exception as e:
            print(f'Error al eliminar la imagen de Cloudinary: {e}')
        
        # Eliminar el registro de la base de datos
        db.session.delete(foto)
    
    # Eliminar la moto después de eliminar las fotos
    db.session.delete(moto)
    db.session.commit()
    
    flash('Moto e imágenes eliminadas correctamente.', 'success')
    
    return redirect(url_for('motos'))


#rutas para el catalogo
@app.route('/catalogo')
def catalogo():
    motos = Motos.query.all()
    
    # Obtener todas las fotos para cada moto
    for moto in motos:
        moto.fotos = MotoFotos.query.filter_by(moto_id=moto.id).all()

    return render_template('admin/catalogo.html', motos=motos)

