import requests
from bs4 import BeautifulSoup


# Parameter is the term to search the price for
# returns a string like this: <item name>: <price> gp
# or, "item not found"
def wikipedia_haku(search_term, country):
    payload = {"search": search_term}
    url = "https://{}.wikipedia.org/wiki".format(country)
    r = requests.post(url, data=payload)

    soup = BeautifulSoup(r.text, "html.parser")

    if not soup.html.head:
        return "Error"
    if not soup.html.head.title:
        return "Error"
    p = soup.p
    s = ""
    try:
        for a in p:
            s += a.string
    except:
        return "Error"

    s = s[:500]
    s, useless = s.rsplit(".", 1)
    s += "."
    return s
