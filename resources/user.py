from flask_restful import Resource
from flask_jwt_extended import jwt_required
from file_sharing.utils import get_current_user

class UserResource(Resource):
    @jwt_required()
    def get(self):
        user = get_current_user()
        if not user:
            return {'message': 'User not found'}, 404

        return {'username': user.username, 'email': user.email, 'is_ops_user': user.is_ops_user}, 200
