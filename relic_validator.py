import requests
from bs4 import BeautifulSoup
import json
import sqlite3

## Base URLs
RELIC_WIKI = "https://wiki.warframe.com/w/Void_Relic"

## Important constants
RELIC_STATUSES = ["Unvaulted", "Vaulted", "Ki'teer"]


## verify_relic: Str -> anyof(False, [Str, Str])
## Produces false if name is not the name of a relic 
## if name is the name of a relic, modifies the string to be in the format "*Era* *Key*" (ex. "Lith D7")
## and returns whether it is vaulted, unvaulted or a baro relic
def verify_relic(name):
    formatted = name.lower().replace(" ","").strip()
    result = False

    con = sqlite3.connect("relics.db")
    cursor = con.cursor()
    relic_names = cursor.execute("SELECT name, status FROM relic_list")

    for name in relic_names:
        if formatted == name[0].lower().replace(" ","").strip():
            return [name[0], name[1]]
    return result



## update_relic_list: None -> None
## Updates the the relic_list table with all non requiem relics in the game according to the wiki
def update_relic_list():
    con = sqlite3.connect("relics.db")
    cursor = con.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS relic_list("
                   "name PRIMARY KEY, status NOT NULL, drop1, drop2, drop3, drop4, drop5, drop6)")

    url = RELIC_WIKI
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    
    unvaulted_table = None
    vaulted_table = None
    kiteer_table = None
    for t in soup.find_all("table"):
        cap = t.find("caption")
        if cap and "unvaulted/available relics" == cap.get_text(strip=True).lower():
            unvaulted_table = t.find_all("tr")[1]
        if cap and "vaulted/unavailable relics" == cap.get_text(strip=True).lower():
            vaulted_table = t.find_all("tr")[1]
        if cap and "baro ki'teer exclusive relics" == cap.get_text(strip=True).lower():
            kiteer_table = t.find_all("tr")[1]
            break
    relic_tables = [unvaulted_table, vaulted_table, kiteer_table]

    ## Write the relics into relic list
    for i in range(0, 3):
        table = relic_tables[i]
        eras = table.find_all("td")[:4]
        for era in eras:
            relic_names = era.find_all("li")
            for name in relic_names:
                relic_name = name.find("span")["data-param-name"]
                cursor.execute("INSERT OR IGNORE INTO relic_list (name, status) VALUES (?,?)", (relic_name, RELIC_STATUSES[i]))
                con.commit()

    
        

