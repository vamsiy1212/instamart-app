from flask import Flask, request, jsonify

app = Flask(__name__)
orders = []  # Temporary memory; lost on restart

@app.route("/place_order", methods=["POST"])
def place_order():
    data = request.json
    orders.append(data)
    return jsonify({"message": "Order received"}), 200

@app.route("/get_orders", methods=["GET"])
def get_orders():
    return jsonify(orders)

if __name__ == "__main__":
    app.run(port=5050)
