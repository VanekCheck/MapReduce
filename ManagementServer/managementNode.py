import math
import os
import shutil
import socket
import uuid
from functools import wraps

from flask import Flask, request, jsonify
import jwt

app = Flask(__name__)

urlAddresses = ['http://127.0.0.1:5001', 'http://127.0.0.1:5002', 'http://127.0.0.1:5003']


def auth_middleware(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            jwt.decode(token, 'future secret key', algorithms=["HS256"])

        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(*args, **kwargs)

    return decorated


if __name__ == '__main__':
    app.run(port=5009)
# python app.py --port 5001
