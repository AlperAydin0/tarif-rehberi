import sqlite3

from tarif_rehberi import globals_
from tarif_rehberi.database.schema import init_db


def test_init_db_creates_database_file(test_db) -> None:
    assert globals_.DATABASE_PATH.exists()


def test_init_db_creates_ingredients_table(test_db) -> None:
    with sqlite3.connect(globals_.DATABASE_PATH) as connection:
        tables = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            AND name = 'ingredients'
            """
        ).fetchall()

    assert tables == [("ingredients",)]


def test_init_db_creates_recipes_table(test_db) -> None:
    with sqlite3.connect(globals_.DATABASE_PATH) as connection:
        tables = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            AND name = 'recipes'
            """
        ).fetchall()

    assert tables == [("recipes",)]


def test_init_db_creates_recipe_ingredients_table(test_db) -> None:
    with sqlite3.connect(globals_.DATABASE_PATH) as connection:
        tables = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            AND name = 'recipe_ingredients'
            """
        ).fetchall()

    assert tables == [("recipe_ingredients",)]


def test_init_db_is_idempotent(test_db) -> None:
    init_db()
    init_db()

    with sqlite3.connect(globals_.DATABASE_PATH) as connection:
        tables = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            ORDER BY name
            """
        ).fetchall()

    assert ("ingredients",) in tables
    assert ("recipes",) in tables
    assert ("recipe_ingredients",) in tables


def test_init_db_enforces_ingredient_quantity_constraint(test_db) -> None:
    with sqlite3.connect(globals_.DATABASE_PATH) as connection:
        columns = connection.execute(
            "PRAGMA table_info(ingredients)"
        ).fetchall()

    column_names = {column[1] for column in columns}

    assert "quantity" in column_names


def test_init_db_enforces_recipe_ingredient_quantity_constraint(
    test_db,
) -> None:
    with sqlite3.connect(globals_.DATABASE_PATH) as connection:
        columns = connection.execute(
            "PRAGMA table_info(recipe_ingredients)"
        ).fetchall()

    column_names = {column[1] for column in columns}

    assert "quantity" in column_names