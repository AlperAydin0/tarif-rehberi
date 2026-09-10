from tarif_rehberi.database.connection import get_connection
from tarif_rehberi.models.ingredient import Ingredient


def add_ingredient_to_recipe(
    recipe_id: int,
    ingredient_id: int,
    quantity: float,
) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO recipe_ingredients (
                recipe_id,
                ingredient_id,
                quantity
            )
            VALUES (?, ?, ?)
            """,
            (
                recipe_id,
                ingredient_id,
                quantity,
            ),
        )

        conn.commit()


RecipeIngredient = tuple[Ingredient, float]


def get_recipe_ingredients(recipe_id: int) -> list[RecipeIngredient]:
    with get_connection() as conn:
        cursor = conn.execute(
            """
            SELECT
                i.id,
                i.name,
                i.quantity,
                i.unit,
                i.unit_price,
                ri.quantity
            FROM recipe_ingredients AS ri
            INNER JOIN ingredients AS i
                ON i.id = ri.ingredient_id
            WHERE ri.recipe_id = ?
            ORDER BY i.name
            """,
            (recipe_id,),
        )

        rows = cursor.fetchall()

        return [
            (
                Ingredient(
                    id=row[0],
                    name=row[1],
                    quantity=row[2],
                    unit=row[3],
                    unit_price=row[4],
                ),
                row[5],
            )
            for row in rows
        ]


def update_recipe_ingredient_quantity(
    recipe_id: int, ingredient_id: int, quantity: float
) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE recipe_ingredients
            SET quantity = ?
            WHERE recipe_id = ? AND ingredient_id = ?
            """,
            (
                quantity,
                recipe_id,
                ingredient_id,
            ),
        )

        conn.commit()


def remove_ingredient_from_recipe(
    recipe_id: int,
    ingredient_id: int,
) -> bool:
    with get_connection() as conn:
        cursor = conn.execute(
            """
            DELETE FROM recipe_ingredients
            WHERE recipe_id = ? AND ingredient_id = ?
            """,
            (
                recipe_id,
                ingredient_id,
            ),
        )
        conn.commit()
        return cursor.rowcount > 0
