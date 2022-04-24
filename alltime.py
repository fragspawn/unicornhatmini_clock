#!/usr/bin/env python3
import time
import json
import requests

from unicornhatmini import UnicornHATMini

unicornhatmini = UnicornHATMini()
display_width, display_height = unicornhatmini.get_shape()

# GLOBALS
hourlyflash = True
purpleair = True

if hourlyflash == True:
    once = 0 
if purpleair == True:
    minutecount = 0

def one(pos, rgb):
    if pos == 0:
        x = 0
    if pos == 1:
        x = 5
    if pos == 2:
        x = 10
    if pos == 3:
        x = 16
    for y in range(display_height):
        unicornhatmini.set_pixel(x, y, rgb[0], rgb[1], rgb[2])

def two(pos, rgb):
    if pos == 0:
        x = 0
    if pos == 1:
        x = 2
    if pos == 2:
        x = 7 
    if pos == 3:
        x = 12 
    for y in [0,3,6]:
        unicornhatmini.set_pixel(x, y, rgb[0], rgb[1], rgb[2])
        unicornhatmini.set_pixel(x+1, y, rgb[0], rgb[1], rgb[2])
        unicornhatmini.set_pixel(x+2, y, rgb[0], rgb[1], rgb[2])
        unicornhatmini.set_pixel(x+3, y, rgb[0], rgb[1], rgb[2])
    for y in [4,5,6]:
        unicornhatmini.set_pixel(x, y, rgb[0], rgb[1], rgb[2])
    for y in [0,1,2]:
        unicornhatmini.set_pixel(x+3, y, rgb[0], rgb[1], rgb[2])

def three(pos, rgb):
    if pos == 0:
        x = 0
    if pos == 1:
        x = 2
    if pos == 2:
        x = 7 
    if pos == 3:
        x = 12 
    for y in [0,3,6]:
        unicornhatmini.set_pixel(x, y, rgb[0], rgb[1], rgb[2])
        unicornhatmini.set_pixel(x+1, y, rgb[0], rgb[1], rgb[2])
        unicornhatmini.set_pixel(x+2, y, rgb[0], rgb[1], rgb[2])
    for y in range(display_height):
        unicornhatmini.set_pixel(x+3, y, rgb[0], rgb[1], rgb[2])

def four(pos, rgb):
    if pos == 0:
        x = 0
    if pos == 1:
        x = 2
    if pos == 2:
        x = 7 
    if pos == 3:
        x = 12 
    for y in range(0,4):
        unicornhatmini.set_pixel(x, y, rgb[0], rgb[1], rgb[2])
    unicornhatmini.set_pixel(x+1, 3, rgb[0], rgb[1], rgb[2])
    unicornhatmini.set_pixel(x+2, 3, rgb[0], rgb[1], rgb[2])
    for y in range(display_height):
        unicornhatmini.set_pixel(x+3, y, rgb[0], rgb[1], rgb[2])

def five(pos, rgb):
    if pos == 0:
        x = 0
    if pos == 1:
        x = 2
    if pos == 2:
        x = 7 
    if pos == 3:
        x = 12 
    for y in [0,3,6]:
        unicornhatmini.set_pixel(x, y, rgb[0], rgb[1], rgb[2])
        unicornhatmini.set_pixel(x+1, y, rgb[0], rgb[1], rgb[2])
        unicornhatmini.set_pixel(x+2, y, rgb[0], rgb[1], rgb[2])
        unicornhatmini.set_pixel(x+3, y, rgb[0], rgb[1], rgb[2])
    for y in [4,5,6]:
        unicornhatmini.set_pixel(x+3, y, rgb[0], rgb[1], rgb[2])
    for y in [0,1,2]:
        unicornhatmini.set_pixel(x, y, rgb[0], rgb[1], rgb[2])

def six(pos, rgb):
    if pos == 0:
        x = 0
    if pos == 1:
        x = 2
    if pos == 2:
        x = 7 
    if pos == 3:
        x = 12 
    for y in range(display_height):
        unicornhatmini.set_pixel(x, y, rgb[0], rgb[1], rgb[2])
    for y in [3,6]:
        unicornhatmini.set_pixel(x+1, y, rgb[0], rgb[1], rgb[2])
        unicornhatmini.set_pixel(x+2, y, rgb[0], rgb[1], rgb[2])
    for y in range(3,7):
        unicornhatmini.set_pixel(x+3, y, rgb[0], rgb[1], rgb[2])

def seven(pos, rgb):
    if pos == 0:
        x = 0
    if pos == 1:
        x = 2
    if pos == 2:
        x = 7 
    if pos == 3:
        x = 12 
    unicornhatmini.set_pixel(x, 0, rgb[0], rgb[1], rgb[2])
    unicornhatmini.set_pixel(x+1, 0, rgb[0], rgb[1], rgb[2])
    unicornhatmini.set_pixel(x+2, 0, rgb[0], rgb[1], rgb[2]) 
    for y in range(display_height):
        unicornhatmini.set_pixel(x+3, y, rgb[0], rgb[1], rgb[2])

def eight(pos, rgb):
    if pos == 0:
        x = 0
    if pos == 1:
        x = 2
    if pos == 2:
        x = 7 
    if pos == 3:
        x = 12 
    for y in range(display_height):
        unicornhatmini.set_pixel(x, y, rgb[0], rgb[1], rgb[2])
    for y in [0,3,6]:
        unicornhatmini.set_pixel(x+1, y, rgb[0], rgb[1], rgb[2])
        unicornhatmini.set_pixel(x+2, y, rgb[0], rgb[1], rgb[2])
    for y in range(display_height):
        unicornhatmini.set_pixel(x+3, y, rgb[0], rgb[1], rgb[2])

def nine(pos, rgb):
    if pos == 0:
        x = 0
    if pos == 1:
        x = 2
    if pos == 2:
        x = 7 
    if pos == 3:
        x = 12 
    for y in range(display_height-3):
        unicornhatmini.set_pixel(x, y, rgb[0], rgb[1], rgb[2])
    for y in [0,3]:
        unicornhatmini.set_pixel(x+1, y, rgb[0], rgb[1], rgb[2])
        unicornhatmini.set_pixel(x+2, y, rgb[0], rgb[1], rgb[2])
    for y in range(display_height):
        unicornhatmini.set_pixel(x+3, y, rgb[0], rgb[1], rgb[2])

def zero(pos, rgb):
    if pos == 0:
        x = 0
    if pos == 1:
        x = 2
    if pos == 2:
        x = 7 
    if pos == 3:
        x = 12
    for y in range(display_height):
        unicornhatmini.set_pixel(x, y, rgb[0], rgb[1], rgb[2])
    unicornhatmini.set_pixel(x+1, 0, rgb[0], rgb[1], rgb[2])
    unicornhatmini.set_pixel(x+1, display_height-1, rgb[0], rgb[1], rgb[2])
    unicornhatmini.set_pixel(x+2, 0, rgb[0], rgb[1], rgb[2])
    unicornhatmini.set_pixel(x+2, display_height-1, rgb[0], rgb[1], rgb[2])
    for y in range(display_height):
        unicornhatmini.set_pixel(x+3, y, rgb[0], rgb[1], rgb[2])

def gettime():
    time_array = [0,0,0,0] 

    month, day, twentyfour, hour, minute = map(int, time.strftime("%m %d %H %I %M").split())
    if hour > 9:
        time_array[0] = 1
        time_array[1] = hour - 10
    else:
        time_array[0] = 0
        time_array[1] = hour
    if minute < 10:
        time_array[2] = 0 
        time_array[3] = minute
    else:
        time_array[2] = int(minute / 10) 
        time_array[3] = minute % 10
    return time_array

def getdate():
    date_array = [0,0,0,0] 

    month, day, twentyfour, hour, minute = map(int, time.strftime("%m %d %H %I %M").split())
    if month > 9:
        date_array[0] = 1
        date_array[1] = month - 10 
    else:
        date_array[0] = 0
        date_array[1] = month - 10 
    if day < 10:
        date_array[2] = 0
        date_array[3] = day % 10 
    else:
        date_array[2] = int(day / 10)
        date_array[3] = day % 10
    return date_array

def gethue(twentyfour):
    r = 255
    g = 255
    b = 255
    if (twentyfour > 20 and twentyfour <= 23) or (twentyfour >= 0 and twentyfour < 6):
        r = 255
        g = 0
        b = 0
    if twentyfour > 4 and twentyfour < 9:
        r = 0 
        g = 0
        b = 255
    if twentyfour > 17 and twentyfour < 21:
        r = 255
        g = 40
        b = 0 
    if twentyfour > 19 and twentyfour < 21:
        r = 255
        g = 10
        b = 0 

    rgb = [r, g, b]
    return rgb

def getbright(twentyfour):
    if (twentyfour > 21 and twentyfour <= 23) or (twentyfour >= 0 and twentyfour < 6):
        unicornhatmini.set_brightness(.02)
    elif twentyfour > 5 and twentyfour < 13:
        unicornhatmini.set_brightness(.2)
    elif twentyfour > 17 and twentyfour < 21:
        unicornhatmini.set_brightness(.05)
    else:
        unicornhatmini.set_brightness(.1)

def hourflash():
    unicornhatmini.set_brightness(1)
    unicornhatmini.set_all(255,255,255)
    unicornhatmini.show()
    time.sleep(.1)
    unicornhatmini.set_all(0,0,0)
    unicornhatmini.show()
    time.sleep(.05)
    unicornhatmini.set_all(255,255,255)
    unicornhatmini.show()
    time.sleep(.1)

def showpurple(action):
    jURL = "http://192.168.1.195/json?live=false"
    jsn = requests.get(jURL).json()

    celsius = int((int(jsn["current_temp_f"]) - 32) * 5 / 9) 
    air_qual = int(jsn["pm2.5_aqi_b"])
    humidity = int(jsn["current_humidity"])
    pressure = int(jsn["pressure"])

    rgb = [255, 255, 255]
    unicornhatmini.clear()

    for measure in [celsius, humidity, pressure, air_qual]:
        measarray = [int(a) for a in str(measure)]
        if len(measarray) == 4:
            pos = 0
        if len(measarray) == 3:
            pos = 1
        if len(measarray) == 2:
            pos = 2
        if len(measarray) == 1:
            pos = 3

        for measdigit in measarray:
            if measdigit == 1:
                one(pos, rgb)
            if measdigit == 2:
                two(pos, rgb)
            if measdigit == 3:
                three(pos, rgb)
            if measdigit == 4:
                four(pos, rgb)
            if measdigit == 5:
                five(pos, rgb)
            if measdigit == 6:
                six(pos, rgb)
            if measdigit == 7:
                seven(pos, rgb)
            if measdigit == 8:
                eight(pos, rgb)
            if measdigit == 9:
                nine(pos, rgb)
            if measdigit == 0:
                zero(pos, rgb)
            pos += 1

        unicornhatmini.show()
        time.sleep(3)
        unicornhatmini.clear()

# MAIN LOOP
while True:
    time_array = gettime()
    tf = int(time.strftime("%H"))
    rgb = gethue(tf)
    getbright(tf)

    if time_array[2] == 0 and time_array[3] == 0 and hourlyflash == True:
        if once == 0:
            hourflash()
            once = 1
    else:
        once = 0

    for pos in range(len(time_array)):
        if pos == 0:
            if time_array[pos] == 1:
                one(pos, rgb)
        else:
            if time_array[pos] == 1:
                one(pos, rgb)
            if time_array[pos] == 2:
                two(pos, rgb)
            if time_array[pos] == 3:
                three(pos, rgb)
            if time_array[pos] == 4:
                four(pos, rgb)
            if time_array[pos] == 5:
                five(pos, rgb)
            if time_array[pos] == 6:
                six(pos, rgb)
            if time_array[pos] == 7:
                seven(pos, rgb)
            if time_array[pos] == 8:
                eight(pos, rgb)
            if time_array[pos] == 9:
                nine(pos, rgb)
            if time_array[pos] == 0:
                zero(pos, rgb)

    unicornhatmini.show()
    time.sleep(.1)

    if purpleair == True:
        minutecount += .1
        if int(minutecount) == 60: 
            if time_array[3] == 1:
                showpurple('temp') 
            if time_array[3] == 3:
                showpurple('qual') 
            if time_array[3] == 5:
                showpurple('pres') 
            if time_array[3] == 7:
                showpurple('humi') 
            if time_array[3] == 9:
                showpurple('pull') 
            minutecount = 0

    unicornhatmini.clear()
