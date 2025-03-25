from dataclasses import dataclass
from typing import Optional

from pokemon_type import PokemonType


@dataclass
class Pokemon:
    name: str
    type_1: PokemonType
    type_2: Optional[PokemonType]
    total_base_stats: int
    is_starter: bool
    link: str
