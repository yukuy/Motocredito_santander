from flask import render_template, redirect, url_for, request, flash, session
from app import app
from datetime import datetime
from app.modelos.models import Valoraciones, Usuario, Motos, db

@app.route('/perfil_vendedor/<int:user_id>')
def perfil_vendedor(user_id):
    vendedor = Usuario.query.get_or_404(user_id)  # Obtener el vendedor por ID

    # Obtener la moto del vendedor
    moto = Motos.query.filter_by(usuario_id=user_id).first()  # Cambia esto según tu lógica de negocio

    moto_id = moto.id  # Ahora moto_id tiene un valor

    return render_template('perfil_vendedor.html', vendedor=vendedor, moto_id=moto_id, datetime=datetime)

# Ruta para la calificación del vendedor
@app.route('/agregar_calificacion/<int:vendedor_id>', methods=['POST'])
def agregar_calificacion(vendedor_id):
    # Obtener la calificación del formulario
    calificacion = request.form.get('calificacion')
    comprador_id = session.get('user_id')  # Obtener el ID del comprador desde la sesión

    if calificacion and comprador_id:
        # Crear una nueva instancia de calificación
        nueva_calificacion = Valoraciones(
            vendedor_id=vendedor_id, 
            comprador_id=comprador_id, 
            calificacion=float(calificacion)
        )

        # Guardar la nueva calificación en la base de datos
        db.session.add(nueva_calificacion)
        db.session.commit()

        # Actualizar la calificación promedio del vendedor
        actualizar_calificacion_promedio(vendedor_id)

        # Obtener el ID de la moto del vendedor para redirigir
        moto = Motos.query.filter_by(usuario_id=vendedor_id).first()
        if moto:
            # Si se encuentra la moto, redirigir a la página de comentarios
            return redirect(url_for('ver_comentarios', moto_id=moto.id))
        else:
            flash('No se encontró ninguna moto asociada al vendedor.', 'error')
            return redirect(url_for('perfil_vendedor', user_id=vendedor_id))
    else:
        flash('Error al enviar la calificación. Intenta nuevamente.', 'error')
        return redirect(url_for('perfil_vendedor', user_id=vendedor_id))

# Función para actualizar la calificación promedio del vendedor
def actualizar_calificacion_promedio(vendedor_id):
    vendedor = Usuario.query.get(vendedor_id)
    valoraciones = Valoraciones.query.filter_by(vendedor_id=vendedor_id).all()
    
    if valoraciones:
        # Calcular el promedio de las valoraciones
        promedio = sum(v.calificacion for v in valoraciones) / len(valoraciones)
        print(f"Nuevo promedio calculado: {promedio}")  # Verificar el promedio calculado

        vendedor.calificacion_promedio = promedio
        db.session.commit()

        # Verificar si el commit se realiza
        print(f"Calificación promedio actualizada en la base de datos: {vendedor.calificacion_promedio}")
    else:
        print("No se encontraron valoraciones para este vendedor")
