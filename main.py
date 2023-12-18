from tkinter import *
import requests
from datetime import datetime
import smtplib
import time

is_run = True
FONT_NAME = "Courier"
RED = "#e7305b"

My_Email = "algorydhem@gmail.com"
My_Password = "Muhammad@Bilal15"

MY_LAT = 31.708780 # Your latitude
MY_LONG = 73.984673 # Your longitude

def is_iss_overhead(): 
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    #Your position is within +5 or -5 degrees of the ISS position.
    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_latitude <= MY_LONG+5:
        return True
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

def mail_fun():
    connection = smtplib.SMTP("smtp.gmail.com")
    connection.starttls()
    connection.login(My_Email,My_Password)
    connection.sendmail(
        from_add = My_Email,
        to_add = My_Email,
        msg = "Subject: Look Up  \n\n  ISS is above you"
        )
def close_window():
    window.destroy()

def stp_track():
    tik_lable.config(text="Tracking is Stoped By Force... ")
    close_window()

def str_track():
    tik_lable.config(text="Tracking is in Progress... ")
    while is_run==True:
        time.sleep(60)
        if is_iss_overhead() and is_night():
            mail_fun()
        else:
            is_run=False

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
iss_img =PhotoImage(file="d.png")
canvas.create_image(170,170,image =iss_img)
canvas.grid(column=1,row=1)

track_btn = Button(text="Start Tracking",command=str_track,highlightthickness=0,font=(FONT_NAME,25,"bold"))
track_btn.grid(column=0,row=2)

stop_btn = Button(text="Stop Tracking",command=stp_track,highlightthickness=0,font=(FONT_NAME,25,"bold"))
stop_btn.grid(column=2,row=2)

tik_lable = Label(text="ISS Tracking Status",fg=RED,highlightthickness=0,font=(FONT_NAME,25,"bold"))
tik_lable.grid(column=1,row=3,padx=5,pady=15)

window.mainloop()