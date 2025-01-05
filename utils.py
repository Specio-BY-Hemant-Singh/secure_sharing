from .config import Config
from flask import request, url_for
from werkzeug.utils import secure_filename
from .models import User
import os

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def generate_secure_url(file_id, token):
    return url_for('secure_download_resource', file_id=file_id, token=token, _external=True)

def get_current_user():
    from flask_jwt_extended import get_jwt_identity
    user_id = get_jwt_identity()
    return User.query.get(user_id)
