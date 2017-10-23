import string

def log(lista, chan):
	try:
                logchan = chan +'log.txt'
    		with open(logchan, 'a+') as f:
		    for thing in lista:
                        f.write(thing+"\n")
  	except:
    		print "Logger error"
