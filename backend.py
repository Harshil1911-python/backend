from flask import Flask, send_file, request, jsonify
from flask_cors import CORS
import csv, os, webbrowser, threading

app = Flask(__name__)
CORS(app)

BASE = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(BASE, "frontend", "index.html")
CSV = os.path.join(BASE, "products.csv")

# ---------- create csv ----------
if not os.path.exists(CSV):
    with open(CSV, "w", newline="") as f:
        csv.writer(f).writerow(["Name", "Price"])


# ---------- home ----------
@app.route("/")
def home():
    return send_file(HTML)


# ---------- add product ----------
@app.route("/add", methods=["POST"])
def add():
    d = request.json

    with open(CSV, "a", newline="") as f:
        csv.writer(f).writerow([d["name"], d["price"]])

    return jsonify({"msg":"Product Saved!"})


# ---------- get products ----------
@app.route("/products")
def products():
    data=[]
    with open(CSV,"r") as f:
        for r in csv.DictReader(f):
            data.append(r)
    return jsonify(data)


# ---------- auto open browser ----------
def open_browser():
    webbrowser.open("http://127.0.0.1:5000")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
