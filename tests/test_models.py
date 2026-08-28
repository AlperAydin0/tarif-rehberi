from tarif_rehberi.models.ingredient import Ingredient
from tarif_rehberi.models.recipe import Recipe


def test_ingredient_creation() -> None:
    ingredient = Ingredient(
        id=None, name="Domates", quantity=5.0, unit="kg", unit_price=40.0
    )
    assert ingredient.id is None
    assert ingredient.name == "Domates"
    assert ingredient.quantity == 5.0
    assert ingredient.unit == "kg"
    assert ingredient.unit_price == 40.0


def test_recipe_creation() -> None:
    recipe: Recipe = Recipe(
        id=None,
        name="Menemen",
        category="Kahvaltı",
        prep_time=15,
        instructions="Domatesleri doğra ve pişir.",
    )

    assert recipe.id is None
    assert recipe.name == "Menemen"
    assert recipe.category == "Kahvaltı"
    assert recipe.prep_time == 15
    assert recipe.instructions == "Domatesleri doğra ve pişir."
