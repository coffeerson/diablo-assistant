DARK_THEME = """
/* Global */
QWidget {
    background-color: #1a1a1a;
    color: #c0c0c0;
    font-family: "Microsoft YaHei", "SimHei", sans-serif;
    font-size: 14px;
}

/* Tab Widget */
QTabWidget::pane {
    border: 1px solid #3a3a3a;
    background-color: #1a1a1a;
}

QTabBar::tab {
    background-color: #2d2d2d;
    color: #c0c0c0;
    padding: 8px 20px;
    border: 1px solid #3a3a3a;
    border-bottom: none;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
}

QTabBar::tab:selected {
    background-color: #8B0000;
    color: #FFD700;
    font-weight: bold;
}

QTabBar::tab:hover:!selected {
    background-color: #3d3d3d;
    color: #FFD700;
}

/* List Widget */
QListWidget {
    background-color: #2d2d2d;
    border: 1px solid #3a3a3a;
    border-radius: 4px;
    padding: 4px;
    outline: none;
}

QListWidget::item {
    padding: 8px 12px;
    border-radius: 3px;
}

QListWidget::item:selected {
    background-color: #8B0000;
    color: #FFD700;
}

QListWidget::item:hover:!selected {
    background-color: #3d3d3d;
    color: #FFD700;
}

/* Push Button */
QPushButton {
    background-color: #8B0000;
    color: #c0c0c0;
    border: 1px solid #6B0000;
    padding: 8px 16px;
    border-radius: 4px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #A00000;
    color: #FFD700;
    border-color: #FFD700;
}

QPushButton:pressed {
    background-color: #6B0000;
}

/* Line Edit */
QLineEdit {
    background-color: #2d2d2d;
    color: #c0c0c0;
    border: 1px solid #3a3a3a;
    padding: 6px 10px;
    border-radius: 4px;
}

QLineEdit:focus {
    border-color: #8B0000;
}

/* Label */
QLabel {
    color: #c0c0c0;
    background: transparent;
}

/* Splitter */
QSplitter::handle {
    background-color: #3a3a3a;
    width: 2px;
}

/* Scrollbar */
QScrollBar:vertical {
    background-color: #1a1a1a;
    width: 10px;
    border-radius: 5px;
}

QScrollBar::handle:vertical {
    background-color: #5a5a5a;
    border-radius: 5px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background-color: #8B0000;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    background-color: #1a1a1a;
    height: 10px;
    border-radius: 5px;
}

QScrollBar::handle:horizontal {
    background-color: #5a5a5a;
    border-radius: 5px;
    min-width: 30px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #8B0000;
}

QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {
    width: 0px;
}

/* Tool Tip */
QToolTip {
    background-color: #2d2d2d;
    color: #FFD700;
    border: 1px solid #8B0000;
    padding: 4px;
}
"""
