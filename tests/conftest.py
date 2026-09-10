from collections.abc import Generator
from pathlib import Path

import pytest

from tarif_rehberi import globals_
from tarif_rehberi.database.schema import init_db


@pytest.fixture
def test_db(
    tmp_path: Path,
) -> Generator[None, None, None]:
    original_database_path: Path = globals_.DATABASE_PATH

    globals_.DATABASE_PATH = tmp_path / "test.db"

    init_db()

    yield

    globals_.DATABASE_PATH = original_database_path
