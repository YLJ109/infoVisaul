import sys
from PyQt6.QtWidgets import QApplication
from visual.page.login_window import LoginWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 设置应用程序图标

    login_window = LoginWindow()
    # 为登录窗口设置图标

    login_window.show()

    
    sys.exit(app.exec())

