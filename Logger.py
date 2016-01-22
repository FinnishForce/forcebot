import string
from datetime import datetime

def log(viesti, chan):
	try:
    		f = open(chan +'log.txt', 'a+')
    		f.write('\n'.encode('utf8') + datetime.now().strftime('%d-%m-%Y %H:%M:%S').encode('utf8') + " " +viesti.encode('utf8'))
    		f.close()
  	except:
    		print "Logger error"
