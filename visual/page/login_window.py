import json
import os
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QMessageBox, QApplication, QFrame, QCheckBox
from visual.page.visual_window import Visual
from visual.page.register_window import RegisterWindow
from visual.template.element_rewrite import *


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("用户登录")
        self.setMinimumSize(450, 500)
        self.resize(500, 550)
        
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
            try:
                self.main_window = Visual()
                # 为可视化窗口设置图标
                self.main_window.setWindowIcon(QIcon("./visual/static/img/icon.png"))
                self.main_window.show()
                self.close()
            except Exception as e:
                QMessageBox.critical(self, "错误", f"打开主窗口时发生错误：{str(e)}")
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