import sys
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QKeySequence, QShortcut, QIcon
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QApplication, QHBoxLayout, QPushButton
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

        self.setWindowTitle('一零九就业市场洞察系统')
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

        companyTypeSalaryVisualization.enlarge_chart_button.clicked.connect(lambda: self.enlarge_chart(companyTypeSalaryVisualization))
        educationSalaryVisualization.enlarge_chart_button.clicked.connect(lambda: self.enlarge_chart(educationSalaryVisualization))
        experienceRequirementDistributionVisualization.enlarge_chart_button.clicked.connect(lambda: self.enlarge_chart(experienceRequirementDistributionVisualization))
        jobTypeKeyRequirementsVisualization.enlarge_chart_button.clicked.connect(lambda: self.enlarge_chart(jobTypeKeyRequirementsVisualization))
        regionalJobVisualization.enlarge_chart_button.clicked.connect(lambda: self.enlarge_chart(regionalJobVisualization))
        salaryRangeVisualization.enlarge_chart_button.clicked.connect(lambda: self.enlarge_chart(salaryRangeVisualization))

        self.w_chart = companyTypeSalaryVisualization.win_w
        self.h_chart = companyTypeSalaryVisualization.win_h

        self.visual_lst = [companyTypeSalaryVisualization,
                      educationSalaryVisualization,
                      experienceRequirementDistributionVisualization,
                      jobTypeKeyRequirementsVisualization,
                      regionalJobVisualization,
                      salaryRangeVisualization]

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

        more_button = QPushButton()
        more_button.clicked.connect(self.show_all_charts)
        more_button.setIcon(QIcon("./visual/static/img/more_button.png"))
        more_button.setIconSize(QSize(40, 40))
        more_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius:6px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
        """)
        more_button.setFixedSize(60, 60)
        more_button.setCursor(Qt.CursorShape.PointingHandCursor)

        title_label = QLabel("\\\\\\  一零九就业市场洞察系统  ///")
        title_label.setStyleSheet("""
            color: #00ffff;
            font-size: 25px;
            font-weight: bold;
            background-color: rbg(0, 25, 64);  /* 半透科技感深蓝背景 */
            text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff;
            letter-spacing: 2px;
            border-bottom: 1px solid rgb(0, 255, 255);
            border-style: solid;  /* 显式设置边框样式（关键） */
            border-top: none;     /* 隐藏上边框，只保留底部边框 */
            border-left: none;    /* 隐藏左边框 */
            border-right: none;   /* 隐藏右边框 */
        """)

        title_label.setFixedHeight(80)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        close_button = QPushButton()
        close_button.clicked.connect(self.close)
        close_button.setIcon(QIcon("./visual/static/img/close_button.png"))
        close_button.setIconSize(QSize(40, 40))
        close_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius:6px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
        """)
        close_button.setFixedSize(60, 60)

        close_button.setCursor(Qt.CursorShape.PointingHandCursor)
        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(0)
        nav_layout.setContentsMargins(10, 0, 10, 0)
        nav_layout.addWidget(more_button)
        nav_layout.addWidget(title_label)
        nav_layout.addWidget(close_button)

        top_layout.addWidget(companyTypeSalaryVisualization)
        top_layout.addWidget(educationSalaryVisualization)
        top_layout.addWidget(experienceRequirementDistributionVisualization)

        bottom_layout.addWidget(jobTypeKeyRequirementsVisualization)
        bottom_layout.addWidget(regionalJobVisualization)
        bottom_layout.addWidget(salaryRangeVisualization)
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 5)
        main_layout.setSpacing(0)
        main_layout.addLayout(nav_layout)
        main_layout.addLayout(top_layout)
        main_layout.addLayout(bottom_layout)


        # 添加全屏切换快捷键 (使用QShortcut替代QAction)
        self.create_actions()

    def show_all_charts(self):
        """显示所有图表"""
        for visual in self.visual_lst:
            if visual.isVisible():
                # 恢复图表按钮可见性
                visual.enlarge_chart_button.setVisible(True)
                # 重置Web视图尺寸限制
                visual.web_view.setMinimumSize(0, 0)
                visual.web_view.setMaximumSize(16777215, 16777215)
                # 重置图表尺寸
                visual.win_h = self.h_chart
                visual.win_w = self.w_chart
                # 更新图表显示
                visual.update_chart()
            else:
                # 显示隐藏的图表
                visual.show()

    def enlarge_chart(self, chart):
        """放大指定图表"""
        # 隐藏其他所有图表
        for visual in self.visual_lst:
            if visual != chart:
                visual.hide()

        # 隐藏当前图表的放大按钮
        chart.enlarge_chart_button.setVisible(False)
        # 设置图表视图尺寸
        chart.web_view.setFixedSize(chart.win_w * 2, chart.win_h * 2)
        # 调整图表尺寸
        chart.win_h = chart.win_h * 2 - 20
        chart.win_w = chart.win_w * 2 - 20
        # 更新图表显示
        chart.update_chart(32,20)
        # 显示放大后的图表
        chart.show()
    
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
