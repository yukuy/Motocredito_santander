import secrets
from datetime import timedelta
import cloudinary

class config:
    # Configura la base de datos PostgreSQL de Supabase
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres.cdrrwdbmcqkvrfjmcshn:E3TKDY2axEeZ3Nck@aws-0-us-west-1.pooler.supabase.com:6543/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'tu_clave_secreta_fija_aqui'  
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
# Configuración de Cloudinary
    CLOUD_NAME = 'dcg9njwmk'
    API_KEY = '173894522551611'
    API_SECRET = 'QpgpM1sFU6F7KDFFa47Jn-jvx5E'  # Asegúrate de que esta sea tu API Secret real

    @staticmethod
    def init_cloudinary():
        cloudinary.config(
            cloud_name=config.CLOUD_NAME,
            api_key=config.API_KEY,
            api_secret=config.API_SECRET
        )