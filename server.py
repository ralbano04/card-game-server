from flask import Flask, request, jsonify
import random

app = Flask(__name__)

rooms = {}

# ---------------- CREATE FULL DECK ----------------
def create_deck():
    ranks = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
    suits = ["S","H","D","C"]
    return [r+s for r in ranks for s in suits]


# ---------------- HOST ----------------
@app.route("/host", methods=["POST"])
def host():
    code = str(random.randint(10000,99999))

    rooms[code] = {
        "players": [],
        "turn": 0,
        "deck": create_deck(),
        "cards": [],
        "third": None
    }

    random.shuffle(rooms[code]["deck"])

    return jsonify({"code": code})


# ---------------- JOIN ----------------
@app.route("/join", methods=["POST"])
def join():
    data = request.json
    code = data["code"]
    name = data["name"]

    if code in rooms:
        rooms[code]["players"].append(name)

    return jsonify({"ok": True})


# ---------------- START ----------------
@app.route("/start/<code>", methods=["POST"])
def start(code):
    room = rooms.get(code)

    if not room:
        return jsonify({"error": "Room not found"})

    room["turn"] = 0
    room["cards"] = []

    return jsonify({"ok": True})


# ---------------- DEAL ----------------
@app.route("/deal/<code>", methods=["POST"])
def deal(code):
    room = rooms.get(code)

    if not room:
        return jsonify({"error": "Room not found"})

    if len(room["deck"]) < 2:
        room["deck"] = create_deck()
        random.shuffle(room["deck"])

    # draw 2 cards
    room["cards"] = [room["deck"].pop(), room["deck"].pop()]

    return jsonify({"cards": room["cards"]})


# ---------------- BET ----------------
@app.route("/bet/<code>", methods=["POST"])
def bet(code):
    room = rooms.get(code)

    if not room:
        return jsonify({"error": "Room not found"})

    if len(room["deck"]) == 0:
        room["deck"] = create_deck()
        random.shuffle(room["deck"])

    # draw third card
    third = room["deck"].pop()
    room["third"] = third

    # move turn
    if room["players"]:
        room["turn"] = (room["turn"] + 1) % len(room["players"])

    return jsonify({"third": third})


# ---------------- PASS ----------------
@app.route("/pass/<code>", methods=["POST"])
def pass_turn(code):
    room = rooms.get(code)

    if not room:
        return jsonify({"error": "Room not found"})

    if room["players"]:
        room["turn"] = (room["turn"] + 1) % len(room["players"])

    return jsonify({"ok": True})


# ---------------- STATE ----------------
@app.route("/state/<code>")
def state(code):
    room = rooms.get(code)

    if not room:
        return jsonify({"error": "Room not found"})

    return jsonify({
        "players": room["players"],
        "turn": room["turn"],
        "cards": room["cards"],
        "third": room["third"]
    })


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)