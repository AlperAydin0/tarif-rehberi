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
