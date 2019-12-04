import os
import time
import datetime
import glob
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
from time import strftime

import RPi.GPIO as GPIO


#define GPIO pins as input
GPIO.setmode(GPIO.BOARD)

GPIO.setup(7, GPIO.IN)
GPIO.setup(11, GPIO.IN)
GPIO.setup(12, GPIO.IN)
GPIO.setup(13, GPIO.IN)
GPIO.setup(15, GPIO.IN)
GPIO.setup(16, GPIO.IN)
GPIO.setup(18, GPIO.IN)
GPIO.setup(22, GPIO.IN)

# Variables for MySQL
db = MySQLdb.connect(host="localhost", user="root",passwd="***", db="testing")
cur = db.cursor()
 
def get_temp():
#while True:
    d0 = GPIO.input(7)
    d1 = GPIO.input(11)
    d2 = GPIO.input(12)
    d3 = GPIO.input(13)
    d4 = GPIO.input(15)
    d5 = GPIO.input(16)
    d6 = GPIO.input(18)
    d7 = GPIO.input(22)
    value = (d7 << 7) + (d6 << 6) + (d5 << 5) + (d4 << 4) + (d3 << 3) + (d2 << 2) + (d1 << 1) + d0
    voltage = (value*5)/256
    temp = voltage*100
    print ("0b%d%d%d%d%d%d%d%d, value=%d, voltage=%f, temp=%f" % \
        (d7, d6, d5, d4, d3, d2, d1, d0, value, voltage, temp))
    return temp
while True:
    temp = get_temp()
    print (temp)
    dateWrite = time.strftime("%Y-%m-%d ") 
    timeWrite = time.strftime("%H:%M:%S")
    print (dateWrite,timeWrite)
    sql = ("""INSERT INTO tbl_sensors_data (sensors_data_id,sensors_temperature_data,sensors_data_date,sensors_data_time) VALUES ("",%s,%s,%s)""",(temp,dateWrite,timeWrite))
    try:
        print ("Writing to database...")
        # Execute the SQL command
        cur.execute(*sql)
        # Commit your changes in the database
        db.commit()
        print ("Write Complete")
 
    except:
        # Rollback in case there is any error
        db.rollback()
        print ("Failed writing to database")
       
    time.sleep(10)
