from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    clave = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(10), nullable=False, default='cliente')  # 'admin' o 'cliente'
    telefono = db.Column(db.BigInteger)
    foto = db.Column(db.String(200), default='static/uploads/perfil.jpg')
    calificacion_promedio = db.Column(db.Float, default=0.0)  # Calificación promedio
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)  # Tiempo en la plataforma

    motos = db.relationship('Motos', backref=db.backref('usuario', lazy=True))

    # Relación con las valoraciones recibidas como vendedor
    valoraciones_vendedor = db.relationship('Valoraciones', foreign_keys='Valoraciones.vendedor_id', backref='vendedor', lazy=True)

    def set_password(self, password):
        self.clave = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.clave, password)
    
class Valoraciones(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vendedor_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    comprador_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    calificacion = db.Column(db.Integer, nullable=False)  # Valor entre 1 y 5 estrellas
    # Relación con el comprador (usuario que deja la valoración)
    comprador = db.relationship('Usuario', foreign_keys=[comprador_id])

class Motos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(45))
    cantidad = db.Column(db.Integer)
    precio = db.Column(db.Integer)
    foto = db.Column(db.String(200))
    descripcion = db.Column(db.Text)

    # Nuevos campos agregados
    marca = db.Column(db.String(45))        # Campo para la marca de la moto
    cilindrada = db.Column(db.Integer)      # Campo para la cilindrada de la moto

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

class Comentarios(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comentario = db.Column(db.Text, nullable=False)
    idUsuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    idMotos = db.Column(db.Integer, db.ForeignKey('motos.id'), nullable=False)

    usuario = db.relationship('Usuario', backref=db.backref('comentario', lazy=True))
    motos = db.relationship('Motos', backref=db.backref('comentario', lazy=True))
