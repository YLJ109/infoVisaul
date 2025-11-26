# 学历要求与薪资关联
# 饼状图
import sys
import pandas as pd
from PyQt6.QtWidgets import QApplication, QMessageBox
import pyecharts.options as opts
from pyecharts.charts import Pie
from pyecharts.globals import ThemeType
from visual.view.Code_Template import CodeTemplate

class EducationSalaryVisualization(CodeTemplate):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("学历要求与薪资关联")
        
    def load_data(self):
        """加载数据"""
        try:
            # 读取CSV文件
            self.df = pd.read_csv(self.data_path, encoding='utf-8')
            # 清理数据，去除空值
            self.df = self.df.dropna(subset=['学历', '薪资'])
        except Exception as e:
            print(f"数据加载失败: {e}")
            self.df = pd.DataFrame()
            QMessageBox.warning(self, "警告", f"数据加载失败: {str(e)}", QMessageBox.StandardButton.Ok)

    def create_job_count_chart(self):
        """创建学历要求与薪资关联饼状图"""
        # 提取学历和薪资数据
        education_salary_data = self.df[['学历', '薪资']].copy()

        # 解析薪资范围并计算平均值
        def parse_salary(salary_str):
            if '-' in salary_str:
                min_salary, max_salary = salary_str.split('-')
                # 处理"K"后缀
                if 'K' in min_salary.upper():
                    min_val = float(min_salary.upper().replace('K', '')) * 1000
                else:
                    min_val = float(min_salary)

                if 'K' in max_salary.upper():
                    max_val = float(max_salary.upper().replace('K', '')) * 1000
                else:
                    max_val = float(max_salary)

                return (min_val + max_val) / 2
            else:
                # 处理单个值的情况
                if 'K' in salary_str.upper():
                    return float(salary_str.upper().replace('K', '')) * 1000
                else:
                    return float(salary_str)

        # 应用薪资解析函数
        education_salary_data['平均薪资'] = education_salary_data['薪资'].apply(parse_salary)

        # 按学历分组并计算平均薪资
        grouped_data = education_salary_data.groupby('学历')['平均薪资'].mean().reset_index()

        # 按平均薪资排序
        grouped_data = grouped_data.sort_values('平均薪资', ascending=False)

        # 取前10个学历类别
        grouped_data = grouped_data.head(10)
        
        # 准备饼图数据
        pie_data = [list(z) for z in zip(grouped_data['学历'], grouped_data['平均薪资'].round(2))]

        # 创建饼状图
        pie = Pie(init_opts=opts.InitOpts(theme=ThemeType.DARK, width=f"{self.win_w-40}px", height=f"{self.win_h-40}px", bg_color=self.web_bg_color))  # 科技感背景色

        # 添加数据
        pie.add(
            series_name="平均薪资",
            data_pair=pie_data,
            radius=["10%", "65%"],
            center=["50%", "60%"],
            rosetype="radius",
            label_opts=opts.LabelOpts(
                is_show=True, 
                position="outside", 
                formatter="{b}\n{c}元\n({d}%)",
                font_size=12,
                color="#00ffff"  # 科技感青蓝色
            ),
        )

        # 全局配置
        pie.set_global_opts(
            # 标题
            title_opts=opts.TitleOpts(
                title="学历要求与平均薪资关联分析",
                title_textstyle_opts=opts.TextStyleOpts(
                    font_size=18,
                    font_weight="bold",
                    font_family="微软雅黑",
                    color="#00ffff"  # 科技感青蓝色
                ),
                pos_top="10px"
            ),
            # 图例
            legend_opts=opts.LegendOpts(
                orient="horizontal",
                pos_top="10%",
                pos_bottom="5%",
                textstyle_opts=opts.TextStyleOpts(font_size=12, color="#00ffff"),  # 科技感青蓝色
                type_="scroll"
            ),
            # 提示框
            tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{a} <br/>{b}: {c}元 ({d}%)", background_color="rgba(0, 0, 0, 0.7)", border_color="#00ffff", border_width=1)  # 科技感青蓝色边框
        )
        
        # 系列配置
        pie.set_series_opts(
            label_opts=opts.LabelOpts(
                formatter="{b}\n{c}元\n({d}%)",
                font_size=12,
                color="#00ffff"  # 科技感青蓝色
            )
        )
        
        return pie


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EducationSalaryVisualization()
    window.show()
    sys.exit(app.exec())