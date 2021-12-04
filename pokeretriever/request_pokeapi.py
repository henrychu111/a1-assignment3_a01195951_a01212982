import enum
import aiohttp
import asyncio
from pokeretriever.pokedex_object import Pokemon
from pokeretriever.pokedex_object import Ability
from pokeretriever.pokedex_object import Stat
from pokeretriever.pokedex_object import Move
from request import Request

POKEMON_ENDPOINT = "https://pokeapi.co/api/v2/pokemon/{}/"
ABILITY_ENDPOINT = "https://pokeapi.co/api/v2/ability/{}/"
STAT_ENDPOINT = "https://pokeapi.co/api/v2/stat/{}/"
MOVE_ENDPOINT = "https://pokeapi.co/api/v2/move/{}/"


class PokedexMode(enum.Enum):
    """
    Lists the various modes that the Pokedex can run in.
    """
    # Pokemon mode
    POKEMON = "pokemon"
    # Ability mode
    ABILITY = "ability"
    # Move mode
    MOVE = "move"


class PokedexProvider:
    @staticmethod
    async def get_pokedex_data(data_identification: str, url: str, session: aiohttp.ClientSession) -> dict:
        """
        An async coroutine that executes GET http request. The response is
        converted to a json. The HTTP request and the json conversion are
        asynchronous processes that need to be awaited.
        :param data_identification: a str
        :param url: a string, the unformatted url (missing parameters)
        :param session: a HTTP session
        :return: a dict, json representation of response.
        """
        target_url = url.format(data_identification)
        try:
            response = await session.request(method="GET", url=target_url)
            if response.status != 200:
                exit("Error: Request URL not found. Unexpected response!")
            json_dict = await response.json()
            return json_dict
        except aiohttp.ClientConnectorError:
            exit("Error: Cannot connect to host!")

    @staticmethod
    async def fetch_pokedex_item_from_api(endpoint: str, request_data: list,
                                          session: aiohttp.ClientSession) -> list:
        """
        An async routine that fetches data from the api based on
        the search request.

        :param endpoint: a string
        :param request_data: a list
        :param session: a HTTP session
        :return: a list of the retrieved data
        """

        pokedex_list = []
        async_coroutines = [PokedexProvider.get_pokedex_data(data_identification, endpoint, session)
                            for data_identification in request_data]
        responses = await asyncio.gather(*async_coroutines)
        if endpoint == ABILITY_ENDPOINT:
            for response in responses:
                data_effect = [effect_entry for effect_entry in response["effect_entries"]
                               if effect_entry["language"]["name"] == "en"][0]

                pokemon_list = [pokemon["pokemon"]["name"] for pokemon in response["pokemon"]]

                pokedex_list.append(Ability(response["name"], response["id"], response["generation"]["name"],
                                            data_effect["effect"], data_effect["short_effect"], pokemon_list))
        elif endpoint == MOVE_ENDPOINT:
            for response in responses:
                data_effect = [effect_entry for effect_entry in response["effect_entries"]
                               if effect_entry["language"]["name"] == "en"][0]

                pokedex_list.append(Move(response["name"], response["id"], response["generation"]["name"],
                                         response["accuracy"], response["pp"], response["power"],
                                         response["type"]["name"],
                                         response["damage_class"]["name"], data_effect["short_effect"]))
        return pokedex_list

    @staticmethod
    async def fetch_pokemon_stat(base_stat: int, identification: str, session: aiohttp.ClientSession) -> list:
        """
        An async coroutine that fetches the pokemon stats data

        :param base_stat: an int
        :param identification: a string
        :param session: a HTTP request
        :return: Stat object
        """
        response = await PokedexProvider.get_pokedex_data(identification, STAT_ENDPOINT, session)
        return Stat(response["name"], response["id"], base_stat, response["is_battle_only"])

    @staticmethod
    def get_request_data(request: Request) -> list:
        """
        Checks the input data that the user enters

        :param request: a Request
        :return: data inputted or list of data from file
        """
        if request.data_input is not None:
            return [request.data_input]
        else:
            request_items = []
            try:
                with open(request.input_file) as f:
                    line = f.readline()
                    while line:
                        request_items.append(line.strip())
                        line = f.readline()
                f.close()
            except FileNotFoundError:
                exit("Error: File does not exist!")
            return request_items

    @staticmethod
    async def execute_request(request: Request) -> list:
        """
        Completes the request to retrieve the data desired

        :param request: a Request
        :return: list of data retrieved
        """
        request_data = PokedexProvider.get_request_data(request)
        pokedex_list = []
        async with aiohttp.ClientSession() as session:
            if request.mode == PokedexMode.POKEMON:
                async_coroutines = [PokedexProvider.get_pokedex_data(data_identification, POKEMON_ENDPOINT, session)
                                    for data_identification in request_data]
                responses = await asyncio.gather(*async_coroutines)
                for response in responses:
                    if request.expanded:
                        abilities = await PokedexProvider.fetch_pokedex_item_from_api(ABILITY_ENDPOINT,
                                                                      [ability["ability"]["name"] for ability in
                                                                       response["abilities"]],
                                                                      session)

                        moves = await PokedexProvider.fetch_pokedex_item_from_api(MOVE_ENDPOINT,
                                                                  [move["move"]["name"] for move in response["moves"]],
                                                                  session)

                        stats = [await PokedexProvider.fetch_pokemon_stat(stat["base_stat"], stat["stat"]["name"], session)
                                 for stat in response["stats"]]

                        pokedex_list.append(
                            Pokemon(response["name"], response["id"], response["height"], response["weight"],
                                    stats, [pokemon_type["type"]["name"] for pokemon_type in response["types"]],
                                    abilities, moves, request.expanded))
                    else:
                        pokedex_list.append(
                            Pokemon(response["name"], response["id"], response["height"], response["weight"], [],
                                    [pokemon_type["type"]["name"] for pokemon_type in response["types"]], [],
                                    [], request.expanded))

            elif request.mode == PokedexMode.ABILITY:
                pokedex_list = await PokedexProvider.fetch_pokedex_item_from_api(ABILITY_ENDPOINT, request_data, session)

            elif request.mode == PokedexMode.MOVE:
                pokedex_list = await PokedexProvider.fetch_pokedex_item_from_api(MOVE_ENDPOINT, request_data, session)
        return pokedex_list

    @staticmethod
    def print_pokedex_result(request: Request, pokedex_result: list):
        if request.output == "print":
            for item in pokedex_result:
                print(item)
        else:
            f = open(request.output, 'w')
            for item in pokedex_result:
                f.write(str(item))
                f.write("\n")
            f.close()
