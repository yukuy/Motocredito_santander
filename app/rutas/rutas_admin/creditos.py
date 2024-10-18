from flask import render_template, request, redirect, url_for, flash, session
from app import app

@app.route('/creditos', methods=['GET'])
def creditos():
    # Función del endpoint
    return render_template('admin/creditos.html')
