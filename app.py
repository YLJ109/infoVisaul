import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from visual.page.login_window import LoginWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 设置应用程序图标
    app.setWindowIcon(QIcon('visual/static/img/icon.png'))
    
    login_window = LoginWindow()
    # 为登录窗口设置图标
    login_window.setWindowIcon(QIcon('visual/static/img/icon.png'))
    login_window.show()
    
    # 确保任务栏图标正确显示
    app.setWindowIcon(QIcon('visual/static/img/icon.png'))
    
    sys.exit(app.exec())

