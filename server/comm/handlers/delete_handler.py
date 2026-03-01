from flask import jsonify

from .tools import verify_token
from server.comm.db import db_delete


def handle_delete(data):

    token = data["token"]
    check,info = verify_token(token)
    # 2. 如果返回的不是 True，说明失败了，直接把错误 Response 返回给前端
    if check is not True:
        return info

    file_id = data["file_id"]
    db_delete("textbook","file_id",file_id)
    return jsonify({"type": "done"}),200

