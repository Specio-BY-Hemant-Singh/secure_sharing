from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask import request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from file_sharing.models import User, File, db
from file_sharing.utils import allowed_file, generate_secure_url, get_current_user
import os
import uuid

class FileResource(Resource):
    @jwt_required()
    def post(self):
        user = get_current_user()
        if not user.is_ops_user:
            return {'message': 'Only Ops users can upload files'}, 403

        if 'file' not in request.files:
            return {'message': 'No file part'}, 400

        file = request.files['file']
        if file.filename == '':
            return {'message': 'No selected file'}, 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            new_file = File(filename=filename, user_id=user.id)
            db.session.add(new_file)
            db.session.commit()
            return {'message': 'File successfully uploaded'}, 201

        return {'message': 'Invalid file type'}, 400

    @jwt_required()
    def get(self):
        user = get_current_user()
        if not user:
            return {'message': 'User not found'}, 404

        files = File.query.filter_by(user_id=user.id).all()
        file_list = [{'id': file.id, 'filename': file.filename} for file in files]
        return {'files': file_list}, 200


class DownloadFileResource(Resource):
    @jwt_required()
    def get(self, file_id):
        user = get_current_user()
        if not user:
            return {'message': 'User not found'}, 404

        file = File.query.get(file_id)
        if not file:
            return {'message': 'File not found'}, 404

        if file.user_id != user.id:
            return {'message': 'Access denied'}, 403

        download_token = str(uuid.uuid4())
        file.download_token = download_token
        db.session.commit()

        download_link = generate_secure_url(file_id, download_token)
        return {'download-link': download_link, 'message': 'success'}, 200


class SecureDownloadResource(Resource):
    def get(self, file_id, token):
        file = File.query.get(file_id)
        if not file:
            return {'message': 'File not found'}, 404

        if file.download_token != token:
            return {'message': 'Invalid download token'}, 403

        return send_from_directory(current_app.config['UPLOAD_FOLDER'], file.filename, as_attachment=True)
