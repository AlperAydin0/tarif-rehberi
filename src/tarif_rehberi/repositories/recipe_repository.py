from tarif_rehberi.database.connection import get_connection
from tarif_rehberi.models.recipe import Recipe


def create_recipe(recipe: Recipe) -> Recipe:
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO recipes (
                name,
                category,
                prep_time,
                instructions
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                recipe.name,
                recipe.category,
                recipe.prep_time,
                recipe.instructions,
            ),
        )
        recipe_id = cursor.lastrowid

        conn.commit()

        return Recipe(
            id=recipe_id,
            name=recipe.name,
            category=recipe.category,
            prep_time=recipe.prep_time,
            instructions=recipe.instructions,
        )


def get_recipe(recipe_id: int) -> Recipe | None:
    with get_connection() as conn:
        cursor = conn.execute(
            """
            SELECT
                id,
                name,
                category,
                prep_time,
                instructions
            FROM recipes
            WHERE id = ?
            """,
            (recipe_id,),
        )

        row = cursor.fetchone()
        if row is None:
            return None

        return Recipe(
            id=row[0],
            name=row[1],
            category=row[2],
            prep_time=row[3],
            instructions=row[4],
        )


def get_all_recipes() -> list[Recipe]:
    with get_connection() as conn:
        cursor = conn.execute(
            """
            SELECT
                id,
                name,
                category,
                prep_time,
                instructions
            FROM recipes
            ORDER BY name
            """
        )

        rows = cursor.fetchall()

        return [
            Recipe(
                id=row[0],
                name=row[1],
                category=row[2],
                prep_time=row[3],
                instructions=row[4],
            )
            for row in rows
        ]


def update_recipe(recipe: Recipe) -> Recipe:
    if recipe.id is None:
        raise ValueError("Invalid id")

    with get_connection() as conn:
        conn.execute(
            """
            UPDATE recipes
            SET
                name = ?,
                category = ?,
                prep_time = ?,
                instructions = ?
            WHERE id = ?
            """,
            (
                recipe.name,
                recipe.category,
                recipe.prep_time,
                recipe.instructions,
                recipe.id,
            ),
        )

        conn.commit()

        return recipe


def delete_recipe(recipe_id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.execute(
            """
            DELETE FROM recipes
            WHERE id = ?
            """,
            (recipe_id,),
        )

        conn.commit()

        return cursor.rowcount > 0
