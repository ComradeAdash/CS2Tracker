# Issues - skins that dont exist such as AWP asiimov fn (they only come in ft) create a mismatch

import re
import data.steam_skins as steam_skins
from rapidfuzz import process, fuzz # rapid fuzz helps process match user queries to actual skins

SKIN_ARRAY = steam_skins.get_all_skin_names(steam_skins.skin_names_url)

wear_map =  {
"ft": "(Field Tested)",
"mw": "(Minimal Wear)",
"fn": "(Factory New)",
"bs": "(Battle Scarred)",
"ww": "(Well Worn)"
}

def normalize(input):
    for abbr, full in wear_map.items():
        input = re.sub(rf"\b{abbr}\b", full, input)
    input = input.lower()
    input = re.sub(r"[^a-z0-9\s]", "", input)
    input = re.sub(r"\s+", " ", input).strip()

    return input

# taking in a user input query, normalizing it, and checking for the skin
# returns the matched skin name from the CS2 item json data

#intended input ex) "ak47 redline fn"
def search_skin(user_query):
    NORM_SKIN_ARRAY = [normalize(skin) for skin in SKIN_ARRAY]
    best_match = None
    best_score = 0

    # parse the input down
    norm_input = normalize(user_query)
    print(norm_input)

    for i,skin in enumerate(NORM_SKIN_ARRAY):
            score = fuzz.token_sort_ratio(norm_input, skin)
            
            if score > best_score:
                best_score = score
                best_match = SKIN_ARRAY[i]
    
    print(best_match)

    return best_match