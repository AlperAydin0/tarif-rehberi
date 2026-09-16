import sys

import pytest
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from tarif_rehberi.gui.main_window import MainWindow
from tarif_rehberi.models.ingredient import Ingredient
from tarif_rehberi.models.recipe import Recipe
from tarif_rehberi.repositories.ingredient_repository import create_ingredient
from tarif_rehberi.repositories.recipe_ingredient_repository import (
    add_ingredient_to_recipe,
)
from tarif_rehberi.repositories.recipe_repository import create_recipe


@pytest.fixture(scope="session")
def qapp() -> QApplication:
    app = QApplication.instance()

    if app is None:
        app = QApplication(sys.argv)

    return app


def test_main_window_can_be_created(qapp: QApplication, test_db) -> None:
    window = MainWindow()

    assert window is not None


def test_main_window_has_expected_title(qapp: QApplication, test_db) -> None:
    window = MainWindow()

    assert window.windowTitle() == "Tarif Rehberi"


def test_main_window_contains_search_field(qapp: QApplication, test_db) -> None:
    window = MainWindow()

    assert hasattr(window, "search_input")


def test_main_window_contains_recipe_list(qapp: QApplication, test_db) -> None:
    window = MainWindow()

    assert hasattr(window, "recipe_list")


def test_main_window_contains_add_recipe_button(qapp: QApplication, test_db) -> None:
    window = MainWindow()

    assert hasattr(window, "add_recipe_button")


def test_main_window_contains_update_recipe_button(qapp: QApplication, test_db) -> None:
    window = MainWindow()

    assert hasattr(window, "update_recipe_button")


def test_main_window_contains_delete_recipe_button(qapp: QApplication, test_db) -> None:
    window = MainWindow()

    assert hasattr(window, "delete_recipe_button")


def test_main_window_contains_category_filter(qapp: QApplication, test_db) -> None:
    window = MainWindow()

    assert hasattr(window, "category_filter")


def test_main_window_contains_sort_selector(qapp: QApplication, test_db) -> None:
    window = MainWindow()

    assert hasattr(window, "sort_selector")


def test_main_window_contains_ingredient_input(qapp: QApplication, test_db) -> None:
    window = MainWindow()

    assert hasattr(window, "ingredient_input")


def test_main_window_loads_recipes(qapp: QApplication, test_db) -> None:
    create_recipe(
        Recipe(
            id=None,
            name="Mercimek Çorbası",
            category="Çorba",
            prep_time=30,
            instructions="Mercimeği pişir.",
        )
    )

    window = MainWindow()

    assert window.recipe_list.count() == 1
    assert "Mercimek Çorbası" in window.recipe_list.item(0).text()


def test_recipe_search_filters_by_name(qapp: QApplication, test_db) -> None:
    create_recipe(
        Recipe(
            id=None,
            name="Mercimek Çorbası",
            category="Çorba",
            prep_time=30,
            instructions="Mercimeği pişir.",
        )
    )

    create_recipe(
        Recipe(
            id=None,
            name="Kuru Fasulye",
            category="Ana Yemek",
            prep_time=60,
            instructions="Fasulyeyi pişir.",
        )
    )

    window = MainWindow()

    window.search_input.setText("Mercimek")

    assert window.recipe_list.count() == 1
    assert "Mercimek Çorbası" in window.recipe_list.item(0).text()


def test_recipe_search_is_case_insensitive(
    qapp: QApplication,
    test_db,
) -> None:

    create_recipe(
        Recipe(
            id=None,
            name="Mercimek Çorbası",
            category="Çorba",
            prep_time=30,
            instructions="Mercimeği pişir.",
        )
    )

    window = MainWindow()

    window.search_input.setText("MERCİMEK")

    assert window.recipe_list.count() == 1


def test_clearing_search_shows_all_recipes(
    qapp: QApplication,
    test_db,
) -> None:

    create_recipe(
        Recipe(
            id=None,
            name="Mercimek Çorbası",
            category="Çorba",
            prep_time=30,
            instructions="Mercimeği pişir.",
        )
    )

    create_recipe(
        Recipe(
            id=None,
            name="Kuru Fasulye",
            category="Ana Yemek",
            prep_time=60,
            instructions="Fasulyeyi pişir.",
        )
    )

    window = MainWindow()

    window.search_input.setText("Mercimek")
    assert window.recipe_list.count() == 1

    window.search_input.clear()

    assert window.recipe_list.count() == 2


def test_recipe_detail_panel_exists(
    qapp: QApplication,
    test_db,
) -> None:
    window = MainWindow()

    assert hasattr(window, "recipe_detail")


def test_clicking_recipe_shows_recipe_details(
    qapp: QApplication,
    test_db,
) -> None:
    create_recipe(
        Recipe(
            id=None,
            name="Mercimek Çorbası",
            category="Çorba",
            prep_time=30,
            instructions="Mercimeği yıka.\nPişir.\nServis et.",
        )
    )

    window = MainWindow()

    window.recipe_list.setCurrentRow(0)

    assert "Mercimek Çorbası" in window.recipe_detail.toPlainText()
    assert "Çorba" in window.recipe_detail.toPlainText()
    assert "30" in window.recipe_detail.toPlainText()
    assert "Mercimeği yıka." in window.recipe_detail.toPlainText()


def test_recipe_detail_is_cleared_when_no_recipe_is_selected(
    qapp: QApplication,
    test_db,
) -> None:
    window = MainWindow()

    window.recipe_list.clearSelection()

    assert window.recipe_detail.toPlainText() == ""


def test_recipe_detail_shows_ingredients(
    qapp: QApplication,
    test_db,
) -> None:

    recipe = create_recipe(
        Recipe(
            id=None,
            name="Menemen",
            category="Ana Yemek",
            prep_time=20,
            instructions="Malzemeleri pişir.",
        )
    )

    ingredient = create_ingredient(
        Ingredient(
            id=None,
            name="Domates",
            quantity=2.0,
            unit="adet",
            unit_price=10.0,
        )
    )

    add_ingredient_to_recipe(
        recipe.id,
        ingredient.id,
        1.5,
    )

    window = MainWindow()
    window.recipe_list.setCurrentRow(0)

    detail = window.recipe_detail.toPlainText()

    assert "Domates" in detail
    assert "1.5" in detail


def test_recipe_detail_shows_recipe_cost(
    qapp: QApplication,
    test_db,
) -> None:
    recipe = create_recipe(
        Recipe(
            id=None,
            name="Menemen",
            category="Ana Yemek",
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

    add_ingredient_to_recipe(recipe.id, tomato.id, 2.0)
    add_ingredient_to_recipe(recipe.id, egg.id, 3.0)

    window = MainWindow()
    window.recipe_list.setCurrentRow(0)

    detail = window.recipe_detail.toPlainText()

    assert "Maliyet" in detail
    assert "35.00" in detail


def test_recipe_with_sufficient_ingredients_is_shown_green(
    qapp: QApplication,
    test_db,
) -> None:
    recipe = create_recipe(
        Recipe(
            id=None,
            name="Menemen",
            category="Ana Yemek",
            prep_time=20,
            instructions="Pişir.",
        )
    )

    ingredient = create_ingredient(
        Ingredient(
            id=None,
            name="Domates",
            quantity=5.0,
            unit="adet",
            unit_price=10.0,
        )
    )

    add_ingredient_to_recipe(recipe.id, ingredient.id, 2.0)

    window = MainWindow()

    item = window.recipe_list.item(0)

    assert item is not None
    assert item.data(Qt.UserRole + 1) == "sufficient"


def test_recipe_with_insufficient_ingredients_is_shown_red(
    qapp: QApplication,
    test_db,
) -> None:
    recipe = create_recipe(
        Recipe(
            id=None,
            name="Menemen",
            category="Ana Yemek",
            prep_time=20,
            instructions="Pişir.",
        )
    )

    ingredient = create_ingredient(
        Ingredient(
            id=None,
            name="Domates",
            quantity=1.0,
            unit="adet",
            unit_price=10.0,
        )
    )

    add_ingredient_to_recipe(recipe.id, ingredient.id, 2.0)

    window = MainWindow()

    item = window.recipe_list.item(0)

    assert item is not None
    assert item.data(Qt.UserRole + 1) == "insufficient"


def test_sufficient_recipe_item_has_green_foreground(
    qapp: QApplication,
    test_db,
) -> None:
    from PySide6.QtCore import Qt
    from tarif_rehberi.models.ingredient import Ingredient
    from tarif_rehberi.models.recipe import Recipe
    from tarif_rehberi.repositories.ingredient_repository import (
        create_ingredient,
    )
    from tarif_rehberi.repositories.recipe_ingredient_repository import (
        add_ingredient_to_recipe,
    )
    from tarif_rehberi.repositories.recipe_repository import create_recipe

    recipe = create_recipe(
        Recipe(
            id=None,
            name="Menemen",
            category="Ana Yemek",
            prep_time=20,
            instructions="Pişir.",
        )
    )

    ingredient = create_ingredient(
        Ingredient(
            id=None,
            name="Domates",
            quantity=5.0,
            unit="adet",
            unit_price=10.0,
        )
    )

    add_ingredient_to_recipe(recipe.id, ingredient.id, 2.0)

    window = MainWindow()
    item = window.recipe_list.item(0)

    assert item is not None
    assert item.foreground().color() == Qt.green


def test_insufficient_recipe_item_has_red_foreground(
    qapp: QApplication,
    test_db,
) -> None:
    recipe = create_recipe(
        Recipe(
            id=None,
            name="Menemen",
            category="Ana Yemek",
            prep_time=20,
            instructions="Pişir.",
        )
    )

    ingredient = create_ingredient(
        Ingredient(
            id=None,
            name="Domates",
            quantity=1.0,
            unit="adet",
            unit_price=10.0,
        )
    )

    add_ingredient_to_recipe(recipe.id, ingredient.id, 2.0)

    window = MainWindow()
    item = window.recipe_list.item(0)

    assert item is not None
    assert item.foreground().color() == Qt.red


def test_insufficient_recipe_shows_missing_ingredient_cost(
    qapp: QApplication,
    test_db,
) -> None:
    recipe = create_recipe(
        Recipe(
            id=None,
            name="Menemen",
            category="Ana Yemek",
            prep_time=20,
            instructions="Pişir.",
        )
    )

    ingredient = create_ingredient(
        Ingredient(
            id=None,
            name="Domates",
            quantity=1.0,
            unit="adet",
            unit_price=10.0,
        )
    )

    add_ingredient_to_recipe(recipe.id, ingredient.id, 3.0)

    window = MainWindow()

    window.recipe_list.setCurrentRow(0)

    detail = window.recipe_detail.toPlainText()

    assert "Eksik Malzeme Maliyeti: 20.00 TL" in detail


def test_ingredient_search_filters_recipes(
    qapp: QApplication,
    test_db,
) -> None:
    menemen = create_recipe(
        Recipe(
            id=None,
            name="Menemen",
            category="Ana Yemek",
            prep_time=20,
            instructions="Pişir.",
        )
    )

    pilav = create_recipe(
        Recipe(
            id=None,
            name="Pilav",
            category="Ana Yemek",
            prep_time=30,
            instructions="Pişir.",
        )
    )

    domates = create_ingredient(
        Ingredient(
            id=None,
            name="Domates",
            quantity=5.0,
            unit="adet",
            unit_price=10.0,
        )
    )

    pirinc = create_ingredient(
        Ingredient(
            id=None,
            name="Pirinç",
            quantity=5.0,
            unit="bardak",
            unit_price=20.0,
        )
    )

    add_ingredient_to_recipe(menemen.id, domates.id, 2.0)
    add_ingredient_to_recipe(pilav.id, pirinc.id, 2.0)

    window = MainWindow()

    window.ingredient_input.setText("domates")

    assert window.recipe_list.count() == 1
    assert window.recipe_list.item(0).text().startswith("Menemen")


def test_ingredient_search_sorts_by_match_percentage(
    qapp: QApplication,
    test_db,
) -> None:
    high_match_recipe = create_recipe(
        Recipe(
            id=None,
            name="Sebzeli Yemek",
            category="Ana Yemek",
            prep_time=20,
            instructions="Pişir.",
        )
    )

    low_match_recipe = create_recipe(
        Recipe(
            id=None,
            name="Karışık Yemek",
            category="Ana Yemek",
            prep_time=30,
            instructions="Pişir.",
        )
    )

    domates = create_ingredient(
        Ingredient(
            id=None,
            name="Domates",
            quantity=5.0,
            unit="adet",
            unit_price=10.0,
        )
    )

    biber = create_ingredient(
        Ingredient(
            id=None,
            name="Biber",
            quantity=5.0,
            unit="adet",
            unit_price=5.0,
        )
    )

    add_ingredient_to_recipe(
        high_match_recipe.id,
        domates.id,
        2.0,
    )
    add_ingredient_to_recipe(
        low_match_recipe.id,
        domates.id,
        2.0,
    )
    add_ingredient_to_recipe(
        low_match_recipe.id,
        biber.id,
        2.0,
    )

    window = MainWindow()

    window.ingredient_input.setText("domates")

    assert window.recipe_list.count() == 2

    first_item = window.recipe_list.item(0)
    second_item = window.recipe_list.item(1)

    assert first_item is not None
    assert second_item is not None

    assert first_item.text().startswith("Sebzeli Yemek")
    assert second_item.text().startswith("Karışık Yemek")


def test_category_filter_filters_recipes(qapp: QApplication, test_db) -> None:
    create_recipe(
        Recipe(
            id=None,
            name="Mercimek Çorbası",
            category="Çorba",
            prep_time=30,
            instructions="Pişir.",
        )
    )

    create_recipe(
        Recipe(
            id=None,
            name="Menemen",
            category="Ana Yemek",
            prep_time=20,
            instructions="Pişir.",
        )
    )

    window = MainWindow()

    window.category_filter.setCurrentText("Çorba")

    assert window.recipe_list.count() == 1
    assert window.recipe_list.item(0).text().startswith("Mercimek Çorbası")


def test_sort_selector_sorts_by_prep_time_ascending(
    qapp: QApplication, test_db
) -> None:
    create_recipe(
        Recipe(
            id=None,
            name="Uzun Tarif",
            category="Ana Yemek",
            prep_time=60,
            instructions="Pişir.",
        )
    )

    create_recipe(
        Recipe(
            id=None,
            name="Kısa Tarif",
            category="Ana Yemek",
            prep_time=15,
            instructions="Pişir.",
        )
    )

    window = MainWindow()

    window.sort_selector.setCurrentText("Hazırlama Süresi ↑")

    assert window.recipe_list.count() == 2
    assert window.recipe_list.item(0).text().startswith("Kısa Tarif")
    assert window.recipe_list.item(1).text().startswith("Uzun Tarif")


def test_sort_selector_sorts_by_prep_time_descending(
    qapp: QApplication, test_db
) -> None:
    create_recipe(
        Recipe(
            id=None,
            name="Uzun Tarif",
            category="Ana Yemek",
            prep_time=60,
            instructions="Pişir.",
        )
    )

    create_recipe(
        Recipe(
            id=None,
            name="Kısa Tarif",
            category="Ana Yemek",
            prep_time=15,
            instructions="Pişir.",
        )
    )

    window = MainWindow()

    window.sort_selector.setCurrentText("Hazırlama Süresi ↓")

    assert window.recipe_list.count() == 2
    assert window.recipe_list.item(0).text().startswith("Uzun Tarif")
    assert window.recipe_list.item(1).text().startswith("Kısa Tarif")


def test_sort_selector_sorts_by_cost_ascending(
    qapp: QApplication,
    test_db,
) -> None:
    from tarif_rehberi.models.ingredient import Ingredient
    from tarif_rehberi.models.recipe import Recipe
    from tarif_rehberi.repositories.ingredient_repository import (
        create_ingredient,
    )
    from tarif_rehberi.repositories.recipe_ingredient_repository import (
        add_ingredient_to_recipe,
    )
    from tarif_rehberi.repositories.recipe_repository import create_recipe

    cheap_recipe = create_recipe(
        Recipe(
            id=None,
            name="Ucuz Tarif",
            category="Ana Yemek",
            prep_time=20,
            instructions="Pişir.",
        )
    )

    expensive_recipe = create_recipe(
        Recipe(
            id=None,
            name="Pahalı Tarif",
            category="Ana Yemek",
            prep_time=20,
            instructions="Pişir.",
        )
    )

    cheap_ingredient = create_ingredient(
        Ingredient(
            id=None,
            name="Patates",
            quantity=10.0,
            unit="adet",
            unit_price=5.0,
        )
    )

    expensive_ingredient = create_ingredient(
        Ingredient(
            id=None,
            name="Et",
            quantity=10.0,
            unit="kg",
            unit_price=100.0,
        )
    )

    add_ingredient_to_recipe(
        cheap_recipe.id,
        cheap_ingredient.id,
        1.0,
    )

    add_ingredient_to_recipe(
        expensive_recipe.id,
        expensive_ingredient.id,
        1.0,
    )

    window = MainWindow()

    window.sort_selector.setCurrentText("Maliyet ↑")

    assert window.recipe_list.count() == 2
    assert window.recipe_list.item(0).text().startswith("Ucuz Tarif")
    assert window.recipe_list.item(1).text().startswith("Pahalı Tarif")


def test_sort_selector_sorts_by_cost_descending(qapp: QApplication, test_db) -> None:
    cheap_recipe = create_recipe(
        Recipe(
            id=None,
            name="Ucuz Tarif",
            category="Ana Yemek",
            prep_time=20,
            instructions="Pişir.",
        )
    )

    expensive_recipe = create_recipe(
        Recipe(
            id=None,
            name="Pahalı Tarif",
            category="Ana Yemek",
            prep_time=20,
            instructions="Pişir.",
        )
    )

    cheap_ingredient = create_ingredient(
        Ingredient(
            id=None,
            name="Patates",
            quantity=10.0,
            unit="adet",
            unit_price=5.0,
        )
    )

    expensive_ingredient = create_ingredient(
        Ingredient(
            id=None,
            name="Et",
            quantity=10.0,
            unit="kg",
            unit_price=100.0,
        )
    )

    add_ingredient_to_recipe(
        cheap_recipe.id,
        cheap_ingredient.id,
        1.0,
    )

    add_ingredient_to_recipe(
        expensive_recipe.id,
        expensive_ingredient.id,
        1.0,
    )

    window = MainWindow()

    window.sort_selector.setCurrentText("Maliyet ↓")

    assert window.recipe_list.count() == 2
    assert window.recipe_list.item(0).text().startswith("Pahalı Tarif")
    assert window.recipe_list.item(1).text().startswith("Ucuz Tarif")


def test_search_and_category_filter_work_together(qapp: QApplication, test_db) -> None:
    create_recipe(
        Recipe(
            id=None,
            name="Mercimek Çorbası",
            category="Çorba",
            prep_time=30,
            instructions="Pişir.",
        )
    )

    create_recipe(
        Recipe(
            id=None,
            name="Mercimek Köftesi",
            category="Meze",
            prep_time=45,
            instructions="Yoğur.",
        )
    )

    create_recipe(
        Recipe(
            id=None,
            name="Domates Çorbası",
            category="Çorba",
            prep_time=25,
            instructions="Pişir.",
        )
    )

    window = MainWindow()

    window.category_filter.setCurrentText("Çorba")
    window.search_input.setText("mercimek")

    assert window.recipe_list.count() == 1
    assert window.recipe_list.item(0).text().startswith("Mercimek Çorbası")


def test_clearing_search_restores_all_recipes(qapp: QApplication, test_db) -> None:
    create_recipe(
        Recipe(
            id=None,
            name="Mercimek Çorbası",
            category="Çorba",
            prep_time=30,
            instructions="Pişir.",
        )
    )

    create_recipe(
        Recipe(
            id=None,
            name="Menemen",
            category="Ana Yemek",
            prep_time=20,
            instructions="Pişir.",
        )
    )

    window = MainWindow()

    assert window.recipe_list.count() == 2

    window.search_input.setText("mercimek")

    assert window.recipe_list.count() == 1

    window.search_input.clear()

    assert window.recipe_list.count() == 2


def test_clearing_category_filter_restores_all_recipes(
    qapp: QApplication,
    test_db,
) -> None:
    from tarif_rehberi.models.recipe import Recipe
    from tarif_rehberi.repositories.recipe_repository import create_recipe

    create_recipe(
        Recipe(
            id=None,
            name="Mercimek Çorbası",
            category="Çorba",
            prep_time=30,
            instructions="Pişir.",
        )
    )

    create_recipe(
        Recipe(
            id=None,
            name="Menemen",
            category="Ana Yemek",
            prep_time=20,
            instructions="Pişir.",
        )
    )

    window = MainWindow()

    assert window.recipe_list.count() == 2

    window.category_filter.setCurrentText("Çorba")

    assert window.recipe_list.count() == 1

    window.category_filter.setCurrentText("Tüm Kategoriler")

    assert window.recipe_list.count() == 2


def test_selecting_different_recipe_updates_recipe_detail(
    qapp: QApplication, test_db
) -> None:
    create_recipe(
        Recipe(
            id=None,
            name="Mercimek Çorbası",
            category="Çorba",
            prep_time=30,
            instructions="Mercimeği pişir.",
        )
    )

    create_recipe(
        Recipe(
            id=None,
            name="Menemen",
            category="Ana Yemek",
            prep_time=20,
            instructions="Domates ve yumurtayı pişir.",
        )
    )

    window = MainWindow()

    mercimek_row = next(
        index
        for index in range(window.recipe_list.count())
        if window.recipe_list.item(index) is not None
        and window.recipe_list.item(index).text().startswith("Mercimek Çorbası")
    )

    menemen_row = next(
        index
        for index in range(window.recipe_list.count())
        if window.recipe_list.item(index) is not None
        and window.recipe_list.item(index).text().startswith("Menemen")
    )

    window.recipe_list.setCurrentRow(mercimek_row)

    assert "Mercimek Çorbası" in (window.recipe_detail.toPlainText())

    window.recipe_list.setCurrentRow(menemen_row)

    detail = window.recipe_detail.toPlainText()

    assert "Menemen" in detail
    assert "Domates ve yumurtayı pişir." in detail
    assert "Mercimek Çorbası" not in detail


def test_category_filter_and_sort_work_together(qapp: QApplication, test_db) -> None:
    create_recipe(
        Recipe(
            id=None,
            name="Uzun Çorba",
            category="Çorba",
            prep_time=60,
            instructions="Pişir.",
        )
    )

    create_recipe(
        Recipe(
            id=None,
            name="Kısa Çorba",
            category="Çorba",
            prep_time=15,
            instructions="Pişir.",
        )
    )

    create_recipe(
        Recipe(
            id=None,
            name="Ana Yemek",
            category="Ana Yemek",
            prep_time=10,
            instructions="Pişir.",
        )
    )

    window = MainWindow()

    window.category_filter.setCurrentText("Çorba")
    window.sort_selector.setCurrentText("Hazırlama Süresi ↑")

    assert window.recipe_list.count() == 2

    assert window.recipe_list.item(0).text().startswith("Kısa Çorba")

    assert window.recipe_list.item(1).text().startswith("Uzun Çorba")


def test_search_and_sort_work_together(
    qapp: QApplication,
    test_db,
) -> None:
    from tarif_rehberi.models.recipe import Recipe
    from tarif_rehberi.repositories.recipe_repository import create_recipe

    create_recipe(
        Recipe(
            id=None,
            name="Uzun Mercimek Çorbası",
            category="Çorba",
            prep_time=60,
            instructions="Pişir.",
        )
    )

    create_recipe(
        Recipe(
            id=None,
            name="Kısa Mercimek Çorbası",
            category="Çorba",
            prep_time=15,
            instructions="Pişir.",
        )
    )

    create_recipe(
        Recipe(
            id=None,
            name="Menemen",
            category="Ana Yemek",
            prep_time=10,
            instructions="Pişir.",
        )
    )

    window = MainWindow()

    window.search_input.setText("mercimek")
    window.sort_selector.setCurrentText("Hazırlama Süresi ↑")

    assert window.recipe_list.count() == 2

    assert window.recipe_list.item(0).text().startswith("Kısa Mercimek Çorbası")

    assert window.recipe_list.item(1).text().startswith("Uzun Mercimek Çorbası")


def test_ingredient_search_respects_category_filter(
    qapp: QApplication,
    test_db,
) -> None:
    from tarif_rehberi.models.ingredient import Ingredient
    from tarif_rehberi.models.recipe import Recipe
    from tarif_rehberi.repositories.ingredient_repository import (
        create_ingredient,
    )
    from tarif_rehberi.repositories.recipe_ingredient_repository import (
        add_ingredient_to_recipe,
    )
    from tarif_rehberi.repositories.recipe_repository import create_recipe

    corba_recipe = create_recipe(
        Recipe(
            id=None,
            name="Domates Çorbası",
            category="Çorba",
            prep_time=20,
            instructions="Pişir.",
        )
    )

    yemek_recipe = create_recipe(
        Recipe(
            id=None,
            name="Domatesli Makarna",
            category="Ana Yemek",
            prep_time=30,
            instructions="Pişir.",
        )
    )

    ingredient = create_ingredient(
        Ingredient(
            id=None,
            name="Domates",
            quantity=10.0,
            unit="adet",
            unit_price=5.0,
        )
    )

    add_ingredient_to_recipe(
        corba_recipe.id,
        ingredient.id,
        2.0,
    )

    add_ingredient_to_recipe(
        yemek_recipe.id,
        ingredient.id,
        3.0,
    )

    window = MainWindow()

    window.category_filter.setCurrentText("Çorba")
    window.ingredient_input.setText("Domates")

    assert window.recipe_list.count() == 1
    assert window.recipe_list.item(0).text().startswith("Domates Çorbası")


def test_ingredient_search_and_sort_work_together(
    qapp: QApplication,
    test_db,
) -> None:
    from tarif_rehberi.models.ingredient import Ingredient
    from tarif_rehberi.models.recipe import Recipe
    from tarif_rehberi.repositories.ingredient_repository import (
        create_ingredient,
    )
    from tarif_rehberi.repositories.recipe_ingredient_repository import (
        add_ingredient_to_recipe,
    )
    from tarif_rehberi.repositories.recipe_repository import create_recipe

    ingredient = create_ingredient(
        Ingredient(
            id=None,
            name="Domates",
            quantity=10.0,
            unit="adet",
            unit_price=5.0,
        )
    )

    long_recipe = create_recipe(
        Recipe(
            id=None,
            name="Uzun Domates Yemeği",
            category="Ana Yemek",
            prep_time=60,
            instructions="Pişir.",
        )
    )

    short_recipe = create_recipe(
        Recipe(
            id=None,
            name="Kısa Domates Yemeği",
            category="Ana Yemek",
            prep_time=15,
            instructions="Pişir.",
        )
    )

    add_ingredient_to_recipe(
        long_recipe.id,
        ingredient.id,
        2.0,
    )

    add_ingredient_to_recipe(
        short_recipe.id,
        ingredient.id,
        2.0,
    )

    window = MainWindow()

    window.ingredient_input.setText("Domates")
    window.sort_selector.setCurrentText("Hazırlama Süresi ↑")

    assert window.recipe_list.count() == 2

    assert window.recipe_list.item(0).text().startswith("Kısa Domates Yemeği")

    assert window.recipe_list.item(1).text().startswith("Uzun Domates Yemeği")


def test_clearing_ingredient_search_preserves_category_filter(
    qapp: QApplication,
    test_db,
) -> None:
    from tarif_rehberi.models.ingredient import Ingredient
    from tarif_rehberi.models.recipe import Recipe
    from tarif_rehberi.repositories.ingredient_repository import (
        create_ingredient,
    )
    from tarif_rehberi.repositories.recipe_ingredient_repository import (
        add_ingredient_to_recipe,
    )
    from tarif_rehberi.repositories.recipe_repository import create_recipe

    ingredient = create_ingredient(
        Ingredient(
            id=None,
            name="Domates",
            quantity=10.0,
            unit="adet",
            unit_price=5.0,
        )
    )

    corba_recipe = create_recipe(
        Recipe(
            id=None,
            name="Domates Çorbası",
            category="Çorba",
            prep_time=20,
            instructions="Pişir.",
        )
    )

    yemek_recipe = create_recipe(
        Recipe(
            id=None,
            name="Domates Yemeği",
            category="Ana Yemek",
            prep_time=30,
            instructions="Pişir.",
        )
    )

    add_ingredient_to_recipe(
        corba_recipe.id,
        ingredient.id,
        2.0,
    )

    add_ingredient_to_recipe(
        yemek_recipe.id,
        ingredient.id,
        3.0,
    )

    window = MainWindow()

    window.category_filter.setCurrentText("Çorba")
    window.ingredient_input.setText("Domates")

    assert window.recipe_list.count() == 1
    assert window.recipe_list.item(0).text().startswith("Domates Çorbası")

    window.ingredient_input.clear()

    assert window.recipe_list.count() == 1
    assert window.recipe_list.item(0).text().startswith("Domates Çorbası")


def test_category_ingredient_search_and_sort_work_together(
    qapp: QApplication,
    test_db,
) -> None:
    from tarif_rehberi.models.ingredient import Ingredient
    from tarif_rehberi.models.recipe import Recipe
    from tarif_rehberi.repositories.ingredient_repository import (
        create_ingredient,
    )
    from tarif_rehberi.repositories.recipe_ingredient_repository import (
        add_ingredient_to_recipe,
    )
    from tarif_rehberi.repositories.recipe_repository import create_recipe

    ingredient = create_ingredient(
        Ingredient(
            id=None,
            name="Domates",
            quantity=10.0,
            unit="adet",
            unit_price=5.0,
        )
    )

    slow_recipe = create_recipe(
        Recipe(
            id=None,
            name="Uzun Domates Çorbası",
            category="Çorba",
            prep_time=50,
            instructions="Pişir.",
        )
    )

    fast_recipe = create_recipe(
        Recipe(
            id=None,
            name="Kısa Domates Çorbası",
            category="Çorba",
            prep_time=10,
            instructions="Pişir.",
        )
    )

    other_recipe = create_recipe(
        Recipe(
            id=None,
            name="Domatesli Makarna",
            category="Ana Yemek",
            prep_time=5,
            instructions="Pişir.",
        )
    )

    add_ingredient_to_recipe(
        slow_recipe.id,
        ingredient.id,
        2.0,
    )

    add_ingredient_to_recipe(
        fast_recipe.id,
        ingredient.id,
        2.0,
    )

    add_ingredient_to_recipe(
        other_recipe.id,
        ingredient.id,
        2.0,
    )

    window = MainWindow()

    window.category_filter.setCurrentText("Çorba")
    window.ingredient_input.setText("Domates")
    window.sort_selector.setCurrentText("Hazırlama Süresi ↑")

    assert window.recipe_list.count() == 2

    assert window.recipe_list.item(0).text().startswith("Kısa Domates Çorbası")

    assert window.recipe_list.item(1).text().startswith("Uzun Domates Çorbası")


def test_category_ingredient_search_and_cost_sort_work_together(
    qapp: QApplication,
    test_db,
) -> None:
    from tarif_rehberi.models.ingredient import Ingredient
    from tarif_rehberi.models.recipe import Recipe
    from tarif_rehberi.repositories.ingredient_repository import (
        create_ingredient,
    )
    from tarif_rehberi.repositories.recipe_ingredient_repository import (
        add_ingredient_to_recipe,
    )
    from tarif_rehberi.repositories.recipe_repository import create_recipe

    cheap_ingredient = create_ingredient(
        Ingredient(
            id=None,
            name="Domates",
            quantity=10.0,
            unit="adet",
            unit_price=5.0,
        )
    )

    expensive_ingredient = create_ingredient(
        Ingredient(
            id=None,
            name="Domates Sosu",
            quantity=10.0,
            unit="adet",
            unit_price=20.0,
        )
    )

    expensive_recipe = create_recipe(
        Recipe(
            id=None,
            name="Pahalı Domates Çorbası",
            category="Çorba",
            prep_time=15,
            instructions="Pişir.",
        )
    )

    cheap_recipe = create_recipe(
        Recipe(
            id=None,
            name="Ucuz Domates Çorbası",
            category="Çorba",
            prep_time=30,
            instructions="Pişir.",
        )
    )

    other_recipe = create_recipe(
        Recipe(
            id=None,
            name="Ucuz Domates Yemeği",
            category="Ana Yemek",
            prep_time=10,
            instructions="Pişir.",
        )
    )

    add_ingredient_to_recipe(
        expensive_recipe.id,
        expensive_ingredient.id,
        2.0,
    )

    add_ingredient_to_recipe(
        cheap_recipe.id,
        cheap_ingredient.id,
        2.0,
    )

    add_ingredient_to_recipe(
        other_recipe.id,
        cheap_ingredient.id,
        1.0,
    )

    window = MainWindow()

    window.category_filter.setCurrentText("Çorba")
    window.ingredient_input.setText("Domates")
    window.sort_selector.setCurrentText("Maliyet ↑")

    assert window.recipe_list.count() == 2

    assert window.recipe_list.item(0).text().startswith("Ucuz Domates Çorbası")

    assert window.recipe_list.item(1).text().startswith("Pahalı Domates Çorbası")


def test_category_ingredient_search_and_descending_cost_sort_work_together(
    qapp: QApplication,
    test_db,
) -> None:
    from tarif_rehberi.models.ingredient import Ingredient
    from tarif_rehberi.models.recipe import Recipe
    from tarif_rehberi.repositories.ingredient_repository import (
        create_ingredient,
    )
    from tarif_rehberi.repositories.recipe_ingredient_repository import (
        add_ingredient_to_recipe,
    )
    from tarif_rehberi.repositories.recipe_repository import create_recipe

    cheap_ingredient = create_ingredient(
        Ingredient(
            id=None,
            name="Domates",
            quantity=10.0,
            unit="adet",
            unit_price=5.0,
        )
    )

    expensive_ingredient = create_ingredient(
        Ingredient(
            id=None,
            name="Domates Sosu",
            quantity=10.0,
            unit="adet",
            unit_price=20.0,
        )
    )

    cheap_recipe = create_recipe(
        Recipe(
            id=None,
            name="Ucuz Domates Çorbası",
            category="Çorba",
            prep_time=30,
            instructions="Pişir.",
        )
    )

    expensive_recipe = create_recipe(
        Recipe(
            id=None,
            name="Pahalı Domates Çorbası",
            category="Çorba",
            prep_time=15,
            instructions="Pişir.",
        )
    )

    other_recipe = create_recipe(
        Recipe(
            id=None,
            name="Pahalı Domates Yemeği",
            category="Ana Yemek",
            prep_time=10,
            instructions="Pişir.",
        )
    )

    add_ingredient_to_recipe(
        cheap_recipe.id,
        cheap_ingredient.id,
        2.0,
    )

    add_ingredient_to_recipe(
        expensive_recipe.id,
        expensive_ingredient.id,
        2.0,
    )

    add_ingredient_to_recipe(
        other_recipe.id,
        expensive_ingredient.id,
        3.0,
    )

    window = MainWindow()

    window.category_filter.setCurrentText("Çorba")
    window.ingredient_input.setText("Domates")
    window.sort_selector.setCurrentText("Maliyet ↓")

    assert window.recipe_list.count() == 2

    assert window.recipe_list.item(0).text().startswith("Pahalı Domates Çorbası")

    assert window.recipe_list.item(1).text().startswith("Ucuz Domates Çorbası")


def test_clearing_ingredient_search_preserves_category_and_sort(
    qapp: QApplication,
    test_db,
) -> None:
    from tarif_rehberi.models.recipe import Recipe
    from tarif_rehberi.repositories.recipe_repository import create_recipe

    slow_recipe = create_recipe(
        Recipe(
            id=None,
            name="Yavaş Çorba",
            category="Çorba",
            prep_time=50,
            instructions="Pişir.",
        )
    )

    fast_recipe = create_recipe(
        Recipe(
            id=None,
            name="Hızlı Çorba",
            category="Çorba",
            prep_time=10,
            instructions="Pişir.",
        )
    )

    other_recipe = create_recipe(
        Recipe(
            id=None,
            name="Hızlı Yemek",
            category="Ana Yemek",
            prep_time=5,
            instructions="Pişir.",
        )
    )

    window = MainWindow()

    window.category_filter.setCurrentText("Çorba")
    window.sort_selector.setCurrentText("Hazırlama Süresi ↑")

    window.ingredient_input.setText("olmayan malzeme")

    assert window.recipe_list.count() == 0

    window.ingredient_input.clear()

    assert window.recipe_list.count() == 2

    assert window.recipe_list.item(0).text().startswith("Hızlı Çorba")

    assert window.recipe_list.item(1).text().startswith("Yavaş Çorba")

    assert all(
        "Hızlı Yemek" not in window.recipe_list.item(index).text()
        for index in range(window.recipe_list.count())
    )


def test_category_ingredient_search_and_descending_prep_time_sort_work_together(
    qapp: QApplication,
    test_db,
) -> None:
    from tarif_rehberi.models.ingredient import Ingredient
    from tarif_rehberi.models.recipe import Recipe
    from tarif_rehberi.repositories.ingredient_repository import (
        create_ingredient,
    )
    from tarif_rehberi.repositories.recipe_ingredient_repository import (
        add_ingredient_to_recipe,
    )
    from tarif_rehberi.repositories.recipe_repository import create_recipe

    ingredient = create_ingredient(
        Ingredient(
            id=None,
            name="Domates",
            quantity=10.0,
            unit="adet",
            unit_price=5.0,
        )
    )

    short_recipe = create_recipe(
        Recipe(
            id=None,
            name="Kısa Domates Çorbası",
            category="Çorba",
            prep_time=10,
            instructions="Pişir.",
        )
    )

    long_recipe = create_recipe(
        Recipe(
            id=None,
            name="Uzun Domates Çorbası",
            category="Çorba",
            prep_time=60,
            instructions="Pişir.",
        )
    )

    other_recipe = create_recipe(
        Recipe(
            id=None,
            name="Uzun Domates Yemeği",
            category="Ana Yemek",
            prep_time=90,
            instructions="Pişir.",
        )
    )

    add_ingredient_to_recipe(
        short_recipe.id,
        ingredient.id,
        2.0,
    )

    add_ingredient_to_recipe(
        long_recipe.id,
        ingredient.id,
        2.0,
    )

    add_ingredient_to_recipe(
        other_recipe.id,
        ingredient.id,
        2.0,
    )

    window = MainWindow()

    window.category_filter.setCurrentText("Çorba")
    window.ingredient_input.setText("Domates")
    window.sort_selector.setCurrentText("Hazırlama Süresi ↓")

    assert window.recipe_list.count() == 2

    assert window.recipe_list.item(0).text().startswith("Uzun Domates Çorbası")

    assert window.recipe_list.item(1).text().startswith("Kısa Domates Çorbası")
