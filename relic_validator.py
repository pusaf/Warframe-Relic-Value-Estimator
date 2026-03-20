import requests
from bs4 import BeautifulSoup
import json


## Base URLs
RELIC_WIKI = "https://wiki.warframe.com/w/Void_Relic"

## Important constants
CSV_HEADER = "Type, Relic Name, Count"

## verify_relic: Str -> anyof(False, -1, [Str, Str])
## Produces false if name is not the name of a relic 
## Produces -1 if the relic_list.txt is not in the correct format or does not exist.
## if name is the name of a relic, modifies the string to be in the format "*Era* *Key*" (ex. "Lith D7")
## and returns whether it is vaulted, unvaulted or a baro relic
def verify_relic(name):
    formatted = name.lower().replace(" ","").strip()
    result = False

    try:
        relic_list = open('relic_list.csv', "r")
    except:
        return -1
    
    firstLine = relic_list.readline().strip()
    if firstLine != CSV_HEADER.strip():
        return -1

    relic = relic_list.readline().strip().split(",")
    while (relic != [""]):
        relic_type = relic[0]
        relic_name = relic[1]
        if relic_name.lower().replace(" ","") == formatted:
            result = [relic_name]
            result.append(relic_type)
            break
        relic = relic_list.readline().strip().split(",")

    relic_list.close()
    return result





## update_relic_list: None -> None
## Updates the file relic_list.csv with all non requiem relics in the game according to the wiki
def update_relic_list():
    relic_list = open('relic_list.csv', 'w')
    temp_relic_list = []
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
    

    ## Write the unvaulted relics into relic list
    unvaulted_eras = unvaulted_table.find_all("td")[:4]
    for era in unvaulted_eras:
        relic_names = era.find_all("li")
        for name in relic_names:
            temp_relic_list.append("Unvaulted," + name.find("span")["data-param-name"] + "\n")
    
    ## Write the vaulted relics into relic list
    vaulted_eras = vaulted_table.find_all("td")[:4]
    for era in vaulted_eras:
        relic_names = era.find_all("li")
        for name in relic_names:
            temp_relic_list.append("Vaulted," + name.find("span")["data-param-name"] + "\n")

    ## Write the ki'teer relics into relic list
    kiteer_eras = kiteer_table.find_all("td")[:4]
    for era in kiteer_eras:
        relic_names = era.find_all("li")
        for name in relic_names:
            temp_relic_list.append("Ki'teer," + name.find("span")["data-param-name"] + "\n")

    relic_list.write(CSV_HEADER + "\n")
    for name in temp_relic_list:
        relic_list.write(name)
    relic_list.close()
        

