import sys
from PyQt6.QtWidgets import QApplication
from floating_button import FloatingButton


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("DiabloAssistant")
    app.setQuitOnLastWindowClosed(False)

    button = FloatingButton()
    button.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
