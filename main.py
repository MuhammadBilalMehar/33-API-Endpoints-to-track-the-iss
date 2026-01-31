import os
from tkinter import *
from tkinter import PhotoImage
import requests
from datetime import datetime
import smtplib
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(BASE_DIR, "d.png")

is_run = True
FONT_NAME = "Courier"
RED = "#e7305b"

My_Email = "algorydhem@gmail.com"
My_Password = "xbdu melm xlry ijqf"

MY_LAT = 31.708780 # Your latitude
MY_LONG = 73.984673 # Your longitude

def is_iss_overhead(): 
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    #Your position is within +5 or -5 degrees of the ISS position.
    if (MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and
    MY_LONG - 5 <= iss_longitude <= MY_LONG + 5):
        return True

    return False

def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True

    return False

last_sent = None

def mail_fun():
    global last_sent

    # Prevent sending email more than once per hour
    if last_sent and (datetime.now() - last_sent).seconds < 3600:
        return

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(My_Email, My_Password)
            connection.sendmail(
                from_addr=My_Email,
                to_addrs=My_Email,
                msg="Subject: Look Up!\n\nThe ISS is currently above your location. Go outside and look up 👀"
            )

        last_sent = datetime.now()  # update only after successful send
        print("📧 Email sent successfully")

    except Exception as e:
        print("❌ Email sending failed:", e)

def close_window():
    window.destroy()

def stp_track():
    global is_run
    is_run = False
    tik_lable.config(text="Tracking stopped")


def str_track():
    global is_run
    if is_run:
        return   # already running
    is_run = True
    tik_lable.config(text="Tracking is in Progress...")
    check_iss()

def check_iss():
    if not is_run:
        return

    try:
        if is_iss_overhead() and is_night():
            mail_fun()
    except Exception as e:
        print("⚠️ Tracking error:", e)

    window.after(60000, check_iss)

#If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.

window = Tk()
window.title("ISS Tracker For Live Location of ISS")
window.config(padx=50,pady=50)


timer_lable = Label(text="ISS Tracker", font=(FONT_NAME,35,"bold"))
timer_lable.grid(column=1,row=0)

canvas = Canvas(width=300,height=300,highlightthickness=0)
iss_img =PhotoImage(file=image_path)
canvas.create_image(170,170,image =iss_img)
canvas.grid(column=1,row=1)

track_btn = Button(text="Start Tracking",command=str_track,highlightthickness=0,font=(FONT_NAME,25,"bold"))
track_btn.grid(column=0,row=2)

stop_btn = Button(text="Stop Tracking",command=stp_track,highlightthickness=0,font=(FONT_NAME,25,"bold"))
stop_btn.grid(column=2,row=2)

tik_lable = Label(text="ISS Tracking Status",fg=RED,highlightthickness=0,font=(FONT_NAME,25,"bold"))
tik_lable.grid(column=1,row=3,padx=5,pady=15)

window.mainloop()