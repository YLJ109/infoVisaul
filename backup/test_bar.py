import sys
import os
import tempfile
import pandas as pd
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QMessageBox, QLabel
from PyQt6.QtWebEngineWidgets import QWebEngineView
import pyecharts.options as opts
from pyecharts.charts import Bar
from pyecharts.globals import ThemeType
import setting

class CompanyTypeSalaryVisualization(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("公司性质与岗位数量关联")
        self.win_w = 500
        self.win_h = 400
        self.setGeometry(100, 100, self.win_w, self.win_h)
        self.data_path = setting.data_path # 数据文件路径
        self.echarts_js_path = setting.echarts_js_path # ECharts JS 文件路径
        self.echarts_js_content = self._load_echarts_js()   # 读取 ECharts JS 内容
        self.init_ui() # 初始化UI
        self.load_data()    # 加载数据
        self.update_chart() # 显示初始图表

    def init_ui(self):
        # 创建主布局
        main_layout = QVBoxLayout(self)
        # 创建网页视图用于显示图表
        self.web_view = QWebEngineView()
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
        try:
            # 读取CSV文件
            self.df = pd.read_csv(self.data_path, encoding='utf-8')
            # 清理数据，去除空值
            self.df = self.df.dropna(subset=['公司性质', '薪资'])
        except Exception as e:
            print(f"数据加载失败: {e}")
            self.df = pd.DataFrame()
            QMessageBox.warning(self, "警告", f"数据加载失败: {str(e)}", QMessageBox.StandardButton.Ok)

    def create_job_count_chart(self):
        """创建按岗位数量统计的分组柱状图"""
        company_counts = self.df['公司性质'].value_counts().head(10)
        bar = Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, width=f"{self.win_w-40}px", height=f"{self.win_h-40}px"))
        bar.add_xaxis(company_counts.index.tolist())
        bar.add_yaxis(series_name="岗位数量", y_axis=company_counts.values.tolist(),
                      label_opts=opts.LabelOpts(is_show=True, position="top"))
        bar.set_global_opts(
            title_opts=opts.TitleOpts(title="公司性质与岗位数量关系",title_textstyle_opts=opts.TextStyleOpts(
                font_size=18,font_weight="bold", font_family="微软雅黑" ), pos_top="10px"),
            xaxis_opts=opts.AxisOpts(type_="category",
                                   axislabel_opts=opts.LabelOpts(rotate=45, font_size=11),
                                   name_gap=5),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axislabel_opts=opts.LabelOpts(font_size=11)
            ),
            tooltip_opts=opts.TooltipOpts(trigger="axis"))
        bar.set_series_opts(
            label_opts=opts.LabelOpts(position="top"))
        return bar

    def update_chart(self):
        # 只生成岗位数量统计图表
        chart = self.create_job_count_chart()

        # 1. 渲染图表到临时HTML文件
        with tempfile.NamedTemporaryFile(suffix='.html', delete=False, mode='w', encoding='utf-8') as temp_file:
            chart.render(path=temp_file.name, template_name="simple_chart.html", echarts_js="")  # echarts_js设为空

        # 2. 读取临时HTML文件内容
        with open(temp_file.name, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # 3. 将ECharts JS内容嵌入到HTML的<head>标签中
        head_end_index = html_content.find('</head>')
        if head_end_index != -1:
            modified_html = (html_content[:head_end_index] + f'<script>{self.echarts_js_content}</script>'
                             + html_content[head_end_index:])
        else:
            # 如果没有</head>标签，就加在<body>前面
            body_start_index = html_content.find('<body>')
            modified_html = (html_content[:body_start_index] + f'<script>{self.echarts_js_content}</script>'
                             + html_content[body_start_index:])
        # 4. 在WebView中显示修改后的HTML
        self.web_view.setHtml(modified_html)
        # 5. 删除临时文件
        os.unlink(temp_file.name)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CompanyTypeSalaryVisualization()
    window.show()
    sys.exit(app.exec())