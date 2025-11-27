import sys
import pandas as pd
from PyQt6.QtWidgets import QApplication, QMessageBox
import pyecharts.options as opts
from pyecharts.charts import Line
from pyecharts.globals import ThemeType
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
        """创建地区分布曲线图"""
        # 检查数据是否为空
        if self.df.empty:
            print("数据为空，无法生成图表")
            return None

        # 统计各地区岗位数量
        region_counts = self.df['地区'].value_counts().head(10)
        
        # 创建曲线图
        line = Line(
            init_opts=opts.InitOpts(
                theme=ThemeType.DARK,
                width=f"{self.win_w}px",
                height=f"{self.win_h}px",
                bg_color=self.web_bg_color  # 科技感背景色
            )
        )
        
        # 添加X轴数据
        line.add_xaxis(region_counts.index.tolist())
        
        # 添加Y轴数据
        line.add_yaxis(
            series_name="岗位数量",

            y_axis=region_counts.values.tolist(),
            label_opts=opts.LabelOpts(is_show=True, position="top", 
                                    font_family="微软雅黑", font_size=12,
                                    color="#00ffff",border_width=0),  # 科技感青蓝色
            linestyle_opts=opts.LineStyleOpts(width=3, color="#1f77b4",
                                            type_="solid"),
            symbol_size=8,
            is_smooth=True,  # 平滑曲线
            symbol="circle",
            itemstyle_opts=opts.ItemStyleOpts(color="#1f77b4",border_width=0),  # 移除了border_width和border_color
            areastyle_opts=opts.AreaStyleOpts(opacity=0.3, color="#1f77b4")

        )

        # 设置全局配置
        line.set_global_opts(
            title_opts=opts.TitleOpts(
                title="地区岗位分布曲线图",
                title_textstyle_opts=opts.TextStyleOpts(
                    font_size=18,
                    font_weight="bold",
                    font_family="微软雅黑",
                    color="#00ffff"  # 科技感青蓝色
                ),

                subtitle_textstyle_opts=opts.TextStyleOpts(
                    font_size=14,
                    font_family="微软雅黑",
                    color="#00ffff"  # 科技感青蓝色
                    ,border_width=0
                ),
                pos_top="10px"

            ),
            xaxis_opts=opts.AxisOpts(
                type_="category",
                axislabel_opts=opts.LabelOpts(rotate=30, font_family="微软雅黑",
                                            font_size=12, color="#00ffff",border_width=0),  # 科技感青蓝色
                axisline_opts=opts.AxisLineOpts(is_show=True,
                                              linestyle_opts=opts.LineStyleOpts(color="#00ffff")),  # 科技感青蓝色
                axistick_opts=opts.AxisTickOpts(is_show=True)
            ),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                name_textstyle_opts=opts.TextStyleOpts(font_family="微软雅黑",
                                                     font_size=14, color="#00ffff",border_width=0),  # 科技感青蓝色
                axislabel_opts=opts.LabelOpts(font_family="微软雅黑", font_size=12,
                                            color="#00ffff",border_width=0),  # 科技感青蓝色
                axisline_opts=opts.AxisLineOpts(is_show=True,
                                              linestyle_opts=opts.LineStyleOpts(color="#00ffff")),  # 科技感青蓝色
                splitline_opts=opts.SplitLineOpts(is_show=True,
                                                linestyle_opts=opts.LineStyleOpts(color="#00ffff"))  # 科技感青蓝色
            ),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="line",
                                        background_color="rgba(0, 0, 0, 0.7)",
                                        border_color="#00ffff",  # 科技感青蓝色
                                        border_width=0),
            legend_opts=opts.LegendOpts(pos_top="40px",
                                      textstyle_opts=opts.TextStyleOpts(font_family="微软雅黑",
                                                                      color="#00ffff",border_width=0),border_width=0),  # 科技感青蓝色

        )
        
        return line


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RegionalJobVisualization()
    window.show()
    sys.exit(app.exec())