# -*- coding: utf-8 -*-

from __future__ import division
from subprocess import PIPE, Popen
from random import randint
import psutil

def refreshCmds():
  with open("joins.txt", 'a+') as joinsfile:
    joins = joinsfile.readlines()

  dik = {}

  for i in range(len(joins)):
    dik.update({joins[i].strip() : ""})
    dik2 = {joins[i].strip() : json.load(open(joins[i].strip()+"commands", "r"))}
    dik.update(dik2)


from Api import *
from Socket import *
from Read import *
from omawikipedia import *
from osrs_ge import *

def readPidFile():
  with open('my_pid', 'r') as f:
        pid = f.read()
  return pid

def writeQuitFile(chan):
  with open('quited', 'w') as f:
        f.write(chan)

def get_cpu_temperature():
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
    output, _error = process.communicate()
    return float(output[output.index('=') + 1:output.rindex("'")])

def tryCommands(s, chan, user, modstatus, message):
    import os
    import subprocess
    from time import sleep, time, mktime
    from datetime import datetime, timedelta
    from Init import joinRoom
    from Logger import log
    from Settings import IDENT, owner
    
    qlist = ["Varmasti", "Voit luottaa siihen", "Vain juontaja tietää sen", "Melko varmasti",
	    "Kyllä", "Ei", "En osaa sanoa", "Ehkä, ehkä ei",
	    "Negative", "Tuohon on pakko sanoa ei", "Epäilen", "Mietippä sitä autisti"]    

    taytelista = [ "ananas",  "anjovis",  "aurajuusto", "sudenliha", "aurinkokuivattu tomaatti",  "banaani",  "basilika",  "bbq",  "broileri",
                   "cheddarjuusto",  "chili",  "chili (vihreä)",  "chili cheese balls",  "chilimajoneesi",  "chilimajoneesia",  "chorizo",
                   "curry",  "currymajoneesia",  "edamjuusto",  "fetajuusto",  "herkkusieni",  "härkä",  "jalapeno",  "jalopeno",
                   "jauheliha",  "juusto",  "juustopizza",  "jäävuorisalaatti",  "kana",  "kanan rintafile",  "kananmuna",  "kananugetteja",
                   "kapris",  "karamelli",  "katkarapu",  "kebab",  "kebabliha",  "kevytjuusto",  "kinkku",  "kirsikkatomaatti",
                   "korianteri",  "kuisma", "kuivattu tomaatti",  "kukkakaali",  "kurkku",  "maissi",  "majoneesi",  "makkara",  "maustekurkku",
                   "maustettu häränliha",  "merilevä",  "mozzarella",  "mozzarella-cheddarjuusto",  "mozzarellajuusto",  "musta oliivi",
                   "mustapippuri",  "mustekala",  "nachoja",  "naudanjauheliha",  "naudanliha",  "naudanlihasuikale",  "oliivi",  "oregano",
                   "paahdettu broileri",  "paahdettu pekoni",  "paholaisenhillo",  "paistettu herkkusieni",  "paistettu mehevä lohifilee",
                   "paistettu okra",  "paistettu sipuli",  "paistettua lampaanlihaa",  "palvikinkku",  "papu",  "parmankinkku",  "parmesanjuusto",
                   "parsa",  "parsakaali",  "pekoni",  "pepperoni",  "pepperonimakkara",  "persikka",  "peruna",  "pesto",  "pippurimakkara",
                   "poro",  "punasipuli",  "raikas salaatti",  "ranskalaiset",  "rucola",  "rukulla vihannekset",  "salaatti",  "salami",  "salsa",
                   "savuporo",  "siitakesieni",  "simpukka",  "sinihomejuusto",  "sipuli",  "sitruunaruoho",  "smetana",  "tabasco",  "talon juusto",
                   "talon tuorejuusto",  "tofu",  "tomaatti",  "tonnikala",  "tuore basilika",  "tuore herkkusieni",  "tuore munakoiso",
                   "tuore parsa",  "tuore persilja",  "tuoretomaatti",  "tupla kebabliha",  "tupla-valkosipuli",  "tuplajuusto",  "tuplakatkarapu",
                   "tuplakebab",  "turkinpippuri",  "valkosipuli",  "vihreäpepperoni",  "vuohenjuusto",  "ylikypsä porsaanliha (pulled pork)",
                   "tuolijakkara",  "hiirenliha",  "siika",  "mursunliha",  "mousen patenttijuusto",  "paprika" ]
    num = 0
    addc = 0
    ismod = 0
    delc = 0
    exists = 0
    worked = 0
    approved = [owner, 'mmorz', 'bulftrik']
    
    delthis = ""      
    if message.startswith('!kysy'):
	try:
	    sendChanMsg(s, chan, random.choice(qlist))
	except Exception, e:
	    print "error !kysy:", e
    
    if message.startswith('!amount '):
      try:
        
        try:
          a, lookup = message.split("!amount ")
        except:
          print "error"
          
        num = 0
        
        with open(chan+'log.txt', 'r') as searchFile:
            first_line = searchFile.readlines()[2]
            with open(chan+'log.txt', 'r') as file:
                for line in file:
                    if lookup.lower() in line.lower():
                        num = num + line.lower().count(lookup.lower())
            timestring1, timestring2, b = first_line.split(' ', 2)
            timestring = timestring1 + " " + timestring2
          
            timestamp = datetime.now() - datetime.strptime(timestring, "%d-%m-%Y %H:%M:%S" )
          
            timestamp, useless= str(timestamp).split('.')
            t1, t2, t3 = timestamp.split(":")
            timestamp = t1 + "h " + t2 + "m " + t3 + "s "
            resp =  str(lookup) + " count during last " + str(timestamp) + ": " + str(num)
            sendChanMsg(s, chan, resp)
      except Exception, e:
        print "!amount error"
        print e

    if message.startswith('!täytteet'):
        try:
            tayteamount = randint(2, 5)
            tayte = []
            for x in range(tayteamount):
                tayte.append(random.choice(taytelista))
                taytelista.remove(tayte[x])
            taytteet = ', '.join(tayte)
            sendChanMsg(s, chan, taytteet)
        except Exception, e:
            print "täytteet error"
            print e
    
    if message == '!juoma':
	try:
	    nimi, hinta, tyyppi, tuotenumero = getDrink()
	    resp = nimi + " (" + tyyppi + ") (" + str(hinta) + "€) https://www.alko.fi/tuotteet/" + str(tuotenumero) + "/"
	    sendChanMsg(s, chan, resp)
	except Exception, e:
	    print "!juoma error", e

    if message.startswith('!drinkki '):
	try:
	    nimi1, lhinta1, tyyppi1 = getMix()
	    nimi2, lhinta2, tyyppi2 = getMix()
	    maara1 = str(randint(1,10))
	    maara2 = str(randint(1,10))
	    maara1 = maara1.replace(",", ".")
	    maara2 = maara2.replace(",", ".")
	    lhinta1, lhinta2 = lhinta1.replace(",", "."), lhinta2.replace(",", ".")
	    hinta1 = float(lhinta1) * float(maara1) * 0.01
	    hinta2 = float(lhinta2) * float(maara2) * 0.01
	    totalhinta = float(hinta1)+float(hinta2)
	    totalhinta = str(round(totalhinta, 2))
	    resp = "{0}cl {1} ({2}) ja {3}cl {4} ({5}), annoksen hinta: {6} €".format(maara1, nimi1, tyyppi1, maara2, nimi2, tyyppi2, totalhinta)
	    sendChanMsg(s, chan, resp)
	except Exception, e:
	    print "drink error", e

    if message.startswith('!title'):
      try:
        try:
          a, thisChan = message.split("!title ")
        except:
          thisChan = chan

        title = getTitle(thisChan)
        resp = "[" + thisChan + "] " + title
        sendChanMsg( s, chan, resp )
      except Exception, e:
        print "!title error "
        print e
    
    #if ("word1" and "word2") in message:
    #  sendChanMsg(s, owner, message)
    
    if message.startswith('!modtest'):
        if modstatus or user == chan or user in approved:
            sendChanMsg(s, chan, "kuseless mod")
        else:
            sendChanMsg(s, chan, "fail")

    if message.startswith("!pid"):
        try:
            resp = "Process id: " + str( os.getpid() )
            sendChanMsg( s, chan, resp )
        except:
            print "error pid"
    
    if message.startswith("!loltest"):
        try:
            a, splitted = message.split("!loltest ")
            
            try:
                name, server = splitted.split("s:")
                name = str(name).strip().lower()
                server = str(server).strip().lower()
            except:
                name = str(splitted).strip()
                server = "euw"

            summonerid = getLeagueSummonerId(server, name)
            summonerid = str(summonerid)
            resp = getLeagueLastGame(server, name, summonerid)
            sendChanMsg(s, chan, resp)
        except:
            print "lolid error"
            
    if message.startswith("!wikipedia "):
        try:
            a, rest = message.split("!wikipedia ")
            try:
                lang, title = rest.split(" ", 1)
                title = title.strip()
                lang = lang.strip()
            except:
                title = rest.strip()
                lang = "en"
            
            sendChanMsg(s, chan, wikipedia_haku(title, lang))
        except:
            print "wikipedia fake error"

    if message.startswith("!wiki "):
        try:
            a, rest = message.split("!wiki ")
            site, title = rest.split("-", 1)
            resp = getWikiaUrl(site.strip(), title.strip())
            sendChanMsg(s, chan, resp)
        except Exception, e:
            print "error at !wiki: "
            print e

    if message.startswith("!lolwiki "):
        try:
            a, title = message.split("!lolwiki")
            resp = getWikiaUrl("lolwiki", title.strip())
            sendChanMsg(s, chan, resp)
        except Exception, e:
            print "error at !lolwiki: "
            print e

    if message.startswith("!rswiki "):
        try:
            a, title = message.split("!rswiki")
            title = title.strip()
            resp = getWikiaUrl("rswiki", title)
            sendChanMsg(s, chan, resp)

        except Exception, e:
            print "error at !rswiki: "
            print e

    if message.startswith("!hswiki "):
        try:
            a, title = message.split("!hswiki")
            resp = getWikiaUrl("hswiki", title.strip())
            sendChanMsg(s, chan, resp)
        except Exception, e:
            print "error at !hswiki: "
            print e

    if message.startswith("!randoms"):
        try:
            start, end = 1, 20
            rnd1, rnd2, rnd3 = randint(start, end), randint(start, end), randint(start, end)
            while rnd1 == rnd2 or rnd1 == rnd3 or rnd2 == rnd3:
                rnd1, rnd2, rnd3 = randint(start, end), randint(start, end), randint(start, end)
            sendChanMsg(s, chan, (str(rnd1) + " " + str(rnd2) + " " + str(rnd3)))
        except Exception, e:
            print e

    if message.startswith("!followstatus"):            
	try:
	    sent = 0
	    try:
		asd, name = message.split("!followstatus ")
		try:
			name, difchan = name.split(" ", 1)
			sendChanMsg(s, chan, getFollowStatus(name, difchan))
			sent = 1
		except:
			pass
		if sent == 0:
			sent = 1
			sendChanMsg(s, chan, getFollowStatus(name, chan))
	    except:
		pass
	    if sent == 0:
		sendChanMsg(s, chan, getFollowStatus(user, chan))
	    sleep(1)
	except:
	    print "followstatus error"

    if message.startswith("!follows") and not message.startswith("!followstatus"):
        try:
            sent = 0
            try:
                asd, name = message.split("!follows ")
                try:
                        name, difchan = name.split(" ", 1)
                        sendChanMsg(s, chan, getFollowStatus(name, difchan))
                        sent = 1
                except:
                        pass
                if sent == 0:
                        sent = 1
                        sendChanMsg(s, chan, getFollowStatus(name, chan))
            except:
                pass
            if sent == 0:
                sendChanMsg(s, chan, getFollowStatus(user, chan))
            sleep(1)
        except:
            print "follows error"



    if message.startswith("!randomviewer"):
        try:
            viewerlist = []
            viewerlist, vieweramount = getViewers(chan)
            try:
                viewerlist.remove(owner)
                viewerlist.remove(IDENT)
                vieweramount -= 2
            except Exception, e:
                print "viewerlist remove error"
                print e
            chosenone = random.choice(viewerlist)

            chance = ( 1.0/float(vieweramount) ) * 100
	    followStatus = getFollowStatus(chosenone, chan)
            resp0 = "Viewers in: " + str(vieweramount) + ", chance to win: " + str( round(chance,2) ) + "%, winner: " + chosenone + " (" + followStatus + ")"
            sendChanMsg(s, chan, resp0)
	    sleep(1)

        except Exception, e:
            print "Error random viewer"
            print e

    if message.startswith("!rаndomviewer"):
	try:
		viewerlist, vieweramount = getViewers(chan)
		chance = ( 1.0/float(vieweramount) ) * 100
		resp0 = "Viewers in: " + str(vieweramount) + ", chance to win: " + str( round(chance,2) ) + "%, winner: wetnis"
		sendChanMsg(s, chan, resp0)
	except:
		print "wetnis viewer error"

    if message.startswith("!restartbot"):
        try:
          if (user == owner) or (modstatus) or (user == chan):
            writeQuitFile(chan)
            killthis = readPidFile()
            killthis = int(killthis)
            os.kill(killthis, 15)
            sendChanMsg(s, chan, "restarting...")
            subprocess.call(["cd /home/pi/Desktop/ForceBotti"], shell=True)
            subprocess.call(["sudo python Run.py"], shell=True)
        except Exception, e:
            print "softreseterror"
            print e
            
    if message.startswith("!rng ") or message.startswith("!random "):
        try:
          if message.startswith("!rng"):
            u, a = message.split("!rng ")
          if message.startswith("!random"):
            u, a = message.split("!random ")
          a, b = a.split(" ")
          a = int(a)
          b = int(b)
            
          if a > b:
              a, b = b, a
          elif b > a:
              pass
                
          r = randint(int(a), int(b))
          resp = "You got " + str(r) + " (" + str(int(a)) + "-" + str(int(b)) + ")"
          sendChanMsg(s, chan, resp)
        except:
          print "rng error"
          log("error rng", "globalerror")
    
    if message.startswith("!joinlobby"):
        try:
            resp = getJoin()
            sendChanMsg(s, chan, resp)
        except:
            print "!join error wot"
            log("error joinlobby", "globalerror")
    
    if message.startswith("!botjoin"):
        try:
            try:
                a, joinhere = message.split("!botjoin ")
                resp = "joined #" + joinhere
            except:
                joinhere = user
                resp = ("joined #" + joinhere)
                sendChanMsg(s, chan, resp)
            if joinhere.startswith("#"):
                joinhere = joinhere.replace("#", '')
                joinChan(s, joinhere)
          
            killthis = readPidFile()
            killthis = int(killthis)
            os.kill(killthis, 15)
            subprocess.call(["cd /home/pi/Desktop/ForceBotti"], shell=True)
            subprocess.call(["sudo python Run.py"], shell=True)
                                                
        except Exception, e:
            print "botjoin error ", e

    if message.startswith("!botquit"):
        try:
            try:
                a, quithere = message.split("!botquit ")
                resp = "leaving from #" + quithere
            except:
                quithere = user
                resp = ("leaving from #" + quithere + ", goodbye")
            sendChanMsg(s, chan, resp)
            if quithere.startswith("#"):
                quithere = quithere.replace("#", '')
                quitChan(s, quithere)
        except Exception, e:
            print "botquit error ", e

    if message.startswith("!cpustats"):
        try:
            cpu_temperature = get_cpu_temperature()
            cpu_usage = psutil.cpu_percent()
            resp1 = "CPU usage: " + str(cpu_usage) + "%" + " | CPU temperature: " +  str(cpu_temperature) + "C"
            sendChanMsg(s, chan, resp1)

        except Exception, e:
            print "cpustatserror ", e


    if message.startswith("!killbot"):
        if (user == owner) or (user in approved):
            try:
                writeQuitFile(chan)
                sendChanMsg(s, chan, "riPepperonis bot, waking from dead in 1-2 min")
                restartbot()
            except Exception, e:
                print "error in restartbotrun.py ", e

    if message.startswith("!pyramid"):
        try:
            if user == owner or user == chan:
                a, b = message.split('!pyramid')
                temp = b
                sendChanMsg(s, chan, temp)
                temp = b+b
                sendChanMsg(s, chan, temp)
                temp = b+b+b
                sendChanMsg(s, chan, temp)
                temp = b+b+b+b
                sendChanMsg(s, chan, temp)
                temp = b+b+b
                sendChanMsg(s, chan, temp)
                temp = b+b
                sendChanMsg(s, chan, temp)
                temp = b 
                sendChanMsg(s, chan, temp)
        except Exception, e:
            print "pyramid error ", e

    if message.startswith("!adminspeak"):
        try:
            if user == owner:
                a, b = message.split('!adminspeak')
                b = b.strip()
                c, m = b.split(' ', 1)
                sendChanMsg(s, c, m)
        except Exception, e:
            print "error adminspeak ", e


    if message.startswith("!csfind"):
        try:
            a, b = message.split('!csfind')
            b = b.strip()
            b = str(b)
            if b.startswith("7656119"):
                resp = getSteamStats(b)
            else:
                b = convertToSteam64(b)
                resp = getSteamStats(b)

            sendChanMsg(s, chan, resp)
        except Exception, e:
            print "error in csfind ", e

    if message.startswith("!vac"):
        try:
            a, b = message.split('!vac')
            b = b.strip()
            b = str(b)
            if b.startswith("7656119"):
                resp = getPlayerBans(b)
            else:
                b = convertToSteam64(b)
                resp = getPlayerBans(b)

            sendChanMsg(s, chan, resp)
        except Exception, e:
            print "error in vac ", e

    if message.startswith("!laststats"):
        try:
            resp = getSteamStats("76561198185015081")
            sendChanMsg(s, chan, resp)
        except Exception, e:
            print "laststat error hapnd ", e

    if message.startswith("!tussarikills"):
        try:      
            b = "76561198185015081"
            b = b.strip()
            b = str(b)
            
            if b.startswith("7656119"):
                resp = getTussariKills(b)
            else:
                b = convertToSteam64(b)
                resp = getTussariKills(b)

            sendChanMsg(s, chan, resp)
        except Exception, e:
            print "tussarikill (hukka) error hapnd ", e

    if message.startswith("!mytussarikills"):
        try:      
            a, b = message.split('!mytussarikills')
            b = b.strip()
            b = str(b)
            
            if b.startswith("7656119"):
                resp = getTussariKills(b)
            else:
                b = convertToSteam64(b)
                resp = getTussariKills(b)

            sendChanMsg(s, chan, resp)
        except Exception, e:
            print "tussarikill (general) error hapnd ", e

    if message.startswith("!kills"):
        try:      
            a, wpn = message.split('!kills')
            b = "76561198185015081"
            b = b.strip()
            b = str(b)
            
            if b.startswith("7656119"):
                resp = getKills(b, wpn)
            else:
                b = convertToSteam64(b)
                resp = getKills(b, wpn)

            sendChanMsg(s, chan, resp)
        except Exception, e:
            print "kills (hukka) error hapnd ", e

    if message.startswith("!ge "):
        try:
            a, searchterm = message.split('!ge ', 1)
            hinta = get_price(searchterm)
            sendChanMsg(s, chan, hinta)
        except Exception, e:
            print "mortsin ge error"
            print e

    if message.startswith("!mykills"):
        try:      
            a, b, wpn = message.split(' ')
            b = b.strip()
            b = str(b)
            wpn = wpn.strip()
            
            if b.startswith("7656119"):
                resp = getKills(b, wpn)
            else:
                b = convertToSteam64(b)
                resp = getKills(b, wpn)

            sendChanMsg(s, chan, resp)
        except Exception, e:
            print "mykills error hapnd ", e


    if message.startswith("!color "):
        try:
            a, b = message.split('!color')
            saythis = "/color " + b.strip()
            sendChanMsg(s, chan, saythis)
        except Exception, e:
            print "error in !color ", e



