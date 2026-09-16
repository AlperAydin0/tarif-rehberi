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
def test_add_ingredient_to_recipe_persists_relation(test_db) -> None:
    recipe = create_recipe(
        Recipe(
            id=None,
            name="Menemen",
            category="Kahvaltı",
            prep_time=20,
            instructions="Pişir.",
        )
    )
    ingredient = create_ingredient(
        Ingredient(
            id=None,
            name="Domates",
            quantity=10.0,
            unit="adet",
            unit_price=10.0,
        )
    )

    assert recipe.id is not None
    assert ingredient.id is not None

    add_ingredient_to_recipe(recipe.id, ingredient.id, 2.5)

    ingredients = get_recipe_ingredients(recipe.id)

    assert ingredients == [(ingredient, 2.5)]


def test_get_recipe_ingredients_returns_multiple_relations(test_db) -> None:
    recipe = create_recipe(
        Recipe(
            id=None,
            name="Menemen",
            category="Kahvaltı",
            prep_time=20,
            instructions="Pişir.",
        )
    )

    tomato = create_ingredient(
        Ingredient(
            id=None,
            name="Domates",
            quantity=10.0,
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

    assert ingredients == [
        (tomato, 2.0),
        (egg, 3.0),
    ]


def test_get_recipe_ingredients_returns_empty_for_recipe_without_ingredients(
    test_db,
) -> None:
    recipe = create_recipe(
        Recipe(
            id=None,
            name="Boş Tarif",
            category="Test",
            prep_time=10,
            instructions="Hazırla.",
        )
    )

    assert recipe.id is not None

    assert get_recipe_ingredients(recipe.id) == []


def test_get_recipe_ingredients_returns_empty_for_unknown_recipe(
    test_db,
) -> None:
    assert get_recipe_ingredients(999999) == []


def test_update_recipe_ingredient_quantity_updates_relation(
    test_db,
) -> None:
    recipe = create_recipe(
        Recipe(
            id=None,
            name="Krep",
            category="Kahvaltı",
            prep_time=20,
            instructions="Karıştır.",
        )
    )

    flour = create_ingredient(
        Ingredient(
            id=None,
            name="Un",
            quantity=10.0,
            unit="kg",
            unit_price=30.0,
        )
    )

    assert recipe.id is not None
    assert flour.id is not None

    add_ingredient_to_recipe(recipe.id, flour.id, 2.0)

    update_recipe_ingredient_quantity(
        recipe.id,
        flour.id,
        4.5,
    )

    ingredients = get_recipe_ingredients(recipe.id)

    assert ingredients == [(flour, 4.5)]


def test_remove_ingredient_from_recipe_removes_only_selected_relation(
    test_db,
) -> None:
    recipe = create_recipe(
        Recipe(
            id=None,
            name="Menemen",
            category="Kahvaltı",
            prep_time=20,
            instructions="Pişir.",
        )
    )

    tomato = create_ingredient(
        Ingredient(
            id=None,
            name="Domates",
            quantity=10.0,
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

    remove_ingredient_from_recipe(recipe.id, tomato.id)

    ingredients = get_recipe_ingredients(recipe.id)

    assert ingredients == [(egg, 3.0)]


def test_remove_ingredient_from_recipe_leaves_recipe_empty(
    test_db,
) -> None:
    recipe = create_recipe(
        Recipe(
            id=None,
            name="Pilav",
            category="Ana Yemek",
            prep_time=30,
            instructions="Pişir.",
        )
    )

    rice = create_ingredient(
        Ingredient(
            id=None,
            name="Pirinç",
            quantity=10.0,
            unit="kg",
            unit_price=50.0,
        )
    )

    assert recipe.id is not None
    assert rice.id is not None

    add_ingredient_to_recipe(recipe.id, rice.id, 2.0)

    remove_ingredient_from_recipe(recipe.id, rice.id)

    assert get_recipe_ingredients(recipe.id) == []


def test_update_recipe_ingredient_quantity_does_not_change_other_relations(
    test_db,
) -> None:
    recipe = create_recipe(
        Recipe(
            id=None,
            name="Krep",
            category="Kahvaltı",
            prep_time=20,
            instructions="Karıştır.",
        )
    )

    flour = create_ingredient(
        Ingredient(
            id=None,
            name="Un",
            quantity=10.0,
            unit="kg",
            unit_price=30.0,
        )
    )

    milk = create_ingredient(
        Ingredient(
            id=None,
            name="Süt",
            quantity=10.0,
            unit="L",
            unit_price=25.0,
        )
    )

    assert recipe.id is not None
    assert flour.id is not None
    assert milk.id is not None

    add_ingredient_to_recipe(recipe.id, flour.id, 2.0)
    add_ingredient_to_recipe(recipe.id, milk.id, 1.0)

    update_recipe_ingredient_quantity(recipe.id, flour.id, 5.0)

    ingredients = get_recipe_ingredients(recipe.id)

    assert set(ingredients) == {
        (flour, 5.0),
        (milk, 1.0),
    }

def test_update_unknown_recipe_ingredient_relation_does_not_create_relation(
    test_db,
) -> None:
    recipe = create_recipe(
        Recipe(
            id=None,
            name="Menemen",
            category="Kahvaltı",
            prep_time=20,
            instructions="Pişir.",
        )
    )

    tomato = create_ingredient(
        Ingredient(
            id=None,
            name="Domates",
            quantity=10.0,
            unit="adet",
            unit_price=10.0,
        )
    )

    assert recipe.id is not None
    assert tomato.id is not None

    update_recipe_ingredient_quantity(
        recipe.id,
        tomato.id,
        5.0,
    )

    assert get_recipe_ingredients(recipe.id) == []


def test_remove_unknown_recipe_ingredient_relation_is_safe(
    test_db,
) -> None:
    recipe = create_recipe(
        Recipe(
            id=None,
            name="Menemen",
            category="Kahvaltı",
            prep_time=20,
            instructions="Pişir.",
        )
    )

    tomato = create_ingredient(
        Ingredient(
            id=None,
            name="Domates",
            quantity=10.0,
            unit="adet",
            unit_price=10.0,
        )
    )

    assert recipe.id is not None
    assert tomato.id is not None

    remove_ingredient_from_recipe(recipe.id, tomato.id)

    assert get_recipe_ingredients(recipe.id) == []


def test_same_ingredient_can_be_used_by_multiple_recipes(
    test_db,
) -> None:
    first_recipe = create_recipe(
        Recipe(
            id=None,
            name="Menemen",
            category="Kahvaltı",
            prep_time=20,
            instructions="Pişir.",
        )
    )

    second_recipe = create_recipe(
        Recipe(
            id=None,
            name="Domates Salatası",
            category="Salata",
            prep_time=10,
            instructions="Karıştır.",
        )
    )

    tomato = create_ingredient(
        Ingredient(
            id=None,
            name="Domates",
            quantity=10.0,
            unit="adet",
            unit_price=10.0,
        )
    )

    assert first_recipe.id is not None
    assert second_recipe.id is not None
    assert tomato.id is not None

    add_ingredient_to_recipe(
        first_recipe.id,
        tomato.id,
        3.0,
    )
    add_ingredient_to_recipe(
        second_recipe.id,
        tomato.id,
        1.0,
    )

    assert get_recipe_ingredients(first_recipe.id) == [
        (tomato, 3.0),
    ]
    assert get_recipe_ingredients(second_recipe.id) == [
        (tomato, 1.0),
    ]


def test_updating_one_recipe_relation_does_not_affect_another(
    test_db,
) -> None:
    first_recipe = create_recipe(
        Recipe(
            id=None,
            name="Menemen",
            category="Kahvaltı",
            prep_time=20,
            instructions="Pişir.",
        )
    )

    second_recipe = create_recipe(
        Recipe(
            id=None,
            name="Domates Sosu",
            category="Sos",
            prep_time=15,
            instructions="Pişir.",
        )
    )

    tomato = create_ingredient(
        Ingredient(
            id=None,
            name="Domates",
            quantity=10.0,
            unit="adet",
            unit_price=10.0,
        )
    )

    assert first_recipe.id is not None
    assert second_recipe.id is not None
    assert tomato.id is not None

    add_ingredient_to_recipe(first_recipe.id, tomato.id, 3.0)
    add_ingredient_to_recipe(second_recipe.id, tomato.id, 1.0)

    update_recipe_ingredient_quantity(
        first_recipe.id,
        tomato.id,
        5.0,
    )

    assert get_recipe_ingredients(first_recipe.id) == [
        (tomato, 5.0),
    ]
    assert get_recipe_ingredients(second_recipe.id) == [
        (tomato, 1.0),
    ]


def test_removing_one_recipe_relation_does_not_affect_another(
    test_db,
) -> None:
    first_recipe = create_recipe(
        Recipe(
            id=None,
            name="Menemen",
            category="Kahvaltı",
            prep_time=20,
            instructions="Pişir.",
        )
    )

    second_recipe = create_recipe(
        Recipe(
            id=None,
            name="Domates Sosu",
            category="Sos",
            prep_time=15,
            instructions="Pişir.",
        )
    )

    tomato = create_ingredient(
        Ingredient(
            id=None,
            name="Domates",
            quantity=10.0,
            unit="adet",
            unit_price=10.0,
        )
    )

    assert first_recipe.id is not None
    assert second_recipe.id is not None
    assert tomato.id is not None

    add_ingredient_to_recipe(first_recipe.id, tomato.id, 3.0)
    add_ingredient_to_recipe(second_recipe.id, tomato.id, 1.0)

    remove_ingredient_from_recipe(
        first_recipe.id,
        tomato.id,
    )

    assert get_recipe_ingredients(first_recipe.id) == []
    assert get_recipe_ingredients(second_recipe.id) == [
        (tomato, 1.0),
    ]