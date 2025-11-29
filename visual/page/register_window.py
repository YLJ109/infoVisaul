import json
import os
from PyQt6.QtGui import  QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QMessageBox,QApplication, QFrame
from visual.template.element_rewrite import *



class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("用户注册")
        self.setMinimumSize(450, 600)
        self.resize(500, 650)
        
        # 设置窗口图标
        self.setWindowIcon(QIcon("./visual/static/img/icon.png"))
        
        # 设置整体样式
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                          stop: 0 #f5f7fa, stop: 1 #c3cfe2);
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
            color: #333;
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 5px;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        subtitle_label = QLabel("填写信息开始使用")
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
            color: #666;
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
        # 为登录窗口设置图标
        self.login_window.setWindowIcon(QIcon("./visual/static/img/icon.png"))
        self.login_window.show()
        self.close()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = RegisterWindow()
    window.show()
    sys.exit(app.exec())