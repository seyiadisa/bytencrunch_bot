from flask import Flask, render_template, request, make_response, jsonify
import os, telegram
import json
from database.queries import update_status, get_order
import requests
from dotenv.main import load_dotenv
from threading import Thread
load_dotenv()

app = Flask(__name__)

@app.route('/flutterwave_webhook', methods=['POST'])
def flutterwave_webhook():
    """Processes Flutterwave payment webhooks."""

    try:
        secret_hash = os.getenv("FLW_SECRET_HASH")
        signature = request.headers.get("verif-hash")

        if not signature or signature != secret_hash:
            return make_response("Unauthorized", 401)

        payload = request.get_json()
        data = payload

        status = data["data"]["status"]
        reference = data["data"]["tx_ref"]

        if status.lower() == 'successful':
            try:
                new_status = update_status(reference, status.lower())

                # Sends order to the order gc
                telegram_token = os.getenv("TOKEN")
                group_id = os.getenv("order_group_id")
                order = get_order(reference)
                bot = telegram.Bot(token=telegram_token)
                bot.send_message(chat_id=group_id, text=order)

                return make_response("OK", 200)
            except Exception as e:
                print("Error processing successful payment:", e)
                return make_response("Internal Server Error", 500)
        else:
            new_status = update_status(reference, status)
            return make_response("Payment Error", 400)

    except (KeyError, ValueError) as e:
        print("Error processing webhook data:", e)
        return make_response("Bad Request", 400)
 
@app.route('/redirect', methods=['GET'])
def redirect():
    return render_template('redirect.html')

def run_flask_server():
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))


if __name__ == '__main__':
    flask_thread = Thread(target=run_flask_server)
    flask_thread.start()
    port = os.getenv('PORT')
    app.run(host='0.0.0.0',port=port)