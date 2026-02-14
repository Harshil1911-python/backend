from flask import Flask, request, jsonify
from flask_cors import CORS
import csv, os

app = Flask(__name__)

# allow all origins (needed for Netlify frontend)
CORS(app, resources={r"/*": {"origins": "*"}})

BASE = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE, "products.csv")


# ---------- create csv if missing ----------
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Price"])


# ---------- home route ----------
@app.route("/")
def home():
    return "Backend is running!"


# ---------- add product ----------
@app.route("/add", methods=["POST"])
def add_product():
    try:
        data = request.get_json()

        name = data.get("name")
        price = data.get("price")

        if not name or not price:
            return jsonify({"error": "Missing data"}), 400

        with open(CSV_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([name, price])

        return jsonify({"msg": "Product saved successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------- get products ----------
@app.route("/products")
def get_products():
    try:
        products = []

        with open(CSV_FILE, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                products.append(row)

        return jsonify(products)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------- run server ----------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
