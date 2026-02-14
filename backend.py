from flask import Flask, request, jsonify
from flask_cors import CORS
import csv, os

app = Flask(__name__)
CORS(app)

BASE = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE, "products.csv")


# ---------- create csv if not exists ----------
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="") as f:
        csv.writer(f).writerow(["Name", "Price"])


# ---------- home route ----------
@app.route("/")
def home():
    return "Backend is running!"


# ---------- add product ----------
@app.route("/add", methods=["POST"])
def add_product():
    data = request.json

    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([data["name"], data["price"]])

    return jsonify({"msg": "Product saved"})


# ---------- get products ----------
@app.route("/products")
def get_products():
    products = []

    with open(CSV_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            products.append(row)

    return jsonify(products)


# ---------- run ----------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
