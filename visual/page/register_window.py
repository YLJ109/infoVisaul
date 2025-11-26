import json
import os
from PyQt6.QtCore import Qt, QEasingCurve, QPropertyAnimation
from PyQt6.QtGui import QFont, QPalette, QColor, QPainter, QPixmap
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QGraphicsDropShadowEffect, QApplication, QFrame


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
                background-color: rgba(0, 25, 64, 0.8);  /* 深蓝背景 */
                border: 2px solid #00ffff;  /* 科技感青蓝色边框 */
                border-radius: 12px;
                padding: 14px;
                font-size: 14px;
                color: #ffffff;  /* 白色文字 */
                selection-background-color: #6C63FF;
            }
            QLineEdit:focus {
                border: 2px solid #6C63FF;
                background-color: rgba(0, 40, 100, 0.9);  /* 聚焦时稍亮的背景 */
            }
        """)
        self.setMinimumHeight(50)


class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("用户注册")
        self.setMinimumSize(450, 600)
        self.resize(500, 650)
        
        # 设置科技感样式
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                          stop: 0 #001940, stop: 1 #003366);  /* 科技感深蓝渐变背景 */
                font-family: "微软雅黑";
            }
        """)
        
        self.setup_ui()
    
    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(50, 50, 50, 50)
        main_layout.setSpacing(20)
        
        # 标题
        title_label = QLabel("创建账户")
        title_label.setStyleSheet("""
            background-color: transparent;
            color: #00ffff;  /* 科技感青蓝色文字 */
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 5px;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        subtitle_label = QLabel("填写信息开始使用")
        subtitle_label.setStyleSheet("""
            background-color: transparent;
            color: #cccccc;  /* 浅灰色文字 */
            font-size: 16px;
            margin-bottom: 30px;
        """)
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 表单容器
        form_container = QFrame()
        form_container.setStyleSheet("""
            QFrame {
                background-color: rgba(0, 25, 64, 0.85);  /* 深蓝半透明背景 */
                border: 1px solid #00ffff;  /* 科技感青蓝色边框 */
                border-radius: 20px;
                padding: 25px;
            }
        """)
        form_layout = QVBoxLayout(form_container)
        form_layout.setSpacing(20)
        
        # 用户名输入
        self.username_input = ModernLineEdit("用户名")
        
        # 密码输入
        self.password_input = ModernLineEdit("密码")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        # 确认密码输入
        self.confirm_password_input = ModernLineEdit("确认密码")
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        # 注册按钮
        register_button = AnimatedButton("注 册")
        register_button.clicked.connect(self.register)
        
        # 添加表单元素
        form_layout.addWidget(self.username_input)
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(self.confirm_password_input)
        form_layout.addWidget(register_button)
        
        # 底部链接
        bottom_layout = QHBoxLayout()
        bottom_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        login_label = QLabel("已有账户?")
        login_label.setStyleSheet("""
            background-color: transparent;
            color: #cccccc;  /* 浅灰色文字 */
            font-size: 14px;
        """)
        
        login_button = QPushButton("立即登录")
        login_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #6C63FF;
                border: none;
                font-size: 14px;
                font-weight: bold;
                text-decoration: underline;
            }
            QPushButton:hover {
                color: #5a52e0;
            }
        """)
        login_button.setCursor(Qt.CursorShape.PointingHandCursor)
        login_button.clicked.connect(self.back_to_login)
        
        bottom_layout.addWidget(login_label)
        bottom_layout.addWidget(login_button)
        
        # 添加所有组件
        main_layout.addWidget(title_label)
        main_layout.addWidget(subtitle_label)
        main_layout.addWidget(form_container)
        main_layout.addLayout(bottom_layout)
        main_layout.addStretch()
        
        self.setLayout(main_layout)
    
    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()
        
        if not username or not password or not confirm_password:
            QMessageBox.warning(self, "警告", "请填写所有字段！")
            return
        
        if len(username) < 3:
            QMessageBox.warning(self, "警告", "用户名至少需要3个字符！")
            return
            
        if len(password) < 6:
            QMessageBox.warning(self, "警告", "密码至少需要6个字符！")
            return
        
        if password != confirm_password:
            QMessageBox.warning(self, "警告", "两次输入的密码不一致！")
            return
        
        # 创建用户数据文件（如果不存在）
        if not os.path.exists('./user_info/userInfo.json'):
            with open('./user_info/userInfo.json', 'w') as f:
                json.dump([], f)
        
        # 读取现有用户数据
        with open('./user_info/userInfo.json', 'r') as f:
            user_list = json.load(f)
        
        # 转换为字典格式以便查找
        users = {user['username']: user['password'] for user in user_list}
        
        # 检查用户名是否已存在
        if username in users:
            QMessageBox.warning(self, "警告", "用户名已存在！")
            return
        
        # 添加新用户
        user_list.append({'username': username, 'password': password})
        
        # 保存更新后的用户数据
        with open('./user_info/userInfo.json', 'w') as f:
            json.dump(user_list, f)
        
        QMessageBox.information(self, "成功", "注册成功！")
        self.back_to_login()
    
    def back_to_login(self):
        from visual.page.login_window import LoginWindow  # Move import here to avoid circular import
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = RegisterWindow()
    window.show()
    sys.exit(app.exec())