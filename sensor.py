import RPIO, time, os, urllib2

API_URL = "https://securitysystem.herokuapp.com/sensors/1234/trip"
RPIO.setmode(RPIO.BCM)
THRESHOLD = 3

def RCtime (RCpin):
	reading = 0
	RPIO.setup(RCpin, RPIO.OUT)
	RPIO.output(RCpin, RPIO.LOW)
	time.sleep(0.1)

	RPIO.setup(RCpin, RPIO.IN)
	while (RPIO.input(RCpin) == RPIO.LOW):
		reading += 1
	return reading

time.sleep(2.0)

#handle basic http auth
mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
mgr.add_password(None, API_URL, 'pi', 'jake=hacker')
handler = urllib2.HTTPBasicAuthHandler(mgr)
opener = urllib2.build_opener(handler)
urllib2.install_opener(opener)

while True:
	val = RCtime(18)
	print val
	if val > THRESHOLD:
		try:
			urllib2.urlopen(API_URL)
		except urllib2.HTTPError as e:
			print "HTTP Error! Code:", e.code
			time.sleep(2.0)
		except urllib2.URLError as e:
			print "URL Error!:", e
			time.sleep(2.0)
		else: 
			time.sleep(1.0)



