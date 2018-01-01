import json

import requests
from fuzzywuzzy import process
from bs4 import BeautifulSoup

RSBUDDY_API = "https://api.rsbuddy.com/grandExchange"

with open("osrs-items.json") as f:
    OSRS_ITEMS = json.load(f)

ITEM_NAMES = [i["name"] for i in OSRS_ITEMS.values()]


def legacy_osrs_price(search_term):
    payload = {"query": search_term}
    url = ("http://services.runescape.com/"
           "m=itemdb_oldschool/results#main-search")

    r = requests.post(url, data=payload)
    soup = BeautifulSoup(r.text, "html.parser")

    tbody = soup.find("tbody")
    if not tbody:
        raise ValueError("Item not found")

    tr = tbody.find("tr")
    item_title = tr.find("td").find("a")["title"]
    price_link = tr.find_all("td")[2].find("a").text

    return item_title, price_link


def get_price(search_term):
    """Search osrs grand exchange price for specific item.

    :param search_term: search input argument
    :returns: string like "item: 55 gp"
    """
    try:
        match = process.extractOne(search_term, ITEM_NAMES)[0]
    except TypeError:
        return "no result found for " + search_term

    match_id = next(id for id
                    in OSRS_ITEMS.keys()
                    if OSRS_ITEMS[id]["name"] == match)

    params = {"i": match_id, "a": "guidePrice"}
    result = requests.get(RSBUDDY_API, params=params).json()

    price = result["overall"]

    # sometimes rsbuddy returns price of 0 if there is not enough traded items.
    # try old price search for those
    if price == 0:
        try:
            match, price = legacy_osrs_price(match)
        except Exception as e:
            print "grand exchange error:", e
            return "no result found for " + search_term
    else:
        price = "{:,}".format(int(price))
    return "{}: {} gp".format(match, price)
