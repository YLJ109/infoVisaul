from PyQt6.QtCore import QPropertyAnimation, Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QLineEdit, QGraphicsDropShadowEffect, QPushButton


class AnimatedButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setStyleSheet("""
            QPushButton {
                background-color: #6C63FF;
                border-radius: 20px;
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
                border: none;
            }
            QPushButton:hover {
                background-color: #5a52e0;
            }
            QPushButton:pressed {
                background-color: #4841c0;
                padding-left: 15px;
                padding-top: 12px;
            }
        """)
        self.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=15, xOffset=0, yOffset=5, color=QColor(108, 99, 255, 80)))
        self.setMinimumHeight(45)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def enterEvent(self, event):
        self.animate_shadow(25)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.animate_shadow(15)
        super().leaveEvent(event)

    def animate_shadow(self, end_value):
        effect = self.graphicsEffect()
        if effect:
            anim = QPropertyAnimation(effect, b"blurRadius")
            anim.setEndValue(end_value)
            anim.setDuration(200)
            anim.start()


class ModernLineEdit(QLineEdit):
    def __init__(self, placeholder):
        super().__init__()
        self.setPlaceholderText(placeholder)
        self.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 255, 255, 0.8);
                border: 2px solid #E0E0E0;
                border-radius: 12px;
                padding: 14px;
                font-size: 14px;
                selection-background-color: #6C63FF;
            }
            QLineEdit:focus {
                border: 2px solid #6C63FF;
                background-color: white;
            }
        """)
        self.setMinimumHeight(50)