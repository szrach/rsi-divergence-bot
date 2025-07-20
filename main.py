from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = "7167998963:AAEqQmQNV_q3lKoM_BNYMzIxZtZe2kFogCI"
USER_CHAT_ID = "5154443088"   # <- you will update this
CHANNEL_CHAT_ID = "-1002781526863"  # <- and this too

def send_telegram_message(chat_id, message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("RECEIVED ALERT:", data)

    symbol = data.get("ticker", "N/A")
    interval = data.get("interval", "N/A")
    price = data.get("close", "N/A")
    type_ = data.get("type", "Unknown")

    msg = f"🚨 *{type_} RSI Divergence!*\n" \
          f"• *Symbol:* {symbol}\n" \
          f"• *Timeframe:* {interval}\n" \
          f"• *Price:* ${price}"

    send_telegram_message(USER_CHAT_ID, msg)
    send_telegram_message(CHANNEL_CHAT_ID, msg)

    return {"status": "ok"}

app.run(host='0.0.0.0', port=8080)
