# 岗位类型与关键条件交叉分析
# 散点图 / 交叉表可视化
import sys
import pandas as pd
from PyQt6.QtWidgets import QApplication, QMessageBox
import pyecharts.options as opts
from pyecharts.charts import Scatter
from pyecharts.globals import ThemeType
from visual.view.Code_Template import CodeTemplate

class JobTypeKeyRequirementsVisualization(CodeTemplate):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("岗位类型与关键条件交叉分析")

    def load_data(self):
        """加载数据"""
        try:
            # 读取CSV文件
            self.df = pd.read_csv(self.data_path, encoding='utf-8')
            # 清理数据，去除空值
            self.df = self.df.dropna(subset=['工作名称', '关键词'])
        except Exception as e:
            print(f"数据加载失败: {e}")
            self.df = pd.DataFrame()
            QMessageBox.warning(self, "警告", f"数据加载失败: {str(e)}", QMessageBox.StandardButton.Ok)

    def create_job_count_chart(self):
        """创建岗位类型与关键条件交叉分析散点图"""
        # 提取岗位类型和关键词数据
        job_requirements_data = self.df[['工作名称', '关键词']].copy()
        
        # 数据预处理：提取前10个最常见的岗位类型
        top_job_types = job_requirements_data['工作名称'].value_counts().head(10).index.tolist()
        job_requirements_data = job_requirements_data[job_requirements_data['工作名称'].isin(top_job_types)]
        
        # 数据预处理：提取前10个最常见的关键词
        all_keywords = []
        for keywords in job_requirements_data['关键词']:
            if isinstance(keywords, str):
                all_keywords.extend([kw.strip() for kw in keywords.split(',') if kw.strip()])
        
        top_keywords = pd.Series(all_keywords).value_counts().head(10).index.tolist()
        
        # 构建交叉表数据
        scatter_data = []
        for job_type in top_job_types:
            job_data = job_requirements_data[job_requirements_data['工作名称'] == job_type]
            total_jobs = len(job_data)
            
            # 统计每个关键词在该岗位类型中的出现次数
            keyword_counts = {}
            for keywords in job_data['关键词']:
                if isinstance(keywords, str):
                    for kw in keywords.split(','):
                        kw = kw.strip()
                        if kw in top_keywords:
                            keyword_counts[kw] = keyword_counts.get(kw, 0) + 1
            
            # 计算关键词在该岗位中的占比
            for keyword in top_keywords:
                count = keyword_counts.get(keyword, 0)
                # 使用百分比作为散点图的值
                percentage = round((count / total_jobs * 100) if total_jobs > 0 else 0, 2)
                scatter_data.append([job_type, keyword, percentage])
        
        # 创建散点图
        scatter = Scatter(
            init_opts=opts.InitOpts(
                theme=ThemeType.DARK,
                width=f"{self.win_w-40}px",
                height=f"{self.win_h-40}px",
                bg_color=self.web_bg_color  # 科技感背景色
            )
        )
        
        # 准备散点图数据
        x_data = [item[0] for item in scatter_data]  # 岗位类型
        y_data = [item[1] for item in scatter_data]  # 关键词
        size_data = [item[2] * 5 for item in scatter_data]  # 百分比作为点的大小，放大5倍便于观察

        # 添加数据
        scatter.add_xaxis(x_data)
        scatter.add_yaxis(
            series_name="关键词出现频率",
            y_axis=[list(z) for z in zip(y_data, size_data)],  # 同时传递y轴数据和点大小
            label_opts=opts.LabelOpts(is_show=False, color="#00ffff"),  # 科技感青蓝色
            itemstyle_opts=opts.ItemStyleOpts(color="#1f77b4"),  # 设置点的颜色
            encode={"tooltip": [0, 1, 2]}  # 编码提示框显示内容
        )

        # 全局配置
        scatter.set_global_opts(
            title_opts=opts.TitleOpts(
                title="岗位类型与关键技能交叉分析",
                title_textstyle_opts=opts.TextStyleOpts(
                    font_size=18,
                    font_weight="bold",
                    font_family="微软雅黑",
                    color="#00ffff"  # 科技感青蓝色
                ),
                pos_top="10px"
            ),
            visualmap_opts=opts.VisualMapOpts(
                is_show=True,
                type_="size",
                min_=0,
                max_=50,
                range_size=[10, 50],
                orient="horizontal",
                pos_left="center",
                pos_top="5%",
                is_calculable=True
            ),
            xaxis_opts=opts.AxisOpts(
                type_="category",
                axislabel_opts=opts.LabelOpts(rotate=45, font_size=11, color="#00ffff"),  # 科技感青蓝色
                name_gap=5
            ),
            yaxis_opts=opts.AxisOpts(
                type_="category",
                axislabel_opts=opts.LabelOpts(font_size=11, color="#00ffff")  # 科技感青蓝色
            ),
            tooltip_opts=opts.TooltipOpts(
                trigger="item",
                formatter="{a} <br/>{b0}: {c0}<br/>{b1}: {c1}%"
            ),
            legend_opts=opts.LegendOpts(is_show=False)
        )
        
        return scatter


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = JobTypeKeyRequirementsVisualization()
    window.show()
    sys.exit(app.exec())