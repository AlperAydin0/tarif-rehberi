from tarif_rehberi.database.connection import get_connection


def test_database_connection(test_db) -> None:
    conn = get_connection()

    try:
        assert conn is not None
    finally:
        conn.close()


def test_database_tables_are_created(test_db) -> None:
    with get_connection() as conn:
        cursor = conn.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            ORDER BY name
            """
        )

        tables: set[str] = {row[0] for row in cursor.fetchall()}

        assert "ingredients" in tables
        assert "recipe_ingredients" in tables
        assert "recipes" in tables


def test_foreign_keys_are_enabled(test_db) -> None:
    with get_connection() as connection:
        cursor = connection.execute("PRAGMA foreign_keys")
        result: tuple[int] | None = cursor.fetchone()

    assert result == (1,)
