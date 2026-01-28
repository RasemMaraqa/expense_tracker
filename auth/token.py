# not used for now


from flask import Blueprint, request, jsonify
import jwt
from functools import wraps

SECRET_KEY = 'af08f872d18b4fd0bfbee70c5132b54f'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token =  request.args.get('token')
        if not token:
            return jsonify({'not verifed': 'Token is missing!'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'not verifed': 'Token is invalid!'}), 403    
    return decorated
