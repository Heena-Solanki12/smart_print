import tkinter as tk
from PIL import Image, ImageTk
import qrcode
import socket

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

ip = get_ip()
url = f"http://{ip}:5000"

qr = qrcode.make(url)
qr.save("qr.png")

root = tk.Tk()
root.attributes('-fullscreen', True)
root.configure(bg="black")

def show_qr():
    img = Image.open("qr.png").resize((300,300))
    photo = ImageTk.PhotoImage(img)
    label.config(image=photo)
    label.image = photo
    text.config(text="Scan QR Code")

btn.destroy()

label = tk.Label(root, bg="black")
label.pack(pady=50)

text = tk.Label(root, text="SMART PRINT KIOSK", fg="white", bg="black", font=("Arial",24))
text.pack(pady=20)

btn = tk.Button(root, text="GET STARTED", font=("Arial",24),
                command=show_qr, bg="green", fg="white")
btn.pack(pady=30)

root.mainloop()
