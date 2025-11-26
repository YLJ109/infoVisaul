import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeySequence, QShortcut, QIcon
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QApplication, QHBoxLayout
from visual.view.CompanyType_Salary_Visualization import CompanyTypeSalaryVisualization
from visual.view.Education_Salary_Visualization import EducationSalaryVisualization
from visual.view.Experience_Requirement_Distribution_Visualization import ExperienceRequirementDistributionVisualization
from visual.view.Job_Type_Key_Requirements_Visualization import JobTypeKeyRequirementsVisualization
from visual.view.Regional_Job_Visualization import RegionalJobVisualization
from visual.view.Salary_Range_Visualization import SalaryRangeVisualization

class Visual(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("./visual/static/img/icon.png"))
        self.is_fullscreen = False
        self.init_ui()
        
    def init_ui(self):

        self.setWindowTitle('奥特曼招聘信息可视化平台')
        self.setGeometry(100, 100, 1300, 700)
        # 设置窗口图标
        self.setWindowIcon(QIcon("./visual/static/img/icon.png"))
        self.showFullScreen()
        companyTypeSalaryVisualization = CompanyTypeSalaryVisualization()
        educationSalaryVisualization = EducationSalaryVisualization()
        experienceRequirementDistributionVisualization = ExperienceRequirementDistributionVisualization()
        jobTypeKeyRequirementsVisualization = JobTypeKeyRequirementsVisualization()
        regionalJobVisualization = RegionalJobVisualization()
        salaryRangeVisualization = SalaryRangeVisualization()

        self.setStyleSheet("""
            QWidget {
                background-color: #001940;  /* 科技感深蓝背景作为备选 */
                font-family: "微软雅黑";
            }
 
        """)

        top_layout = QHBoxLayout()
        top_layout.setSpacing(0)
        top_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(0)
        bottom_layout.setContentsMargins(0, 0, 0, 0)

        title_label = QLabel("奥特曼招聘信息可视化平台")
        title_label.setStyleSheet("""
            color: #00ffff;
            font-size: 25px;
            font-weight: bold;
            background-color: #000b29;  /* 半透科技感深蓝背景 */
            text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff;
            letter-spacing: 2px;
        """)
        title_label.setFixedHeight(70)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        top_layout.addWidget(companyTypeSalaryVisualization)
        top_layout.addWidget(educationSalaryVisualization)
        top_layout.addWidget(experienceRequirementDistributionVisualization)

        bottom_layout.addWidget(jobTypeKeyRequirementsVisualization)
        bottom_layout.addWidget(regionalJobVisualization)
        bottom_layout.addWidget(salaryRangeVisualization)
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(title_label)
        main_layout.addLayout(top_layout)
        main_layout.addLayout(bottom_layout)
        
        # 添加全屏切换快捷键 (使用QShortcut替代QAction)
        self.create_actions()
        
    def create_actions(self):
        # 创建全屏快捷键 (使用QShortcut)
        fullscreen_shortcut = QShortcut(QKeySequence(Qt.Key.Key_F11), self)
        fullscreen_shortcut.activated.connect(self.toggle_fullscreen)
        
        # 创建退出快捷键 (使用QShortcut)
        quit_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Escape), self)
        quit_shortcut.activated.connect(self.close)
    
    def toggle_fullscreen(self):
        """切换全屏/窗口模式"""
        if self.isFullScreen():
            self.showNormal()
            self.is_fullscreen = False
        else:
            self.showFullScreen()
            self.is_fullscreen = True

        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = Visual()
    login_window.show()
    sys.exit(app.exec())