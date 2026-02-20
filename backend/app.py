from flask import Flask, request, jsonify, send_from_directory
import os, json

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
JOB_FILE = "jobs.json"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

if not os.path.exists(JOB_FILE):
    with open(JOB_FILE, "w") as f:
        json.dump({}, f)

@app.route("/")
def home():
    return send_from_directory("../web", "index.html")

@app.route("/script.js")
def script():
    return send_from_directory("../web", "script.js")

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files['pdf']
    bw = request.form['bw']
    side = request.form['side']
    copies = int(request.form['copies'])

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    pages = 1
    if side == "double":
        pages = 0.5

    base = 2 if bw == "bw" else 5
    amount = int(base * copies / pages)

    job = {
        "file": filepath,
        "bw": bw,
        "side": side,
        "copies": copies,
        "amount": amount,
        "status": "pending"
    }

    with open(JOB_FILE, "w") as f:
        json.dump(job, f)

    return jsonify({"status": "success", "amount": amount})

@app.route("/get_job")
def get_job():
    with open(JOB_FILE) as f:
        job = json.load(f)
    return jsonify(job)

@app.route("/clear_job")
def clear_job():
    with open(JOB_FILE, "w") as f:
        json.dump({}, f)
    return jsonify({"status": "cleared"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
