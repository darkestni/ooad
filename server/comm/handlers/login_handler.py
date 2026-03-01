import time

from flask import jsonify
from server.comm.db import db_select, db_insert, db_exists_multi, db_delete
import secrets

def generate_token(n_bytes: int = 32) -> str:
    return secrets.token_urlsafe(n_bytes)

def handle_login(data): #TODO
    username = data["username"]
    password = data["password"]
    if not db_exists_multi("users",{"username":username,"password":password}):
        return jsonify({"type": "error", "msg": "用户名或密码错误"}), 201

    token = generate_token()
    db_delete("token","username",username)
    db_insert("token", {"token": token, "TTL": time.time() + 900, "username": username})

    history = db_select("history","username",username)
    print("success")
    return jsonify({"type": "history", "token": token,"history":history}), 200