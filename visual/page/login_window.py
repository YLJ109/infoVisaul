import json
import os
from PyQt6.QtCore import Qt, QEasingCurve, QPropertyAnimation, QRect
from PyQt6.QtGui import QFont, QPalette, QColor, QPainter, QPixmap, QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QGraphicsDropShadowEffect, QApplication, QFrame, QCheckBox

from visual.page.visual import Visual
from visual.page.register_window import RegisterWindow


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


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("用户登录")
        self.setMinimumSize(450, 500)
        self.resize(500, 550)
        
        # 设置整体样式
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                          stop: 0 #f5f7fa, stop: 1 #c3cfe2);
                font-family: "微软雅黑";
            }
        """)
        
        self.setup_ui()
        self.load_saved_credentials()
    
    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(50, 50, 50, 50)
        main_layout.setSpacing(20)
        
        # 标题
        title_label = QLabel("欢迎回来")
        title_label.setStyleSheet("""
            background-color: transparent;
            color: #333;
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 5px;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        subtitle_label = QLabel("请登录您的账户")
        subtitle_label.setStyleSheet("""
            background-color: transparent;
            color: #666;
            font-size: 16px;
            margin-bottom: 30px;
        """)
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 表单容器
        form_container = QFrame()
        form_container.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.85);
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
        self.password_input.returnPressed.connect(self.login)
        
        # 记住密码复选框
        self.remember_checkbox = QCheckBox("记住密码")
        self.remember_checkbox.setStyleSheet("""
            QCheckBox {
                color: #666;
                font-size: 14px;
                background-color: transparent;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #ccc;
                border-radius: 3px;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #6C63FF;
                border-radius: 3px;
                background-color: #6C63FF;
            }
        """)
        
        # 登录按钮
        login_button = AnimatedButton("登 录")
        login_button.clicked.connect(self.login)
        
        # 添加表单元素
        form_layout.addWidget(self.username_input)
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(self.remember_checkbox)
        form_layout.addWidget(login_button)
        
        # 底部链接
        bottom_layout = QHBoxLayout()
        bottom_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        register_label = QLabel("还没有账户?")
        register_label.setStyleSheet("""
            background-color: transparent;
            color: #666;
            font-size: 14px;
        """)
        
        register_button = QPushButton("立即注册")
        register_button.setStyleSheet("""
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
        register_button.setCursor(Qt.CursorShape.PointingHandCursor)
        register_button.clicked.connect(self.open_register_window)
        
        bottom_layout.addWidget(register_label)
        bottom_layout.addWidget(register_button)
        
        # 添加所有组件
        main_layout.addWidget(title_label)
        main_layout.addWidget(subtitle_label)
        main_layout.addWidget(form_container)
        main_layout.addLayout(bottom_layout)
        main_layout.addStretch()
        
        self.setLayout(main_layout)
    
    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "警告", "请填写所有字段！")
            return
        
        # 检查用户数据文件是否存在
        if not os.path.exists('./user_info/userInfo.json'):
            QMessageBox.warning(self, "错误", "用户不存在，请先注册！")
            return
        
        # 读取用户数据
        with open('./user_info/userInfo.json', 'r') as f:
            user_list = json.load(f)
        
        # 转换为字典格式以便查找
        users = {user['username']: user['password'] for user in user_list}
        
        # 验证用户凭据
        if username in users and users[username] == password:
            # 保存凭证如果选择了记住密码
            if self.remember_checkbox.isChecked():
                self.save_credentials(username, password)
            else:
                self.clear_saved_credentials()
            
            # 这里可以打开主应用窗口
            self.main_window = Visual()
            self.main_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "失败", "用户名或密码错误！")
    
    def open_register_window(self):
        self.register_window = RegisterWindow()
        self.register_window.show()
        self.hide()
    
    def save_credentials(self, username, password):
        """保存用户名和密码到文件"""
        # 确保目录存在
        os.makedirs('./user_info', exist_ok=True)
        
        credentials = {
            'username': username,
            'password': password
        }
        
        with open('./user_info/saved_credentials.json', 'w') as f:
            json.dump(credentials, f)
    
    def load_saved_credentials(self):
        """加载已保存的凭证"""
        try:
            if os.path.exists('./user_info/saved_credentials.json'):
                with open('./user_info/saved_credentials.json', 'r') as f:
                    credentials = json.load(f)
                    self.username_input.setText(credentials.get('username', ''))
                    self.password_input.setText(credentials.get('password', ''))
                    self.remember_checkbox.setChecked(True)
        except Exception as e:
            print(f"加载保存的凭证时出错: {e}")
    
    def clear_saved_credentials(self):
        """清除已保存的凭证"""
        if os.path.exists('./user_info/saved_credentials.json'):
            os.remove('./user_info/saved_credentials.json')



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())