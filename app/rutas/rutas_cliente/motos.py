from flask import render_template, request, redirect, url_for, flash, session
from app import app
from app.modelos.models import Motos, Usuario, db
import cloudinary.uploader
import os


#rutas para el catalogo
@app.route('/catalogo1')
def catalogo1():
    moto = Motos.query.all()
    return render_template('cliente/catalogo1.html', moto=moto)