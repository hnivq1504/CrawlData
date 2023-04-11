import requests
bot_token = "6216004222:AAHo7A_DoK5e6sCdfBHp2VpwOn_H-Hg9Og8"
chat_id = "-901299271"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    response = requests.post(url, data=data)
    if not response.ok:
        print("Failed to send message:", response.text)

send_telegram_message("test ne")