# -*- coding: utf-8 -*-

from __future__ import division

from Api import *
from Socket import *
from omawikipedia import wikipedia_haku
from osrs_ge import *
import random

def tryCommands(s, chan, user, modstatus, message):
    from time import sleep
    from Settings import IDENT, OWNER

    qlist = ["Varmasti", "Voit luottaa siihen", "Vain juontaja tietää sen", "Melko varmasti",
             "Kyllä", "Ei", "En osaa sanoa", "Ehkä, ehkä ei",
             "Negative", "Tuohon on pakko sanoa ei", "Epäilen", "Mietippä sitä autisti"]

    taytelista = ["ananas", "anjovis", "aurajuusto", "sudenliha", "aurinkokuivattu tomaatti", "banaani", "basilika",
                  "bbq", "broileri",
                  "cheddarjuusto", "chili", "chili (vihreä)", "chili cheese balls", "chilimajoneesi", "chilimajoneesia",
                  "chorizo",
                  "curry", "currymajoneesia", "edamjuusto", "fetajuusto", "herkkusieni", "härkä", "jalapeno",
                  "jalopeno",
                  "jauheliha", "juusto", "juustopizza", "jäävuorisalaatti", "kana", "kanan rintafile", "kananmuna",
                  "kananugetteja",
                  "kapris", "karamelli", "katkarapu", "kebab", "kebabliha", "kevytjuusto", "kinkku", "kirsikkatomaatti",
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
                  "talon tuorejuusto", "tofu", "tomaatti", "tonnikala", "tuore basilika", "tuore herkkusieni",
                  "tuore munakoiso",
                  "tuore parsa", "tuore persilja", "tuoretomaatti", "tupla kebabliha", "tupla-valkosipuli",
                  "tuplajuusto", "tuplakatkarapu",
                  "tuplakebab", "turkinpippuri", "valkosipuli", "vihreäpepperoni", "vuohenjuusto",
                  "ylikypsä porsaanliha (pulled pork)",
                  "tuolijakkara", "hiirenliha", "siika", "mursunliha", "mousen patenttijuusto", "paprika"]

    approved = [OWNER, 'mmorz', 'bulftrik']

    if message.startswith('!kysy'):
        try:
            sendChanMsg(s, chan, random.choice(qlist))
        except Exception, e:
            print "error !kysy:", e

    if message.startswith('!randomgame'):
        try:
            with open('gamelist.txt', 'a+') as f:
                pelilista = json.load(f)
            sendChanMsg(s, chan, random.choice(pelilista))
        except Exception, e:
            print "randomgame error", e


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

    if message.startswith('!juoma'):
        try:
            nimi, hinta, tyyppi, tuotenumero = getDrink()
            resp = nimi + " (" + tyyppi + ") (" + str(hinta) + "€) https://www.alko.fi/tuotteet/" + str(
                tuotenumero) + "/"
            sendChanMsg(s, chan, resp)
        except Exception, e:
            print "!juoma error", e

    if message.startswith('!drinkki'):
        try:
            nimi1, lhinta1, tyyppi1 = getMix()
            nimi2, lhinta2, tyyppi2 = getMix()
            maara1 = str(randint(1, 10))
            maara2 = str(randint(1, 10))
            maara1 = maara1.replace(",", ".")
            maara2 = maara2.replace(",", ".")
            lhinta1, lhinta2 = lhinta1.replace(",", "."), lhinta2.replace(",", ".")
            hinta1 = float(lhinta1) * float(maara1) * 0.01
            hinta2 = float(lhinta2) * float(maara2) * 0.01
            totalhinta = float(hinta1) + float(hinta2)
            totalhinta = str(round(totalhinta, 2))
            resp = "{0}cl {1} ({2}) ja {3}cl {4} ({5}), annoksen hinta: {6} €".format(maara1, nimi1, tyyppi1, maara2,
                                                                                      nimi2, tyyppi2, totalhinta)
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
            sendChanMsg(s, chan, resp)
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

            sendChanMsg(s, chan, wikipedia_haku(title, lang))
        except:
            print "wikipedia fake error"

    if message.startswith("!wiki "):
        try:
            a, rest = message.split("!wiki ")
            site, title = rest.split("-", 1)
            resp = getWikiaUrl(site, title)
            sendChanMsg(s, chan, resp)
        except Exception, e:
            print "error at !wiki: "
            print e

    if message.startswith("!lolwiki "):
        try:
            a, title = message.split("!lolwiki ")
            resp = getWikiaUrl("lolwiki", title)
            sendChanMsg(s, chan, resp)
        except Exception, e:
            print "error at !lolwiki: "
            print e

    if message.startswith("!rswiki "):
        try:
            a, title = message.split("!rswiki ")
            resp = getWikiaUrl("rswiki", title)
            sendChanMsg(s, chan, resp)

        except Exception, e:
            print "error at !rswiki: "
            print e

    if message.startswith("!hswiki "):
        try:
            a, title = message.split("!hswiki ")
            resp = getWikiaUrl("hswiki", title)
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
            sendChanMsg(s, chan, resp)
            sleep(1)

        except Exception, e:
            print "Error random viewer"
            print e

    if message.startswith("!rаndomviewer"):
        try:
            viewerlist, vieweramount = getViewers(chan)
            chance = (1.0 / float(vieweramount)) * 100
            resp = "Viewers in: " + str(vieweramount) + ", chance to win: " + str(
                round(chance, 2)) + "%, winner: wetnis"
            sendChanMsg(s, chan, resp)
        except Exception, e:
            print "wetnis viewer error", e


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

    if message.startswith("!pyramid") and (user == OWNER or user == chan):
        try:
            a, b = message.split('!pyramid')
            temp = b
            sendChanMsg(s, chan, temp)
            temp = b + b
            sendChanMsg(s, chan, temp)
            temp = b + b + b
            sendChanMsg(s, chan, temp)
            temp = b + b + b + b
            sendChanMsg(s, chan, temp)
            temp = b + b + b
            sendChanMsg(s, chan, temp)
            temp = b + b
            sendChanMsg(s, chan, temp)
            temp = b
            sendChanMsg(s, chan, temp)
        except Exception, e:
            print "pyramid error ", e

    if message.startswith("!adminspeak") and user == OWNER:
        try:
            unused, chan_msg = message.split('!adminspeak')
            ch, mg = chan_msg.split(' ', 1)
            sendChanMsg(s, ch, mg)
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

            sendChanMsg(s, chan, resp)
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

            sendChanMsg(s, chan, resp)
        except Exception, e:
            print "error in vac ", e

    if message.startswith("!ge "):
        try:
            unused, searchterm = message.split('!ge ', 1)
            hinta = get_price(searchterm)
            sendChanMsg(s, chan, hinta)
        except Exception, e:
            print "mortsin ge error"
            print e

    if message.startswith("!color "):
        try:
            unused, color = message.split('!color', 1)
            resp = "/color " + color
            sendChanMsg(s, chan, resp)
        except Exception, e:
            print "error in !color ", e
