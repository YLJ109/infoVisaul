# 经验要求分布可视化
# 分类占比趋势折线图
import sys
import pandas as pd
from PyQt6.QtWidgets import QApplication, QMessageBox
import pyecharts.options as opts
from pyecharts.charts import Line
from pyecharts.globals import ThemeType
from visual.template.view_Template import CodeTemplate


class ExperienceRequirementDistributionVisualization(CodeTemplate):
    """经验要求分布可视化类"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("经验要求分布")

    def load_data(self):
        """加载数据"""
        try:
            # 读取CSV文件
            self.df = pd.read_csv(self.data_path, encoding='utf-8')
            # 清理数据，去除空值
            self.df = self.df.dropna(subset=['经验要求'])
        except Exception as e:
            print(f"数据加载失败: {e}")
            self.df = pd.DataFrame()
            QMessageBox.warning(self, "警告", f"数据加载失败: {str(e)}", QMessageBox.StandardButton.Ok)

    def create_job_count_chart(self, title_size=18, text_size=12):
        """创建经验要求分布分类占比趋势折线图
        
        Args:
            title_size (int): 标题字体大小
            text_size (int): 文本字体大小
            
        Returns:
            Line: 配置好的折线图对象
        """
        # 检查数据是否为空
        if self.df.empty:
            print("数据为空，无法生成图表")
            return None

        # 统计经验要求分布
        experience_counts = self.df['经验要求'].value_counts()
        
        # 定义经验要求的正确顺序
        experience_order = ['无经验', '1年以下', '1-3年', '3-5年', '5-10年', '10年以上']
        
        # 按照指定顺序重新排列数据
        ordered_data = {}
        for exp in experience_order:
            if exp in experience_counts.index:
                ordered_data[exp] = experience_counts[exp]
            else:
                ordered_data[exp] = 0
                
        # 转换为Series
        experience_counts = pd.Series(ordered_data)

        # 检查统计数据是否为空
        if experience_counts.sum() == 0:
            print("经验要求统计数据为空，无法生成图表")
            return None

        # 计算百分比
        total = experience_counts.sum()
        experience_percentages = (experience_counts / total) * 100

        # 创建折线图
        line = Line(init_opts=opts.InitOpts(
            theme=ThemeType.DARK, 
            width=f"{self.win_w}px", 
            height=f"{self.win_h}px", 
            bg_color="transparent"
        ))  # 改为透明背景

        # 添加X轴和Y轴数据
        line.add_xaxis(experience_percentages.index.tolist())
        line.add_yaxis(
            series_name="岗位占比",
            y_axis=[round(val) for val in experience_percentages.values.tolist()],
            symbol="circle",
            symbol_size=10,
            is_smooth=True,  # 平滑曲线
            label_opts=opts.LabelOpts(
                is_show=True, 
                position="top", 
                formatter="{c}%", 
                color="#00ffff"
            ),  # 科技感青蓝色
            linestyle_opts=opts.LineStyleOpts(width=2, color="#00ffff"),
            itemstyle_opts=opts.ItemStyleOpts(color="#00ffff")
        )

        # 全局配置
        line.set_global_opts(
            title_opts=opts.TitleOpts(
                title="工作经验要求分布占比趋势",
                title_textstyle_opts=opts.TextStyleOpts(
                    font_size=title_size, 
                    font_weight="bold", 
                    font_family="微软雅黑", 
                    color="#00ffff"
                )  # 科技感青蓝色
            ),
            legend_opts=opts.LegendOpts(
                pos_top="10%",
                border_width=0,
                textstyle_opts=opts.TextStyleOpts(
                    font_size=text_size, 
                    font_family="微软雅黑", 
                    color="#00ffff"
                )  # 科技感青蓝色
            ),
            xaxis_opts=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(
                    font_size=text_size, 
                    rotate=45, 
                    font_family="微软雅黑", 
                    color="#00ffff", 
                    interval=0
                ),  # 科技感青蓝色
                name_gap=20
            ),
            yaxis_opts=opts.AxisOpts(
                name="占比(%)",
                name_textstyle_opts=opts.TextStyleOpts(
                    font_size=text_size, 
                    font_family="微软雅黑", 
                    color="#00ffff"
                ),  # 科技感青蓝色
                axislabel_opts=opts.LabelOpts(
                    font_size=text_size, 
                    font_family="微软雅黑", 
                    formatter="{value}%", 
                    color="#00ffff"
                )  # 科技感青蓝色
            ),
            tooltip_opts=opts.TooltipOpts(
                trigger="axis", 
                axis_pointer_type="line", 
                background_color="rgba(0, 0, 0, 0.7)", 
                border_color="#00ffff", 
                border_width=1, 
                textstyle_opts=opts.TextStyleOpts(
                    font_size=text_size, 
                    color="#00ffff"
                )
            ),  # 科技感青蓝色边框
        )

        return line


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExperienceRequirementDistributionVisualization()
    window.show()
    sys.exit(app.exec())