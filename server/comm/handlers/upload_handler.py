import base64
import os

from flask import jsonify

from server.comm.handlers.tools import verify_token
from server.comm.rag_service import kb_manager

UPLOAD_DIR = "uploaded_pdfs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def handle_upload(data):
    print("111")
    token = data["token"]
    check, username = verify_token(token)
    if check is not True:
        return username

    textbook = data["textbook"]
    file_name = textbook["name"]
    file_id = textbook["file_id"]
    file_data = textbook["data"]

    # 解析扩展名，支持 pdf / docx / pptx
    _, ext = os.path.splitext(file_name)
    ext = ext.lower()

    if ext not in [".pdf", ".docx", ".pptx"]:
        return jsonify({
            "type": "error",
            "status": 400,
            "message": f"当前仅支持上传 PDF / Word(.docx) / PPTX 文件，收到类型：{ext}"
        }), 400

    # 文件实际保存路径：file_id + 原始扩展名
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}{ext}")
    with open(file_path, "wb") as f:
        f.write(base64.b64decode(file_data))

    # 这里把原始文件名也传进去，方便元数据记录
    chunks = kb_manager.upload_data(file_id, file_path, original_name=file_name)

    return jsonify({
        "type": "done",
        "status": 200,
        "chunks": len(chunks)
    }), 200
