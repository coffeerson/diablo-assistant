from PyQt6.QtWidgets import QWidget, QVBoxLayout, QToolBar, QToolButton
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QAction


class BrowserTab(QWidget):
    def __init__(self, url: str, favorites_manager=None, on_favorite_added=None, parent=None):
        super().__init__(parent)
        self.url = url
        self._favorites_manager = favorites_manager
        self._on_favorite_added = on_favorite_added
        self._setup_ui()
        self.browser.setUrl(QUrl(url))

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Browser
        self.browser = QWebEngineView()

        # Toolbar
        toolbar = QToolBar()
        toolbar.setStyleSheet("QToolBar { background: #2d2d2d; border: none; padding: 2px; spacing: 4px; }")

        back_action = QAction("◀", self)
        back_action.triggered.connect(self.browser.back)
        toolbar.addAction(back_action)

        forward_action = QAction("▶", self)
        forward_action.triggered.connect(self.browser.forward)
        toolbar.addAction(forward_action)

        refresh_action = QAction("↻", self)
        refresh_action.triggered.connect(self.browser.reload)
        toolbar.addAction(refresh_action)

        if self._favorites_manager:
            fav_action = QAction("⭐", self)
            fav_action.setToolTip("收藏当前页面")
            fav_action.triggered.connect(self._add_current_to_favorites)
            toolbar.addAction(fav_action)

        layout.addWidget(toolbar)
        layout.addWidget(self.browser)

    def _add_current_to_favorites(self):
        title = self.browser.page().title()
        url = self.browser.url().toString()
        if url and self._favorites_manager:
            self._favorites_manager.add(title or url, url)
            if self._on_favorite_added:
                self._on_favorite_added()
