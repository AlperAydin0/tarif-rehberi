from dataclasses import dataclass


@dataclass(frozen=True)
class Recipe:
    id: int | None
    name: str
    category: str
    prep_time: int
    instructions: str
