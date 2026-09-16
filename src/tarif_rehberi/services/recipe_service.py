from tarif_rehberi.models.ingredient import Ingredient
from tarif_rehberi.models.recipe import Recipe
from tarif_rehberi.repositories.recipe_ingredient_repository import (
    get_recipe_ingredients,
)
from tarif_rehberi.repositories.recipe_repository import get_all_recipes

RecipeIngredient = tuple[Ingredient, float]


def calculate_recipe_match(recipe_id: int, user_ingredients: dict[int, float]) -> float:
    recipe_ingredients: list[RecipeIngredient] = get_recipe_ingredients(recipe_id)

    if not recipe_ingredients:
        return 0.0

    available_count: int = sum(
        1
        for i, required_quantity in recipe_ingredients
        if i.id is not None and user_ingredients.get(i.id, 0.0) >= required_quantity
    )

    match: float = (available_count / len(recipe_ingredients)) * 100

    return round(match, 2)


def find_missing_ingredients(
    recipe_id: int,
    user_ingredients: dict[int, float],
) -> list[Ingredient]:
    recipe_ingredients: list[RecipeIngredient] = get_recipe_ingredients(recipe_id)

    missing: list[Ingredient] = [
        ingredient
        for ingredient, required_quantity in recipe_ingredients
        if ingredient.id is None
        or user_ingredients.get(ingredient.id, 0.0) < required_quantity
    ]

    return missing


RecipeMatch = tuple[Recipe, float]


def recommend_recipes(user_ingredients: dict[int, float]) -> list[RecipeMatch]:
    recipes: list[Recipe] = get_all_recipes()

    recommendations: list[RecipeMatch] = []

    for recipe in recipes:
        if recipe.id is None:
            continue

        match_percentage: float = calculate_recipe_match(
            recipe.id,
            user_ingredients,
        )
        if match_percentage <= 0.0:
            continue

        recommendations.append((recipe, match_percentage))

    recommendations.sort(
        key=lambda item: (
            -item[1],
            item[0].name,
        )
    )

    return recommendations


def calculate_recipe_cost(recipe_id: int) -> float:
    recipe_ingredients: list[RecipeIngredient] = get_recipe_ingredients(recipe_id)

    total_cost: float = 0.0

    for ingredient, required_quantity in recipe_ingredients:
        total_cost += ingredient.unit_price * required_quantity

    return round(total_cost, 2)
