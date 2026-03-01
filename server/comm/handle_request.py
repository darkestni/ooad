from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["POST"])
def handle_packet():
    data = request.get_json(force=True)

    if not data or "type" not in data:
        return jsonify({"error": "invalid packet"}), 400

    packet_type = data["type"]

    # 分发处理
    if packet_type == "upload":
        return handle_upload(data)
    elif packet_type == "delete":
        return handle_delete(data)
    elif packet_type == "login":
        return handle_login(data)
    else:
        return jsonify({"error": "unknown type"}), 400


def handle_upload(data):
    pass


def handle_delete(data):
    pass

def handle_login(data):
    pass

def handle_reg(data):
    pass

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8765)
