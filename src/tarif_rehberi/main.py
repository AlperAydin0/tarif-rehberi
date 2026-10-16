import sys

from PySide6.QtWidgets import QApplication

from tarif_rehberi.database.schema import init_db
from tarif_rehberi.gui.main_window import MainWindow


def main() -> int:
    init_db()

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
