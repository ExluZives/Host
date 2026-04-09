from flask import Flask, request, jsonify
import time

app = Flask(__name__)

users = {}
last_command = {}

# 📡 регистрация игрока
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    users[str(data["userId"])] = {
        "name": data["name"],
        "jobId": data["jobId"],
        "placeId": data["placeId"],
        "time": time.time()
    }
    return jsonify({"status": "ok"})

# 📥 получить игроков
@app.route("/users", methods=["GET"])
def get_users():
    # чистим старых (оффлайн)
    now = time.time()
    active = {}

    for uid, data in users.items():
        if now - data["time"] < 15:
            active[uid] = data

    return jsonify(active)

# 📤 отправить команду
@app.route("/command", methods=["POST"])
def send_command():
    global last_command
    last_command = request.json
    return jsonify({"status": "sent"})

# 📥 получить команду
@app.route("/command", methods=["GET"])
def get_command():
    return jsonify(last_command)

app.run(host="0.0.0.0", port=3000)