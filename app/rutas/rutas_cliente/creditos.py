from flask import render_template, request, redirect, url_for, flash, session
from app import app

@app.route('/creditos1', methods=['GET'])
def creditos1():
    # Función del endpoint
    return render_template('cliente/creditos1.html')
