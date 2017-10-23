# -*- coding: utf-8 -*-
import json
import urllib
import urllib2
from bs4 import BeautifulSoup
import re
import websocket
from datetime import datetime, timedelta, date, time
from time import sleep, mktime, strptime, strftime, localtime
from time import time as currenttime
import wikia
import wikipedia
import requests
import codecs
from Settings import *
import random
from random import randint
from dateutil import relativedelta as rd

def getSteamStats(steamid):
        try:
                favs = ['1','Desert Eagle','2','Dual Berettas','3','Five-SeveN','4','Glock-18','7','AK-47','8','AUG','9','AWP','10','FAMAS','11','G3SG1','13','Galil AR','14','M249','16','M4A4 or A1','17','MAC-10','19','P90','35','Nova','60','M4A1-S','24','UMP-45','25','XM1014','26','PP-Bizon','27','MAG-7','28','Negev','29','Sawed-Off','30','Tec-9','31','Zeus x27','32','P2000','33','MP7','34','MP9','36','P250','38','SCAR-20','39','SG 553','40','SSG 08','42','Knife','61','USP-S','63','CZ75-Auto']
                favweapon = "null"
                totalwins = 0
                url = ("http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=730&key=" + steamapikey + "&steamid=" + steamid)
                req = urllib2.Request(url)
                resp = urllib2.urlopen(req)
                page = json.load(resp)
                for entry in page['playerstats']['stats']:
                        if entry['name'] == 'last_match_t_wins':
                                t_wins = entry['value']
                        if entry['name'] == 'last_match_ct_wins':
                                ct_wins = entry['value']
                                totalwins = t_wins + ct_wins
                        if entry['name'] == 'last_match_wins':
                                last_wins = entry['value']
                                last_loses = totalwins-last_wins
                        if entry['name'] == 'last_match_kills':
                                last_kills = entry['value']
                        if entry['name'] == 'last_match_deaths':
                                last_deaths = entry['value']
                        if entry['name'] == 'last_match_mvps':
                                last_mvps = entry['value']
                        if entry['name'] == 'last_match_favweapon_id':
                                favweapon_id = entry['value']
                                for i, j in zip(favs, favs[1:]):
                                        if str(favweapon_id) == str(i):
                                                favweapon = j
                                                break
                                
                        if entry['name'] == 'last_match_favweapon_shots':
                                favweapon_shots = entry['value']
                        if entry['name'] == 'last_match_favweapon_hits':
                                favweapon_hits = entry['value']
                        if entry['name'] == 'last_match_favweapon_kills':
                                favweapon_kills = entry['value']
                        if entry['name'] == 'last_match_damage':
                                last_damage = entry['value']
                        if entry['name'] == 'last_match_money_spent':
                                last_money_spent = entry['value']
                if last_deaths > 0:
                        kd = last_kills/float(last_deaths)
                else:
                        kd = last_kills
                kd = round(kd, 2)
                if favweapon_shots > 0:
                        accuracy = favweapon_hits/float(favweapon_shots)
                else:
                        accuracy = 0
                accuracy = accuracy * 100
                accuracy = round(accuracy, 1)
                
                if (last_wins > last_loses):
                        result = "Won"
                elif (last_wins == last_loses):
                        result = "Tied"
                else:
                        result = "Lost"
                        
                if (totalwins < 16):
                        result = "Score:"
                playerName = ""
                playerName = getPlayerName(steamid)
                
                roundscore = playerName + "'s last game: " + result + " " + str(last_wins) + "-" + str(last_loses)
                koodee = str(last_kills) + "K/" + str(last_deaths) + "D (" + str(kd) + " KD), " + str(last_mvps) + " MVPS"
                favwpn = "Favourite weapon: " + str(favweapon) + " with " + str(favweapon_kills) + " kills (" + str(favweapon_shots) + " shots, " + str(favweapon_hits) + " hits, " + str(accuracy) + "% accuracy)"
                uselessinfo = "Damage dealt: " + str(last_damage) + ", money spent: " + str(last_money_spent)
                resp = roundscore + " -- " + koodee + " -- " + favwpn + " -- " + uselessinfo
                return resp
                                
                
        except Exception, e:
                print "getSteamStats api.py error "
                print e

def getUptime(chan):

        try:    
                url = ("https://api.twitch.tv/kraken/streams/" + chan)
                req = urllib2.Request(url)
                req.add_header("Client-ID", tclientid)
                resp = urllib2.urlopen(req)
                page = json.load(resp)

                if page['stream'] == None:
                        return "0:00:00 (stream offline)"

                started = page['stream']['created_at']
                timeFormat = "%Y-%m-%dT%H:%M:%SZ"
                startdate = datetime.strptime(started, timeFormat)
                current = datetime.utcnow()
                combined = current - startdate - timedelta(microseconds=current.microsecond)
                combined = str(combined)
                part1, part2, part3 = combined.split(":")
                completed = part1 + "h " + part2 + "m " + part3 + "s"
                return completed

        except Exception, e:
                print "getuptime api.py error "
                print e

def updateMods(chan):
        try:    
                url = ("http://tmi.twitch.tv/group/user/" + chan + "/chatters")
                req = urllib2.Request(url)
                resp = urllib2.urlopen(req)
                page = json.load(resp)
                
                if page['chatters']['moderators'] == None:
                        print "no moderators"
                        return 0                
                
                apimods = page['chatters']['moderators']
                addc = 0
                chanmods = chan + 'mods.txt'
                modsfile = open(chanmods, 'a+')
                mods = modsfile.readlines()
                if not mods:
                        modsfile.write(chan.encode('utf8') + '\n'.encode('utf8'))

                for somethings in mods:
                        if mods[addc].strip().decode('utf8') == apimods[addc].decode('utf8'):
                                sleep(0.1)
                        else:
                                modsfile.write(apimods[addc].encode('utf8') + '\n'.encode('utf8'))
                        
                        addc = addc + 1


                modsfile.close()

        except:
                print "updatemods api.py error"

def restartbot():
    command = "/usr/bin/sudo /sbin/shutdown -r now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print output

def whitelist(domain):
    command = "/usr/bin/sudo whitelist.sh" + domain
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print output


def convertToSteam64(vanity):
        
        try:
                url = ("http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=" + steamapikey + "&vanityurl=" + vanity)
                req = urllib2.Request(url)
                resp = urllib2.urlopen(req)
                page = json.load(resp)
                if page['response']['success'] == 1:
                        steam64id = page['response']['steamid']
                        return steam64id
                else:
                        print "vanity url not found"
        except Exception, e:
                print "error in convertToSteam64 "
                print e

def getTussariKills(steamid):
        try:
                url = ("http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=730&key=" + steamapikey + "&steamid=" + steamid)
                req = urllib2.Request(url)
                resp = urllib2.urlopen(req)
                page = json.load(resp)
                for entry in page['playerstats']['stats']:
                        if entry['name'] == 'total_kills_nova':
                                novakills = entry['value']
                playerName = getPlayerName(steamid)
                resp = playerName + " has " + str(novakills) + " kills with tussari"
                return resp
        except Exception, e:
                print "tussarikills error "
                print e

def getPlayerName(steamid):
        try:
                playerName = "null"
                url = ("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=" + steamapikey + "&steamids=" + steamid)
                req = urllib2.Request(url)
                resp = urllib2.urlopen(req)
                page = json.load(resp)
                for entry in page['response']['players']:
                        playerName = entry['personaname']
                return playerName
                
        except Exception, e:
                print "error in getPlayerName "
                print e


def getPlayerBans(steamid):
        try:
                playerName = "null"
                url = ("http://api.steampowered.com/ISteamUser/GetPlayerBans/v1/?key=" + steamapikey + "&steamids=" + steamid)
                req = urllib2.Request(url)
                resp = urllib2.urlopen(req)
                page = json.load(resp)
                for entry in page['players']:
                        vacs = entry['NumberOfVACBans']
                        lastban = entry['DaysSinceLastBan']
                        gamebans = entry['NumberOfGameBans']
                        ecoban = entry['EconomyBan']
                        
                playerName = getPlayerName(steamid)
                
                if lastban == 0 and vacs == 0 and gamebans == 0:
                        lastban = ""
                else:
                        lastban = str(lastban) + " days since last VAC/game ban."
                        
                resp = "User " + playerName + " has " + str(vacs) + " VAC bans and " + str(gamebans) +" game bans. " + "Trade ban status: "  + str(ecoban) + ". " + str(lastban)
                return resp
        except Exception, e:
                print "error in getPlayerBans "
                print e
                        

def getKills(steamid, wpn):
        try:
                what = 'total_kills_' + wpn.strip()
                what = what.lower()
                url = ("http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=730&key=" + steamapikey + "&steamid=" + steamid)
                req = urllib2.Request(url)
                resp = urllib2.urlopen(req)
                page = json.load(resp)
                for entry in page['playerstats']['stats']:
                        if entry['name'] == what:
                                kills = entry['value']
                playerName = getPlayerName(steamid)
                resp = playerName + " has " + str(kills) + " kills with " + wpn
                return resp
        except Exception, e:
                print "getkills error "
                print e


def getJoin():
        try:
                html_page = urllib2.urlopen("http://steamcommunity.com/profiles/76561198185015081/")
                soup = BeautifulSoup(html_page, "html.parser")
                for link in soup.findAll('a', attrs={'href': re.compile("^steam://")}):
                        if link.get('href') == "steam://":
                                return "Joining not possible at the moment."
                        else:
                                return link.get('href')
        except Exception, e:
                print "getjoin error "
                print e
                return "Joining not possible at the moment."


def getViewers(chan):
        try:
                errors = 0
                while(errors <= 10):
                        try:
                                url = ("https://tmi.twitch.tv/group/user/" + chan + "/chatters")
                                req = urllib2.Request(url)
                                resp = urllib2.urlopen(req, timeout=10)
                                page = json.load(resp)
                                viewers = []
                                amount = page['chatter_count']
                                for entry in page['chatters']['moderators']:
                                        viewers.append(entry)
                                for entry in page['chatters']['staff']:
                                        viewers.append(entry)
                                for entry in page['chatters']['admins']:
                                        viewers.append(entry)
                                for entry in page['chatters']['global_mods']:
                                        viewers.append(entry)
                                for entry in page['chatters']['viewers']:
                                        viewers.append(entry)

                                #try:
                                #        if owner in viewers:
                                #                viewers = viewers.remove(owner)
                                #        if IDENT in viewers:
                                #                viewers = viewers.remove(IDENT)
                                #except Exception, e:
                                #        print "getviewers remove attempt failed"
                                #        print e
				
                                #print viewlist
				#random.shuffle(viewers)
                                return viewers, amount
                        except Exception, e:
                                print "errors: " + str(errors)
                                print e
                                sleep(0.5)
                                errors += 1

                
        except Exception, e:
                print "getViewers error "
                print e


                
def getWikiaUrl(site, title):
        try:
                if site == "lolwiki":
                        site = "leagueoflegends"
                elif site == "rswiki":
                        site = "2007.runescape"
                elif site == "hswiki":
                        site = "hearthstone"
                elif site == "rsfi":
                        site = "fi.runescape"
                search = wikia.search(site, title)
                title = search[0]
                page = wikia.page(site, title)
		url = page.url
		url = url.replace(" ", "_")
                return urllib2.quote(url, safe="http://")
	except:
		print "api wikiaurl error"


def getAnyWikiaUrl(site, title):
        try:
                search = wikia.search(site, title)
                title = search[0]
                page = wikia.page(site, title)
		url = page.url
		url = url.replace(" ", "_")
                return urllib2.quote(url, safe="http://")
	except:
		print "api anywikiurl error"


def getWikipediaUrl(title, lang):
	try:
		wikipedia.set_lang(lang)
		search = wikipedia.search(title)
		title = search[0]
		page = wikipedia.page(title)
		print page.url
		print page.url.encode("utf8")
		url = page.url
		url.replace(" ", "_")
		url = url.replace("(", "%28")
		url = url.replace(")", "%29")
		return url, wikipedia.summary(title, sentences=1)
	except:
		print "wikipedia error"


def getLeagueSummonerId(server, name):
        try:
                url = ("https://" + server + ".api.pvp.net/api/lol/" + server + "/v1.4/summoner/by-name/" + name + "?api_key=" + lolapikey)
                req = urllib2.Request(url)
                resp = urllib2.urlopen(req)
                page = json.load(resp)
                summonerid = page[name]['id']
                return summonerid
        except:
                print "getlolsummonerid error"


def getLeagueLastGame(server, name, summonerid):
        try:
                url = ("https://" + server + ".api.pvp.net/api/lol/" + server + "/v1.3/game/by-summoner/" + summonerid + "/recent?api_key=" + lolapikey)
                req = urllib2.Request(url)
                resp = urllib2.urlopen(req)
                page = json.load(resp)
                stats = page['games'][0]['stats']
                try:
                        chid = page['games'][0]['championId']
                        gametype = page['games'][0]['subType']
                except:
                        gametype = "RANKED_SOLO_5x5"
                champion = getLeagueChampion(chid)
                if gametype == "RANKED_SOLO_5x5":
                        gametype = "Ranked Solo"

                try:
                        position = stats['playerPosition']
                except:
                        position = 0
                if position == 1:
                        position = "Top"
                elif position == 2:
                        position = "Mid"
                elif position == 3:
                        position = "Jungle"
                elif position == 4:
                        position = "Bot"
                
                assists = stats['assists']
                kills = stats['championsKilled']
                try:
                        deaths = stats['numDeaths']
                except:
                        deaths = 0
                dmgToChampions = stats['totalDamageDealtToChampions']
                result = stats['win']
                if result == True:
                        result = "Win"
                elif result == False:
                        result = "Lose"
                try:
                        largestSpree = stats['largestKillingSpree']
                except:
                        largestSpree = 0
                try:
                        largestMulti = stats['largestMultiKill']
                except:
                        largestMulti = 0
                try:
                        level = stats['level']
                except:
                        level = 0
                timePlayed = stats['timePlayed']
                        
                timeFormat = "T%M:%SZ"
                try:
                        timePlayed = datetime.strptime(str(timePlayed), timeFormat)
                        print timePlayed
                except:
                        timePlayed = 0
                response = name + "'s last game: " + result + " " +  position + " " +  gametype + "Dmg to champions: " + str(dmgToChampions) + " KDA: " + str(kills) + "/" + str(deaths) + "/" + str(assists) + " largest killing spree: " + str(largestSpree) + " largest multikill: " + str(largestMulti)
                return response
        except:
                print "getlollastgame error"



def getLeagueChampion(chid):
        try:
                url = ("https://global.api.pvp.net/api/lol/static-data/euw/v1.2/champion/" + chid + "?api_key=" + lolapikey)
                req = urllib2.Request(url)
                resp = urllib2.urlopen(req)
                page = json.load(resp)

                chname = page['name']

                return chname
        except:
                print "error leaguechampion"

def getTitle(chan):
        try:
                url = ("https://api.twitch.tv/kraken/channels/" + chan)
                req = urllib2.Request(url)
                req.add_header("Client-ID", tclientid)
                resp = urllib2.urlopen(req)
                page = json.load(resp)
                title = page['status']
                return title
        except Exception, e:
                print "error gettitle "
                print e
                

def getDrink():
	try:
		with open('alko.json') as alkofile:
			data = json.load(alkofile)
			num = randint(0, len(data))
			nimi, hinta, tyyppi, tuotenumero = data[num]["Nimi"], data[num]["Hinta"], data[num]["Tyyppi"], data[num]["Numero"]
			tuotenumero = str(tuotenumero).rjust(6, '0')
			return nimi, hinta, tyyppi, tuotenumero
	except Exception, e:
		print "getdrink error", e

def getFollowing(user, chan):
	try:	
		try:
			url = ("https://api.twitch.tv/kraken/users/"+user+"/follows/channels/"+chan)
                	req = urllib2.Request(url)
                	req.add_header("Client-ID", tclientid)
                	resp = urllib2.urlopen(req)
                	page = json.load(resp)
			dateFollowed = page['created_at']
		except:
			return "0"
		#timediff = currenttime()-mktime(strptime(dateFollowed, "%Y-%m-%dT%H:%M:%SZ"))
		#delta = timedelta(seconds=timediff-7200)
		dif = rd.relativedelta(datetime.fromtimestamp(currenttime()-7200), datetime.fromtimestamp(mktime(strptime(dateFollowed, "%Y-%m-%dT%H:%M:%SZ"))))
		if dif.years != 0:
			return "{0} years, {1} months, {2} days, {3} hrs".format(dif.years, dif.months, dif.days, dif.hours)
		if dif.months != 0:
			return "{0} months, {1} days, {2} hrs".format(dif.months, dif.days, dif.hours)
		if dif.days != 0:
			return "{0} days, {1} hrs, {2} min".format(dif.days, dif.hours, dif.minutes)
		if dif.hours != 0:
			return "{0} hours, {1} minutes".format(dif.hours, dif.minutes)
		return "{0} minutes, {1} seconds".format(dif.minutes, dif.seconds)
	except Exception, e:
		print "getFollowing error at Api.py, info:", e


def getFollowStatus(user, chan):
	try:
		howlong = getFollowing(user, chan)
		if howlong == "0":
			return user + " is not following " + chan
		else:
			return user + " has been following " + chan + " for " + howlong
	except Exception, e:
		print "get follow status error, info:", e

def getMix():
        try:
                with open('alko.json') as alkofile:
                        data = json.load(alkofile)
                        num = randint(0, len(data))
                        nimi, litrahinta, tyyppi = data[num]["Nimi"], data[num]["Litrahinta"], data[num]["Tyyppi"]
                        return nimi, litrahinta, tyyppi
        except Exception, e:
                print "getmix error", e


