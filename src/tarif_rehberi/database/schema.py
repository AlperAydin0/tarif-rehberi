from tarif_rehberi.database.connection import get_connection

CREATE_RECIPES_TABLE = """
CREATE TABLE IF NOT EXISTS recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    category TEXT NOT NULL,
    prep_time INTEGER NOT NULL CHECK (prep_time > 0),
    instructions TEXT NOT NULL
);
"""

CREATE_INGREDIENTS_TABLE = """
CREATE TABLE IF NOT EXISTS ingredients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    quantity REAL NOT NULL CHECK (quantity >= 0),
    unit TEXT NOT NULL,
    unit_price  REAL NOT NULL CHECK (unit_price >= 0)
);
"""

CREATE_RECIPE_INGREDIENTS_TABLE = """
CREATE TABLE IF NOT EXISTS recipe_ingredients (
    recipe_id INTEGER NOT NULL,
    ingredient_id INTEGER NOT NULL,
    quantity REAL NOT NULL CHECK (quantity > 0),

    PRIMARY KEY (recipe_id, ingredient_id),

    FOREIGN KEY (recipe_id)
        REFERENCES recipes(id)
        ON DELETE CASCADE,

    
    FOREIGN KEY (ingredient_id)
        REFERENCES ingredients(id)
        ON DELETE CASCADE
);
"""


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(CREATE_RECIPES_TABLE)
        conn.execute(CREATE_INGREDIENTS_TABLE)
        conn.execute(CREATE_RECIPE_INGREDIENTS_TABLE)

        conn.commit()
