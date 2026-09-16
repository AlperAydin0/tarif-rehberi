from tarif_rehberi.models.ingredient import Ingredient
from tarif_rehberi.repositories.ingredient_repository import (
    create_ingredient,
    delete_ingredient,
    get_ingredient,
    get_all_ingredients,
    update_ingredient,
)
from tarif_rehberi.services.ingredient_service import (
    create_ingredient_if_not_exists,
    delete_ingredient_by_id,
    get_all_ingredients_sorted,
    get_ingredient_by_id,
    update_ingredient_by_id,
)


def test_create_ingredient_if_not_exists_creates_ingredient(
    test_db,
) -> None:
    ingredient = Ingredient(
        id=None,
        name="Domates",
        quantity=5.0,
        unit="adet",
        unit_price=10.0,
    )

    created = create_ingredient_if_not_exists(ingredient)

    assert created.id is not None
    assert created.name == "Domates"
    assert created.quantity == 5.0
    assert created.unit == "adet"
    assert created.unit_price == 10.0


def test_create_ingredient_if_not_exists_returns_existing_ingredient(
    test_db,
) -> None:
    existing = create_ingredient(
        Ingredient(
            id=None,
            name="Domates",
            quantity=5.0,
            unit="adet",
            unit_price=10.0,
        )
    )

    duplicate = Ingredient(
        id=None,
        name="Domates",
        quantity=8.0,
        unit="kg",
        unit_price=20.0,
    )

    result = create_ingredient_if_not_exists(duplicate)

    assert result == existing
    assert len(get_all_ingredients()) == 1


def test_get_ingredient_by_id(test_db) -> None:
    ingredient = create_ingredient(
        Ingredient(
            id=None,
            name="Soğan",
            quantity=5.0,
            unit="adet",
            unit_price=7.0,
        )
    )

    assert ingredient.id is not None

    result = get_ingredient_by_id(ingredient.id)

    assert result == ingredient


def test_get_nonexistent_ingredient_by_id(test_db) -> None:
    result = get_ingredient_by_id(999)

    assert result is None


def test_update_ingredient_by_id(test_db) -> None:
    ingredient = create_ingredient(
        Ingredient(
            id=None,
            name="Domates",
            quantity=5.0,
            unit="adet",
            unit_price=10.0,
        )
    )

    assert ingredient.id is not None

    updated = Ingredient(
        id=ingredient.id,
        name="Domates",
        quantity=10.0,
        unit="kg",
        unit_price=15.0,
    )

    result = update_ingredient_by_id(updated)

    assert result == updated
    assert get_ingredient(ingredient.id) == updated


def test_delete_ingredient_by_id(test_db) -> None:
    ingredient = create_ingredient(
        Ingredient(
            id=None,
            name="Domates",
            quantity=5.0,
            unit="adet",
            unit_price=10.0,
        )
    )

    assert ingredient.id is not None

    result = delete_ingredient_by_id(ingredient.id)

    assert result is True
    assert get_ingredient(ingredient.id) is None


def test_delete_nonexistent_ingredient_by_id(test_db) -> None:
    result = delete_ingredient_by_id(999)

    assert result is False


def test_get_all_ingredients_sorted(test_db) -> None:
    create_ingredient(
        Ingredient(
            id=None,
            name="Zeytin",
            quantity=1.0,
            unit="kg",
            unit_price=50.0,
        )
    )

    create_ingredient(
        Ingredient(
            id=None,
            name="Domates",
            quantity=5.0,
            unit="adet",
            unit_price=10.0,
        )
    )

    create_ingredient(
        Ingredient(
            id=None,
            name="Biber",
            quantity=3.0,
            unit="adet",
            unit_price=8.0,
        )
    )

    ingredients = get_all_ingredients_sorted()

    assert [ingredient.name for ingredient in ingredients] == [
        "Biber",
        "Domates",
        "Zeytin",
    ]
def test_create_ingredient_if_not_exists_creates_new_ingredient(
    test_db,
) -> None:
    ingredient = Ingredient(
        id=None,
        name="Domates",
        quantity=5.0,
        unit="adet",
        unit_price=10.0,
    )

    result = create_ingredient_if_not_exists(ingredient)

    assert result.id is not None
    assert result.name == "Domates"
    assert result.quantity == 5.0
    assert result.unit == "adet"
    assert result.unit_price == 10.0


def test_create_ingredient_if_not_exists_returns_existing_ingredient(
    test_db,
) -> None:
    existing = create_ingredient(
        Ingredient(
            id=None,
            name="Domates",
            quantity=5.0,
            unit="adet",
            unit_price=10.0,
        )
    )

    result = create_ingredient_if_not_exists(
        Ingredient(
            id=None,
            name="Domates",
            quantity=20.0,
            unit="adet",
            unit_price=15.0,
        )
    )

    assert result == existing


def test_get_ingredient_by_id_returns_ingredient(test_db) -> None:
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

    result = get_ingredient_by_id(ingredient.id)

    assert result == ingredient


def test_get_ingredient_by_id_returns_none_for_unknown_id(
    test_db,
) -> None:
    assert get_ingredient_by_id(999999) is None


def test_update_ingredient_by_id_updates_existing_ingredient(
    test_db,
) -> None:
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
        unit_price=30.0,
    )

    result = update_ingredient_by_id(updated)

    assert result == updated
    assert get_ingredient_by_id(ingredient.id) == updated


def test_delete_ingredient_by_id_removes_existing_ingredient(
    test_db,
) -> None:
    ingredient = create_ingredient(
        Ingredient(
            id=None,
            name="Soğan",
            quantity=5.0,
            unit="adet",
            unit_price=5.0,
        )
    )

    assert ingredient.id is not None

    delete_ingredient_by_id(ingredient.id)

    assert get_ingredient_by_id(ingredient.id) is None


def test_get_all_ingredients_sorted_returns_alphabetical_order(
    test_db,
) -> None:
    create_ingredient(
        Ingredient(
            id=None,
            name="Yumurta",
            quantity=10.0,
            unit="adet",
            unit_price=5.0,
        )
    )
    create_ingredient(
        Ingredient(
            id=None,
            name="Domates",
            quantity=10.0,
            unit="adet",
            unit_price=10.0,
        )
    )
    create_ingredient(
        Ingredient(
            id=None,
            name="Biber",
            quantity=10.0,
            unit="adet",
            unit_price=8.0,
        )
    )

    ingredients = get_all_ingredients_sorted()

    assert [ingredient.name for ingredient in ingredients] == [
        "Biber",
        "Domates",
        "Yumurta",
    ]


def test_get_all_ingredients_sorted_returns_empty_list(
    test_db,
) -> None:
    assert get_all_ingredients_sorted() == []


def test_create_ingredient_if_not_exists_does_not_duplicate_name(
    test_db,
) -> None:
    first = create_ingredient_if_not_exists(
        Ingredient(
            id=None,
            name="Un",
            quantity=2.0,
            unit="kg",
            unit_price=30.0,
        )
    )

    second = create_ingredient_if_not_exists(
        Ingredient(
            id=None,
            name="Un",
            quantity=10.0,
            unit="kg",
            unit_price=40.0,
        )
    )

    assert first.id == second.id
    assert len(get_all_ingredients_sorted()) == 1
def test_create_ingredient_if_not_exists_preserves_existing_data(
    test_db,
) -> None:
    existing = create_ingredient(
        Ingredient(
            id=None,
            name="Pirinç",
            quantity=5.0,
            unit="kg",
            unit_price=50.0,
        )
    )

    result = create_ingredient_if_not_exists(
        Ingredient(
            id=None,
            name="Pirinç",
            quantity=100.0,
            unit="kg",
            unit_price=999.0,
        )
    )

    assert result == existing
    assert result.quantity == 5.0
    assert result.unit_price == 50.0