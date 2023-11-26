from flask import Blueprint, request, jsonify, redirect, url_for


from kluster import jwt
from kluster.helpers import convert_pic_to_link, query_one_filtered
from kluster.models.profiles import Profiles
from kluster.models.roles import Roles
from kluster.models.users import Users

profile_bp = Blueprint("profile", __name__, url_prefix="/api/v1/profile")


@profile_bp.route("/", methods=["GET"])
def test():
    return "profile", 200
    

def standard_response(message, status_code):
    return jsonify({'message': message}), status_code

def update_profile_fields(profile, data):
    fields_to_update = ['first_name', 'last_name', 'date_of_birth', 'gender', 'address', 
                        'blood_group', 'allergies', 'age']
    for field in fields_to_update:
        if field in data:
            setattr(profile, field, data[field])

    if 'display_picture' in request.files:
        profile.display_picture = convert_pic_to_link(request.files['display_picture'])

@profile_bp.route("/<string:email>", methods=["GET","PUT","DELETE"])
def profile(email:str) -> None:
    try:

        data = request.form
        user = query_one_filtered(Users, email=email)

        if not user:
            return "User not found", 404
        
        profile = query_one_filtered(Profiles, user_id=user.id)

        if request.method == "GET":

                if profile:
                    return jsonify(profile.format()), 200
                else:
                    return standard_response("profile not found", 404)
            
        if request.method == "PUT":
                #update profile
                if profile:
                    update_profile_fields(profile, data)
                    profile.update()
                    return (
                        jsonify(
                            {
                                "Message": "Profile updated successfully",
                                "data":profile.format(),
                        }), 200)
                else:
                    return standard_response("profile not found", 404)
                
        if request.method == "DELETE":
                if profile:
                    profile.delete()
                    return standard_response("profile deleted successfully", 204)
                else:
                    return standard_response("profile not found", 404)
    except Exception as e:
        return standard_response(f"An error occured :{str(e)}", 500)