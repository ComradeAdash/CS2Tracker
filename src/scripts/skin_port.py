'''

SkinPort price retrieval Methods

Notes:

    json format example:

    {'market_hash_name': 'UMP-45 | Primal Saber (Minimal Wear)',
    'version': None, 'currency': 'CAD', 'suggested_price': 22.4, 
    'item_page': 'https://skinport.com/item/ump-45-primal-saber-minimal-wear', 
    'market_page': 'https://skinport.com/market/smg/ump-45?item=Primal%20Saber', 
    'min_price': 13.99, 
    'max_price': 21.57, 
    'mean_price': 18.3, 
    'median_price': 18.77, 
    'quantity': 13, 
    'created_at': 1535988294, 
    'updated_at': 1783210212}

'''

import httpx
ITEMS = "https://api.skinport.com/v1/items"

# Returns json data of all current CS2 skin listings on SkinPort
def get_sp_json(currency="CAD", tradable=0):
    params = {
            "app_id": 730, # CS2 code
            "currency": currency, # CAD
            "tradable": tradable  # 0 = all items, 1 = tradable only
        }
    
    r  = httpx.get(ITEMS,params=params)

    return r.json()