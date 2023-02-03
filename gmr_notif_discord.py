import asyncio
from datetime import datetime
from json import loads
from pathlib import Path

from aiohttp import ClientSession
from dateutil.parser import isoparse
from discord import Color, Embed, Webhook

config: dict[str, str] = loads(Path("config.json").read_text())

SLEEP_TIME_SEC = 60

def find_game(games: dict[str, dict[str, str]]) -> dict[str, str]:
    for game in games["Games"]:
        if game["Name"] == config["game_name"]:
            return game


async def main():
    last_player: str = ""
    first_run = True

    async with ClientSession() as session:
        webhook = Webhook.from_url(config["webhook_url"], session=session)

        while True:
            async with session.get(
                f"{config['gmr_api_url']}/GetGamesAndPlayers?playerIDText={config['my_id']}&authKey={config['gmr_auth_key']}"
            ) as response:
                players_and_games: dict[str, str] = await response.json()
            current_game = find_game(players_and_games)

            if current_game is None:
                await asyncio.sleep(SLEEP_TIME_SEC)
                continue

            current_turn = current_game["CurrentTurn"]

            if first_run: # drop first message on startup to prevent spam
                last_player = current_turn["UserId"]
                first_run = False


            if last_player == current_turn["UserId"]:
                await asyncio.sleep(SLEEP_TIME_SEC)
                continue

            last_player = current_turn["UserId"]

            await webhook.send(
                embed=Embed(
                    title=f"Game: {current_game['Name']}",
                    description=f"<@{config['gmr_discord_lut'][str(current_turn['UserId'])]}> [it's your turn.](http://multiplayerrobot.com/Game#{current_game['GameId']})",
                    color=Color.purple(),
                    timestamp=datetime.now(),
                )
                .set_author(
                    name="Giant Multiplayer Robot",
                    icon_url="http://multiplayerrobot.com/Content/images/New_Unit_Mech_94.png",
                )
                .set_footer(text="👾")
                .add_field(
                    name=f"Your turn expires <t:{int(isoparse(current_turn['Expires']).timestamp())}:R>.",
                    value="",
                )
            )

            await asyncio.sleep(SLEEP_TIME_SEC)


if __name__ == "__main__":
    asyncio.run(main())
