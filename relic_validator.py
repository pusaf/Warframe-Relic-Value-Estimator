import requests
from bs4 import BeautifulSoup
import json

## Base URLs
relic_wiki = "https://wiki.warframe.com/w/Void_Relic"
warframe_market = "https://api.warframe.market/v2/"


## verify_relic: Str -> anyof(False, -1, [Str, Str])
## Produces false if name is not the name of a relic 
## Produces -1 if the relic_list.txt is not in the correct format or does not exist.
## if name is the name of a relic, modifies the string to be in the format "*Era* *Key*" (ex. "Lith D7")
## and returns whether it is vaulted, unvaulted or a baro relic
def verify_relic(name):
    formatted = name.lower().replace(" ","").strip()
    result = False

    try:
        relic_list = open('relic_list.txt', "r")
    except:
        return -1
    
    tempLine = relic_list.readline()
    if tempLine == None:
        return -1
    unvault_count = int(tempLine.split()[-1])
    vault_count = int(relic_list.readline().split()[-1])
    kiteer_count = int(relic_list.readline().split()[-1])

    count = 0
    relic_name = relic_list.readline().strip()
    while (relic_name != ""):
        count += 1

        if relic_name.lower().replace(" ","") == formatted:
            result = [relic_name]
            if count <= unvault_count:
                result.append("Unvaulted")
            elif count <= unvault_count + vault_count:
                result.append("Vaulted")
            else:
                result.append("Ki'teer")
            break
        
        relic_name = relic_list.readline().strip()


    relic_list.close()
    return result





## update_relic_list: None -> None
## Updates the file relic_list.txt with the name of all non requiem relics in the game according to the wiki
def update_relic_list():
    relic_list = open('relic_list.txt', 'w')
    temp_relic_list = []
    vault_count = 0
    unvault_count = 0
    kiteer_count = 0

    url = relic_wiki
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
            temp_relic_list.append(name.find("span")["data-param-name"] + "\n")
            unvault_count += 1
    
    ## Write the vaulted relics into relic list
    vaulted_eras = vaulted_table.find_all("td")[:4]
    for era in vaulted_eras:
        relic_names = era.find_all("li")
        for name in relic_names:
            temp_relic_list.append(name.find("span")["data-param-name"] + "\n")
            vault_count += 1

    ## Write the ki'teer relics into relic list
    kiteer_eras = kiteer_table.find_all("td")[:4]
    for era in kiteer_eras:
        relic_names = era.find_all("li")
        for name in relic_names:
            temp_relic_list.append(name.find("span")["data-param-name"] + "\n")
            kiteer_count += 1

    relic_list.write("Unvaulted Relics: " + str(unvault_count) + "\nVaulted Relics: " + str(vault_count) + "\nKi'Teer Relics: " + str(kiteer_count) + "\n")

    for name in temp_relic_list:
        relic_list.write(name)
    relic_list.close()
        


