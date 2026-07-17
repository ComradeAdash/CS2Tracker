# CS2Tracker

This project currently tracks CS2 skin prices by using the SkinPort V1 API endpoint. It pulls all active listings and
stores them into a PostgreSQL database using Cron for regular updates.

# Features

## Skin Lemur

Skin Lemur is a supplementary discord bot that shows prices for live listings on the Steam Community Marketplace, CSFloat, and SkinPort :DD

### Commands

### Steam Market Price - /skin

``` /skin ak47 vulcan ft ```

This displays the lowest and median price found on the Steam market

The query should be in the "weapon skin-name wear/quality" format, as shown above