from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_uploads import UploadSet, configure_uploads, DOCUMENTS
from file_sharing.config import Config
from file_sharing.resources.auth import SignUpResource, VerifyEmailResource, LoginResource
from file_sharing.resources.user import UserResource
from file_sharing.resources.files import FileResource, DownloadFileResource, SecureDownloadResource
from file_sharing.models import db
import os

# Initialize the app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
jwt = JWTManager(app)
mail = Mail(app)

# Configure file uploads
documents = UploadSet('documents', DOCUMENTS)
app.config['UPLOADED_DOCUMENTS_DEST'] = app.config['UPLOAD_FOLDER']
configure_uploads(app, documents)

# Initialize API
api = Api(app)
api.add_resource(SignUpResource, '/signup')
api.add_resource(VerifyEmailResource, '/verify/<string:token>')
api.add_resource(LoginResource, '/login')
api.add_resource(UserResource, '/user')
api.add_resource(FileResource, '/files')
api.add_resource(DownloadFileResource, '/download-file/<int:file_id>')
api.add_resource(SecureDownloadResource, '/download/<int:file_id>/<string:token>')

# Database creation (Use migrations in production)
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
