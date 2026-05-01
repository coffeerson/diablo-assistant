from PyQt6.QtWidgets import QWidget, QVBoxLayout, QToolBar
from PyQt6.QtWebEngineWidgets import QWebEngineView

from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QAction


class BrowserTab(QWidget):
    def __init__(self, url: str, parent=None):
        super().__init__(parent)
        self.url = url
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

        layout.addWidget(toolbar)
        layout.addWidget(self.browser)
