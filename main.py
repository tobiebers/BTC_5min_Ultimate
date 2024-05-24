from flask import Flask, request, jsonify
from functions import open_position_with_sl_tp, calculate_order_size, fetch_current_price, fetch_swap_balance, is_position_open
import threading
import time

app = Flask(__name__)

# Globale Variable, um den Zustand der Position zu verfolgen
position_open = False

@app.route('/webhook', methods=['POST'])
def webhook():
    global position_open
    # Daten aus dem Body der Anfrage als Text holen
    direction = request.data.decode().strip().lower()
    print("Webhook received:", direction)

    if position_open:
        return jsonify({"error": "Position bereits offen, warte auf Schließung"}), 429

    symbol = "BTCUSDT"
    trade_percentage = 20
    leverage = 15

    swap_balances = fetch_swap_balance()
    print("Swap Balances:", swap_balances)
    current_price = fetch_current_price(symbol)
    order_size = calculate_order_size(trade_percentage, leverage, symbol)

    if direction == 'long':
        stop_loss_price = current_price * (1 - 0.016)  # 1.6% unter dem aktuellen Preis
        take_profit_price = current_price * (1 + 0.016)  # 1.6% über dem aktuellen Preis
    elif direction == 'short':
        stop_loss_price = current_price * (1 + 0.016)  # 1.6% über dem aktuellen Preis
        take_profit_price = current_price * (1 - 0.016)  # 1.6% unter dem aktuellen Preis
    else:
        return jsonify({"error": "Invalid direction received"}), 400

    open_position_with_sl_tp(symbol, direction, order_size, stop_loss_price, take_profit_price)
    position_open = True
    threading.Thread(target=check_position).start()

    return jsonify({"status": "Position eröffnet"}), 200

def check_position():
    global position_open
    while position_open:
        if not is_position_open():
            position_open = False
        print("Position bereits offen")
        time.sleep(4)  # Überprüfe alle 4 Sekunden

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
