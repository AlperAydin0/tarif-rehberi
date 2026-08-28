import sqlite3

from tarif_rehberi.database.connection import get_connection
from tarif_rehberi.models.ingredient import Ingredient


def create_ingredient(ingredient: Ingredient) -> Ingredient:
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO ingredients (
                name,
                quantity,
                unit,
                unit_price
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                ingredient.name,
                ingredient.quantity,
                ingredient.unit,
                ingredient.unit_price,
            ),
        )

        conn.commit()

        ingredient_id: int | None = cursor.lastrowid
        assert ingredient_id is not None

        return Ingredient(
            id=ingredient_id,
            name=ingredient.name,
            quantity=ingredient.quantity,
            unit=ingredient.unit,
            unit_price=ingredient.unit_price,
        )


def get_ingredient(ingredient_id: int) -> Ingredient | None:
    with get_connection() as conn:
        cursor: sqlite3.Cursor = conn.execute(
            """
            SELECT
                id,
                name,
                quantity,
                unit,
                unit_price
            FROM ingredients
            WHERE id = ?
            """,
            (ingredient_id,),
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return Ingredient(
            id=row[0],
            name=row[1],
            quantity=row[2],
            unit=row[3],
            unit_price=row[4],
        )


def get_all_ingredients() -> list[Ingredient]:

    with get_connection() as conn:
        cursor: sqlite3.Cursor = conn.execute(
            """
            SELECT
                id,
                name,
                quantity,
                unit,
                unit_price
            FROM ingredients
            ORDER BY name
            """
        )

        rows = cursor.fetchall()

        return [
            Ingredient(
                id=row[0],
                name=row[1],
                quantity=row[2],
                unit=row[3],
                unit_price=row[4],
            )
            for row in rows
        ]


def update_ingredient(ingredient: Ingredient) -> Ingredient:

    if ingredient.id is None:
        raise ValueError("Cannot update an ingredient without an id.")

    with get_connection() as conn:
        conn.execute(
            """
            UPDATE ingredients
            SET
                name = ?,
                quantity = ?,
                unit = ?,
                unit_price = ?
            WHERE id = ?
            """,
            (
                ingredient.name,
                ingredient.quantity,
                ingredient.unit,
                ingredient.unit_price,
                ingredient.id,
            ),
        )

        conn.commit()

        return ingredient


def delete_ingredient(ingredient_id: int) -> bool:

    with get_connection() as conn:
        cursor: sqlite3.Cursor = conn.execute(
            """
            DELETE FROM ingredients
            WHERE id = ?
            """,
            (ingredient_id,),
        )

        conn.commit()

        return cursor.rowcount > 0