import sqlite3

import pytest

from tarif_rehberi.models.recipe import Recipe
from tarif_rehberi.repositories.recipe_repository import (
    create_recipe,
    delete_recipe,
    get_all_recipes,
    get_recipe,
    update_recipe,
)


def test_create_recipe(test_db) -> None:
    recipe: Recipe = Recipe(
        id=None,
        name="Mercimek Çorbası",
        category="Çorba",
        prep_time=30,
        instructions="Mercimeği yıka ve pişir.",
    )

    created: Recipe = create_recipe(recipe)

    assert created.id is not None
    assert created.name == "Mercimek Çorbası"
    assert created.category == "Çorba"
    assert created.prep_time == 30
    assert created.instructions == "Mercimeği yıka ve pişir."


def test_get_recipe(test_db) -> None:
    recipe: Recipe = Recipe(
        id=None,
        name="Menemen",
        category="Kahvaltı",
        prep_time=20,
        instructions="Malzemeleri pişir.",
    )

    created: Recipe = create_recipe(recipe)

    assert created.id is not None

    found: Recipe | None = get_recipe(created.id)

    assert found is not None
    assert found.id == created.id
    assert found.name == "Menemen"
    assert found.category == "Kahvaltı"
    assert found.prep_time == 20
    assert found.instructions == "Malzemeleri pişir."


def test_get_nonexistent_recipe(test_db) -> None:
    found: Recipe | None = get_recipe(999)

    assert found is None


def test_get_all_recipes(test_db) -> None:
    first_recipe: Recipe = Recipe(
        id=None,
        name="Mercimek Çorbası",
        category="Çorba",
        prep_time=30,
        instructions="Mercimeği pişir.",
    )

    second_recipe: Recipe = Recipe(
        id=None,
        name="Menemen",
        category="Kahvaltı",
        prep_time=20,
        instructions="Domates ve yumurtayı pişir.",
    )

    create_recipe(first_recipe)
    create_recipe(second_recipe)

    recipes: list[Recipe] = get_all_recipes()

    assert len(recipes) == 2

    names: list[str] = [recipe.name for recipe in recipes]

    assert names == [
        "Menemen",
        "Mercimek Çorbası",
    ]


def test_update_recipe(test_db) -> None:
    recipe: Recipe = Recipe(
        id=None,
        name="Menemen",
        category="Kahvaltı",
        prep_time=20,
        instructions="Domates ve yumurtayı pişir.",
    )

    created: Recipe = create_recipe(recipe)

    assert created.id is not None

    updated: Recipe = Recipe(
        id=created.id,
        name="Menemen",
        category="Ana Yemek",
        prep_time=25,
        instructions="Yeni tarif talimatları.",
    )

    result: Recipe = update_recipe(updated)

    assert result == updated

    found: Recipe | None = get_recipe(created.id)

    assert found == updated


def test_delete_recipe(test_db) -> None:
    recipe: Recipe = Recipe(
        id=None,
        name="Menemen",
        category="Kahvaltı",
        prep_time=20,
        instructions="Domates ve yumurtayı pişir.",
    )

    created: Recipe = create_recipe(recipe)

    assert created.id is not None

    deleted: bool = delete_recipe(created.id)

    assert deleted is True

    found: Recipe | None = get_recipe(created.id)

    assert found is None


def test_delete_nonexistent_recipe(test_db) -> None:
    deleted: bool = delete_recipe(999)

    assert deleted is False


def test_duplicate_recipe_is_rejected(test_db) -> None:
    recipe: Recipe = Recipe(
        id=None,
        name="Menemen",
        category="Kahvaltı",
        prep_time=20,
        instructions="Domates ve yumurtayı pişir.",
    )

    create_recipe(recipe)

    with pytest.raises(sqlite3.IntegrityError):
        create_recipe(recipe)
