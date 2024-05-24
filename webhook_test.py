from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    print("Received Headers:", request.headers)  # Gibt die Header aus, um den Content-Type zu überprüfen

    if request.content_type.startswith('application/json'):
        data = request.get_json(force=True)  # Erzwingt die Interpretation als JSON
        print("Webhook received as JSON:")
    elif request.content_type.startswith('application/x-www-form-urlencoded'):
        data = request.form.to_dict()
        print("Webhook received as form data:")
    else:
        data = request.data.decode()  # Nimmt an, dass es Text ist, wenn kein anderer Typ passt
        print("Webhook received as unknown format:")

    print(data)  # Gibt die empfangenen Daten aus
    return jsonify({"status": "received"}), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)
