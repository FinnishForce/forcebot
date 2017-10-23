import requests
from bs4 import BeautifulSoup
 
# Parameter is the term to search the price for
# returns a string like this: <item name>: <price> gp
# or, "item not found"
def get_price(search_term):
        payload = {"query": search_term}
        url = "http://services.runescape.com/m=itemdb_oldschool/results#main-search"
        r = requests.post(url, data = payload)
        soup = BeautifulSoup(r.text, "html.parser")
 
        tbody = soup.find("tbody")
        if not tbody:
                return "Item not found"
        tr = tbody.find("tr")
        item_title = tr.find("td").find("a")["title"]
        price_link = tr.find_all("td")[2].find("a").text
 
        return "{}: {} gp".format(item_title, price_link)
 
# This should print "Old School Runescape bond: 3.2m gp"
#print(get_price("bond"))
