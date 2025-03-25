from argparse import ArgumentParser, BooleanOptionalAction
from collections import deque
from dataclasses import asdict
from typing import Any

from pandas import DataFrame
from requests import get

from pokemon import Pokemon
from pokemon_type import PokemonType

_POKE_API_BASE_URL = "https://pokeapi.co/api/v2/"
_BULBAPEDIA_BASE_URL = "https://bulbapedia.bulbagarden.net/wiki/"


def main():
    game_versions = get_game_versions()

    argument_parser = ArgumentParser(
        description="This script generates a CSV file of candidate Pokémon to be considered when generating a Pokémon team.")
    argument_parser.add_argument("-g", "--game-version-id",
                                 dest="game_version_id",
                                 choices=game_versions.keys(),
                                 required=True,
                                 help="The game version ID for which to generate the candidate Pokémon, as defined by PokéAPI. Generally a hyphenated, lower-case string of the game title, such as \"omega-ruby\". Read more at https://pokeapi.co/docs/v2#version.")
    argument_parser.add_argument("-e", "--include-pokemon-which-can-evolve", dest="include_pokemon_which_can_evolve",
                                 action=BooleanOptionalAction,
                                 default=False,
                                 help="Whether or not Pokémon which can still evolve should be considered as candidates. Teams are generally made up of fully evolved Pokémon, so this is not enabled by default.")
    argument_parser.add_argument("-o", "--output-file", dest="output_file_name", default="candidate_pokemon.csv")

    args = argument_parser.parse_args()
    game_version_id = args.game_version_id

    print(f"Generating candidate Pokémon for {game_version_id}...")

    data_frame = DataFrame([asdict(candidate_pokemon) for candidate_pokemon in
                            generate_candidate_pokemon_list(pokedex_url=get_pokedex_url(game_versions[game_version_id]),
                                                            include_pokemon_which_can_evolve=args.include_pokemon_which_can_evolve)])
    data_frame.rename(columns={
        "name": "Name",
        "type_1": "Type 1",
        "type_2": "Type 2",
        "total_base_stats": "Total Base Stats",
        "is_starter": "Is Starter",
        "link": "Link",
    })
    data_frame.to_csv(path_or_buf=args.output_file_name, index=False)

    print(f"Candidate Pokémon have been successfully generated and output to {args.output_file_name}.")


def get_game_versions() -> dict[str, str]:
    return {result["name"]: result["url"] for result in
            get(f"{_POKE_API_BASE_URL}/version?limit=100").json()["results"]}


def get_pokedex_url(game_version_url: str) -> str:
    return get(get(game_version_url).json()["version_group"]["url"]).json()["pokedexes"][0]["url"]


def generate_candidate_pokemon_list(pokedex_url: str, include_pokemon_which_can_evolve: bool) -> list[Pokemon]:
    candidate_pokemon_list = []
    for pokemon_entry in get(pokedex_url).json()['pokemon_entries']:
        species = get(pokemon_entry["pokemon_species"]["url"]).json()
        pokemon = get(f"{_POKE_API_BASE_URL}pokemon/{species["id"]}").json()
        if include_pokemon_which_can_evolve or is_final_evolution(species=species):
            capitalized_name = pokemon["name"].capitalize()
            candidate_pokemon_list.append(
                Pokemon(
                    name=capitalized_name,
                    type_1=PokemonType.from_string(pokemon["types"][0]["type"]["name"]),
                    type_2=PokemonType.from_string(pokemon["types"][1]["type"]["name"]) if len(
                        pokemon["types"]) > 1 else None,
                    total_base_stats=sum([stat["base_stat"] for stat in pokemon["stats"]]),
                    is_starter=pokemon_entry["entry_number"] <= 9,
                    link=f"{_BULBAPEDIA_BASE_URL}{pokemon["name"].capitalize()}_(Pokemon)"
                )
            )
    return candidate_pokemon_list


def is_final_evolution(species: dict[str, Any]) -> bool:
    evolution_chain = get(species["evolution_chain"]["url"]).json()
    final_evolutions = set()
    queue = deque()
    queue.append(evolution_chain["chain"])
    while len(queue) > 0:
        chain = queue.popleft()
        if not chain["evolves_to"]:
            final_evolutions.add(chain["species"]["name"])
        queue.extend(chain["evolves_to"])

    return species["name"] in final_evolutions


if __name__ == "__main__":
    main()
