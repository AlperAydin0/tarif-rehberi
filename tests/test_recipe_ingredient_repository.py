import sqlite3

import pytest

from tarif_rehberi.models.ingredient import Ingredient
from tarif_rehberi.models.recipe import Recipe
from tarif_rehberi.repositories.ingredient_repository import (
    create_ingredient,
    delete_ingredient,
)
from tarif_rehberi.repositories.recipe_ingredient_repository import (
    add_ingredient_to_recipe,
    get_recipe_ingredients,
    remove_ingredient_from_recipe,
    update_recipe_ingredient_quantity,
)
from tarif_rehberi.repositories.recipe_repository import (
    create_recipe,
    delete_recipe,
)


def test_add_ingredient_to_recipe(test_db) -> None:
    recipe = create_recipe(
        Recipe(
            id=None,
            name="Menemen",
            category="Kahvaltı",
            prep_time=20,
            instructions="Domates ve yumurtayı pişir.",
        )
    )

    ingredient = create_ingredient(
        Ingredient(
            id=None,
            name="Domates",
            quantity=5.0,
            unit="adet",
            unit_price=10.0,
        )
    )

    assert recipe.id is not None
    assert ingredient.id is not None

    add_ingredient_to_recipe(
        recipe.id,
        ingredient.id,
        2.0,
    )

    ingredients = get_recipe_ingredients(recipe.id)

    assert len(ingredients) == 1
    assert ingredients[0] == (ingredient, 2.0)


def test_get_recipe_ingredients(test_db) -> None:
    recipe = create_recipe(
        Recipe(
            id=None,
            name="Menemen",
            category="Kahvaltı",
            prep_time=20,
            instructions="Domates ve yumurtayı pişir.",
        )
    )

    tomato = create_ingredient(
        Ingredient(
            id=None,
            name="Domates",
            quantity=5.0,
            unit="adet",
            unit_price=10.0,
        )
    )

    egg = create_ingredient(
        Ingredient(
            id=None,
            name="Yumurta",
            quantity=10.0,
            unit="adet",
            unit_price=5.0,
        )
    )

    assert recipe.id is not None
    assert tomato.id is not None
    assert egg.id is not None

    add_ingredient_to_recipe(recipe.id, tomato.id, 2.0)
    add_ingredient_to_recipe(recipe.id, egg.id, 3.0)

    ingredients = get_recipe_ingredients(recipe.id)

    assert len(ingredients) == 2
    assert ingredients[0] == (tomato, 2.0)
    assert ingredients[1] == (egg, 3.0)


def test_update_recipe_ingredient_quantity(test_db) -> None:
    recipe = create_recipe(
        Recipe(
            id=None,
            name="Menemen",
            category="Kahvaltı",
            prep_time=20,
            instructions="Domates ve yumurtayı pişir.",
        )
    )

    ingredient = create_ingredient(
        Ingredient(
            id=None,
            name="Domates",
            quantity=5.0,
            unit="adet",
            unit_price=10.0,
        )
    )

    assert recipe.id is not None
    assert ingredient.id is not None

    add_ingredient_to_recipe(recipe.id, ingredient.id, 2.0)

    update_recipe_ingredient_quantity(
        recipe.id,
        ingredient.id,
        4.0,
    )

    ingredients = get_recipe_ingredients(recipe.id)

    assert len(ingredients) == 1
    assert ingredients[0] == (ingredient, 4.0)


def test_remove_ingredient_from_recipe(test_db) -> None:
    recipe = create_recipe(
        Recipe(
            id=None,
            name="Menemen",
            category="Kahvaltı",
            prep_time=20,
            instructions="Domates ve yumurtayı pişir.",
        )
    )

    ingredient = create_ingredient(
        Ingredient(
            id=None,
            name="Domates",
            quantity=5.0,
            unit="adet",
            unit_price=10.0,
        )
    )

    assert recipe.id is not None
    assert ingredient.id is not None

    add_ingredient_to_recipe(recipe.id, ingredient.id, 2.0)

    removed = remove_ingredient_from_recipe(
        recipe.id,
        ingredient.id,
    )

    assert removed is True
    assert get_recipe_ingredients(recipe.id) == []


def test_remove_nonexistent_recipe_ingredient(test_db) -> None:
    removed = remove_ingredient_from_recipe(999, 999)

    assert removed is False


def test_duplicate_recipe_ingredient_is_rejected(test_db) -> None:
    recipe = create_recipe(
        Recipe(
            id=None,
            name="Menemen",
            category="Kahvaltı",
            prep_time=20,
            instructions="Domates ve yumurtayı pişir.",
        )
    )

    ingredient = create_ingredient(
        Ingredient(
            id=None,
            name="Domates",
            quantity=5.0,
            unit="adet",
            unit_price=10.0,
        )
    )

    assert recipe.id is not None
    assert ingredient.id is not None

    add_ingredient_to_recipe(recipe.id, ingredient.id, 2.0)

    with pytest.raises(sqlite3.IntegrityError):
        add_ingredient_to_recipe(recipe.id, ingredient.id, 3.0)


def test_recipe_delete_cascades_to_recipe_ingredients(test_db) -> None:
    recipe = create_recipe(
        Recipe(
            id=None,
            name="Menemen",
            category="Kahvaltı",
            prep_time=20,
            instructions="Domates ve yumurtayı pişir.",
        )
    )

    ingredient = create_ingredient(
        Ingredient(
            id=None,
            name="Domates",
            quantity=5.0,
            unit="adet",
            unit_price=10.0,
        )
    )

    assert recipe.id is not None
    assert ingredient.id is not None

    add_ingredient_to_recipe(recipe.id, ingredient.id, 2.0)

    deleted = delete_recipe(recipe.id)

    assert deleted is True
    assert get_recipe_ingredients(recipe.id) == []


def test_ingredient_delete_cascades_to_recipe_ingredients(
    test_db,
) -> None:
    recipe = create_recipe(
        Recipe(
            id=None,
            name="Menemen",
            category="Kahvaltı",
            prep_time=20,
            instructions="Domates ve yumurtayı pişir.",
        )
    )

    ingredient = create_ingredient(
        Ingredient(
            id=None,
            name="Domates",
            quantity=5.0,
            unit="adet",
            unit_price=10.0,
        )
    )

    assert recipe.id is not None
    assert ingredient.id is not None

    add_ingredient_to_recipe(recipe.id, ingredient.id, 2.0)

    deleted = delete_ingredient(ingredient.id)

    assert deleted is True
    assert get_recipe_ingredients(recipe.id) == []
