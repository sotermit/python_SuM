import pandas as pd
from bs4 import BeautifulSoup
import requests
import time
import RPi.GPIO as GPIO          
from time import sleep

in1 = 23
in2 = 24
en = 25
temp1=1

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
p=GPIO.PWM(en,1000)
p.start(25)

while(True):
    url0 = 'https://sotermit.pythonanywhere.com/'
    req0 = requests.get(url0)
    html0 = req0.text
    q_power = '/auto'
    n_q_power = html0.find(q_power)
    n_power = '<p>auto'
    n_a_power = html0.find(n_power)
    v_power=html0[n_q_power+33:n_q_power+37]   
    q_city = '광주):'
    n_q_city = html0.find(q_city)
    v_city=html0[n_q_city+32:n_q_city+34]
    q_dist = ':북구):'
    n_q_dist = html0.find(q_dist)
    v_dist = html0[n_q_dist+33:n_q_dist+35]
    v_dist1 = html0[n_q_dist+33:n_q_dist+36]

    if v_power == 'auto':
        url = 'http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnMesureSidoLIst?serviceKey=JGW1twhgsz%2F9pxs1jiHzo051TMC9n0P1Nz9q2a%2FIEAIntaWrMNYU2%2F0GSLrVmvHxteArzLnftsHCp4N7PRzCcA%3D%3D&numOfRows=30&pageSize=10&pageNo=1&startPage=1&sidoName='+ v_city +'&searchCondition=HOUR'
        req = requests.get(url)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        distlist = soup.find_all('cityname')
        dist = '<cityname>'+v_dist+'</cityname>'
        dist1 = '<cityname>'+v_dist1+'</cityname>'
        if dist in distlist:
            dist = dist
        else:
            dist = dist1
        for rdist in distlist:
            if dist == str(rdist):
               n = distlist.index(rdist)

        pm10 = soup.find_all('pm10value')
        pm25 = soup.find_all('pm25value')

        미세먼지 = int(pm10[n].text)
        초미세먼지 = int(pm25[n].text)

        if 미세먼지 <= 80 and 초미세먼지 <=35:
            power = 'r'
        else:
            power = 's'
    elif v_power == 'off<':
        power = 's'
    elif v_power == 'low<':
        power = 'l'
    elif v_power == 'medi':
        power = 'm'
    elif v_power == 'high':
        power = 'h'
        
    x = power
    
    if x=='r':
        print("run")
        if(temp1==1):
         GPIO.output(in1,GPIO.HIGH)
         GPIO.output(in2,GPIO.LOW)
         print("forward")
         x='z'
        else:
         GPIO.output(in1,GPIO.LOW)
         GPIO.output(in2,GPIO.HIGH)
         print("backward")
         x='z'


    elif x=='s':
        print("stop")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        x='z'

    elif x=='f':
        print("forward")
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        temp1=1
        x='z'

    elif x=='b':
        print("backward")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        temp1=0
        x='z'

    elif x=='l':
        print("low")
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        p.ChangeDutyCycle(25)
        x='z'

    elif x=='m':
        print("medium")
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        p.ChangeDutyCycle(50)
        x='z'

    elif x=='h':
        print("high")
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        p.ChangeDutyCycle(75)
        x='z'
    time.sleep(5)

