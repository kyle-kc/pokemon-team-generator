from enum import Enum


class PokemonType(str, Enum):
    FIGHTING = "Fighting"
    GROUND = "Ground"
    FIRE = "Fire"
    ICE = "Ice"
    ROCK = "Rock"
    WATER = "Water"
    GRASS = "Grass"
    FLYING = "Flying"
    BUG = "Bug"
    ELECTRIC = "Electric"
    PSYCHIC = "Psychic"
    GHOST = "Ghost"
    DARK = "Dark"
    STEEL = "Steel"
    POISON = "Poison"
    DRAGON = "Dragon"
    FAIRY = "Fairy"
    NORMAL = "Normal"

    @classmethod
    def from_string(cls, pokemon_type_string: str):
        return cls[pokemon_type_string.upper()]

ALL_POKEMON_TYPES = [pokemon_type for pokemon_type in PokemonType]

SUPER_EFFECTIVENESS_MAP = {
    PokemonType.FIGHTING: [PokemonType.ICE, PokemonType.ROCK, PokemonType.STEEL, PokemonType.DARK, PokemonType.NORMAL],
    PokemonType.GROUND: [PokemonType.ROCK, PokemonType.STEEL, PokemonType.FIRE, PokemonType.ELECTRIC,
                         PokemonType.POISON],
    PokemonType.FIRE: [PokemonType.STEEL, PokemonType.ICE, PokemonType.BUG, PokemonType.GRASS],
    PokemonType.ICE: [PokemonType.GROUND, PokemonType.FLYING, PokemonType.GRASS, PokemonType.DRAGON],
    PokemonType.ROCK: [PokemonType.FIRE, PokemonType.FLYING, PokemonType.ICE, PokemonType.BUG],
    PokemonType.WATER: [PokemonType.FIRE, PokemonType.GROUND, PokemonType.ROCK],
    PokemonType.GRASS: [PokemonType.GROUND, PokemonType.ROCK, PokemonType.WATER],
    PokemonType.FLYING: [PokemonType.FIGHTING, PokemonType.BUG, PokemonType.GRASS],
    PokemonType.BUG: [PokemonType.DARK, PokemonType.PSYCHIC, PokemonType.GRASS],
    PokemonType.ELECTRIC: [PokemonType.FLYING, PokemonType.WATER],
    PokemonType.PSYCHIC: [PokemonType.FIGHTING, PokemonType.POISON],
    PokemonType.GHOST: [PokemonType.PSYCHIC, PokemonType.GHOST],
    PokemonType.DARK: [PokemonType.PSYCHIC, PokemonType.GHOST],
    PokemonType.STEEL: [PokemonType.ICE, PokemonType.ROCK, PokemonType.FAIRY],
    PokemonType.POISON: [PokemonType.GRASS, PokemonType.FAIRY],
    PokemonType.DRAGON: [PokemonType.DRAGON],
    PokemonType.FAIRY: [PokemonType.FIGHTING, PokemonType.DRAGON, PokemonType.DARK],
    PokemonType.NORMAL: [],
}