import serial
import time
import string
import pynmea2
import pandas as pd
#import geopandas as gpd
import geopy
import subprocess
import pyrebase

firebaseConfig = {
     "apiKey": "AIzaSyBRYIpKhCOMrf9wSJhKGoupsaRq-AxYq0o",
    "authDomain": "connectingfbtopy.firebaseapp.com",
    "projectId": "connectingfbtopy",
    "databaseURL": "https://connectingfbtopy-default-rtdb.firebaseio.com/",
    "storageBucket": "connectingfbtopy.appspot.com",
    "messagingSenderId": "921973152097",
    "appId": "1:921973152097:web:56e04327d2f65c039f8d20",
    "measurementId": "G-DPMCW1GJSB"
 };
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()


def execute_unix(inputcommand):
    p = subprocess.Popen(inputcommand, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    return output

from geopy.geocoders import Nominatim
#from geopy.extra.rate_limiter import Ratelimiter

while True:
    port="/dev/ttyS0"
    ser=serial.Serial(port, baudrate=9600, timeout=0.5)
    dataout = pynmea2.NMEAStreamReader()
    newdata=ser.readline()

    if newdata[0:6] == "$GPRMC":
        newmsg=pynmea2.parse(newdata)
        lat=newmsg.latitude
        lng=newmsg.longitude
        gps = "Latitude:" + str(lat) + " Longitude:" + str(lng)
        print(gps)
        locator = Nominatim(user_agent="myGeocoder")
        latitude= str(lat)
        longitude=str(lng)
        coordinates = ""+latitude+", "+longitude
        location = locator.reverse(coordinates)
        addr=location.address
        data = {"Latitude": latitude, "Longitude": longitude, "Location":addr}
        db.push(data)
        print(addr)
        string = "You are currently at "+addr
        c = 'espeak -ven+m4 -k5 -s140 --punct="?" "%s" 2>>/dev/null' % string
        execute_unix(c)
        
