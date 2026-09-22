'''

variables / data structures for discord, database, .env, and static data

'''

import os
import re
from dotenv import load_dotenv

# Ensure we load the .env file located in the same directory as this config file
_here = os.path.dirname(__file__)
load_dotenv(os.path.join(_here, ".env"))

DATABASE_URL = os.getenv("DATABASE_URL")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Constant Data

EXTERIOR_ORDER = {
    "Factory New": 1,
    "Minimal Wear": 2,
    "Field-Tested": 3,
    "Well-Worn": 4,
    "Battle-Scarred": 5,
}

WEAPON_TYPES = {

    "CZ75-Auto": "Pistol",
    "Desert Eagle": "Pistol",
    "Dual Berettas": "Pistol",
    "Five-SeveN": "Pistol",
    "Glock-18": "Pistol",
    "P2000": "Pistol",
    "P250": "Pistol",
    "R8 Revolver": "Pistol",
    "Tec-9": "Pistol",
    "USP-S": "Pistol",

    "AK-47": "Rifle",
    "AUG": "Rifle",
    "AWP": "Rifle",
    "FAMAS": "Rifle",
    "G3SG1": "Rifle",
    "Galil AR": "Rifle",
    "M4A1-S": "Rifle",
    "M4A4": "Rifle",
    "SCAR-20": "Rifle",
    "SG 553": "Rifle",
    "SSG 08": "Rifle",

    "MAC-10": "SMG",
    "MP5-SD": "SMG",
    "MP7": "SMG",
    "MP9": "SMG",
    "P90": "SMG",
    "PP-Bizon": "SMG",
    "UMP-45": "SMG",

    "MAG-7": "Heavy",
    "Nova": "Heavy",
    "Sawed-Off": "Heavy",
    "XM1014": "Heavy",
    "M249": "Heavy",
    "Negev": "Heavy",

    "Bayonet": "Knife",
    "Bowie Knife": "Knife",
    "Butterfly Knife": "Knife",
    "Classic Knife": "Knife",
    "Falchion Knife": "Knife",
    "Flip Knife": "Knife",
    "Gut Knife": "Knife",
    "Huntsman Knife": "Knife",
    "Karambit": "Knife",
    "Kukri Knife": "Knife",
    "M9 Bayonet": "Knife",
    "Navaja Knife": "Knife",
    "Nomad Knife": "Knife",
    "Paracord Knife": "Knife",
    "Shadow Daggers": "Knife",
    "Skeleton Knife": "Knife",
    "Stiletto Knife": "Knife",
    "Survival Knife": "Knife",
    "Talon Knife": "Knife",
    "Ursus Knife": "Knife",

    "Bloodhound Gloves": "Gloves",
    "Broken Fang Gloves": "Gloves",
    "Driver Gloves": "Gloves",
    "Hand Wraps": "Gloves",
    "Hydra Gloves": "Gloves",
    "Moto Gloves": "Gloves",
    "Specialist Gloves": "Gloves",
    "Sport Gloves": "Gloves",
}

# main target categories

CATEGORIES = [
    "Knife",
    "Gloves",
    "Pistol",
    "Rifle",
    "SMG",
    "heavy",
    "agent"
]

SKIN_PATTERN = re.compile(
    r"^(?P<weapon>.+?)"
    r"\s\|\s"
    r"(?P<skin>.+?)"
    r"\s\((?P<exterior>"
    r"Factory New|"
    r"Minimal Wear|"
    r"Field-Tested|"
    r"Well-Worn|"
    r"Battle-Scarred"
    r")\)$"
)