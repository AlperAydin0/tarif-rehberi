from tarif_rehberi.models.ingredient import Ingredient
from tarif_rehberi.repositories.ingredient_repository import (
    create_ingredient,
    delete_ingredient,
    get_all_ingredients,
    get_ingredient,
    update_ingredient,
)


def create_ingredient_if_not_exists(
    ingredient: Ingredient,
) -> Ingredient:
    ingredients: list[Ingredient] = get_all_ingredients()

    for existing in ingredients:
        if existing.name == ingredient.name:
            return existing

    return create_ingredient(ingredient)


def get_ingredient_by_id(
    ingredient_id: int,
) -> Ingredient | None:
    return get_ingredient(ingredient_id)


def update_ingredient_by_id(
    ingredient: Ingredient,
) -> Ingredient:
    return update_ingredient(ingredient)


def delete_ingredient_by_id(
    ingredient_id: int,
) -> bool:
    return delete_ingredient(ingredient_id)


def get_all_ingredients_sorted() -> list[Ingredient]:
    ingredients: list[Ingredient] = get_all_ingredients()

    return sorted(
        ingredients,
        key=lambda ingredient: ingredient.name.lower(),
    )