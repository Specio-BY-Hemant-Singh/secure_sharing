from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token
from flask_mail import Message
from flask import current_app
from file_sharing.models import User, db
from file_sharing.utils import allowed_file, generate_secure_url, get_current_user
import uuid

parser = reqparse.RequestParser()
parser.add_argument('username', type=str, required=True, help="Username cannot be blank!")
parser.add_argument('email', type=str, required=True, help="Email cannot be blank!")
parser.add_argument('password', type=str, required=True, help="Password cannot be blank!")

class SignUpResource(Resource):
    def post(self):
        args = parser.parse_args()
        username = args['username']
        email = args['email']
        password = args['password']

        if User.query.filter_by(username=username).first():
            return {'message': 'Username already exists'}, 400
        if User.query.filter_by(email=email).first():
            return {'message': 'Email already exists'}, 400

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        new_user.generate_verification_token()

        db.session.add(new_user)
        db.session.commit()

        # Send verification email
        msg = Message('Verify Your Email', sender=current_app.config['MAIL_USERNAME'], recipients=[email])
        msg.body = f"Please click the following link to verify your email: {generate_secure_url(new_user.verification_token)}"
        current_app.mail.send(msg)

        return {'message': 'User created successfully. Please check your email to verify.'}, 201

class VerifyEmailResource(Resource):
    def get(self, token):
        user = User.query.filter_by(verification_token=token).first()
        if not user:
            return {'message': 'Invalid token'}, 400

        user.email_verified = True
        user.verification_token = None
        db.session.commit()

        return {'message': 'Email verified successfully'}, 200

class LoginResource(Resource):
    def post(self):
        args = parser.parse_args()
        username = args['username']
        password = args['password']

        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            return {'message': 'Invalid username or password'}, 401

        if not user.email_verified:
            return {'message': 'Email not verified. Please verify your email first.'}, 400

        access_token = create_access_token(identity=user.id)
        return {'access_token': access_token}, 200
