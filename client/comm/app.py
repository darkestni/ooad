# backend/app.py
import threading

from flask import Flask, request, jsonify
from flask_cors import CORS   # 允许前端 JS 调用
from regi_login import submit_auth
from upload import upload_file, delete as delete_textbook
from question import upload_question
from export import export_cli
app = Flask(__name__)
CORS(app)

@app.post("/api/auth")
def auth():
    data = request.get_json()
    res = submit_auth(
        data.get("username",""),
        data.get("password",""),
        data.get("confirm_password",""),
        data.get("type","")
    )
    return jsonify(res)

from flask import request

@app.post("/api/upload-textbook")
def upload_textbook():
    # 前端用 multipart/form-data 传：token + file
    token = request.form.get("token")
    file = request.files.get("file")

    if not token or not file:
        return jsonify({"success": False, "msg": "缺少 token 或 file"}), 400

    # 直接复用你写好的 upload_file：它就是“拿文件对象”的逻辑
    res = upload_file(token, file)
    return jsonify(res)

@app.post("/api/delete-textbook")
def delete_textbook_api():
    data = request.get_json()
    token = data.get("token")
    path = data.get("path")
    res = delete_textbook(token, path)
    return jsonify(res)

@app.post("/api/question")
def question_api():
    data = request.get_json()
    token = data.get("token")
    text = data.get("text")
    images = data.get("images", [])
    session_id = data.get("session_id",1)
    res = upload_question(token, text, images,session_id)
    return jsonify(res)

@app.post("/api/export")
def export_api():
    data = request.get_json()
    token = data.get("token")
    threading.Thread(target=export_cli, args=(token,), daemon=True).start()
    return jsonify({"status": "started"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9876, debug=True)
