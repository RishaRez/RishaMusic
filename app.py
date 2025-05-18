from flask import Flask, request, jsonify
import hashlib
import hmac
import os

app = Flask(__name__, static_folder="static")
BOT_TOKEN = "ВАШ_ТОКЕН_БОТА"  # Замени на свой!

# Проверка данных от Telegram WebApp
def verify_telegram_data(data_check_string, telegram_hash):
    secret_key = hashlib.sha256(BOT_TOKEN.encode()).digest()
    computed_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
    return computed_hash == telegram_hash

# Главная страница (WebApp)
@app.route("/")
def index():
    return app.send_static_file("index.html")

# Обработка данных от WebApp
@app.route("/webapp-data", methods=["POST"])
def handle_webapp_data():
    data = request.json
    init_data = data.get("initData")
    
    # Проверяем подпись Telegram
    params = {}
    for pair in init_data.split("&"):
        key, value = pair.split("=")
        params[key] = value
    
    if not verify_telegram_data(params.get("hash"), params):
        return jsonify({"status": "error", "message": "Invalid data"}), 403
    
    user_id = params.get("user", {}).get("id")
    print(f"Данные получены от пользователя: {user_id}")
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)