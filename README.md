<div align="center">
  <h1 align="center">Counter-Strike 2 Item Tracker</h1>

  <p align="center">
    Track Counter-strike 2 skin prices over time and check Steam Market prices directly from Discord
  </p>
</div>

<div align="center">
  <h3>Built With</h3>

  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&amp;logo=python&amp;logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&amp;logo=postgresql&amp;logoColor=white" alt="PostgreSQL" />
  <img src="https://img.shields.io/badge/Docker_Compose-2496ED?style=flat-square&amp;logo=docker&amp;logoColor=white" alt="Docker Compose" />
  <img src="https://img.shields.io/badge/discord.py-5865F2?style=flat-square&amp;logo=discord&amp;logoColor=white" alt="discord.py" />
  <img src="https://img.shields.io/badge/Requests-2A6F97?style=flat-square" alt="Requests" />
  <img src="https://img.shields.io/badge/HTTPX-3B82F6?style=flat-square" alt="HTTPX" />
  <img src="https://img.shields.io/badge/RapidFuzz-F59E0B?style=flat-square" alt="RapidFuzz" />
  <img src="https://img.shields.io/badge/Psycopg-336791?style=flat-square" alt="Psycopg" />
  <img src="https://img.shields.io/badge/python--dotenv-ECD53F?style=flat-square&amp;logo=dotenv&amp;logoColor=black" alt="python-dotenv" />
</div>

## About The Project

CS2 skins have their own market, and keeping up with prices can mean jumping
between sites just to check a single item. CS2Tracker brings together price
collection and Discord lookups to make that a little easier.

The project collects item price summaries from the Skinport V1 API and stores
them in PostgreSQL. Each collection run adds price observations, building a
history without overwriting earlier prices.

Skin Lemur is the project's supplementary Discord bot (and a really cool
lemur). Give it a weapon, skin name, and wear condition, and it looks up the
lowest and median prices returned by the Steam Community Market.

These are separate workflows: the database collector uses Skinport, while
the Discord bot queries Steam directly.

### Features

- **Skinport price collection:** Fetch item price summaries, including minimum,
  maximum, mean, median, and suggested prices, plus available quantity.
- **Price history:** Store observations by item and collection run in PostgreSQL.
- **Organized item data:** Store categories, weapon names, wear conditions,
  and StatTrak or Souvenir flags alongside item records.
- **Discord price lookups:** Use `/skin` to request Steam Market prices without
  leaving your server.
- **Flexible skin searches:** Use abbreviated queries such as `ak47 vulcan ft`,
  with RapidFuzz matching them to market item names.
- **Local database setup:** Run PostgreSQL through the included Docker Compose
  configuration.

## Skin Lemur

### Steam Market Price — `/skin`

Select the `/skin` command in Discord and enter a query in its `skin` field:

```text
ak47 vulcan ft
```

The bot matches your query to a market item name and responds with an embed
showing its lowest and median Steam Market prices, when available.

Queries follow the format:

```text
weapon skin-name wear
```

Supported wear abbreviations:

| Abbreviation | Wear condition |
| --- | --- |
| `fn` | Factory New |
| `mw` | Minimal Wear |
| `ft` | Field-Tested |
| `ww` | Well-Worn |
| `bs` | Battle-Scarred |

Skin Lemur also includes a `/hello` command. Say hi. :)

## Project Structure

```text
cs_skin_tracker/
├── requirements.txt           Python dependencies
└── src/
    ├── botRunner.py           Discord bot entry point
    ├── dbRunner.py            Skinport database collection entry point
    ├── config.py              Environment loading and item definitions
    ├── compose.yaml           Local PostgreSQL service
    ├── bot/
    │   └── discord_api.py     Discord commands and response embeds
    ├── scripts/
    │   ├── steam.py           Steam prices and skin-name catalog retrieval
    │   ├── skin_port.py       Skinport API requests
    │   ├── weapon_skin.py     Query normalization and fuzzy matching
    │   └── seed.py            Database reference-data seeding
    ├── data/
    │   ├── schema.sql         Tables, constraints, and indexes
    │   ├── setup.py           Reference-data insertion helpers
    │   └── queries.py         Item updates and price-history storage
    └── tests/
        └── test_weapon_skin.py  Normalization and matching tests
```

## Acknowledgments

- Skinport for the item pricing API used by the database collector.
- Steam Community Market for the price data used by Skin Lemur.
- [ByMykel's CSGO-API](https://github.com/ByMykel/CSGO-API) for the skin-name
  catalog used in searches.
- The open-source libraries that power the bot, database integration, and
  fuzzy matching.

<!--
Original README preserved below.

# CS2Tracker

This project currently tracks CS2 skin prices by using the SkinPort V1 API endpoint. It pulls all active listings and
stores them into a PostgreSQL database using Cron for regular updates.

# Features

## Skin Lemur

Skin Lemur is a supplementary discord bot (also a really cool Lemur) that shows prices for live listings on the Steam Community Marketplace

### Commands

### Steam Market Price - /skin

``` /skin ak47 vulcan ft ```

This displays the lowest and median price found on the Steam market

The query should be in the "weapon skin-name wear/quality" format, as shown above
-->
