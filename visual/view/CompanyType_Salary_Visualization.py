import sys
import pandas as pd
from PyQt6.QtWidgets import QApplication,QMessageBox
import pyecharts.options as opts
from pyecharts.charts import Bar
from pyecharts.globals import ThemeType
from visual.view.Code_Template import CodeTemplate

class CompanyTypeSalaryVisualization(CodeTemplate):

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
        bar = Bar(
            init_opts=opts.InitOpts(
                theme=ThemeType.DARK,
                width=f"{self.win_w-40}px",
                height=f"{self.win_h-40}px",
                bg_color=self.web_bg_color  # 深蓝色科技感背景
            )
        )
        bar.add_xaxis(company_counts.index.tolist())
        bar.add_yaxis(series_name="岗位数量",
                      y_axis=company_counts.values.tolist(),
                      label_opts=opts.LabelOpts(
                          is_show=True,
                          position="top",
                          color="#00ffff"  # 科技蓝白色标签文字
                      )
                      )
        bar.set_global_opts(
            title_opts=opts.TitleOpts(
                title="公司性质与岗位数量关系",
                title_textstyle_opts=opts.TextStyleOpts(
                    font_size=18,
                    font_weight="bold",
                    font_family="微软雅黑",
                    color="#00ffff"  # 科技蓝白色标题文字
                ),
                pos_top="10px"
            ),
            legend_opts=opts.LegendOpts(
                pos_top="10%",
                textstyle_opts=opts.TextStyleOpts(
                    font_size=12,
                    color="#00ffff"  # 科技蓝白色图例文字
                )
            ),
            xaxis_opts=opts.AxisOpts(
                type_="category",
                axislabel_opts=opts.LabelOpts(
                    rotate=45,
                    font_size=11,
                    color="#00ffff"  # 科技蓝白色X轴标签文字
                ),
                name_gap=5,
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#00ffff")  # 科技蓝白色轴线
                )
            ),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axislabel_opts=opts.LabelOpts(
                    font_size=11,
                    color="#00ffff"  # 科技蓝白色Y轴标签文字
                ),
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#00ffff")  # 科技蓝白色轴线
                )
            ),
            tooltip_opts=opts.TooltipOpts(
                trigger="axis",
                textstyle_opts=opts.TextStyleOpts(color="#00ffff"),  # 科技蓝白色提示文字
                background_color="rgba(0, 0, 0, 0.7)"  # 深色提示框背景
            )
        )
        bar.set_series_opts(
            label_opts=opts.LabelOpts(
                position="top",
                color="#00ffff"  # 科技蓝白色数据标签
            )
        )
        return bar


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CompanyTypeSalaryVisualization()
    window.show()
    sys.exit(app.exec())