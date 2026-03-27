from flask import Flask, render_template, request, jsonify
import qrcode, socket, os, json, time

app = Flask(__name__, template_folder="../templates", static_folder="../static")

UPLOAD_FOLDER = "../backend/uploads"
JOB_FILE = "jobs.json"
QR_PATH = "../static/qr.png"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    ip = s.getsockname()[0]
    s.close()
    return ip

# Home Screen
@app.route("/")
def home():
    return render_template("home.html")

# Generate QR
@app.route("/generate_qr")
def generate_qr():
    ip = get_ip()
    url = f"http://{ip}:5000/form"

    img = qrcode.make(url)
    img.save(QR_PATH)

    return render_template("qr.html")

# Form page
@app.route("/form")
def form():
    return render_template("form.html")

# Submit form
@app.route("/submit", methods=["POST"])
def submit():

    file = request.files['pdf']
    bw = request.form.get("bw")
    side = request.form.get("side")
    copies = int(request.form.get("copies"))

    filename = str(int(time.time())) + "_" + file.filename
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # price logic
    price = 2 if bw=="bw" else 5
    if side=="double":
        price *= 0.8

    amount = int(price * copies)

    job = {
        "file": filepath,
        "bw": bw,
        "side": side,
        "copies": copies,
        "amount": amount,
        "status": "pending"
    }

    with open(JOB_FILE,"w") as f:
        json.dump(job,f)

    return jsonify({"amount":amount})

# Get job
@app.route("/get_job")
def get_job():
    try:
        with open(JOB_FILE) as f:
            return jsonify(json.load(f))
    except:
        return jsonify({})

# Clear job
@app.route("/clear_job")
def clear_job():
    with open(JOB_FILE,"w") as f:
        json.dump({},f)
    return jsonify({"status":"cleared"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
