import sys
import tempfile
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QMessageBox
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6 import QtCore
import visual.setting as setting
import os
class CodeTemplate(QWidget):
    def __init__(self):
        super().__init__()
        # 设置科技感背景色
        self.setStyleSheet("""

              border:1px solid #0d577f;

        """)
        self.web_view = None
        self.setWindowTitle("公司性质与岗位数量关联")
        self.win_w = 470
        self.win_h = 370
        self.web_bg_color = "#001940"  # 科技感深蓝背景
        # self.setFixedSize(self.win_w+20, self.win_h+20)
        self.setMinimumHeight(self.win_h+20)
        self.setMinimumWidth(self.win_w+20)
        self.data_path = setting.data_path # 数据文件路径
        self.echarts_js_path = setting.echarts_js_path # ECharts JS 文件路径
        self.echarts_js_content = self._load_echarts_js()   # 读取 ECharts JS 内容
        self.init_ui() # 初始化UI
        self.load_data()    # 加载数据
        self.update_chart() # 显示初始图表

    def init_ui(self):
        # 创建主布局
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        # 创建网页视图用于显示图表
        self.web_view = QWebEngineView()
        # 设置WebEngine的参数，解决可能的显示问题
        self.web_view.settings().setAttribute(self.web_view.settings().WebAttribute.LocalContentCanAccessRemoteUrls, True)
        self.web_view.settings().setAttribute(self.web_view.settings().WebAttribute.LocalContentCanAccessFileUrls, True)
        main_layout.addWidget(self.web_view)
        
    def _load_echarts_js(self):
        """读取 ECharts JS 文件内容"""
        try:
            with open(self.echarts_js_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            QMessageBox.warning(self, "警告", f"无法加载 ECharts JS 文件: {str(e)}", QMessageBox.StandardButton.Ok)
            return None

    def load_data(self):
        """加载数据"""
        pass

    def create_job_count_chart(self):
        """创建按岗位数量统计的分组柱状图"""
        pass

    def update_chart(self):
        # 只生成岗位数量统计图表
        chart = self.create_job_count_chart()

        # 检查图表是否成功创建
        if chart is None:
            # 图表创建失败
            return

        # 1. 渲染图表到临时HTML文件
        with tempfile.NamedTemporaryFile(suffix='.html', delete=False, mode='w', encoding='utf-8') as temp_file:
            chart.render(path=temp_file.name, template_name="simple_chart.html", echarts_js="")  # echarts_js设为空

        # 2. 读取临时HTML文件内容
        with open(temp_file.name, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # 3. 将ECharts JS内容嵌入到HTML的<head>标签中，并设置body背景色
        head_end_index = html_content.find('</head>')
        if head_end_index != -1:
            # 在head中添加自定义CSS样式设置body背景色以及padding和margin为0
            custom_style = '<style>body { background-color: #001940 !important; border:1px solid #0d577f; padding:0px !important; margin:5px !important;}</style>'
            modified_html = (html_content[:head_end_index] + f'<script>{self.echarts_js_content}</script>' + custom_style
                             + html_content[head_end_index:])
        else:
            # 如果没有</head>标签，就加在<body>前面
            body_start_index = html_content.find('<body>')
            custom_style = '<style>body { background-color: #001940 !important; }</style>'
            modified_html = (html_content[:body_start_index] + f'<script>{self.echarts_js_content}</script>' + custom_style
                             + html_content[body_start_index:])
        # 4. 在WebView中显示修改后的HTML
        self.web_view.setHtml(modified_html, baseUrl=QtCore.QUrl.fromLocalFile(temp_file.name))
        # 5. 删除临时文件
        os.unlink(temp_file.name)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CodeTemplate()
    window.show()
    sys.exit(app.exec())