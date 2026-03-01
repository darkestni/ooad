import time

from flask import jsonify
from server.comm.db import db_exists,db_insert
import secrets

def generate_token(n_bytes: int = 32) -> str:
    return secrets.token_urlsafe(n_bytes)

def handle_reg(data):

    username = data["username"]

    if db_exists("users","username",username):
        return jsonify({"type": "reg_done"}),201

    password = data["password"]
    db_insert("users",{"username":username,"password":password})
    token = generate_token()
    db_insert("token", {"token": token, "TTL": time.time() + 900,"username":username})
    return jsonify({"type": "reg_done","token":token}),200
