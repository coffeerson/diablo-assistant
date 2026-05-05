import json
from PyQt6.QtWidgets import QPushButton, QApplication, QMenu
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QMouseEvent, QAction
from main_window import MainWindow
from favorites_manager import get_data_dir

SETTINGS_FILE = "settings.json"
DRAG_THRESHOLD = 5


def _settings_path():
    return get_data_dir() / SETTINGS_FILE


def _load_position():
    try:
        with open(_settings_path(), "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("x"), data.get("y")
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return None, None


def _save_position(x: int, y: int):
    data = {"x": x, "y": y}
    with open(_settings_path(), "w", encoding="utf-8") as f:
        json.dump(data, f)


class FloatingButton(QPushButton):
    def __init__(self):
        super().__init__()
        self._drag_pos = QPoint()
        self._drag_start = QPoint()
        self._was_dragged = False
        self.main_window = MainWindow()

        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
        self.setFixedSize(60, 60)
        self.setText("💀")
        self.setStyleSheet("""
            QPushButton {
                background-color: #8B0000;
                color: #FFD700;
                border: 2px solid #6B0000;
                border-radius: 30px;
                font-size: 24px;
            }
            QPushButton:hover {
                background-color: #A00000;
                border-color: #FFD700;
            }
            QPushButton:pressed {
                background-color: #6B0000;
            }
        """)
        self.setToolTip("暗黑破坏神助手 — 左键打开 右键菜单")

        # Restore saved position or use default
        saved_x, saved_y = _load_position()
        if saved_x is not None and saved_y is not None:
            self.move(saved_x, saved_y)
        else:
            screen = QApplication.primaryScreen().availableGeometry()
            self.move(screen.width() - 80, screen.height() // 2 - 30)

    # ── click vs drag ──────────────────────────────────────────────

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            self._drag_start = event.globalPosition().toPoint()
            self._was_dragged = False
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() & Qt.MouseButton.LeftButton:
            delta = event.globalPosition().toPoint() - self._drag_start
            if abs(delta.x()) > DRAG_THRESHOLD or abs(delta.y()) > DRAG_THRESHOLD:
                self._was_dragged = True
            if self._was_dragged:
                self.move(event.globalPosition().toPoint() - self._drag_pos)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            if self._was_dragged:
                _save_position(self.x(), self.y())
            else:
                self._toggle_window()
        super().mouseReleaseEvent(event)

    # ── right-click menu ───────────────────────────────────────────

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu { background-color: #2d2d2d; color: #c0c0c0; border: 1px solid #3a3a3a; }
            QMenu::item:selected { background-color: #8B0000; color: #FFD700; }
        """)

        quit_action = menu.addAction("退出")
        action = menu.exec(event.globalPos())

        if action == quit_action:
            QApplication.instance().quit()

    # ── window toggle ──────────────────────────────────────────────

    def _toggle_window(self):
        if self.main_window.isVisible():
            self.main_window.hide()
        else:
            btn_center = self.frameGeometry().center()
            win_geo = self.main_window.frameGeometry()
            win_geo.moveCenter(btn_center)
            screen = QApplication.primaryScreen().availableGeometry()
            if win_geo.left() < screen.left():
                win_geo.moveLeft(screen.left())
            if win_geo.top() < screen.top():
                win_geo.moveTop(screen.top())
            if win_geo.right() > screen.right():
                win_geo.moveRight(screen.right())
            if win_geo.bottom() > screen.bottom():
                win_geo.moveBottom(screen.bottom())
            self.main_window.move(win_geo.topLeft())
            self.main_window.show()
            self.main_window.raise_()
