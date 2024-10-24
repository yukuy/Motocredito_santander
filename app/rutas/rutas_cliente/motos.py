from flask import render_template, request, redirect, url_for, flash, session
from app import app
from app.modelos.models import Motos, Usuario, MotoFotos, db
import cloudinary.uploader
import os


#rutas para el catalogo
@app.route('/catalogo1')
def catalogo1():
    motos = Motos.query.all()
    
    # Obtener todas las fotos para cada moto
    for moto in motos:
        moto.fotos = MotoFotos.query.filter_by(moto_id=moto.id).all()

    return render_template('cliente/catalogo1.html', motos=motos)