import httpx

SKINPORT_ITEMS_URL = "https://api.skinport.com/v1/items"

def get_skinport_prices(currency="CAD", tradable=0):
    params = {
        "app_id": 730,        # CS2
        "currency": currency,
        "tradable": tradable  # 0 = all items, 1 = tradable only
    }

    headers = {
        "Accept-Encoding": "br",
        "User-Agent": "SkinLemur"
    }

    response = httpx.get(
        SKINPORT_ITEMS_URL,
        params=params,
        headers=headers,
        timeout=30
    )

    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    items = get_skinport_prices()
    #print(items)

    print(f"Returned {len(items)} items")

    '''

    the JSON that gets returned. 

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

    # for item in items[:10]:
    #     print("--------------------------------")
    #     print("Name:", item.get("market_hash_name"))
    #     print("Min price:", item.get("min_price"))
    #     print("Median price:", item.get("median_price"))
    #     print("Suggested price:", item.get("suggested_price"))
    #     print("Quantity:", item.get("quantity"))