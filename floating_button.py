import json
import math
from PyQt6.QtWidgets import QPushButton, QApplication, QMenu
from PyQt6.QtCore import Qt, QPoint, QPointF, QRectF
from PyQt6.QtGui import (
    QMouseEvent, QAction, QIcon, QPixmap, QPainter, QPen,
    QColor, QPainterPath,
)
from main_window import MainWindow
from favorites_manager import get_data_dir

SETTINGS_FILE = "settings.json"
DRAG_THRESHOLD = 5
BTN_SIZE = 36
ICON_SIZE = 30


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


def _make_diablo_icon() -> QIcon:
    pixmap = QPixmap(ICON_SIZE, ICON_SIZE)
    pixmap.fill(Qt.GlobalColor.transparent)
    p = QPainter(pixmap)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)

    # Dark background
    bg = QRectF(1, 1, ICON_SIZE - 2, ICON_SIZE - 2)
    p.setBrush(QColor("#1a0000"))
    p.setPen(QPen(QColor("#FFD700"), 1.5))
    p.drawRoundedRect(bg, 3, 3)

    # Five-pointed star
    cx, cy = ICON_SIZE / 2.0, ICON_SIZE / 2.0
    outer_r = 10.0
    inner_r = 3.8

    star_path = QPainterPath()
    for i in range(5):
        ao = math.radians(-90 + i * 72)
        ox, oy = cx + outer_r * math.cos(ao), cy + outer_r * math.sin(ao)
        ai = math.radians(-90 + 36 + i * 72)
        ix, iy = cx + inner_r * math.cos(ai), cy + inner_r * math.sin(ai)
        if i == 0:
            star_path.moveTo(ox, oy)
        else:
            star_path.lineTo(ox, oy)
        star_path.lineTo(ix, iy)
    star_path.closeSubpath()

    p.setBrush(QColor("#FFD700"))
    p.setPen(QPen(QColor("#DAA520"), 0.5))
    p.drawPath(star_path)

    # Tiny center dot
    p.setBrush(Qt.BrushStyle.NoBrush)
    p.setPen(QPen(QColor("#FFD700"), 0.5))
    p.drawEllipse(QPointF(cx, cy), 1.5, 1.5)

    p.end()
    return QIcon(pixmap)


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
        self.setFixedSize(BTN_SIZE, BTN_SIZE)
        self.setIcon(_make_diablo_icon())
        self.setIconSize(self.size())
        self.setStyleSheet("""
            QPushButton {
                background-color: #1a1a1a;
                border: none;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #2a2a2a;
            }
        """)
        self.setToolTip("暗黑破坏神助手 — 左键打开 右键菜单")
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        saved_x, saved_y = _load_position()
        if saved_x is not None and saved_y is not None:
            self.move(saved_x, saved_y)
        else:
            screen = QApplication.primaryScreen().availableGeometry()
            self.move(screen.width() - 60, screen.height() // 2 - 18)

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
        menu.addAction("退出").triggered.connect(lambda: QApplication.instance().quit())
        menu.exec(event.globalPos())

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
