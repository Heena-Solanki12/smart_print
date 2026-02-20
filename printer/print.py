import RPi.GPIO as GPIO
import time, requests, os

BUTTON = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("Waiting for print job...")

while True:
    try:
        r = requests.get("http://localhost:5000/get_job").json()

        if r.get("status") == "pending":
            print("Job Found: ₹", r["amount"])
            print("Press Button To Print")

            while GPIO.input(BUTTON) == 1:
                time.sleep(0.1)

            print("Printing...")
            os.system(f"lp {r['file']}")

            requests.get("http://localhost:5000/clear_job")
            print("Done")
            time.sleep(2)

    except:
        pass

    time.sleep(1)
