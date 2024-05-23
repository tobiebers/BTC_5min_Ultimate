from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    # Empfange die Daten von TradingView
    data = request.json
    print("Empfangene Daten:", data)

    # Hier kannst du die empfangenen Daten verarbeiten
    process_trading_signal(data)

    # Eine einfache Antwort zurücksenden
    return jsonify({"status": "success", "message": "Daten empfangen"}), 200


def process_trading_signal(data):
    # Verarbeite die Trading Signale
    # Zum Beispiel kannst du prüfen, ob es ein Kauf- oder Verkaufssignal ist
    if 'action' in data:
        if data['action'] == 'buy':
            print("Kaufsignal empfangen")
        elif data['action'] == 'sell':
            print("Verkaufsignal empfangen")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
