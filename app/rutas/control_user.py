from flask import render_template, request, redirect, url_for, flash, session
from app import app
from app.modelos.models import Usuario, db
from datetime import datetime
import cloudinary.uploader
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        password = request.form['password']
        telefono = request.form['telefono']
        foto = None
        
         # Agregar foto
        if 'foto' in request.files:
            foto_file = request.files['foto']
            if foto_file.filename != '':
                # Subir la imagen a Cloudinary
                upload_result = cloudinary.uploader.upload(foto_file)
                # Guardar la URL de la imagen subida
                foto = upload_result['secure_url']
            else:
                # Si no se selecciona ninguna imagen, usa la imagen predeterminada
                foto = 'static/uploads/perfil.jpg'
        else:
            foto = 'static/uploads/perfil.jpg'

        # Verificar si es el primer usuario en registrarse
        if Usuario.query.count() == 0:
            role = 'admin'
        else:
            role = 'cliente'
            
        nuevo_usuario = Usuario(nombre=nombre, correo=correo, role=role, telefono=telefono, foto=foto)
        nuevo_usuario.set_password(password)
        db.session.add(nuevo_usuario)
        db.session.commit()
        flash('Registro exitoso. Puedes iniciar sesión ahora.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

#login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        password = request.form['password']
        usuario = Usuario.query.filter_by(correo=correo).first()

        if usuario and usuario.check_password(password):
            session['user_id'] = usuario.id
            session['user_nombre'] = usuario.nombre
            session['user_role'] = usuario.role
            session.permanent = True  # Marca la sesión como permanente

            if usuario.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('cliente_dashboard'))
        else:
            flash('Correo o contraseña incorrecta', 'danger')

    return render_template('login.html')

#serrar sesión
@app.route('/logout')
def logout():
    session.clear()  # Elimina toda la información de la sesión
    flash('Sesión cerrada correctamente', 'success')
    return redirect(url_for('login'))

#control de usuarios 
@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user_role' not in session or session['user_role'] != 'admin':
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('login'))
    
    if 'user_id' not in session:
        flash('Por favor, inicia sesión primero', 'warning')
        return redirect(url_for('login'))
    
    return render_template('admin/admin_dashboard.html', user=session['user_nombre'])

@app.route('/cliente_dashboard')
def cliente_dashboard():
    if 'user_role' not in session or session['user_role'] != 'cliente':
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('login'))
    
    if 'user_id' not in session:
        flash('Por favor, inicia sesión primero', 'warning')
        return redirect(url_for('login'))
    
    return render_template('cliente/cliente_dashboard.html', user=session['user_nombre'])
