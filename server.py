from flask import Flask, request, jsonify
import random

app = Flask(__name__)

rooms = {}

def generate_code():
    return str(random.randint(10000, 99999))

@app.route("/host", methods=["POST"])
def host():
    code = generate_code()
    rooms[code] = {"players": []}
    return jsonify({"code": code})

@app.route("/join", methods=["POST"])
def join():
    data = request.json
    code = data["code"]
    name = data["name"]

    if code not in rooms:
        return jsonify({"error": "Invalid code"}), 400

    rooms[code]["players"].append(name)
    return jsonify({"success": True})

@app.route("/lobby/<code>", methods=["GET"])
def lobby(code):
    if code not in rooms:
        return jsonify({"error": "Invalid code"}), 400

    return jsonify({"players": rooms[code]["players"]})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)