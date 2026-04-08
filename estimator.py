import requests
from bs4 import BeautifulSoup
import json
import time
import sqlite3

## Important constants
P_INTACT = [0.2533, 0.2533, 0.2533, 0.11, 0.11, 0.02]
P_EXCEPTIONAL = [0.2333, 0.2333, 0.2333, 0.13, 0.13, 0.04]
P_FLAWLESS = [0.20, 0.20, 0.20, 0.17, 0.17, 0.06]
P_RADIANT = [0.1667, 0.1667, 0.1667, 0.2, 0.2, 0.1]
P_REFINEMENTS = [P_INTACT, P_EXCEPTIONAL, P_FLAWLESS, P_RADIANT] 
FORMA_VALUE = 0
DROP_COUNT = 6


## Base URLs
WARFRAME_WIKI = "https://wiki.warframe.com/w/"
WARFRAME_MARKET = "https://api.warframe.market/v2/"


def kompressa_bugfix(drop):
    """
    For some reason, the Kompressa Prime Receiver has been misspelled on warframe.market as Reciever
    for over a month. This accounts for that issue and will be removed if it ever actually gets fixed.

    Parameters:
        drop (str): Drop name.

    Returns:
          str: Fixed drop name.
    """
    if (drop == "kompressa_prime_receiver"):
        return "kompressa_prime_reciever"
    else:
        return drop


def get_drops(relic):
    """
    Takes in a relic name (ex. Lith_D7) and returns its drops in order of low, medium then high rarity. 

    Parameters:
        relic (str): Relic name. Must be of the form "*Era* *Key*" (ex. Lith C7).

    Returns:
          [str, str, str, str, str, str]: A list of the relic's drops.
    """
    ## Check if drops are already saved in the table
    con = sqlite3.connect("relics.db")
    cursor = con.cursor()
    drops_saved = cursor.execute("SELECT name, drop1, drop2, drop3, drop4, drop5, drop6 FROM relic_list WHERE name=? AND drop1 IS NOT NULL", (relic,)).fetchone()

    if not drops_saved:
        # Grab wiki page for chosen relic and find its droptable
        url = WARFRAME_WIKI + relic.replace(" ","_")
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        droptable = soup.find(id="72656C6963table")
        
        # For each row, find the section that has the title and take its text, then append it to our list of drops.
        drops = []
        for row in droptable.find_all("tr"):
            first_cell = row.find("td")
            if first_cell == None:
                continue
            titles = first_cell.find_all("a")
            if titles == []:
                continue
            drops.append(titles[-1].text.strip())
        
        # Save the drops to the database
        cursor.execute("Update relic_list SET drop1=?, drop2=?, drop3=?, drop4=?, drop5=?, drop6=? WHERE name=?", 
                       (drops[0],drops[1],drops[2],drops[3],drops[4],drops[5],relic))
        con.commit()

        return drops
    else:
        drops = []
        for i in range(1,7):
            drops.append(drops_saved[i])
        return drops


def expected_value(relic):
    """
    Takes in a relic, then calculates the expected plat value if cracked.

    Parameters:
        relic (str): Relic name. Must be of the form "*Era* *Key*" (ex. Lith C7).

    Returns:
            [float, float, float, float]: In order, expected value for intact, exceptional, flawless and radiant refinements
    """
    drops = get_drops(relic)
    for i in range(DROP_COUNT):
        drops[i] = drops[i].replace(" ", "_").lower()
        
    prices = []

    # Get top 3 orders for each item and average out their price
    for i in range(DROP_COUNT):
        if drops[i] == "forma_blueprint":
            if i >= 3:
                prices.append(2 * FORMA_VALUE)
            else:
                prices.append(FORMA_VALUE)  
            continue
        
        # Make warframe.market API call and just get the sell order information
        item_top_order = "orders/item/" + kompressa_bugfix(drops[i]) + "/top"
        top_orders = requests.get(WARFRAME_MARKET + item_top_order)
        data = json.loads(top_orders.text)
        sell_data = data["data"]["sell"]

        price_sum = 0
        average = 3

        for sell_order in sell_data[:average]:
            price_sum += sell_order["platinum"]
            if sell_order["platinum"] == 0 and average != 1:
                average -= 1
        prices.append(price_sum / 3) 
    
    # Calculated expected value for each refinement level
    expected_values = []
    for p_set in P_REFINEMENTS:
        value = 0
        for i in range(DROP_COUNT):
            value += prices[i] * p_set[i]
        expected_values.append(float("%.2f"%(value)))
    return expected_values





