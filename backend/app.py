@app.route("/generate_qr")
def generate_qr():

    url = "https://bit.ly/pixoprint"   # your website

    img = qrcode.make(url)
    img.save("../static/qr.png")

    return render_template("qr.html")
