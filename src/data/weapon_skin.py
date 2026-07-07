'''

Weapon skin name normalization / searching methods

Issues: skins that dont exist such as AWP asiimov fn (they only come in ft) create a mismatch

'''

import re
import data.steam as steam
from rapidfuzz import fuzz

SKIN_ARRAY = steam.get_all_skin_names(steam.skin_names_url)

wear_map =  {
"ft": "(Field Tested)",
"mw": "(Minimal Wear)",
"fn": "(Factory New)",
"bs": "(Battle Scarred)",
"ww": "(Well Worn)"
}

# Strips the query down, so it's easy to process
def normalize(input):
    for abbr, full in wear_map.items():
        input = re.sub(rf"\b{abbr}\b", full, input)
    input = input.lower()
    input = re.sub(r"[^a-z0-9\s]", "", input)
    input = re.sub(r"\s+", " ", input).strip()

    return input

# Taking in a user input query, normalizing it, and checking for the skin
# Returns the matched skin name from the CS2 item json data
#Intended input ex) "ak47 redline fn"
def search_skin(user_query):
    NORM_SKIN_ARRAY = [normalize(skin) for skin in SKIN_ARRAY]
    best_match = None
    best_score = 0

    norm_input = normalize(user_query)
    print(norm_input)

    for i,skin in enumerate(NORM_SKIN_ARRAY):
            score = fuzz.token_sort_ratio(norm_input, skin)
            
            if score > best_score:
                best_score = score
                best_match = SKIN_ARRAY[i]
    
    print(best_match)

    return best_match