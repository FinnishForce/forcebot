# -*- coding: utf-8 -*-
import json
import urllib2

from datetime import datetime, timedelta
from random import randint
from time import sleep, mktime, strptime
from time import time as currenttime
import requests
import wikia
import wikipedia
from bs4 import BeautifulSoup
from dateutil import relativedelta as rd

from settings import *


def get_steam_stats(steamid):
    try:
        favs = ['1', 'Desert Eagle', '2', 'Dual Berettas', '3', 'Five-SeveN', '4', 'Glock-18', '7', 'AK-47', '8', 'AUG',
                '9', 'AWP', '10', 'FAMAS', '11', 'G3SG1', '13', 'Galil AR', '14', 'M249', '16', 'M4A4 or A1', '17',
                'MAC-10', '19', 'P90', '35', 'Nova', '60', 'M4A1-S', '24', 'UMP-45', '25', 'XM1014', '26', 'PP-Bizon',
                '27', 'MAG-7', '28', 'Negev', '29', 'Sawed-Off', '30', 'Tec-9', '31', 'Zeus x27', '32', 'P2000', '33',
                'MP7', '34', 'MP9', '36', 'P250', '38', 'SCAR-20', '39', 'SG 553', '40', 'SSG 08', '42', 'Knife', '61',
                'USP-S', '63', 'CZ75-Auto']
        favweapon = "null"
        totalwins = 0
        url = (
            "http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=730&key=" + STEAM_API_KEY + "&steamid=" + steamid)
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
                last_loses = totalwins - last_wins
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
            kd = last_kills / float(last_deaths)
        else:
            kd = last_kills
        kd = round(kd, 2)
        if favweapon_shots > 0:
            accuracy = favweapon_hits / float(favweapon_shots)
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
        playerName = get_steam_player_name(steamid)

        roundscore = playerName + "'s last game: " + result + " " + str(last_wins) + "-" + str(last_loses)
        koodee = str(last_kills) + "K/" + str(last_deaths) + "D (" + str(kd) + " KD), " + str(last_mvps) + " MVPS"
        favwpn = "Favourite weapon: " + str(favweapon) + " with " + str(favweapon_kills) + " kills (" + str(
            favweapon_shots) + " shots, " + str(favweapon_hits) + " hits, " + str(accuracy) + "% accuracy)"
        uselessinfo = "Damage dealt: " + str(last_damage) + ", money spent: " + str(last_money_spent)
        resp = roundscore + " -- " + koodee + " -- " + favwpn + " -- " + uselessinfo
        return resp


    except Exception, e:
        print "get_steam_stats api.py error "
        print e


def get_uptime(chan):
    try:
        url = ("https://api.twitch.tv/helix/streams?user_login=" + chan)
        req = urllib2.Request(url)
        req.add_header("Client-ID", TCLIENTID)
        resp = urllib2.urlopen(req)
        page = json.load(resp)
        if page["data"] == []:
            return "0:00:00 (stream offline)"

        started = page['data'][0]['started_at']
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


def convert_to_steam64(vanity):
    try:
        url = (
            "http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=" + STEAM_API_KEY + "&vanityurl=" + vanity)
        req = urllib2.Request(url)
        resp = urllib2.urlopen(req)
        page = json.load(resp)
        if page['response']['success'] == 1:
            steam64id = page['response']['steamid']
            return steam64id
        else:
            print "vanity url not found"
    except Exception, e:
        print "error in convert_to_steam64 "
        print e


def get_steam_player_name(steamid):
    try:
        playerName = "null"
        url = (
            "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=" + STEAM_API_KEY + "&steamids=" + steamid)
        req = urllib2.Request(url)
        resp = urllib2.urlopen(req)
        page = json.load(resp)
        for entry in page['response']['players']:
            playerName = entry['personaname']
        return playerName

    except Exception, e:
        print "error in get_steam_player_name "
        print e


def get_steam_bans(steamid):
    try:
        playerName = "null"
        url = ("http://api.steampowered.com/ISteamUser/GetPlayerBans/v1/?key=" + STEAM_API_KEY + "&steamids=" + steamid)
        req = urllib2.Request(url)
        resp = urllib2.urlopen(req)
        page = json.load(resp)
        for entry in page['players']:
            vacs = entry['NumberOfVACBans']
            lastban = entry['DaysSinceLastBan']
            gamebans = entry['NumberOfGameBans']
            ecoban = entry['EconomyBan']

        playerName = get_steam_player_name(steamid)

        if lastban == 0 and vacs == 0 and gamebans == 0:
            lastban = ""
        else:
            lastban = str(lastban) + " days since last VAC/game ban."

        resp = "User " + playerName + " has " + str(vacs) + " VAC bans and " + str(
            gamebans) + " game bans. " + "Trade ban status: " + str(ecoban) + ". " + str(lastban)
        return resp
    except Exception, e:
        print "error in get_steam_bans "
        print e


def get_viewers(chan):
    try:
        errors = 0
        while (errors <= 10):
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

                return viewers, amount
            except Exception, e:
                print "errors: " + str(errors)
                print e
                sleep(0.5)
                errors += 1


    except Exception, e:
        print "get_viewers error "
        print e


def get_wikia_url(site, title):
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

def get_osrs_wiki(title):
    try:
        payload = {"search": title}
        url = "https://oldschool.runescape.wiki"
        r = requests.post(url, data=payload)

        soup = BeautifulSoup(r.text, "html.parser")

        url = soup.find(rel="canonical")
        url = url.get("href")
        return url
    except Exception, e:
        print "get_osrs_wiki error-->", e


def get_any_wikia_url(site, title):
    try:
        search = wikia.search(site, title)
        title = search[0]
        page = wikia.page(site, title)
        url = page.url
        url = url.replace(" ", "_")
        return urllib2.quote(url, safe="http://")
    except:
        print "api anywikiurl error"


def get_wikipedia_url(title, lang):
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


def get_title(chan):
    try:
        url = ("https://api.twitch.tv/helix/streams?user_login=" + chan)
        req = urllib2.Request(url)
        req.add_header("Client-ID", TCLIENTID)
        resp = urllib2.urlopen(req)
        page = json.load(resp)
        title = page["data"][0]["title"]
        return title
    except Exception, e:
        print "error gettitle "
        print e


def get_drink():
    try:
        with open('alko.json') as alkofile:
            data = json.load(alkofile)
            num = randint(0, len(data))
            nimi, hinta, tyyppi, tuotenumero = data[num]["Nimi"], data[num]["Hinta"], data[num]["Tyyppi"], data[num][
                "Numero"]
            tuotenumero = str(tuotenumero).rjust(6, '0')
            return nimi, hinta, tyyppi, tuotenumero
    except Exception, e:
        print "getdrink error", e

def get_twitch_id(name):
    try:
        url = ("https://api.twitch.tv/helix/users?login=" + name)
        req = urllib2.Request(url)
        req.add_header("Client-ID", TCLIENTID)
        resp = urllib2.urlopen(req)
        page = json.load(resp)
        return page.get("data")[0]["id"]    
    except Exception, e:
        print "get_twitch_id error ->", e

def get_following(user, chan):
    try:
        try:
            userid = get_twitch_id(user)
            chanid = get_twitch_id(chan)
            url = ("https://api.twitch.tv/helix/users/follows?from_id=" + userid + "&to_id=" + chanid)
            print url
            req = urllib2.Request(url)
            req.add_header("Client-ID", TCLIENTID)
            print req
            resp = urllib2.urlopen(req)
            page = json.load(resp)
            print page
            dateFollowed = page['data'][0]['followed_at']
            
        except Exception, e:
            print e
            return "0"
            # timediff = currenttime()-mktime(strptime(dateFollowed, "%Y-%m-%dT%H:%M:%SZ"))
            # delta = timedelta(seconds=timediff-7200)
        dif = rd.relativedelta(datetime.fromtimestamp(currenttime() - 7200), #10800 summer 7200 winter time
                               datetime.fromtimestamp(mktime(strptime(dateFollowed, "%Y-%m-%dT%H:%M:%SZ"))))
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
        print "get_following error at api.py, info:", e


def get_follow_status(user, chan):
    try:
        howlong = get_following(user, chan)
        if howlong == "0":
            return user + " is not following " + chan
        else:
            return user + " has been following " + chan + " for " + howlong
    except Exception, e:
        print "get follow status error, info:", e


def get_drink_mix():
    try:
        with open('alko.json') as alkofile:
            data = json.load(alkofile)
            num = randint(0, len(data))
            nimi, litrahinta, tyyppi = data[num]["Nimi"], data[num]["Litrahinta"], data[num]["Tyyppi"]
            return nimi, litrahinta, tyyppi
    except Exception, e:
        print "getmix error", e
