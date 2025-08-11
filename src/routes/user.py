from flask import Blueprint, jsonify

user_bp = Blueprint('user', __name__)

@user_bp.route('/ping', methods=['GET'])
def ping():
    return jsonify({"message": "User route is working!"})

