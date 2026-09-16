import sqlite3

import pytest

from tarif_rehberi.models.ingredient import Ingredient
from tarif_rehberi.repositories.ingredient_repository import (
    create_ingredient,
    delete_ingredient,
    get_all_ingredients,
    get_ingredient,
    update_ingredient,
)


def test_create_ingredient(test_db) -> None:
    ingredient = Ingredient(
        id=None,
        name="Domates",
        quantity=5.0,
        unit="kg",
        unit_price=40.0,
    )

    created: Ingredient = create_ingredient(ingredient)
    assert created.id is not None
    assert created.name == "Domates"
    assert created.quantity == 5.0
    assert created.unit == "kg"
    assert created.unit_price == 40.0


def test_get_ingredient(test_db) -> None:
    ingredient = Ingredient(
        id=None,
        name="Soğan",
        quantity=3.0,
        unit="kg",
        unit_price=30.0,
    )

    created = create_ingredient(ingredient)
    assert created.id is not None

    found: Ingredient | None = get_ingredient(created.id)
    assert found is not None
    assert found.id == created.id
    assert found.name == "Soğan"
    assert found.quantity == 3.0
    assert found.unit == "kg"
    assert found.unit_price == 30.0


def test_get_nonexistent_ingredient(test_db) -> None:
    found: Ingredient | None = get_ingredient(999)
    assert found is None


def test_get_all_ingredients(test_db) -> None:
    domates = Ingredient(
        id=None,
        name="Domates",
        quantity=5.0,
        unit="kg",
        unit_price=40.0,
    )

    sogan = Ingredient(
        id=None,
        name="Soğan",
        quantity=3.0,
        unit="kg",
        unit_price=30.0,
    )

    create_ingredient(domates)
    create_ingredient(sogan)

    ingredients: list[Ingredient] = get_all_ingredients()

    assert len(ingredients) == 2

    names: list[str] = [i.name for i in ingredients]

    assert names == [
        "Domates",
        "Soğan",
    ]


def test_update_ingredient(test_db) -> None:
    ingredient = Ingredient(
        id=None,
        name="Domates",
        quantity=5.0,
        unit="kg",
        unit_price=40.0,
    )

    created = create_ingredient(ingredient)

    assert created.id is not None

    updated = Ingredient(
        id=created.id,
        name="Domates",
        quantity=10.0,
        unit="kg",
        unit_price=50.0,
    )

    result: Ingredient = update_ingredient(updated)
    assert result == updated

    found: Ingredient | None = get_ingredient(created.id)
    assert found == updated


def test_delete_ingredient(test_db) -> None:
    ingredient = Ingredient(
        id=None,
        name="Domates",
        quantity=5.0,
        unit="kg",
        unit_price=40.0,
    )

    created = create_ingredient(ingredient)
    assert created.id is not None

    deleted: bool = delete_ingredient(created.id)
    assert deleted is True

    found: Ingredient | None = get_ingredient(created.id)
    assert found is None


def test_delete_nonexistent_ingredient(test_db) -> None:
    deleted: bool = delete_ingredient(999)
    assert deleted is False


def test_duplicate_ingredient_is_rejected(test_db) -> None:
    ingredient = Ingredient(
        id=None,
        name="Domates",
        quantity=5.0,
        unit="kg",
        unit_price=40.0,
    )

    create_ingredient(ingredient)
    with pytest.raises(sqlite3.IntegrityError):
        create_ingredient(ingredient)


def test_create_ingredient_persists_all_fields(test_db) -> None:
    ingredient = Ingredient(
        id=None,
        name="Domates",
        quantity=5.5,
        unit="kg",
        unit_price=18.75,
    )

    created = create_ingredient(ingredient)

    assert created.id is not None
    assert created.name == "Domates"
    assert created.quantity == 5.5
    assert created.unit == "kg"
    assert created.unit_price == 18.75


def test_get_ingredient_returns_created_ingredient(test_db) -> None:
    ingredient = create_ingredient(
        Ingredient(
            id=None,
            name="Yumurta",
            quantity=12.0,
            unit="adet",
            unit_price=5.0,
        )
    )

    assert ingredient.id is not None

    result = get_ingredient(ingredient.id)

    assert result == ingredient


def test_get_ingredient_returns_none_for_unknown_id(test_db) -> None:
    assert get_ingredient(999999) is None


def test_get_all_ingredients_returns_all_ingredients(test_db) -> None:
    first = create_ingredient(
        Ingredient(
            id=None,
            name="Domates",
            quantity=5.0,
            unit="adet",
            unit_price=10.0,
        )
    )
    second = create_ingredient(
        Ingredient(
            id=None,
            name="Biber",
            quantity=3.0,
            unit="adet",
            unit_price=8.0,
        )
    )

    ingredients = get_all_ingredients()

    assert first in ingredients
    assert second in ingredients
    assert len(ingredients) == 2


def test_get_all_ingredients_returns_empty_list(test_db) -> None:
    assert get_all_ingredients() == []


def test_update_ingredient_updates_all_fields(test_db) -> None:
    ingredient = create_ingredient(
        Ingredient(
            id=None,
            name="Süt",
            quantity=2.0,
            unit="L",
            unit_price=25.0,
        )
    )

    assert ingredient.id is not None

    updated = Ingredient(
        id=ingredient.id,
        name="Tam Yağlı Süt",
        quantity=5.0,
        unit="L",
        unit_price=32.5,
    )

    result = update_ingredient(updated)

    assert result == updated
    assert get_ingredient(ingredient.id) == updated


def test_delete_ingredient_removes_ingredient(test_db) -> None:
    ingredient = create_ingredient(
        Ingredient(
            id=None,
            name="Soğan",
            quantity=4.0,
            unit="adet",
            unit_price=5.0,
        )
    )

    assert ingredient.id is not None

    delete_ingredient(ingredient.id)

    assert get_ingredient(ingredient.id) is None


def test_delete_ingredient_does_not_delete_other_ingredients(
    test_db,
) -> None:
    first = create_ingredient(
        Ingredient(
            id=None,
            name="Domates",
            quantity=5.0,
            unit="adet",
            unit_price=10.0,
        )
    )
    second = create_ingredient(
        Ingredient(
            id=None,
            name="Biber",
            quantity=3.0,
            unit="adet",
            unit_price=8.0,
        )
    )

    assert first.id is not None
    assert second.id is not None

    delete_ingredient(first.id)

    assert get_ingredient(first.id) is None
    assert get_ingredient(second.id) == second


def test_update_ingredient_does_not_change_id(test_db) -> None:
    ingredient = create_ingredient(
        Ingredient(
            id=None,
            name="Un",
            quantity=2.0,
            unit="kg",
            unit_price=30.0,
        )
    )

    assert ingredient.id is not None

    updated = Ingredient(
        id=ingredient.id,
        name="Buğday Unu",
        quantity=4.0,
        unit="kg",
        unit_price=35.0,
    )

    result = update_ingredient(updated)

    assert result.id == ingredient.id
