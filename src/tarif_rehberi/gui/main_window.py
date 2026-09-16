import unicodedata

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from tarif_rehberi.models.recipe import Recipe
from tarif_rehberi.repositories.recipe_ingredient_repository import (
    get_recipe_ingredients,
)
from tarif_rehberi.repositories.recipe_repository import get_all_recipes
from tarif_rehberi.services.recipe_service import (
    calculate_recipe_cost,
    find_missing_ingredients,
)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self._match_percentages = {}
        self.setWindowTitle("Tarif Rehberi")
        self.resize(1000, 700)

        self._recipes: list[Recipe] = []
        self._visible_recipes: list[Recipe] = []

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Tarif adı ara...")
        main_layout.addWidget(self.search_input)

        filter_layout = QHBoxLayout()

        self.category_filter = QComboBox()
        self.category_filter.addItem("Tüm Kategoriler")
        filter_layout.addWidget(self.category_filter)

        self.sort_selector = QComboBox()
        self.sort_selector.addItems(
            [
                "Sıralama",
                "Hazırlama Süresi ↑",
                "Hazırlama Süresi ↓",
                "Maliyet ↑",
                "Maliyet ↓",
            ]
        )
        filter_layout.addWidget(self.sort_selector)

        self.ingredient_input = QLineEdit()
        self.ingredient_input.setPlaceholderText("Malzeme ara veya ekle...")
        filter_layout.addWidget(self.ingredient_input)

        main_layout.addLayout(filter_layout)

        self.recipe_list = QListWidget()
        main_layout.addWidget(self.recipe_list)

        self.recipe_detail = QTextEdit()
        self.recipe_detail.setReadOnly(True)
        self.recipe_detail.setPlaceholderText("Tarif detayları burada gösterilecek...")
        main_layout.addWidget(self.recipe_detail)

        self.recipe_list.currentRowChanged.connect(self._show_recipe_detail)
        # self.recipe_list.itemSelectionChanged.connect(self._handle_recipe_selection)
        button_layout = QHBoxLayout()

        self.add_recipe_button = QPushButton("Tarif Ekle")
        self.update_recipe_button = QPushButton("Tarif Güncelle")
        self.delete_recipe_button = QPushButton("Tarif Sil")

        button_layout.addWidget(self.add_recipe_button)
        button_layout.addWidget(self.update_recipe_button)
        button_layout.addWidget(self.delete_recipe_button)

        main_layout.addLayout(button_layout)

        self.sort_selector.currentTextChanged.connect(self._sort_recipes)
        self.search_input.textChanged.connect(self._filter_recipes)
        self.ingredient_input.textChanged.connect(self._filter_by_ingredient)
        self.category_filter.currentTextChanged.connect(self._filter_by_category)

        self._load_recipes()

    def _load_recipes(self) -> None:
        self._recipes = get_all_recipes()

        current_category = self.category_filter.currentText()

        self.category_filter.blockSignals(True)
        self.category_filter.clear()
        self.category_filter.addItem("Tüm Kategoriler")

        categories = sorted(
            {recipe.category for recipe in self._recipes if recipe.category}
        )

        self.category_filter.addItems(categories)

        if current_category in categories:
            self.category_filter.setCurrentText(current_category)
        else:
            self.category_filter.setCurrentText("Tüm Kategoriler")

        self.category_filter.blockSignals(False)

        self._match_percentages = {}

        self._display_recipes(self._recipes)

    def _display_recipes(self, recipes: list[Recipe]) -> None:
        self.recipe_list.blockSignals(True)
        self.recipe_list.clear()

        self._visible_recipes = list(recipes)

        for recipe in self._visible_recipes:
            match_percentage = self._match_percentages.get(recipe.id)

            display_text = f"{recipe.name} | {recipe.prep_time} dk | {recipe.category}"

            if match_percentage is not None:
                display_text += f" | Eşleşme: %{match_percentage:.0f}"

            item = QListWidgetItem(display_text)

            item.setData(
                Qt.UserRole,
                recipe.id,
            )

            recipe_ingredients = get_recipe_ingredients(recipe.id)

            is_sufficient = all(
                ingredient.quantity >= required_quantity
                for ingredient, required_quantity in recipe_ingredients
            )

            item.setData(
                Qt.UserRole + 1,
                "sufficient" if is_sufficient else "insufficient",
            )
            if is_sufficient:
                item.setForeground(Qt.green)
            else:
                item.setForeground(Qt.red)

            self.recipe_list.addItem(item)

        self.recipe_list.setCurrentRow(-1)
        self.recipe_detail.clear()

        self.recipe_list.blockSignals(False)

    @staticmethod
    def _normalize_search_text(text: str) -> str:
        text = text.strip().casefold()

        return "".join(
            character
            for character in unicodedata.normalize("NFD", text)
            if unicodedata.category(character) != "Mn"
        )

    def _show_recipe_detail(self, row: int) -> None:
        self.recipe_detail.clear()

        if row < 0:
            return

        item = self.recipe_list.item(row)

        if item is None:
            return

        recipe_id = item.data(Qt.UserRole)

        if recipe_id is None:
            return

        recipe = next(
            (recipe for recipe in self._visible_recipes if recipe.id == recipe_id),
            None,
        )

        if recipe is None:
            return

        recipe_cost = calculate_recipe_cost(recipe.id)

        recipe_ingredients = get_recipe_ingredients(recipe.id)

        missing_cost = 0.0

        for ingredient, required_quantity in recipe_ingredients:
            if ingredient.quantity < required_quantity:
                missing_quantity = required_quantity - ingredient.quantity
                missing_cost += missing_quantity * ingredient.unit_price

        detail_lines = [
            f"Tarif: {recipe.name}",
            f"Kategori: {recipe.category}",
            f"Hazırlama Süresi: {recipe.prep_time} dakika",
            f"Maliyet: {recipe_cost:.2f} TL",
        ]

        if missing_cost > 0:
            detail_lines.append(f"Eksik Malzeme Maliyeti: {missing_cost:.2f} TL")

        detail_lines.extend(
            [
                "",
                "Malzemeler:",
            ]
        )

        for ingredient, required_quantity in recipe_ingredients:
            detail_lines.append(
                f"- {ingredient.name}: {required_quantity:g} {ingredient.unit}"
            )

        detail_lines.extend(
            [
                "",
                "Talimatlar:",
                recipe.instructions,
            ]
        )

        self.recipe_detail.setPlainText("\n".join(detail_lines))

    def _recipe_contains_ingredient(self, recipe: Recipe, ingredient_name: str) -> bool:
        search_text = self._normalize_search_text(ingredient_name)

        recipe_ingredients = get_recipe_ingredients(recipe.id)

        return any(
            search_text in self._normalize_search_text(ingredient.name)
            for ingredient, _ in recipe_ingredients
        )

    def _filter_recipes(self, text: str) -> None:
        search_text = self._normalize_search_text(text)
        selected_category = self.category_filter.currentText()

        filtered_recipes = list(self._recipes)

        if selected_category != "Tüm Kategoriler":
            filtered_recipes = [
                recipe
                for recipe in filtered_recipes
                if recipe.category == selected_category
            ]

        if search_text:
            filtered_recipes = [
                recipe
                for recipe in filtered_recipes
                if search_text in self._normalize_search_text(recipe.name)
            ]

        self._display_recipes(filtered_recipes)

    def _filter_by_ingredient(self, text: str) -> None:
        search_text = text.strip()

        if not search_text:
            self._filter_recipes(self.search_input.text())
            return

        selected_category = self.category_filter.currentText()

        recipes = list(self._recipes)

        if selected_category != "Tüm Kategoriler":
            recipes = [
                recipe for recipe in recipes if recipe.category == selected_category
            ]

        normalized_search = self._normalize_search_text(search_text)

        matching_recipes = []

        for recipe in recipes:
            recipe_ingredients = get_recipe_ingredients(recipe.id)

            if not recipe_ingredients:
                continue

            matched_count = sum(
                normalized_search in self._normalize_search_text(ingredient.name)
                for ingredient, _ in recipe_ingredients
            )

            if matched_count == 0:
                continue

            match_percentage = matched_count / len(recipe_ingredients) * 100

            matching_recipes.append((recipe, match_percentage))

        matching_recipes.sort(
            key=lambda item: (
                -item[1],
                self._normalize_search_text(item[0].name),
            )
        )

        self._match_percentages = {
            recipe.id: percentage for recipe, percentage in matching_recipes
        }

        self._display_recipes([recipe for recipe, _ in matching_recipes])

    def _filter_by_category(self, category: str) -> None:
        search_text = self.search_input.text()

        if search_text:
            self._filter_recipes(search_text)
            return

        if category == "Tüm Kategoriler":
            self._display_recipes(self._recipes)
            return

        filtered_recipes = [
            recipe for recipe in self._recipes if recipe.category == category
        ]

        self._display_recipes(filtered_recipes)

    def _sort_recipes(self, sort_option: str) -> None:
        recipes = list(self._recipes)

        selected_category = self.category_filter.currentText()

        if selected_category != "Tüm Kategoriler":
            recipes = [
                recipe for recipe in recipes if recipe.category == selected_category
            ]

        search_text = self._normalize_search_text(self.search_input.text())

        if search_text:
            recipes = [
                recipe
                for recipe in recipes
                if search_text in self._normalize_search_text(recipe.name)
            ]

        if sort_option == "Hazırlama Süresi ↑":
            recipes.sort(key=lambda recipe: recipe.prep_time)

        elif sort_option == "Hazırlama Süresi ↓":
            recipes.sort(
                key=lambda recipe: recipe.prep_time,
                reverse=True,
            )

        elif sort_option == "Maliyet ↑":
            recipes.sort(key=lambda recipe: calculate_recipe_cost(recipe.id))

        elif sort_option == "Maliyet ↓":
            recipes.sort(
                key=lambda recipe: calculate_recipe_cost(recipe.id),
                reverse=True,
            )

        self._display_recipes(recipes)

    def _handle_recipe_selection(self) -> None:
        row = self.recipe_list.currentRow()
        self._show_recipe_detail(row)
