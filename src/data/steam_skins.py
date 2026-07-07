"""

Request methods for the Steam API to get CS2 skin prices and names.

"""

import requests

the_skin = "" 
url = f"https://steamcommunity.com/market/priceoverview/"
skin_names_url = "https://raw.githubusercontent.com/ByMykel/CSGO-API/main/public/api/en/skins_not_grouped.json"
parameters = { 
    "market_hash_name": the_skin,
    "appid": 730,
    "currency" : 20, # code for CAD, 1 is for USD
    "language" : "english",
    "format" : "json"
}

# ------------ Request Methods ----------------

def fetch_request(the_skin, params=None, headers=None, timeout=10):
    if params is None:
        params = {}
    params.update({"market_hash_name": the_skin})
    response = requests.get(url, params=params, headers=headers, timeout=timeout)
    if response.status_code == 200:
        skin_data = response.json() # raw JSON data
        return skin_data
    else:
        print(f"Error: Unable to fetch data, status code {response.status_code}")

def get_all_skin_names(url, params=None, headers=None, timeout=10):
    skin_names = []
    data = requests.get(skin_names_url).json()
    for it in data:
        hash_name =  it.get("market_hash_name")
        skin_names.append(hash_name)
    return skin_names

# ------------ Testing ----------------     

# skin_array = get_all_skin_names(skin_names_url)
# print(skin_array)