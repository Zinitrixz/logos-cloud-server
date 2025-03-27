from flask import Flask, request, jsonify
from flask_cors import CORS
from db_utils import (
    init_db, create_user, get_user_state, update_user_state, save_insight, get_insights,
    draw_card, get_task, get_role_by_zone, get_ritual,
    store_zion, get_zion_manifest
)

app = Flask(__name__)
CORS(app)
init_db()

@app.route("/")
def index():
    return "🧬 Logos Cloud Server 2.0 is online."

# --- USER ---

@app.route("/initUser", methods=["POST"])
def init_user():
    data = request.json
    username = data.get("username")
    if username:
        create_user(username)
        return jsonify({"status": "created", "username": username})
    return jsonify({"status": "error", "message": "Missing username"}), 400

@app.route("/getUserState", methods=["GET"])
def get_user_state_route():
    username = request.args.get("username")
    if not username:
        return jsonify({"error": "Missing username"}), 400
    state = get_user_state(username)
    return jsonify(state)

@app.route("/switchMode", methods=["POST"])
def switch_mode():
    data = request.json
    username = data.get("username")
    mode = data.get("mode")
    role = data.get("role", "Guide")
    wincoin = data.get("wincoin", 0)
    update_user_state(username, mode, role, wincoin)
    return jsonify({"status": "mode updated", "mode": mode})

# --- INSIGHTS ---

@app.route("/saveInsight", methods=["POST"])
def save():
    data = request.json
    username = data.get("user")
    zone = data.get("zone")
    insight = data.get("insight")
    wincoin = data.get("wincoin", 0)
    save_insight(username, zone, insight, wincoin)
    return jsonify({"status": "success", "saved": data})

@app.route("/getProgress", methods=["GET"])
def get_progress():
    username = request.args.get("user")
    if not username:
        return jsonify({"error": "Missing user"}), 400
    insights = get_insights(username)
    return jsonify(insights)

# --- CARDS / TASKS / ROLES / RITUALS ---

@app.route("/drawCard", methods=["GET"])
def draw_card_route():
    category = request.args.get("category")
    zone = request.args.get("zone", None)
    if not category:
        return jsonify({"error": "Missing category"}), 400
    card = draw_card(category, zone)
    return jsonify(card)

@app.route("/getTask", methods=["GET"])
def get_task_route():
    zone = request.args.get("zone")
    if not zone:
        return jsonify({"error": "Missing zone"}), 400
    task = get_task(zone)
    return jsonify(task)

@app.route("/getRoleByZone", methods=["GET"])
def role_by_zone():
    zone = request.args.get("zone")
    if not zone:
        return jsonify({"error": "Missing zone"}), 400
    role = get_role_by_zone(zone)
    return jsonify(role)

@app.route("/getRitual", methods=["GET"])
def ritual():
    mode = request.args.get("mode")
    trigger = request.args.get("trigger")
    if not (mode and trigger):
        return jsonify({"error": "Missing mode or trigger"}), 400
    r = get_ritual(mode, trigger)
    return jsonify(r)

@app.route("/generateInsight", methods=["GET"])
def generate_insight():
    import random
    phrases = [
        "Я могу быть собой.",
        "Мне позволено чувствовать.",
        "Мои страхи — ключ к росту.",
        "Истина раскрывается в тишине.",
        "Я выбираю доверие жизни."
    ]
    insight = random.choice(phrases)
    reward = random.randint(1, 5)
    return jsonify({"insight": insight, "reward": reward})

# --- ZION ---

@app.route("/zion/manifest", methods=["GET"])
def zion_manifest():
    zion = get_zion_manifest()
    return jsonify({"zion_manifest": zion})

@app.route("/zion/store", methods=["POST"])
def zion_store():
    data = request.json
    content = data.get("content")
    ztype = data.get("type", "insight")
    created_by = data.get("created_by", "Logos")
    store_zion(content, ztype, created_by)
    return jsonify({"status": "stored in ZION", "content": content})

# --- PING / HEALTH CHECK ---

@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"status": "ok", "message": "Logos Cloud Server 2.0 is running."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
