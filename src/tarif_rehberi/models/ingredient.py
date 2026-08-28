from dataclasses import dataclass


@dataclass(frozen=True)
class Ingredient:
    id: int | None
    name: str
    quantity: float
    unit: str
    unit_price: float
