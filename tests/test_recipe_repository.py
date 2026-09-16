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


def test_create_recipe_persists_all_fields(test_db) -> None:
    recipe = Recipe(
        id=None,
        name="Mercimek Çorbası",
        category="Çorba",
        prep_time=35,
        instructions="Mercimeği pişir.",
    )

    created = create_recipe(recipe)

    assert created.id is not None
    assert created.name == "Mercimek Çorbası"
    assert created.category == "Çorba"
    assert created.prep_time == 35
    assert created.instructions == "Mercimeği pişir."


def test_get_recipe_returns_created_recipe(test_db) -> None:
    recipe = Recipe(
        id=None,
        name="Menemen",
        category="Kahvaltı",
        prep_time=20,
        instructions="Karıştır ve pişir.",
    )

    created = create_recipe(recipe)

    assert created.id is not None

    result = get_recipe(created.id)

    assert result == created


def test_get_recipe_returns_none_for_unknown_id(test_db) -> None:
    result = get_recipe(999999)

    assert result is None


def test_get_all_recipes_returns_all_created_recipes(test_db) -> None:
    first = create_recipe(
        Recipe(
            id=None,
            name="Menemen",
            category="Kahvaltı",
            prep_time=20,
            instructions="Pişir.",
        )
    )

    second = create_recipe(
        Recipe(
            id=None,
            name="Pilav",
            category="Ana Yemek",
            prep_time=30,
            instructions="Pişir.",
        )
    )

    recipes = get_all_recipes()

    assert first in recipes
    assert second in recipes
    assert len(recipes) == 2


def test_update_recipe_updates_all_fields(test_db) -> None:
    recipe = create_recipe(
        Recipe(
            id=None,
            name="Eski Tarif",
            category="Eski Kategori",
            prep_time=10,
            instructions="Eski talimat.",
        )
    )

    assert recipe.id is not None

    updated_recipe = Recipe(
        id=recipe.id,
        name="Yeni Tarif",
        category="Yeni Kategori",
        prep_time=45,
        instructions="Yeni talimat.",
    )

    result = update_recipe(updated_recipe)

    assert result == updated_recipe
    assert get_recipe(recipe.id) == updated_recipe


def test_delete_recipe_removes_recipe(test_db) -> None:
    recipe = create_recipe(
        Recipe(
            id=None,
            name="Silinecek Tarif",
            category="Test",
            prep_time=15,
            instructions="Sil.",
        )
    )

    assert recipe.id is not None

    delete_recipe(recipe.id)

    assert get_recipe(recipe.id) is None


def test_get_all_recipes_returns_empty_list_when_database_is_empty(
    test_db,
) -> None:
    assert get_all_recipes() == []


def test_update_unknown_recipe_does_not_create_recipe(test_db) -> None:
    recipe = Recipe(
        id=999999,
        name="Olmayan Tarif",
        category="Test",
        prep_time=10,
        instructions="Hazırla.",
    )

    update_recipe(recipe)

    assert get_recipe(999999) is None
    assert get_all_recipes() == []


def test_delete_unknown_recipe_is_safe(test_db) -> None:
    delete_recipe(999999)

    assert get_all_recipes() == []


def test_update_one_recipe_does_not_affect_another(
    test_db,
) -> None:
    first = create_recipe(
        Recipe(
            id=None,
            name="Menemen",
            category="Kahvaltı",
            prep_time=20,
            instructions="Pişir.",
        )
    )

    second = create_recipe(
        Recipe(
            id=None,
            name="Pilav",
            category="Ana Yemek",
            prep_time=30,
            instructions="Pişir.",
        )
    )

    assert first.id is not None
    assert second.id is not None

    updated_first = Recipe(
        id=first.id,
        name="Acılı Menemen",
        category="Kahvaltı",
        prep_time=25,
        instructions="Acı biber ekleyip pişir.",
    )

    update_recipe(updated_first)

    assert get_recipe(first.id) == updated_first
    assert get_recipe(second.id) == second


def test_delete_one_recipe_does_not_affect_another(
    test_db,
) -> None:
    first = create_recipe(
        Recipe(
            id=None,
            name="Menemen",
            category="Kahvaltı",
            prep_time=20,
            instructions="Pişir.",
        )
    )

    second = create_recipe(
        Recipe(
            id=None,
            name="Pilav",
            category="Ana Yemek",
            prep_time=30,
            instructions="Pişir.",
        )
    )

    assert first.id is not None
    assert second.id is not None

    delete_recipe(first.id)

    assert get_recipe(first.id) is None
    assert get_recipe(second.id) == second


def test_get_all_recipes_preserves_created_recipe_data(
    test_db,
) -> None:
    first = create_recipe(
        Recipe(
            id=None,
            name="Krep",
            category="Kahvaltı",
            prep_time=15,
            instructions="Karıştır.",
        )
    )

    second = create_recipe(
        Recipe(
            id=None,
            name="Mercimek Çorbası",
            category="Çorba",
            prep_time=40,
            instructions="Kaynat.",
        )
    )

    recipes = get_all_recipes()

    assert first in recipes
    assert second in recipes

    first_from_list = next(recipe for recipe in recipes if recipe.id == first.id)
    second_from_list = next(recipe for recipe in recipes if recipe.id == second.id)

    assert first_from_list == first
    assert second_from_list == second
