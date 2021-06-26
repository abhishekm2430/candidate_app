import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
from candidate_analysis.models import User

blueprint = Blueprint('sessions_controller', __name__, url_prefix='/api/v1')

@blueprint.route('/login', methods=['GET','POST'])
def login():
    # if request.method=='POST':
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    user = User.query.filter_by(username=username).first()
    print(user,"..........")
    if user == None:
        return jsonify({ "status": 404, "error_code": "UserNotFound", "message": "Invalid username", "data": {}}), 404
    elif not user.is_authorized(password):
        return jsonify({ "status": 401, "error_code": "Unauthorized", "message": "Invalid username or password", "data": {}}), 401

    ret = {"status": 200, "error_code": "", "message": "Logged in successfully", "data": { "access_token":create_access_token(identity = username) }}
    return jsonify(ret), 200
    # return render_template('login.html')

@blueprint.route('/', methods=['GET'])
def welcome():
    return jsonify({ "message": "Welcome to candidate analysis" }), 200

@blueprint.route('/protected', methods=['GET'])
@jwt_required
def protected():
    current_user = get_jwt_identity()
    return jsonify({'status':200,'Logged in as':current_user}), 200
