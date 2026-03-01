import time
from flask import jsonify
from server.comm.db import db_select, db_insert, db_delete

def verify_token(token):
    rows = db_select("token", "token", token,"TTL")
    if not rows:
        print("用户不存在！")
        return False, (jsonify({"type": "error","msg":"用户不存在"}), 201)

    row = rows[0]
    username = row["username"]

    if row["ttl"] < time.time():
        print("会话过期！")
        return False, (jsonify({"type": "error","msg":"会话已过期"}), 201)

    db_delete("token", "token", token)
    db_insert("token", {"token": token, "TTL": time.time() + 900, "username": username})

    return True, username
