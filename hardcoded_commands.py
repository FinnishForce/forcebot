# -*- coding: utf-8 -*-

from __future__ import division

import json
import os
import random
from time import sleep

from api import getDrink, getMix, getTitle, getWikiaUrl, getFollowStatus, getSteamStats, getPlayerBans, convertToSteam64, getViewers
from message_sending_service import sendingService
from settings import IDENT, OWNER
from omawikipedia import wikipedia_haku
from osrs_ge import get_price


def refresh_store():
    with open("joins.txt", 'a+') as joinsfile:
        joins = joinsfile.readlines()

    store = {}

    for i in range(len(joins)):
        store.update({joins[i].strip() : ""})
        filepath = joins[i].strip()+"store"

        if os.path.isfile(filepath) and os.path.getsize(filepath) > 0:
            store2 = {  joins[i].strip() : json.load( open( filepath, "a+" ) )  }
        else:
            defaultdik = { "djalksdjlaksdjlksa" : "0" }
            json.dump( defaultdik, open(filepath, "a+") )
            store2 = {joins[i].strip() : json.load(open(filepath, "a+") )}

        store.update(store2)

    return store


def hardcoded_commands(s, chan, user, modstatus, message):

    #store = refreshStore()
    #if (chan.startswith("jtv")):
    #    store = store["jtv"]
    #else:
    #    store = store[chan]
    qlist = ["Voit luottaa siihen", "Vain juontaja tietää sen",
             "Kyllä", "Ei", "En halua kertoa",
             "Negative", "Tuohon on pakko sanoa ei", "Parempi kun jätän vastaamatta"]

    taytelista = ["ananas", "anjovis", "aurajuusto", "sudenliha", "banaani", "basilika",
                  "bbq", "broileri",
                  "cheddarjuusto", "khili", "chili (vihreä)", "chili cheese balls", "chilimajoneesi",
                  "chorizo",
                  "curry", "currymajoneesia", "edamjuusto", "fetajuusto", "herkkusieni", "härkä", "jalapeno",
                  "jalopeno",
                  "jauheliha", "juusto", "juustopizza", "jäävuorisalaatti", "kana", "kanan rintafile", "kananmuna",
                  "kananugetteja",
                  "kapris", "karamelli", "katkarapu", "kebab", "kevytjuusto", "kinkku", "kirsikkatomaatti",
                  "korianteri", "kuisma", "kuivattu tomaatti", "kukkakaali", "kurkku", "maissi", "majoneesi", "makkara",
                  "maustekurkku",
                  "maustettu häränliha", "merilevä", "mozzarella", "mozzarella-cheddarjuusto", "mozzarellajuusto",
                  "musta oliivi",
                  "mustapippuri", "mustekala", "nachoja", "naudanjauheliha", "naudanliha", "naudanlihasuikale",
                  "oliivi", "oregano",
                  "paahdettu broileri", "paahdettu pekoni", "paholaisenhillo", "paistettu herkkusieni",
                  "paistettu mehevä lohifilee",
                  "paistettu okra", "paistettu sipuli", "paistettua lampaanlihaa", "palvikinkku", "papu",
                  "parmankinkku", "parmesanjuusto",
                  "parsa", "parsakaali", "pekoni", "pepperoni", "pepperonimakkara", "persikka", "peruna", "pesto",
                  "pippurimakkara",
                  "poro", "punasipuli", "raikas salaatti", "ranskalaiset", "rucola", "rukulla vihannekset", "salaatti",
                  "salami", "salsa",
                  "savuporo", "siitakesieni", "simpukka", "sinihomejuusto", "sipuli", "sitruunaruoho", "smetana",
                  "tabasco", "talon juusto",
                  "talon tuorejuusto", "tofu", "tonnikala", "tuore basilika", "tuore herkkusieni",
                  "tuore munakoiso",
                  "tuore parsa", "tuore persilja", "tuoretomaatti", "tupla kebabliha", "tupla-valkosipuli",
                  "tuplajuusto", "tuplakatkarapu",
                  "tuplakebab", "turkinpippuri", "valkosipuli", "vihreäpepperoni", "vuohenjuusto",
                  "ylikypsä porsaanliha (pulled pork)",
                  "hiirenliha", "siika", "mursunliha", "mousen patenttijuusto", "paprika",
                  "euron kolikoita", "toukka", "suolaa", "auringonkukansiemeniä", "3x tomaatti", "3/4 osa kupopallollinen jalapenoa"]
    random.shuffle(taytelista)
    '''
    try:
        toStore = message.split()
        for word in toStore:
            try:
                store[word] += 1
            except:
                store[word] = 1
                
        if chan.startswith("jtv"):
            json.dump(store, open("jtvstore", 'wb'), sort_keys=True, indent=3)
        else:
            json.dump(store, open(chan + "store", 'wb'), sort_keys=True, indent=3)
    
        
    except Exception, exx:
        print "storing error:"
        print exx
    
    if message.startswith("!howmany "):
        try:
            dump, wordToSearch = message.split("!howmany ")
            answer = str(wordToSearch) + " has been said " + str(store[wordToSearch]) + " times in this channel"
            print "would sent" + answer
            sendingService.send_msg(s, chan, answer)
        except Exception, e:
            print "error !howmany:", e

    '''
    if message.startswith('!kysy'):
        try:
            r=0
            if "pelataan" in message:
                qlist.append("Ei pelata")
                qlist.append("Pelataan")
                r=1
            if "kokeillaan" in message:
                qlist.append("Ei kokeilla")
                qlist.append("Kokeillaan")
                r=1
            if "mennään" in message:
                qlist.append("Ei mennä")
                qlist.append("Mennään")
                r=1
            if "onko" in message and "homo" in message:
                qlist.append("Taidat itse olla homo")
            if "tulee" in message and not "paljo" in message:
                qlist.append("Ei tule")
                qlist.append("Tulee tulee")
                r=1
            if "joko" in message:
                qlist.append("Ei vielä")
                qlist.append("Wait and see")
            if "onko" in message and "paska" in message:
                qlist.append("On paska")
            if "onko" in message:
                qlist.append("On")
                qlist.append("Ei ole")
                r=1
            if "miksi" in message:
                qlist.append("Katso striimiä niin ehkä ymmärrät miksi")
            if "mistä" in message:
                qlist.append("Varmaan Turusta")
            if chan in message:
                qlist.append("Jätän vastaamatta suojatakseni juontajan yksityisyyttä")
            if "paljo" in message or "monta" in message:
                qlist.append("Veikkaan että "+str(random.randint(0, 150)))
            if "tyhmä" in message:
                qlist.append("Kysymyksen kysyjä taitaa olla tyhmempi")
            if "huono" in message:
                qlist.append("On huono")
                qlist.append("Ei ole huono")
            if r==1:
                qlist.remove("Kyllä")
                qlist.remove("Ei")
            random.shuffle(qlist)
            random.shuffle(qlist)
            random.shuffle(qlist)
            sendingService.send_msg(s, chan, random.choice(qlist))
        except Exception, e:
            print "error !kysy:", e

    if message.startswith('!randomgame'):
        try:
            with open('gamelist.txt', 'a+') as f:
                pelilista = json.load(f)
            sendingService.send_msg(s, chan, random.choice(pelilista))
        except Exception, e:
            print "randomgame error", e

    if message.startswith('!täytteet'):
        try:
            tayteamount = random.randint(2, 5)
            tayte = []
            for x in range(tayteamount):
                tayte.append(random.choice(taytelista))
                taytelista.remove(tayte[x])
            taytteet = ', '.join(tayte)
            sendingService.send_msg(s, chan, taytteet)
        except Exception, e:
            print "täytteet error"
            print e

    if message.startswith('!juoma'):
        try:
            nimi, hinta, tyyppi, tuotenumero = getDrink()
            resp = nimi + " (" + tyyppi + ") (" + str(hinta) + "€)"# https://www.alko.fi/tuotteet/" + str(
                #tuotenumero) + "/"
            sendingService.send_msg(s, chan, resp)
        except Exception, e:
            print "!juoma error", e

    if message.startswith('!drinkki'):
        try:
            nimi1, lhinta1, tyyppi1 = getMix()
            nimi2, lhinta2, tyyppi2 = getMix()
            maara1 = str(random.randint(1, 10))
            maara2 = str(random.randint(1, 10))
            maara1 = maara1.replace(",", ".")
            maara2 = maara2.replace(",", ".")
            lhinta1, lhinta2 = lhinta1.replace(",", "."), lhinta2.replace(",", ".")
            hinta1 = float(lhinta1) * float(maara1) * 0.01
            hinta2 = float(lhinta2) * float(maara2) * 0.01
            totalhinta = float(hinta1) + float(hinta2)
            totalhinta = str(round(totalhinta, 2))
            resp = "{0}cl {1} ({2}) ja {3}cl {4} ({5}), annoksen hinta: {6} €".format(maara1, nimi1, tyyppi1, maara2,
                                                                                      nimi2, tyyppi2, totalhinta)
            sendingService.send_msg(s, chan, resp)
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
            sendingService.send_msg(s, chan, resp)
        except Exception, e:
            print "!title error "
            print e

    if message.startswith("!wikipedia "):
        try:
            a, rest = message.split("!wikipedia ")
            try:
                lang, title = rest.split(" ", 1)
                title = title
                lang = lang
            except:
                title = rest
                lang = "en"

            sendingService.send_msg(s, chan, wikipedia_haku(title, lang))
        except:
            print "wikipedia fake error"

    if message.startswith("!wiki "):
        try:
            a, rest = message.split("!wiki ")
            site, title = rest.split("-", 1)
            resp = getWikiaUrl(site, title)
            sendingService.send_msg(s, chan, resp)
        except Exception, e:
            print "error at !wiki: "
            print e

    if message.startswith("!lolwiki "):
        try:
            a, title = message.split("!lolwiki ")
            resp = getWikiaUrl("lolwiki", title)
            sendingService.send_msg(s, chan, resp)
        except Exception, e:
            print "error at !lolwiki: "
            print e

    if message.startswith("!rswiki "):
        try:
            a, title = message.split("!rswiki ")
            resp = getWikiaUrl("rswiki", title)
            sendingService.send_msg(s, chan, resp)

        except Exception, e:
            print "error at !rswiki: "
            print e

    if message.startswith("!hswiki "):
        try:
            a, title = message.split("!hswiki ")
            resp = getWikiaUrl("hswiki", title)
            sendingService.send_msg(s, chan, resp)
        except Exception, e:
            print "error at !hswiki: "
            print e

    if message.startswith("!randoms"):
        try:
            start, end = 1, 20
            roll = random.randint
            rnd1, rnd2, rnd3 = roll(start, end), roll(start, end), roll(start, end)
            while rnd1 == rnd2 or rnd1 == rnd3 or rnd2 == rnd3:
                rnd1, rnd2, rnd3 = roll(start, end), roll(start, end), roll(start, end)
            sendingService.send_msg(s, chan, (str(rnd1) + " " + str(rnd2) + " " + str(rnd3)))
        except Exception, e:
            print e

    if message.startswith("!followstatus"):
        try:
            sent = 0
            try:
                asd, name = message.split("!followstatus ")
                try:
                    name, difchan = name.split(" ", 1)
                    sendingService.send_msg(s, chan, getFollowStatus(name, difchan))
                    sent = 1
                except:
                    pass
                if sent == 0:
                    sent = 1
                    sendingService.send_msg(s, chan, getFollowStatus(name, chan))
            except:
                pass
            if sent == 0:
                sendingService.send_msg(s, chan, getFollowStatus(user, chan))
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
                    sendingService.send_msg(s, chan, getFollowStatus(name, difchan))
                    sent = 1
                except:
                    pass
                if sent == 0:
                    sent = 1
                    sendingService.send_msg(s, chan, getFollowStatus(name, chan))
            except:
                pass
            if sent == 0:
                sendingService.send_msg(s, chan, getFollowStatus(user, chan))
            sleep(1)
        except:
            print "follows error"

    if message.startswith("!followage"):
        try:
            sent = 0
            try:
                asd, name = message.split("!followage ")
                try:
                    name, difchan = name.split(" ", 1)
                    sendingService.send_msg(s, chan, getFollowStatus(name, difchan))
                    sent = 1
                except:
                    pass
                if sent == 0:
                    sent = 1
                    sendingService.send_msg(s, chan, getFollowStatus(name, chan))
            except:
                pass
            if sent == 0:
                sendingService.send_msg(s, chan, getFollowStatus(user, chan))
            sleep(1)
        except:
            print "followage error"

    if message.startswith("!randomviewer"):
        try:
            viewerlist, vieweramount = getViewers(chan)
            try:
                viewerlist.remove(OWNER)
                viewerlist.remove(IDENT)
                vieweramount -= 2
            except Exception, e:
                print "viewerlist remove error"
                print e
            chosenone = random.choice(viewerlist)

            chance = (1.0 / float(vieweramount)) * 100
            followStatus = getFollowStatus(chosenone, chan)
            resp = "Viewers in: " + str(vieweramount) + ", chance to win: " + str(
                round(chance, 2)) + "%, winner: " + chosenone + " (" + followStatus + ")"
            sendingService.send_msg(s, chan, resp)
            sleep(1)

        except Exception, e:
            print "Error random viewer"
            print e

    if message.startswith("!rаndomviewer"):
        try:
            viewerlist, vieweramount = getViewers(chan)
            chance = (1.0 / float(vieweramount)) * 100
            with open("winner.txt", 'r') as f:
                winner = f.readlines()[0]
            followStatus = getFollowStatus(winner, chan)
            resp = "Viewers in: " + str(vieweramount) + ", chance to win: " + str(
                round(chance, 2)) + "%, winner: " + winner + " (" + followStatus + ")"
            sendingService.send_msg(s, chan, resp)
        except Exception, e:
            print "wetnis viewer error", e
            
    if message.startswith("!setwinner ") and user == OWNER:
        try:
            dump, winner = message.split("!setwinner ")
            with open("winner.txt", 'w') as f:
                f.write(winner)

        except Exception, e:
            print "setwinner error", e

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

            r = random.randint(a, b)
            resp = "You got " + str(r) + " (" + str(a) + "-" + str(b) + ")"
            sendingService.send_msg(s, chan, resp)
        except:
            print "rng error"

    if message.startswith("!pyramid") and (user == OWNER or user == chan):
        try:
            a, b = message.split('!pyramid')
            temp = b
            sendingService.send_msg(s, chan, temp)
            temp = b + b
            sendingService.send_msg(s, chan, temp)
            temp = b + b + b
            sendingService.send_msg(s, chan, temp)
            temp = b + b
            sendingService.send_msg(s, chan, temp)
            temp = b
            sendingService.send_msg(s, chan, temp)
        except Exception, e:
            print "pyramid error ", e

    if message.startswith("!adminspeak") and user == OWNER:
        try:
            unused, chan_msg = message.split('!adminspeak')
            ch, mg = chan_msg.split(' ', 1)
            sendingService.send_msg(s, ch, mg)
        except Exception, e:
            print "error adminspeak ", e

    if message.startswith("!csfind "):
        try:
            unused, steam_id = message.split('!csfind ')
            steam_id = str(steam_id)
            if steam_id.startswith("7656119"):
                resp = getSteamStats(steam_id)
            else:
                resp = getSteamStats(convertToSteam64(steam_id))

            sendingService.send_msg(s, chan, resp)
        except Exception, e:
            print "error in csfind ", e

    if message.startswith("!vac "):
        try:
            unused, steam_id = message.split('!vac ')
            steam_id = str(steam_id)
            if steam_id.startswith("7656119"):
                resp = getPlayerBans(steam_id)
            else:
                resp = getPlayerBans(convertToSteam64(steam_id))

            sendingService.send_msg(s, chan, resp)
        except Exception, e:
            print "error in vac ", e

    if message.startswith("!ge "):
        try:
            unused, searchterm = message.split('!ge ', 1)
            hinta = get_price(searchterm)
            sendingService.send_msg(s, chan, hinta)
        except Exception, e:
            print "mortsin ge error"
            print e

    if message.startswith("!color "):
        try:
            unused, color = message.split('!color', 1)
            resp = "/color " + color
            sendingService.send_msg(s, chan, resp)
        except Exception, e:
            print "error in !color ", e
