import fcntl, socket, struct, dweepy, time, platform, random, math, sqlite3

from grovepi import*
#sensor ports 
dht_sensor_port = 7
ultrasonic_ranger = 4
Relay_pin = 2
potentiometer = 2
led = 5

#assigned modes
pinMode(led, "OUTPUT")
pinMode(Relay_pin, "OUTPUT")
#pinMode(button, "OUTPUT")
#pinMode(button, "INPUT")

def getUltrasonic():
	distant = ultrasonicRead(ultrasonic_ranger) #getting distance
	print distant, 'cm'
	if distant <= 10:
		digitalWrite(Relay_pin,1)
	else:
		digitalWrite(Relay_pin,0)
	return distant
def getLedFade():
	i = analogRead(potentiometer) #getting rotatory reading
	print (i)
	analogWrite(led,i/4) 
	return i
def getTemp():
	try:
		[temp,humidity] = dht(dht_sensor_port,0) #getting humidity 
		if math.isnan(temp): #nan error so return 0
			temp = 0
			return float(temp)
		else:
			return temp
	except (IOError, TypeError) as e:
		print "Error"
def getHumidity():
	try:
		[temp,humidity] = dht(dht_sensor_port,0) #getting temperature
		if math.isnan(humidity):
			humidity = 0
                        return float(humidity)
                else:
			return humidity
	except (IOError, TypeError) as e:
		print "Error" 

#def getButtonp():
 #       while True:
  #              try:
   #                     button_status = digitalRead(button)
    #                    if button_status:
     #                           digitalWrite(button, 1)
#				return 1
 #                       else:
  #                              digitalWrite(button, 0)
     #                           return 2
#		except  KeyboardInterrupt:
#			digitalWrite(button, 0)
#			break
 #               except (IOError, TypeError) as e:
  #                              print(e, "Error")



def  getOS():
	return platform.platform()

# from http://stackoverflow.com/questions/59137/getting-mac-address
def getHwAddr(ifname):
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	info = fcntl.ioctl(s.fileno(), 0x8927, struct.pack('256s', ifname[:15]))
	return ':'.join(['%02x' % ord(char) for char in info[18:24]])

def get_file(): #points to text file
	with open('thing.txt', 'r') as text:
		for sen in text:
			return sen.strip('\n')

def post(result): #posts to dweet
	thing = get_file()
	print dweepy.dweet_for(thing, result)

def getReadings():
	result = {}
        result["ultrasonic"] = getUltrasonic()
        result["ledfade"] = getLedFade()
	result["temperature"] = getTemp();
	result["humidity"] = getHumidity();
	#result["mac-address"] = getHwAddr('eth0')
	#result["operating system"] = getOS()
	
	conn = sqlite3.connect('pi.db')
	c = conn.cursor()
	c.execute('INSERT INTO sensors VALUES(?, ?, ?, ?)',(getUltrasonic(),  getLedFade(), getTemp(),  getHumidity()))
	#c.execute('SELECT * FROM sensors')
	#all_rows = c.fetchall()
	#print('1):', all_rows)
	conn.commit()

	return result

while True:
	result = getReadings();
	post(result)
	time.sleep(5)
