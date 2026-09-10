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


from tarif_rehberi.models.ingredient import Ingredient
from tarif_rehberi.models.recipe import Recipe
from tarif_rehberi.repositories.ingredient_repository import (
    create_ingredient,
)
from tarif_rehberi.repositories.recipe_ingredient_repository import (
    add_ingredient_to_recipe,
)
from tarif_rehberi.repositories.recipe_repository import (
    create_recipe,
)
from tarif_rehberi.services.recipe_service import (
    calculate_recipe_match,
    find_missing_ingredients,
    recommend_recipes,
)


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

    assert missing == [flour, milk]


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
