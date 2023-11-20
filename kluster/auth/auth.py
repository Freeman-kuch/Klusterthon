from flask import Blueprint, request, jsonify

auth = Blueprint("authentication", __name__, url_prefix="/api/v1/auth")


@auth.route('/sign_up', methods=['POST'])
def sign_up():
    """view function responsible for registering new user"""
    data = request.form
    first_name = data.get('first_name', None)
    last_name = data.get('last_name', None)
    email = data.get('email', None)
    password = data.get('password', None)
    gender = data.get('gender', None)
    date_of_birth = data.get('date_of_birth', None)

    try:
        assert first_name is not None
        assert last_name is not None
        assert email is not None
        assert password is not None
        assert gender is not None
        assert date_of_birth is not None
    except AssertionError:
        return jsonify({
            "message": "Bad Request",
            "error": "Missing Field"
        }), 400
