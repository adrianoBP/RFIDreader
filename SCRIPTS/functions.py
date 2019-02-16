import datetime


DBpath = "../DB/accesses.sqlite"
pathLogOffline = "../LOGS/databaseOffline.log"
pathLogNotRecognized = "../LOGS/notRecognized.log"


def cycle(cb):
	import RPi.GPIO as GPIO
	import serial
	import time
	import os
	pinoutGreen = 24
	pinoutRed = 26
	GPIO.setmode(GPIO.BOARD)
	GPIO.setwarnings(False)
	GPIO.setup(pinoutGreen, GPIO.OUT)
	GPIO.output(pinoutGreen, False)
	GPIO.setup(pinoutRed, GPIO.OUT)
	GPIO.output(pinoutRed, False)
	serialport = serial.Serial("/dev/ttyAMA0",9600)
	serialport.close()
	serialport.open()
	msg = "In attesa di scansione ..."
	code = ""
	count = 0
	def getID(code):
		c = 0
		approved = False
		approved2 = False
		delim = u"\u0003"
		temp = code
		code = ""
		for i in temp:
			if approved2:
				if not i == delim:
					code+=i
				else :
					if len(code) == 12:
						break
					else:
						code = ""
			if i == u"\u0002" and approved and c==3:
				approved2 = True
			if i == delim:
				approved = True
				c+=1
		
		line = "Scansionato RFID con ID: " + code + " - Date: "+ str(datetime.datetime.now()) + "\n"
		print line
		cbResult = cb(code)
		delay = float(cbResult['delay'])
		serialport.close()
		pin = ""
		if cbResult['color'] == "green":
			pin = pinoutGreen
		else:
			pin = pinoutRed
		GPIO.output(pin,True)
		time.sleep(delay)
		GPIO.output(pin,False)
		serialport.open()
		print "\n" + msg
	print msg
	while True:
		char = serialport.read()
		if count <55:	
			code+=char
			count+=1
		else:
			if count == 55:
				getID(code)
			code = ""	
			count = 0

def rfidExists(code):
	queryRes = dbQuery('SELECT COUNT(*) FROM rfids WHERE code=?', [code])
	queryRes = queryRes['data'][0][0]
	if queryRes == 0:
		return False
	else:
		return True

def dbQuery(queryString, data):
	import sqlite3
	import os.path
	if not os.path.isfile(DBpath):
		 raise Exception('ERRORE: database non presente.')
	connection = sqlite3.connect(DBpath)
	cursor = connection.cursor()
	cursor.execute(queryString, data)
	queryRes = cursor.fetchall()
	res = {'data':queryRes, 'rowcount':cursor.rowcount}
	connection.commit()
	connection.close()
	return res

def logAccessOffline(code):
	try:
		line = "ID: " + code + " - Date: "+str(datetime.datetime.now())+"\n"
		log = open(pathLogOffline, 'a')
		log.write(line)
		log.close()
		return True
	except:
		return False
def logAccessNotRecognized(code):
	try:
		line = "ID: " + code + " - Date: "+ str(datetime.datetime.now()) + "\n"
		log = open(pathLogNotRecognized, 'a')
		log.write(line)
		log.close()
		return True
	except:
		return False
