from flask import Flask, request, jsonify
import random

app = Flask(__name__)

rooms = {}

cards = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
values = {r:i for i,r in enumerate(cards, start=2)}

def draw_card():
    return random.choice(cards)

def generate_code():
    return str(random.randint(10000, 99999))

@app.route("/host", methods=["POST"])
def host():
    code = generate_code()
    rooms[code] = {
        "players": [],
        "turn": 0,
        "cards": [],
        "started": False
    }
    return jsonify({"code": code})

@app.route("/join", methods=["POST"])
def join():
    data = request.json
    code = data["code"]
    name = data["name"]

    if code in rooms:
        rooms[code]["players"].append(name)
        return jsonify({"status": "ok"})
    return jsonify({"status": "error"})

@app.route("/start/<code>", methods=["POST"])
def start(code):
    room = rooms[code]
    room["started"] = True
    room["cards"] = [draw_card(), draw_card()]
    return jsonify(room)

@app.route("/state/<code>")
def state(code):
    return jsonify(rooms[code])

@app.route("/deal/<code>", methods=["POST"])
def deal(code):
    room = rooms[code]
    room["cards"] = [draw_card(), draw_card()]
    return jsonify(room["cards"])

@app.route("/bet/<code>", methods=["POST"])
def bet(code):
    data = request.json
    room = rooms[code]

    third = draw_card()
    room["cards"].append(third)

    room["turn"] = (room["turn"] + 1) % len(room["players"])

    return jsonify({
        "third": third,
        "turn": room["turn"]
    })

@app.route("/pass/<code>", methods=["POST"])
def pass_turn(code):
    room = rooms[code]
    room["turn"] = (room["turn"] + 1) % len(room["players"])
    return jsonify({"turn": room["turn"]})

app.run(host="0.0.0.0", port=10000)