from flask import request, jsonify
from functools import wraps

from server import server

import jwt

#-----------------------------------------#
#       AUTENTICAÇÃO JSON WEB TOKEN       #
#-----------------------------------------#
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({'error': 'Token is missing!'}), 403

        try:
            data = jwt.decode(token, server.config['JWT'])
        except:
            return jsonify({'error': 'Token is invalid!'}), 403

        return f(*args, *kwargs)
    
    return decorated