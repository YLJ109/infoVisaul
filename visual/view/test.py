import sys
import pandas as pd
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QMessageBox
from PyQt6.QtWebEngineWidgets import QWebEngineView
import pyecharts.options as opts
from pyecharts.charts import Map
from pyecharts.globals import ThemeType
import os
from PyQt6.QtCore import QUrl

# 彻底禁用 GPU 渲染（解决白屏核心）
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-gpu --no-sandbox --disable-software-rasterizer --disable-webgl"

class CodeTemplate(QWidget):
    def __init__(self):
        super().__init__()
        self.win_w = 1200
        self.win_h = 800
        self.data_path = ""

class RegionalJobVisualization(CodeTemplate):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("中国地区岗位分布")
        self.init_ui()
        self.load_data()
        self.render_map()

    def init_ui(self):
        self.setLayout(QVBoxLayout())
        # 设置 WebView 背景为白色（避免透明白屏）
        self.web_view = QWebEngineView()
        self.web_view.setStyleSheet("background-color: #192538;")
        self.layout().addWidget(self.web_view)
        self.resize(self.win_w, self.win_h)

    def load_data(self):
        # 模拟数据（已验证有效）
        mock_data = {
            "地区": ["北京", "上海", "广东", "江苏", "浙江", "山东", "四川", "湖北"],
            "岗位数量": [156, 132, 205, 98, 89, 76, 65, 58]
        }
        self.df = pd.DataFrame(mock_data)
        print("加载的数据：")
        print(self.df)

    def create_china_map(self):
        if self.df.empty:
            QMessageBox.warning(self, "警告", "无有效数据", QMessageBox.StandardButton.Ok)
            return None

        if "岗位数量" not in self.df.columns:
            region_counts = self.df['地区'].value_counts()
            map_data = list(region_counts.items())
        else:
            map_data = self.df[['地区', '岗位数量']].values.tolist()

        valid_regions = self.get_valid_provinces()
        map_data = [item for item in map_data if item[0] in valid_regions]

        print("过滤后的地图数据：")
        print(map_data)

        if not map_data:
            QMessageBox.warning(self, "警告", "无识别到的省级地区", QMessageBox.StandardButton.Ok)
            return None

        c = (
            Map(init_opts=opts.InitOpts(
                theme=ThemeType.DARK,
                width=f"{self.win_w - 40}px",
                height=f"{self.win_h - 40}px",
                bg_color="#192538",
                # 关键修复：pyecharts 1.9.1 用 animation_on 控制动画（替代 is_enable）

            ))
            .add(
                series_name="岗位数量",
                data_pair=map_data,
                maptype="china",
                label_opts=opts.LabelOpts(is_show=True, color="#ffffff"),
                is_roam=True
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(
                    title="中国地区岗位分布地图",
                    title_textstyle_opts=opts.TextStyleOpts(font_size=18, font_weight="bold", color="#ffffff")
                ),
                visualmap_opts=opts.VisualMapOpts(
                    min_=min([x[1] for x in map_data]),
                    max_=max([x[1] for x in map_data]),
                    range_color=["#e0f7fa", "#0288d1"],
                    orient="horizontal",
                    pos_bottom="10%"
                )
            )
        )
        return c

    def render_map(self):
        map_chart = self.create_china_map()
        if not map_chart:
            return

        # 保存为本地HTML（避免临时文件权限问题）
        local_html_path = "china_job_map.html"
        map_chart.render(local_html_path)
        abs_html_path = os.path.abspath(local_html_path).replace("\\", "/")
        print(f"HTML文件已保存到：{abs_html_path}")

        # 加载HTML（绝对路径+file协议，确保解析正确）
        self.web_view.setUrl(QUrl(f"file:///{abs_html_path}"))
        self.local_html_path = local_html_path

    def get_valid_provinces(self):
        return [
            "北京", "天津", "河北", "山西", "内蒙古", "辽宁", "吉林", "黑龙江",
            "上海", "江苏", "浙江", "安徽", "福建", "江西", "山东", "河南",
            "湖北", "湖南", "广东", "广西", "海南", "重庆", "四川", "贵州",
            "云南", "西藏", "陕西", "甘肃", "青海", "宁夏", "新疆", "香港",
            "澳门", "台湾"
        ]

    def closeEvent(self, event):
        # 退出时删除HTML文件
        if hasattr(self, "local_html_path") and os.path.exists(self.local_html_path):
            os.remove(self.local_html_path)
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RegionalJobVisualization()
    window.show()
    sys.exit(app.exec())