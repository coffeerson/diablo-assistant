from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QListWidget, QListWidgetItem, QPushButton, QLabel,
    QDialog, QFormLayout, QLineEdit, QDialogButtonBox,
    QMenu, QMessageBox,
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, Qt


class FavoriteDialog(QDialog):
    def __init__(self, title="添加收藏", name="", url="", parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumWidth(400)
        self.setStyleSheet("""
            QDialog { background-color: #2d2d2d; }
            QLabel { background: transparent; }
        """)

        layout = QFormLayout(self)

        self.name_edit = QLineEdit(name)
        self.name_edit.setPlaceholderText("BD名称，如：旋风斩蛮子")
        layout.addRow("名称:", self.name_edit)

        self.url_edit = QLineEdit(url)
        self.url_edit.setPlaceholderText("https://www.d2core.com/d4/builds/...")
        layout.addRow("URL:", self.url_edit)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def get_data(self):
        return self.name_edit.text().strip(), self.url_edit.text().strip()


class FavoritesTab(QWidget):
    def __init__(self, favorites_manager, parent=None):
        super().__init__(parent)
        self.manager = favorites_manager
        self._setup_ui()
        self._load_favorites()

    def refresh(self):
        self._load_favorites()

    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 7)

        # Left panel
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(8, 8, 4, 8)

        title = QLabel("我的收藏")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #FFD700; background: transparent;")
        left_layout.addWidget(title)

        self.list_widget = QListWidget()
        self.list_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.list_widget.customContextMenuRequested.connect(self._show_context_menu)
        self.list_widget.itemClicked.connect(self._on_item_clicked)
        left_layout.addWidget(self.list_widget)

        add_btn = QPushButton("+ 添加收藏")
        add_btn.clicked.connect(self._add_favorite)
        left_layout.addWidget(add_btn)

        splitter.addWidget(left_panel)

        # Right panel - browser
        self.browser = QWebEngineView()
        self.browser.setHtml(
            '<div style="display:flex;align-items:center;justify-content:center;'
            'height:100%;color:#5a5a5a;font-size:18px;'
            'background-color:#1a1a1a;">'
            '从左侧选择一个收藏的BD查看</div>'
        )
        splitter.addWidget(self.browser)

        layout.addWidget(splitter)

    def _load_favorites(self):
        self.list_widget.clear()
        for item in self.manager.get_all():
            list_item = QListWidgetItem(item["name"])
            list_item.setData(Qt.ItemDataRole.UserRole, item["id"])
            list_item.setToolTip(item["url"])
            self.list_widget.addItem(list_item)

    def _on_item_clicked(self, item):
        item_id = item.data(Qt.ItemDataRole.UserRole)
        for fav in self.manager.get_all():
            if fav["id"] == item_id:
                self.browser.setUrl(QUrl(fav["url"]))
                break

    def _add_favorite(self):
        dialog = FavoriteDialog(parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            name, url = dialog.get_data()
            if name and url:
                self.manager.add(name, url)
                self._load_favorites()

    def _edit_favorite(self, item_id: str):
        for fav in self.manager.get_all():
            if fav["id"] == item_id:
                dialog = FavoriteDialog("编辑收藏", fav["name"], fav["url"], parent=self)
                if dialog.exec() == QDialog.DialogCode.Accepted:
                    name, url = dialog.get_data()
                    if name and url:
                        self.manager.update(item_id, name, url)
                        self._load_favorites()
                break

    def _delete_favorite(self, item_id: str):
        reply = QMessageBox.question(
            self, "确认删除", "确定要删除这个收藏吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.manager.delete(item_id)
            self._load_favorites()
            self.browser.setHtml(
                '<div style="display:flex;align-items:center;justify-content:center;'
                'height:100%;color:#5a5a5a;font-size:18px;'
                'background-color:#1a1a1a;">'
                '从左侧选择一个收藏的BD查看</div>'
            )

    def _show_context_menu(self, pos):
        item = self.list_widget.itemAt(pos)
        if not item:
            return
        item_id = item.data(Qt.ItemDataRole.UserRole)

        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu { background-color: #2d2d2d; color: #c0c0c0; border: 1px solid #3a3a3a; }
            QMenu::item:selected { background-color: #8B0000; color: #FFD700; }
        """)

        edit_action = menu.addAction("编辑")
        delete_action = menu.addAction("删除")

        action = menu.exec(self.list_widget.mapToGlobal(pos))
        if action == edit_action:
            self._edit_favorite(item_id)
        elif action == delete_action:
            self._delete_favorite(item_id)
