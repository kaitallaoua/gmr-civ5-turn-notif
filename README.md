# gmr-civ5-turn-notif
Notify discord users when its their turn in giant multiplayer robot (civ5). This code was tested on python 3.10.4. Currently, it does not support opt-out for specific users if they wish to not be mentioned, though it wouldn't be too hard to add.

# How to use
1. Clone the repo
2. Install requirements: `pip install -r requirements.txt`
3. Rename `sample.config.json` to `config.json` and modify the entries as following

| `webhook_url`     | The URL of your discord webhook                                                                                      |
|-------------------|----------------------------------------------------------------------------------------------------------------------|
| `gmr_api_url`     | Do not modifiy                                                                                                       |
| `my_id`           | Your steam id/gmr id                                                                                                 |
| `gmr_auth_key`    | The auth key for your gmr game                                                                                       |
| `game_name`       | The name of your game                                                                                                |
| `gmr_discord_lut` | A sub dictionary for each user in the game where the key represents the steam/gmr id and the value is the discord id |
4. Run with `python3 gmr_notif_discord.py`
