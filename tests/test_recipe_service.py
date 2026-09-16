from tarif_rehberi.models.ingredient import Ingredient
from tarif_rehberi.models.recipe import Recipe
from tarif_rehberi.repositories.ingredient_repository import (
    create_ingredient,
)
from tarif_rehberi.repositories.recipe_ingredient_repository import (
    add_ingredient_to_recipe,
)
from tarif_rehberi.repositories.recipe_repository import create_recipe
from tarif_rehberi.services.recipe_service import (
    calculate_recipe_cost,
    calculate_recipe_match,
    find_missing_ingredients,
    recommend_recipes,
)


def create_test_recipe(
    test_db,
) -> tuple[
    Recipe,
    Ingredient,
    Ingredient,
    Ingredient,
]:
    recipe = create_recipe(
        Recipe(
            id=None,
            name="Menemen",
            category="Kahvaltı",
            prep_time=20,
            instructions="Malzemeleri pişir.",
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

    onion = create_ingredient(
        Ingredient(
            id=None,
            name="Soğan",
            quantity=5.0,
            unit="adet",
            unit_price=7.0,
        )
    )

    assert recipe.id is not None
    assert tomato.id is not None
    assert egg.id is not None
    assert onion.id is not None

    add_ingredient_to_recipe(recipe.id, tomato.id, 2.0)
    add_ingredient_to_recipe(recipe.id, egg.id, 3.0)
    add_ingredient_to_recipe(recipe.id, onion.id, 1.0)

    return recipe, tomato, egg, onion


def test_calculate_recipe_match_with_all_ingredients(test_db) -> None:

    recipe, tomato, egg, onion = create_test_recipe(test_db)

    assert tomato.id is not None
    assert egg.id is not None
    assert onion.id is not None

    user_ingredients: dict[int, float] = {
        tomato.id: 100.0,
        egg.id: 100.0,
        onion.id: 100.0,
    }

    match = calculate_recipe_match(
        recipe.id,
        user_ingredients,
    )

    assert match == 100.0


def test_calculate_recipe_match_with_partial_ingredients(test_db) -> None:
    recipe, tomato, egg, onion = create_test_recipe(test_db)

    assert tomato.id is not None
    assert egg.id is not None
    assert onion.id is not None

    user_ingredients: dict[int, float] = {
        tomato.id: 1000.0,
        egg.id: 1000.0,
    }

    match = calculate_recipe_match(
        recipe.id,
        user_ingredients,
    )

    assert match == 66.67


def test_calculate_recipe_match_with_no_ingredients(test_db) -> None:
    recipe, _, _, _ = create_test_recipe(test_db)

    match = calculate_recipe_match(
        recipe.id,
        {},
    )

    assert match == 0.0


def test_find_missing_ingredients(test_db) -> None:
    recipe, tomato, egg, onion = create_test_recipe(test_db)

    assert tomato.id is not None
    assert egg.id is not None
    assert onion.id is not None

    user_ingredients: dict[int, float] = {
        tomato.id: 1000.0,
        egg.id: 10000.0,
    }

    missing = find_missing_ingredients(
        recipe.id,
        user_ingredients,
    )

    assert missing == [onion]


def test_find_missing_ingredients_with_all_ingredients(test_db) -> None:
    recipe, tomato, egg, onion = create_test_recipe(test_db)

    assert tomato.id is not None
    assert egg.id is not None
    assert onion.id is not None

    user_ingredients: dict[int, float] = {
        tomato.id: 1000.0,
        egg.id: 1000.0,
        onion.id: 1000.0,
    }

    missing = find_missing_ingredients(
        recipe.id,
        user_ingredients,
    )

    assert missing == []


def test_recommend_recipes(test_db) -> None:
    first_recipe, tomato, egg, _ = create_test_recipe(test_db)

    second_recipe = create_recipe(
        Recipe(
            id=None,
            name="Domates Yemeği",
            category="Ana Yemek",
            prep_time=30,
            instructions="Domatesleri pişir.",
        )
    )

    assert second_recipe.id is not None

    assert tomato.id is not None
    assert egg.id is not None

    add_ingredient_to_recipe(
        second_recipe.id,
        tomato.id,
        3.0,
    )

    user_ingredients: dict[int, float] = {
        tomato.id: 1000.0,
        egg.id: 1000.0,
    }

    recommendations = recommend_recipes(
        user_ingredients,
    )
    assert len(recommendations) == 2
    print(recommendations)

    assert recommendations[1][0].id == first_recipe.id
    assert recommendations[1][1] == 66.67

    assert recommendations[0][0].id == second_recipe.id
    assert recommendations[0][1] == 100.0


def test_recipe_match_respects_required_quantity(test_db) -> None:
    recipe = create_recipe(
        Recipe(
            id=None,
            name="Menemen",
            category="Kahvaltı",
            prep_time=20,
            instructions="Malzemeleri pişir.",
        )
    )

    tomato = create_ingredient(
        Ingredient(
            id=None,
            name="Domates",
            quantity=1.0,
            unit="adet",
            unit_price=10.0,
        )
    )

    assert recipe.id is not None
    assert tomato.id is not None

    add_ingredient_to_recipe(recipe.id, tomato.id, 3.0)

    user_ingredients: dict[int, float] = {
        tomato.id: 2.0,
    }

    match = calculate_recipe_match(
        recipe.id,
        user_ingredients,
    )

    assert match == 0.0


def test_recipe_match_respects_sufficient_quantity(test_db) -> None:
    recipe = create_recipe(
        Recipe(
            id=None,
            name="Menemen",
            category="Kahvaltı",
            prep_time=20,
            instructions="Malzemeleri pişir.",
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

    assert recipe.id is not None
    assert tomato.id is not None

    add_ingredient_to_recipe(recipe.id, tomato.id, 3.0)

    user_ingredients: dict[int, float] = {
        tomato.id: 3.0,
    }

    match = calculate_recipe_match(
        recipe.id,
        user_ingredients,
    )

    assert match == 100.0


def test_find_missing_ingredients_includes_insufficient_quantity(
    test_db,
) -> None:
    recipe = create_recipe(
        Recipe(
            id=None,
            name="Menemen",
            category="Kahvaltı",
            prep_time=20,
            instructions="Malzemeleri pişir.",
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

    assert recipe.id is not None
    assert tomato.id is not None

    add_ingredient_to_recipe(recipe.id, tomato.id, 3.0)

    user_ingredients: dict[int, float] = {
        tomato.id: 2.0,
    }

    missing = find_missing_ingredients(
        recipe.id,
        user_ingredients,
    )

    assert missing == [tomato]


def test_recommend_recipes_uses_available_quantities(
    test_db,
) -> None:
    first_recipe = create_recipe(
        Recipe(
            id=None,
            name="Menemen",
            category="Kahvaltı",
            prep_time=20,
            instructions="Malzemeleri pişir.",
        )
    )

    second_recipe = create_recipe(
        Recipe(
            id=None,
            name="Domates Yemeği",
            category="Ana Yemek",
            prep_time=30,
            instructions="Domatesleri pişir.",
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
        5.0,
    )

    add_ingredient_to_recipe(
        second_recipe.id,
        tomato.id,
        2.0,
    )

    user_ingredients: dict[int, float] = {
        tomato.id: 3.0,
    }

    recommendations = recommend_recipes(
        user_ingredients,
    )

    assert recommendations[0][0].id == second_recipe.id
    assert recommendations[0][1] == 100.0


def test_recommend_recipes_excludes_zero_match_recipes(
    test_db,
) -> None:
    recipe = create_recipe(
        Recipe(
            id=None,
            name="Menemen",
            category="Kahvaltı",
            prep_time=20,
            instructions="Malzemeleri pişir.",
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

    assert recipe.id is not None
    assert tomato.id is not None

    add_ingredient_to_recipe(
        recipe.id,
        tomato.id,
        2.0,
    )

    recommendations = recommend_recipes({})

    assert recommendations == []


def test_recommend_recipes_returns_missing_ingredients(
    test_db,
) -> None:
    recipe = create_recipe(
        Recipe(
            id=None,
            name="Menemen",
            category="Kahvaltı",
            prep_time=20,
            instructions="Malzemeleri pişir.",
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

    add_ingredient_to_recipe(
        recipe.id,
        tomato.id,
        2.0,
    )

    add_ingredient_to_recipe(
        recipe.id,
        egg.id,
        3.0,
    )

    user_ingredients: dict[int, float] = {
        tomato.id: 2.0,
    }

    recommendations = recommend_recipes(
        user_ingredients,
    )

    assert len(recommendations) == 1
    assert recommendations[0][0].id == recipe.id
    assert recommendations[0][1] == 50.0


def test_calculate_recipe_match_handles_partial_quantity(
    test_db,
) -> None:
    recipe = create_recipe(
        Recipe(
            id=None,
            name="Pilav",
            category="Ana Yemek",
            prep_time=30,
            instructions="Pirinci pişir.",
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

    add_ingredient_to_recipe(
        recipe.id,
        rice.id,
        2.0,
    )

    user_ingredients: dict[int, float] = {
        rice.id: 1.99,
    }

    match = calculate_recipe_match(
        recipe.id,
        user_ingredients,
    )

    assert match == 0.0


def test_calculate_recipe_match_with_extra_quantity(
    test_db,
) -> None:
    recipe = create_recipe(
        Recipe(
            id=None,
            name="Pilav",
            category="Ana Yemek",
            prep_time=30,
            instructions="Pirinci pişir.",
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

    add_ingredient_to_recipe(
        recipe.id,
        rice.id,
        2.0,
    )

    user_ingredients: dict[int, float] = {
        rice.id: 5.0,
    }

    match = calculate_recipe_match(
        recipe.id,
        user_ingredients,
    )

    assert match == 100.0


def test_find_missing_ingredients_returns_all_insufficient_ingredients(
    test_db,
) -> None:
    recipe = create_recipe(
        Recipe(
            id=None,
            name="Krep",
            category="Kahvaltı",
            prep_time=20,
            instructions="Malzemeleri karıştır.",
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
            quantity=5.0,
            unit="L",
            unit_price=25.0,
        )
    )

    egg = create_ingredient(
        Ingredient(
            id=None,
            name="Yumurta",
            quantity=20.0,
            unit="adet",
            unit_price=5.0,
        )
    )

    assert recipe.id is not None
    assert flour.id is not None
    assert milk.id is not None
    assert egg.id is not None

    add_ingredient_to_recipe(
        recipe.id,
        flour.id,
        2.0,
    )
    add_ingredient_to_recipe(
        recipe.id,
        milk.id,
        1.0,
    )
    add_ingredient_to_recipe(
        recipe.id,
        egg.id,
        2.0,
    )

    user_ingredients: dict[int, float] = {
        flour.id: 1.0,
        milk.id: 0.5,
        egg.id: 2.0,
    }

    missing = find_missing_ingredients(
        recipe.id,
        user_ingredients,
    )

    assert missing == [milk, flour]


def test_recommend_recipes_orders_by_match_percentage(
    test_db,
) -> None:
    low_match_recipe = create_recipe(
        Recipe(
            id=None,
            name="A Tarifi",
            category="Ana Yemek",
            prep_time=20,
            instructions="Malzemeleri pişir.",
        )
    )

    high_match_recipe = create_recipe(
        Recipe(
            id=None,
            name="B Tarifi",
            category="Ana Yemek",
            prep_time=20,
            instructions="Malzemeleri pişir.",
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

    onion = create_ingredient(
        Ingredient(
            id=None,
            name="Soğan",
            quantity=10.0,
            unit="adet",
            unit_price=7.0,
        )
    )

    assert low_match_recipe.id is not None
    assert high_match_recipe.id is not None
    assert tomato.id is not None
    assert egg.id is not None
    assert onion.id is not None

    add_ingredient_to_recipe(
        low_match_recipe.id,
        tomato.id,
        1.0,
    )
    add_ingredient_to_recipe(
        low_match_recipe.id,
        egg.id,
        1.0,
    )
    add_ingredient_to_recipe(
        low_match_recipe.id,
        onion.id,
        1.0,
    )

    add_ingredient_to_recipe(
        high_match_recipe.id,
        tomato.id,
        1.0,
    )
    add_ingredient_to_recipe(
        high_match_recipe.id,
        egg.id,
        1.0,
    )

    user_ingredients: dict[int, float] = {
        tomato.id: 1.0,
        egg.id: 1.0,
    }

    recommendations = recommend_recipes(
        user_ingredients,
    )

    assert len(recommendations) == 2
    assert recommendations[0] == (
        high_match_recipe,
        100.0,
    )
    assert recommendations[1] == (
        low_match_recipe,
        66.67,
    )


def test_recommend_recipes_uses_name_as_tiebreaker(
    test_db,
) -> None:
    first_recipe = create_recipe(
        Recipe(
            id=None,
            name="Zeytinyağlı",
            category="Ana Yemek",
            prep_time=20,
            instructions="Pişir.",
        )
    )

    second_recipe = create_recipe(
        Recipe(
            id=None,
            name="Mercimek",
            category="Ana Yemek",
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

    assert first_recipe.id is not None
    assert second_recipe.id is not None
    assert tomato.id is not None

    add_ingredient_to_recipe(
        first_recipe.id,
        tomato.id,
        1.0,
    )

    add_ingredient_to_recipe(
        second_recipe.id,
        tomato.id,
        1.0,
    )

    user_ingredients: dict[int, float] = {
        tomato.id: 1.0,
    }

    recommendations = recommend_recipes(
        user_ingredients,
    )

    assert recommendations[0][0] == second_recipe
    assert recommendations[1][0] == first_recipe


def test_recommend_recipes_returns_empty_for_empty_database(
    test_db,
) -> None:
    recommendations = recommend_recipes({})

    assert recommendations == []


def test_calculate_recipe_match_handles_zero_required_quantity(
    test_db,
) -> None:
    recipe = create_recipe(
        Recipe(
            id=None,
            name="Test Tarifi",
            category="Test",
            prep_time=10,
            instructions="Test.",
        )
    )

    ingredient = create_ingredient(
        Ingredient(
            id=None,
            name="Test Malzeme",
            quantity=10.0,
            unit="adet",
            unit_price=1.0,
        )
    )

    assert recipe.id is not None
    assert ingredient.id is not None

    add_ingredient_to_recipe(
        recipe.id,
        ingredient.id,
        0.001,
    )

    user_ingredients: dict[int, float] = {
        ingredient.id: 0.001,
    }

    assert (
        calculate_recipe_match(
            recipe.id,
            user_ingredients,
        )
        == 100.0
    )


def test_calculate_recipe_match_handles_decimal_quantities(
    test_db,
) -> None:
    recipe = create_recipe(
        Recipe(
            id=None,
            name="Kek",
            category="Tatlı",
            prep_time=40,
            instructions="Pişir.",
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

    add_ingredient_to_recipe(
        recipe.id,
        flour.id,
        0.75,
    )

    user_ingredients: dict[int, float] = {
        flour.id: 0.75,
    }

    assert (
        calculate_recipe_match(
            recipe.id,
            user_ingredients,
        )
        == 100.0
    )


def test_find_missing_ingredients_does_not_mutate_user_ingredients(
    test_db,
) -> None:
    recipe = create_recipe(
        Recipe(
            id=None,
            name="Çorba",
            category="Çorba",
            prep_time=30,
            instructions="Pişir.",
        )
    )

    lentil = create_ingredient(
        Ingredient(
            id=None,
            name="Mercimek",
            quantity=5.0,
            unit="kg",
            unit_price=40.0,
        )
    )

    assert recipe.id is not None
    assert lentil.id is not None

    add_ingredient_to_recipe(
        recipe.id,
        lentil.id,
        1.0,
    )

    user_ingredients: dict[int, float] = {
        lentil.id: 2.0,
    }

    original: dict[int, float] = user_ingredients.copy()

    find_missing_ingredients(
        recipe.id,
        user_ingredients,
    )

    assert user_ingredients == original


def test_recommend_recipes_does_not_mutate_user_ingredients(
    test_db,
) -> None:
    recipe = create_recipe(
        Recipe(
            id=None,
            name="Çorba",
            category="Çorba",
            prep_time=30,
            instructions="Pişir.",
        )
    )

    lentil = create_ingredient(
        Ingredient(
            id=None,
            name="Mercimek",
            quantity=5.0,
            unit="kg",
            unit_price=40.0,
        )
    )

    assert recipe.id is not None
    assert lentil.id is not None

    add_ingredient_to_recipe(
        recipe.id,
        lentil.id,
        1.0,
    )

    user_ingredients: dict[int, float] = {
        lentil.id: 2.0,
    }

    original: dict[int, float] = user_ingredients.copy()

    recommend_recipes(user_ingredients)

    assert user_ingredients == original


def test_recommend_recipes_with_unknown_ingredient_id(
    test_db,
) -> None:
    recipe = create_recipe(
        Recipe(
            id=None,
            name="Çorba",
            category="Çorba",
            prep_time=30,
            instructions="Pişir.",
        )
    )

    lentil = create_ingredient(
        Ingredient(
            id=None,
            name="Mercimek",
            quantity=5.0,
            unit="kg",
            unit_price=40.0,
        )
    )

    assert recipe.id is not None
    assert lentil.id is not None

    add_ingredient_to_recipe(
        recipe.id,
        lentil.id,
        1.0,
    )

    recommendations = recommend_recipes(
        {999999: 10.0},
    )

    assert recommendations == []


def test_recommend_recipes_with_multiple_equal_matches(
    test_db,
) -> None:
    first_recipe = create_recipe(
        Recipe(
            id=None,
            name="Elma Tatlısı",
            category="Tatlı",
            prep_time=20,
            instructions="Hazırla.",
        )
    )

    second_recipe = create_recipe(
        Recipe(
            id=None,
            name="Armut Tatlısı",
            category="Tatlı",
            prep_time=20,
            instructions="Hazırla.",
        )
    )

    apple = create_ingredient(
        Ingredient(
            id=None,
            name="Elma",
            quantity=10.0,
            unit="adet",
            unit_price=10.0,
        )
    )

    assert first_recipe.id is not None
    assert second_recipe.id is not None
    assert apple.id is not None

    add_ingredient_to_recipe(
        first_recipe.id,
        apple.id,
        1.0,
    )

    add_ingredient_to_recipe(
        second_recipe.id,
        apple.id,
        1.0,
    )

    recommendations = recommend_recipes(
        {apple.id: 1.0},
    )

    assert recommendations == [
        (second_recipe, 100.0),
        (first_recipe, 100.0),
    ]


def test_calculate_recipe_cost_with_multiple_ingredients(test_db) -> None:
    recipe = create_recipe(
        Recipe(
            id=None,
            name="Menemen",
            category="Kahvaltı",
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
            unit_price=5.0,
        )
    )

    pepper = create_ingredient(
        Ingredient(
            id=None,
            name="Biber",
            quantity=10.0,
            unit="adet",
            unit_price=3.0,
        )
    )

    assert recipe.id is not None
    assert tomato.id is not None
    assert pepper.id is not None

    add_ingredient_to_recipe(recipe.id, tomato.id, 2.0)
    add_ingredient_to_recipe(recipe.id, pepper.id, 3.0)

    result = calculate_recipe_cost(recipe.id)

    assert result == 19.0


def test_calculate_recipe_cost_with_no_ingredients(test_db) -> None:
    recipe = create_recipe(
        Recipe(
            id=None,
            name="Boş Tarif",
            category="Diğer",
            prep_time=5,
            instructions="Hazırla.",
        )
    )

    assert recipe.id is not None

    result = calculate_recipe_cost(recipe.id)

    assert result == 0.0


def test_calculate_recipe_cost_with_decimal_values(test_db) -> None:
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
            unit_price=42.50,
        )
    )

    assert recipe.id is not None
    assert rice.id is not None

    add_ingredient_to_recipe(recipe.id, rice.id, 0.5)

    result = calculate_recipe_cost(recipe.id)

    assert result == 21.25


def test_calculate_recipe_cost_with_three_ingredients(test_db) -> None:
    recipe = create_recipe(
        Recipe(
            id=None,
            name="Kahvaltı",
            category="Kahvaltı",
            prep_time=15,
            instructions="Hazırla.",
        )
    )

    tomato = create_ingredient(
        Ingredient(
            id=None,
            name="Domates",
            quantity=10.0,
            unit="adet",
            unit_price=5.0,
        )
    )

    egg = create_ingredient(
        Ingredient(
            id=None,
            name="Yumurta",
            quantity=10.0,
            unit="adet",
            unit_price=4.0,
        )
    )

    cheese = create_ingredient(
        Ingredient(
            id=None,
            name="Peynir",
            quantity=5.0,
            unit="kg",
            unit_price=100.0,
        )
    )

    assert recipe.id is not None
    assert tomato.id is not None
    assert egg.id is not None
    assert cheese.id is not None

    add_ingredient_to_recipe(recipe.id, tomato.id, 2.0)
    add_ingredient_to_recipe(recipe.id, egg.id, 3.0)
    add_ingredient_to_recipe(recipe.id, cheese.id, 0.25)

    result = calculate_recipe_cost(recipe.id)

    assert result == 47.0


def test_calculate_recipe_cost_with_fractional_quantities(
    test_db,
) -> None:
    recipe = create_recipe(
        Recipe(
            id=None,
            name="Kek",
            category="Tatlı",
            prep_time=40,
            instructions="Pişir.",
        )
    )

    flour = create_ingredient(
        Ingredient(
            id=None,
            name="Un",
            quantity=10.0,
            unit="kg",
            unit_price=40.0,
        )
    )

    milk = create_ingredient(
        Ingredient(
            id=None,
            name="Süt",
            quantity=5.0,
            unit="L",
            unit_price=30.0,
        )
    )

    assert recipe.id is not None
    assert flour.id is not None
    assert milk.id is not None

    add_ingredient_to_recipe(recipe.id, flour.id, 0.75)
    add_ingredient_to_recipe(recipe.id, milk.id, 0.25)

    result = calculate_recipe_cost(recipe.id)

    assert result == 37.5


def test_calculate_recipe_cost_rounds_total_to_two_decimal_places(
    test_db,
) -> None:
    recipe = create_recipe(
        Recipe(
            id=None,
            name="Özel Tarif",
            category="Test",
            prep_time=10,
            instructions="Hazırla.",
        )
    )

    first_ingredient = create_ingredient(
        Ingredient(
            id=None,
            name="Malzeme 1",
            quantity=10.0,
            unit="kg",
            unit_price=10.111,
        )
    )

    second_ingredient = create_ingredient(
        Ingredient(
            id=None,
            name="Malzeme 2",
            quantity=10.0,
            unit="kg",
            unit_price=20.222,
        )
    )

    assert recipe.id is not None
    assert first_ingredient.id is not None
    assert second_ingredient.id is not None

    add_ingredient_to_recipe(
        recipe.id,
        first_ingredient.id,
        1.0,
    )

    add_ingredient_to_recipe(
        recipe.id,
        second_ingredient.id,
        1.0,
    )

    result = calculate_recipe_cost(recipe.id)

    assert result == 30.33


def test_calculate_recipe_cost_with_expensive_ingredient(
    test_db,
) -> None:
    recipe = create_recipe(
        Recipe(
            id=None,
            name="Pahalı Tarif",
            category="Ana Yemek",
            prep_time=60,
            instructions="Hazırla.",
        )
    )

    ingredient = create_ingredient(
        Ingredient(
            id=None,
            name="Özel Malzeme",
            quantity=1.0,
            unit="kg",
            unit_price=1250.75,
        )
    )

    assert recipe.id is not None
    assert ingredient.id is not None

    add_ingredient_to_recipe(
        recipe.id,
        ingredient.id,
        2.0,
    )

    result = calculate_recipe_cost(recipe.id)

    assert result == 2501.50


def test_calculate_recipe_cost_with_very_small_quantity(
    test_db,
) -> None:
    recipe = create_recipe(
        Recipe(
            id=None,
            name="Baharatlı Tarif",
            category="Test",
            prep_time=10,
            instructions="Hazırla.",
        )
    )

    ingredient = create_ingredient(
        Ingredient(
            id=None,
            name="Baharat",
            quantity=1.0,
            unit="kg",
            unit_price=1000.0,
        )
    )

    assert recipe.id is not None
    assert ingredient.id is not None

    add_ingredient_to_recipe(
        recipe.id,
        ingredient.id,
        0.001,
    )

    result = calculate_recipe_cost(recipe.id)

    assert result == 1.0


def test_calculate_recipe_cost_is_independent_between_recipes(
    test_db,
) -> None:
    first_recipe = create_recipe(
        Recipe(
            id=None,
            name="Birinci Tarif",
            category="Test",
            prep_time=10,
            instructions="Hazırla.",
        )
    )

    second_recipe = create_recipe(
        Recipe(
            id=None,
            name="İkinci Tarif",
            category="Test",
            prep_time=10,
            instructions="Hazırla.",
        )
    )

    ingredient = create_ingredient(
        Ingredient(
            id=None,
            name="Un",
            quantity=10.0,
            unit="kg",
            unit_price=20.0,
        )
    )

    assert first_recipe.id is not None
    assert second_recipe.id is not None
    assert ingredient.id is not None

    add_ingredient_to_recipe(
        first_recipe.id,
        ingredient.id,
        2.0,
    )

    add_ingredient_to_recipe(
        second_recipe.id,
        ingredient.id,
        5.0,
    )

    first_cost = calculate_recipe_cost(first_recipe.id)
    second_cost = calculate_recipe_cost(second_recipe.id)

    assert first_cost == 40.0
    assert second_cost == 100.0
def test_calculate_recipe_match_with_empty_recipe(
    test_db,
) -> None:
    recipe = create_recipe(
        Recipe(
            id=None,
            name="Boş Tarif",
            category="Test",
            prep_time=5,
            instructions="Hazırla.",
        )
    )

    assert recipe.id is not None

    match = calculate_recipe_match(
        recipe.id,
        {},
    )

    assert match == 0.0


def test_calculate_recipe_match_with_unknown_ingredient(
    test_db,
) -> None:
    recipe = create_recipe(
        Recipe(
            id=None,
            name="Çorba",
            category="Çorba",
            prep_time=20,
            instructions="Pişir.",
        )
    )

    ingredient = create_ingredient(
        Ingredient(
            id=None,
            name="Mercimek",
            quantity=5.0,
            unit="kg",
            unit_price=40.0,
        )
    )

    assert recipe.id is not None
    assert ingredient.id is not None

    add_ingredient_to_recipe(
        recipe.id,
        ingredient.id,
        2.0,
    )

    match = calculate_recipe_match(
        recipe.id,
        {999999: 10.0},
    )

    assert match == 0.0


def test_calculate_recipe_match_with_exact_quantities(
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

    add_ingredient_to_recipe(
        recipe.id,
        tomato.id,
        3.0,
    )

    add_ingredient_to_recipe(
        recipe.id,
        egg.id,
        2.0,
    )

    match = calculate_recipe_match(
        recipe.id,
        {
            tomato.id: 3.0,
            egg.id: 2.0,
        },
    )

    assert match == 100.0


def test_calculate_recipe_match_with_one_missing_ingredient(
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

    add_ingredient_to_recipe(
        recipe.id,
        tomato.id,
        3.0,
    )

    add_ingredient_to_recipe(
        recipe.id,
        egg.id,
        2.0,
    )

    match = calculate_recipe_match(
        recipe.id,
        {
            tomato.id: 3.0,
        },
    )

    assert match == 50.0


def test_calculate_recipe_match_with_multiple_missing_ingredients(
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
            quantity=5.0,
            unit="L",
            unit_price=25.0,
        )
    )

    egg = create_ingredient(
        Ingredient(
            id=None,
            name="Yumurta",
            quantity=20.0,
            unit="adet",
            unit_price=5.0,
        )
    )

    assert recipe.id is not None
    assert flour.id is not None
    assert milk.id is not None
    assert egg.id is not None

    add_ingredient_to_recipe(
        recipe.id,
        flour.id,
        2.0,
    )

    add_ingredient_to_recipe(
        recipe.id,
        milk.id,
        1.0,
    )

    add_ingredient_to_recipe(
        recipe.id,
        egg.id,
        2.0,
    )

    match = calculate_recipe_match(
        recipe.id,
        {
            flour.id: 2.0,
        },
    )

    assert match == 33.33


def test_calculate_recipe_match_rounds_to_two_decimal_places(
    test_db,
) -> None:
    recipe = create_recipe(
        Recipe(
            id=None,
            name="Test Tarifi",
            category="Test",
            prep_time=10,
            instructions="Hazırla.",
        )
    )

    first_ingredient = create_ingredient(
        Ingredient(
            id=None,
            name="Malzeme 1",
            quantity=10.0,
            unit="adet",
            unit_price=10.0,
        )
    )

    second_ingredient = create_ingredient(
        Ingredient(
            id=None,
            name="Malzeme 2",
            quantity=10.0,
            unit="adet",
            unit_price=10.0,
        )
    )

    third_ingredient = create_ingredient(
        Ingredient(
            id=None,
            name="Malzeme 3",
            quantity=10.0,
            unit="adet",
            unit_price=10.0,
        )
    )

    assert recipe.id is not None
    assert first_ingredient.id is not None
    assert second_ingredient.id is not None
    assert third_ingredient.id is not None

    add_ingredient_to_recipe(
        recipe.id,
        first_ingredient.id,
        1.0,
    )

    add_ingredient_to_recipe(
        recipe.id,
        second_ingredient.id,
        1.0,
    )

    add_ingredient_to_recipe(
        recipe.id,
        third_ingredient.id,
        1.0,
    )

    match = calculate_recipe_match(
        recipe.id,
        {
            first_ingredient.id: 1.0,
        },
    )

    assert match == 33.33


def test_calculate_recipe_match_with_more_available_than_required(
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

    add_ingredient_to_recipe(
        recipe.id,
        rice.id,
        2.0,
    )

    match = calculate_recipe_match(
        recipe.id,
        {
            rice.id: 100.0,
        },
    )

    assert match == 100.0


def test_calculate_recipe_match_with_insufficient_one_of_two_ingredients(
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

    add_ingredient_to_recipe(
        recipe.id,
        tomato.id,
        3.0,
    )

    add_ingredient_to_recipe(
        recipe.id,
        egg.id,
        2.0,
    )

    match = calculate_recipe_match(
        recipe.id,
        {
            tomato.id: 3.0,
            egg.id: 1.0,
        },
    )

    assert match == 50.0

def test_recommend_recipes_with_empty_user_ingredients(test_db) -> None:
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

    add_ingredient_to_recipe(recipe.id, tomato.id, 2.0)

    recommendations = recommend_recipes({})

    assert recommendations == []


def test_recommend_recipes_with_unknown_ingredient_only(test_db) -> None:
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

    recommendations = recommend_recipes({999999: 100.0})

    assert recommendations == []


def test_recommend_recipes_returns_only_positive_matches(test_db) -> None:
    recipe_full = create_recipe(
        Recipe(
            id=None,
            name="Menemen",
            category="Kahvaltı",
            prep_time=20,
            instructions="Pişir.",
        )
    )

    recipe_zero = create_recipe(
        Recipe(
            id=None,
            name="Pilav",
            category="Ana Yemek",
            prep_time=30,
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

    rice = create_ingredient(
        Ingredient(
            id=None,
            name="Pirinç",
            quantity=10.0,
            unit="kg",
            unit_price=50.0,
        )
    )

    assert recipe_full.id is not None
    assert recipe_zero.id is not None
    assert tomato.id is not None
    assert rice.id is not None

    add_ingredient_to_recipe(recipe_full.id, tomato.id, 2.0)
    add_ingredient_to_recipe(recipe_zero.id, rice.id, 2.0)

    recommendations = recommend_recipes({tomato.id: 2.0})

    assert recommendations == [(recipe_full, 100.0)]


def test_recommend_recipes_with_single_ingredient_recipe(test_db) -> None:
    recipe = create_recipe(
        Recipe(
            id=None,
            name="Omlet",
            category="Kahvaltı",
            prep_time=10,
            instructions="Pişir.",
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
    assert egg.id is not None

    add_ingredient_to_recipe(recipe.id, egg.id, 2.0)

    recommendations = recommend_recipes({egg.id: 2.0})

    assert recommendations == [(recipe, 100.0)]


def test_recommend_recipes_with_insufficient_quantity(test_db) -> None:
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

    recommendations = recommend_recipes(
        {
            flour.id: 2.0,
            milk.id: 0.5,
        }
    )

    assert recommendations == [(recipe, 50.0)]


def test_recommend_recipes_with_more_than_required_quantity(test_db) -> None:
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

    recommendations = recommend_recipes({rice.id: 100.0})

    assert recommendations == [(recipe, 100.0)]


def test_recommend_recipes_orders_three_recipes_by_match_percentage(
    test_db,
) -> None:
    recipe_full = create_recipe(
        Recipe(
            id=None,
            name="A Tarifi",
            category="Test",
            prep_time=10,
            instructions="Hazırla.",
        )
    )

    recipe_half = create_recipe(
        Recipe(
            id=None,
            name="B Tarifi",
            category="Test",
            prep_time=10,
            instructions="Hazırla.",
        )
    )

    recipe_third = create_recipe(
        Recipe(
            id=None,
            name="C Tarifi",
            category="Test",
            prep_time=10,
            instructions="Hazırla.",
        )
    )

    ingredient_a = create_ingredient(
        Ingredient(
            id=None,
            name="Malzeme A",
            quantity=10.0,
            unit="adet",
            unit_price=10.0,
        )
    )

    ingredient_b = create_ingredient(
        Ingredient(
            id=None,
            name="Malzeme B",
            quantity=10.0,
            unit="adet",
            unit_price=10.0,
        )
    )

    ingredient_c = create_ingredient(
        Ingredient(
            id=None,
            name="Malzeme C",
            quantity=10.0,
            unit="adet",
            unit_price=10.0,
        )
    )

    assert recipe_full.id is not None
    assert recipe_half.id is not None
    assert recipe_third.id is not None
    assert ingredient_a.id is not None
    assert ingredient_b.id is not None
    assert ingredient_c.id is not None

    add_ingredient_to_recipe(recipe_full.id, ingredient_a.id, 1.0)

    add_ingredient_to_recipe(recipe_half.id, ingredient_a.id, 1.0)
    add_ingredient_to_recipe(recipe_half.id, ingredient_b.id, 1.0)

    add_ingredient_to_recipe(recipe_third.id, ingredient_a.id, 1.0)
    add_ingredient_to_recipe(recipe_third.id, ingredient_b.id, 1.0)
    add_ingredient_to_recipe(recipe_third.id, ingredient_c.id, 1.0)

    recommendations = recommend_recipes(
        {
            ingredient_a.id: 1.0,
            ingredient_b.id: 1.0,
            ingredient_c.id: 1.0,
        }
    )

    assert recommendations == [
        (recipe_full, 100.0),
        (recipe_half, 100.0),
        (recipe_third, 100.0),
    ]

def test_calculate_recipe_cost_with_single_ingredient(test_db) -> None:
    recipe = create_recipe(
        Recipe(
            id=None,
            name="Omlet",
            category="Kahvaltı",
            prep_time=10,
            instructions="Pişir.",
        )
    )

    egg = create_ingredient(
        Ingredient(
            id=None,
            name="Yumurta",
            quantity=10.0,
            unit="adet",
            unit_price=6.5,
        )
    )

    assert recipe.id is not None
    assert egg.id is not None

    add_ingredient_to_recipe(recipe.id, egg.id, 3.0)

    assert calculate_recipe_cost(recipe.id) == 19.5


def test_calculate_recipe_cost_with_many_decimal_values(
    test_db,
) -> None:
    recipe = create_recipe(
        Recipe(
            id=None,
            name="Test Tarifi",
            category="Test",
            prep_time=10,
            instructions="Hazırla.",
        )
    )

    first = create_ingredient(
        Ingredient(
            id=None,
            name="Malzeme A",
            quantity=10.0,
            unit="kg",
            unit_price=12.345,
        )
    )

    second = create_ingredient(
        Ingredient(
            id=None,
            name="Malzeme B",
            quantity=10.0,
            unit="L",
            unit_price=7.891,
        )
    )

    assert recipe.id is not None
    assert first.id is not None
    assert second.id is not None

    add_ingredient_to_recipe(recipe.id, first.id, 1.5)
    add_ingredient_to_recipe(recipe.id, second.id, 2.0)

    assert calculate_recipe_cost(recipe.id) == 34.3


def test_calculate_recipe_cost_returns_zero_for_unknown_recipe(
    test_db,
) -> None:
    assert calculate_recipe_cost(999999) == 0.0


def test_find_missing_ingredients_returns_empty_for_unknown_recipe(
    test_db,
) -> None:
    assert find_missing_ingredients(999999, {}) == []


def test_calculate_recipe_match_returns_zero_for_unknown_recipe(
    test_db,
) -> None:
    assert calculate_recipe_match(999999, {}) == 0.0


def test_recommend_recipes_does_not_return_unknown_recipe(
    test_db,
) -> None:
    recommendations = recommend_recipes({999999: 100.0})

    assert recommendations == []


def test_recommend_recipes_preserves_recipe_objects(
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

    add_ingredient_to_recipe(recipe.id, tomato.id, 2.0)

    recommendations = recommend_recipes({tomato.id: 2.0})

    assert len(recommendations) == 1

    recommended_recipe, match = recommendations[0]

    assert recommended_recipe == recipe
    assert recommended_recipe.id == recipe.id
    assert match == 100.0