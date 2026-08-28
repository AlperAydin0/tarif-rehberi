import sqlite3
import pytest

from tarif_rehberi.models.recipe import Recipe


def test_create_recipe(test_db) -> None:
    recipe = Recipe(
        id=None,
        name="Mercimek Çorbası",
        category="Çorba",
        prep_time=15,
        instructions="""""",
    )
    created: Recipe = create_recipe(recipe)
    assert created.id is not None
    assert created.name == "Mercimek Çorbası"
    assert created.category == "Çorba"
    assert created.prep_time == 15
    assert created.instructions == """"""


def test_get_recipe(test_db) -> None:
    recipe = Recipe(
        id=None,
        name="Mercimek Çorbası",
        category="Çorba",
        prep_time=15,
        instructions="""""",
    )
    created: Recipe = create_recipe(recipe)
    assert created.id is not None

    found: Recipe | None = get_recipe(created.id)
    assert found is not None
    assert found.name == "Mercimek Çorbası"
    assert found.category == "Çorba"
    assert found.prep_time == 15
    assert found.instructions == """"""


def test_get_nonexistent_recipe(test_db) -> None:
    found: Ingredient | None = get_recipe(999)
    assert found is None


def test_get_all_recipes(test_db) -> None:
    recipe_1 = Recipe(
        id=None,
        name="Mercimek Çorbası",
        category="Çorba",
        prep_time=15,
        instructions="""""",
    )
    recipe_2 = Recipe(
        id=None,
        name="Ezogelin Çorbası",
        category="Çorba",
        prep_time=15,
        instructions="""""",
    )

    create_recipe(recipe_1)
    create_recipe(recipe_2)

    recipes: list[Recipe] = get_all_recipes()
    assert len(recipes) == 2

    names: list[str] = [r.name for r in recipes]
    assert names == [
        "Mercimek Çorbası",
        "Ezogelin Çorbası",
    ]


def test_update_recipe(test_db) -> None:
    recipe = Recipe(
        id=None,
        name="Mercimek Çorbası",
        category="Çorba",
        prep_time=15,
        instructions="""""",
    )

    created: Recipe = create_recipe(recipe)
    assert created.id is not None

    updated = Recipe(
        id=created.id,
        name="Mercimek Çorbası",
        category="Çorba",
        prep_time=20,
        instructions="""Tarif""",
    )

    result: Recipe = update_recipe(updated)
    assert result == updated

    found: Recipe | None = get_recipe(created.id)
    assert found == updated


def test_delete_recipe(test_db) -> None:
    recipe = Recipe(
        id=None,
        name="Mercimek Çorbası",
        category="Çorba",
        prep_time=15,
        instructions="""""",
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
    recipe = Recipe(
        id=None,
        name="Mercimek Çorbası",
        category="Çorba",
        prep_time=15,
        instructions="""""",
    )

    create_recipe(recipe)
    with pytest.raises(sqlite3.IntegrityError):
        create_recipe(recipe)
