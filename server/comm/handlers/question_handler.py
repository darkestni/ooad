# 现在只能传一张图片，且不能解析图片

import time
from flask import jsonify
from server.comm.db import db_insert
from server.comm.handlers.tools import verify_token
from server.comm.rag_service import assistant
from datetime import datetime, timezone

def handle_question(data):

    token = data["token"]
    check, username = verify_token(token)
    if check is not True:
        return username

    timestamp = data["timestamp"]
    timestamp = datetime.fromtimestamp(timestamp, tz=timezone.utc)
    payload = data["payload"]
    session_id = data["session_id"]
    print("blueblue")
    # ========== 1. 写入用户历史记录 ==========
    db_insert("history", {
        "username": username,
        "timestamp": timestamp,
        "payload": payload,
        "role": "user",
        "session_id":session_id
    })

    # 提取文本 & 图片
    user_text = ""
    user_image = None
    for item in payload:
        if "text" in item:
            user_text += item["text"]
        if "image" in item:
            user_image = item["image"]

    # ========== 2. 调用 RAG Assistant ==========
    rag_result = assistant.handle_user_query(
        user_id=username,
        query=user_text,
        image_paths=user_image
    )

    final_answer = rag_result["final_answer"]
    print(final_answer)
    answer_timestamp = datetime.fromtimestamp(time.time(), tz=timezone.utc)


    # ========== 3. 写入 LLM 回复历史 ==========
    db_insert("history", {
        "username": username,
        "timestamp": answer_timestamp,
        "payload": [{"text": final_answer}],
        "role": "LLM",
        "session_id":session_id
    })

    # ========== 4. 返回客户端 response ==========
    return jsonify({
        "type": "response",
        "timestamp": answer_timestamp,
        "answer": final_answer,
        "session_id":session_id
    }), 200
