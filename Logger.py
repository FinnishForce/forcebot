import string
from datetime import datetime

def log(viesti, chan):
	try:
                logchan = chan +'log.txt'
    		with open(logchan, 'a+') as f:
                        f.write('\n'.encode('utf8') + datetime.now().strftime('%d-%m-%Y %H:%M:%S').encode('utf8') + " " +viesti.encode('utf8'))
  	except:
    		print "Logger error"
