from PyQt6.QtWidgets import QMainWindow, QTabWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCloseEvent
from browser_tab import BrowserTab
from favorites_tab import FavoritesTab
from theme import DARK_THEME


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("暗黑破坏神助手")
        self.resize(1200, 800)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.setStyleSheet(DARK_THEME)

        self.tabs = QTabWidget()
        self.tabs.addTab(BrowserTab("https://www.d2core.com/d4/builds"), "暗黑核")
        self.tabs.addTab(BrowserTab("https://maxroll.gg/d4/tierlists"), "Maxroll")
        self.tabs.addTab(FavoritesTab(), "收藏")

        self.setCentralWidget(self.tabs)

    def closeEvent(self, event: QCloseEvent):
        event.ignore()
        self.hide()
