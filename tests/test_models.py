from dataclasses import FrozenInstanceError

import pytest

from tarif_rehberi.models.ingredient import Ingredient
from tarif_rehberi.models.recipe import Recipe


def test_ingredient_creation() -> None:
    ingredient = Ingredient(
        id=None, name="Domates", quantity=5.0, unit="kg", unit_price=40.0
    )
    assert ingredient.id is None
    assert ingredient.name == "Domates"
    assert ingredient.quantity == 5.0
    assert ingredient.unit == "kg"
    assert ingredient.unit_price == 40.0


def test_recipe_creation() -> None:
    recipe: Recipe = Recipe(
        id=None,
        name="Menemen",
        category="Kahvaltı",
        prep_time=15,
        instructions="Domatesleri doğra ve pişir.",
    )

    assert recipe.id is None
    assert recipe.name == "Menemen"
    assert recipe.category == "Kahvaltı"
    assert recipe.prep_time == 15
    assert recipe.instructions == "Domatesleri doğra ve pişir."


def test_ingredient_stores_all_fields() -> None:
    ingredient = Ingredient(
        id=1,
        name="Domates",
        quantity=5.5,
        unit="kg",
        unit_price=18.75,
    )

    assert ingredient.id == 1
    assert ingredient.name == "Domates"
    assert ingredient.quantity == 5.5
    assert ingredient.unit == "kg"
    assert ingredient.unit_price == 18.75


def test_ingredient_accepts_none_id() -> None:
    ingredient = Ingredient(
        id=None,
        name="Domates",
        quantity=5.0,
        unit="adet",
        unit_price=10.0,
    )

    assert ingredient.id is None


def test_ingredient_is_immutable() -> None:
    ingredient = Ingredient(
        id=1,
        name="Domates",
        quantity=5.0,
        unit="adet",
        unit_price=10.0,
    )

    with pytest.raises(FrozenInstanceError):
        ingredient.name = "Biber"


def test_ingredient_equality_uses_all_fields() -> None:
    first = Ingredient(
        id=1,
        name="Domates",
        quantity=5.0,
        unit="adet",
        unit_price=10.0,
    )
    second = Ingredient(
        id=1,
        name="Domates",
        quantity=5.0,
        unit="adet",
        unit_price=10.0,
    )

    assert first == second


def test_ingredient_different_values_are_not_equal() -> None:
    first = Ingredient(
        id=1,
        name="Domates",
        quantity=5.0,
        unit="adet",
        unit_price=10.0,
    )
    second = Ingredient(
        id=1,
        name="Domates",
        quantity=6.0,
        unit="adet",
        unit_price=10.0,
    )

    assert first != second


def test_recipe_stores_all_fields() -> None:
    recipe = Recipe(
        id=1,
        name="Menemen",
        category="Kahvaltı",
        prep_time=20,
        instructions="Malzemeleri karıştır ve pişir.",
    )

    assert recipe.id == 1
    assert recipe.name == "Menemen"
    assert recipe.category == "Kahvaltı"
    assert recipe.prep_time == 20
    assert recipe.instructions == "Malzemeleri karıştır ve pişir."


def test_recipe_accepts_none_id() -> None:
    recipe = Recipe(
        id=None,
        name="Menemen",
        category="Kahvaltı",
        prep_time=20,
        instructions="Pişir.",
    )

    assert recipe.id is None


def test_recipe_is_immutable() -> None:
    recipe = Recipe(
        id=1,
        name="Menemen",
        category="Kahvaltı",
        prep_time=20,
        instructions="Pişir.",
    )

    with pytest.raises(FrozenInstanceError):
        recipe.name = "Krep"


def test_recipe_equality_uses_all_fields() -> None:
    first = Recipe(
        id=1,
        name="Menemen",
        category="Kahvaltı",
        prep_time=20,
        instructions="Pişir.",
    )
    second = Recipe(
        id=1,
        name="Menemen",
        category="Kahvaltı",
        prep_time=20,
        instructions="Pişir.",
    )

    assert first == second


def test_recipe_different_values_are_not_equal() -> None:
    first = Recipe(
        id=1,
        name="Menemen",
        category="Kahvaltı",
        prep_time=20,
        instructions="Pişir.",
    )
    second = Recipe(
        id=1,
        name="Menemen",
        category="Kahvaltı",
        prep_time=30,
        instructions="Pişir.",
    )

    assert first != second
