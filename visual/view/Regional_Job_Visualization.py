import sys
import pandas as pd
from PyQt6.QtWidgets import QApplication, QMessageBox
import pyecharts.options as opts
from pyecharts.charts import Geo
from pyecharts.globals import ThemeType
from pyecharts.commons.utils import JsCode
from visual.view.Code_Template import CodeTemplate


class RegionalJobVisualization(CodeTemplate):
    def load_data(self):
        """加载数据"""
        try:
            # 读取CSV文件
            self.df = pd.read_csv(self.data_path, encoding='utf-8')
            # 清理数据，去除空值
            self.df = self.df.dropna(subset=['地区'])
        except Exception as e:
            print(f"数据加载失败: {e}")
            self.df = pd.DataFrame()
            QMessageBox.warning(self, "警告", f"数据加载失败: {str(e)}", QMessageBox.StandardButton.Ok)

    def create_job_count_chart(self):
        """创建中国地图岗位分布图"""
        # 检查数据是否为空
        if self.df.empty:
            print("数据为空，无法生成图表")
            return None

        # 地区名称映射，确保与pyecharts中的地区名称一致
        REGION_MAP = {
            "西安": "陕西",
            "北京": "北京",
            "上海": "上海",
            "广州": "广东",
            "深圳": "广东",
            "成都": "四川",
            "杭州": "浙江",
            "武汉": "湖北",
            "南京": "江苏",
            "重庆": "重庆",
            "天津": "天津",
            "长沙": "湖南",
            "苏州": "江苏"
        }

        # 应用地区映射
        self.df['mapped_region'] = self.df['地区'].map(REGION_MAP).fillna(self.df['地区'])

        # 统计各地区岗位数量
        region_counts = self.df['mapped_region'].value_counts()

        # 准备地图数据
        data_pairs = [(region, count) for region, count in region_counts.items()]

        # 创建地理坐标图（中国地图）
        geo = Geo(
            init_opts=opts.InitOpts(
                theme=ThemeType.DARK,
                width=f"{self.win_w}px",
                height=f"{self.win_h}px",
                bg_color="transparent",  # 改为透明背景
                renderer="canvas"  # 强制使用canvas渲染器，避免WebGL问题
            )
        )

        # 添加地图类型设置
        geo.add_schema(maptype="china")

        # 添加数据
        geo.add(
            series_name="岗位数量",
            data_pair=data_pairs,
            type_="effectScatter",  # 使用涟漪效果散点图
            symbol_size=10,

        )

        # 设置全局配置
        geo.set_global_opts(
            title_opts=opts.TitleOpts(
                title="全国岗位分布地图",
                title_textstyle_opts=opts.TextStyleOpts(
                    font_size=18,
                    font_weight="bold",
                    font_family="微软雅黑",
                    color="#00ffff"  # 科技感青蓝色
                ),
                subtitle_textstyle_opts=opts.TextStyleOpts(
                    font_size=14,
                    font_family="微软雅黑",
                    color="#00ffff",  # 科技感青蓝色
                ),
                pos_top="10px"
            ),
            visualmap_opts=opts.VisualMapOpts(
                is_show=True,
                type_="color",
                is_calculable=True,
                pos_left="left",
                pos_top="bottom",
                textstyle_opts=opts.TextStyleOpts(color="#00ffff"),
                range_color=["#50a3ba", "#eac763", "#d94e5d"],
            ),
            tooltip_opts=opts.TooltipOpts(
                trigger="item",
                formatter=JsCode(
                    """function(params) {
                        if (typeof params.value == 'undefined') {
                            return params.name + ': 0';
                        } else {
                            return params.name + ': ' + params.value;
                        }
                    }"""
                ),
                background_color="rgba(0, 0, 0, 0.7)",
                border_color="#00ffff",
                border_width=0,
            ),
            legend_opts=opts.LegendOpts(
                pos_top="40px",
                border_width=0,
                textstyle_opts=opts.TextStyleOpts(
                    font_family="微软雅黑",
                    color="#00ffff"
                    ,border_width=0
                )
            ),
        )

        # 设置系列配置
        geo.set_series_opts(
            label_opts=opts.LabelOpts(
                is_show=False,
                font_family="微软雅黑",
                font_size=12,
                color="#00ffff"

            )
        )
        return geo


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RegionalJobVisualization()
    window.show()
    sys.exit(app.exec())