from PyQt6.QtWidgets import QPushButton, QApplication
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QMouseEvent
from main_window import MainWindow


class FloatingButton(QPushButton):
    def __init__(self):
        super().__init__()
        self._drag_pos = QPoint()
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
        self.setToolTip("暗黑破坏神助手 - 点击打开")

        screen = QApplication.primaryScreen().availableGeometry()
        self.move(screen.width() - 80, screen.height() // 2 - 30)

        self.clicked.connect(self._toggle_window)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() & Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
        super().mouseMoveEvent(event)

    def _toggle_window(self):
        if self.main_window.isVisible():
            self.main_window.hide()
        else:
            btn_center = self.frameGeometry().center()
            win_geo = self.main_window.frameGeometry()
            win_geo.moveCenter(btn_center)
            # Keep window within screen bounds
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
