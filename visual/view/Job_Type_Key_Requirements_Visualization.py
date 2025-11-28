# 岗位类型与关键条件交叉分析
# 热力图
import sys
import pandas as pd
from PyQt6.QtWidgets import QApplication, QMessageBox
import pyecharts.options as opts
from pyecharts.charts import HeatMap
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
            self.df = self.df.dropna(subset=['经验要求', '关键词', '薪资'])
            
            # 处理薪资范围数据，提取平均值作为代表
            def extract_salary_avg(salary_str):
                if pd.isna(salary_str):
                    return None
                try:
                    # 分割薪资范围字符串
                    # 处理不同的薪资格式，如"10-15K"或"10K-15K"
                    salary_str = str(salary_str).replace('K', '').replace('k', '').replace('元/月', '')
                    parts = salary_str.split('-')
                    if len(parts) == 2:
                        low = float(parts[0])
                        high = float(parts[1])
                        return (low + high) / 2 * 1000  # 转换为元
                    else:
                        # 如果不是范围格式，尝试直接转换为数值
                        return float(salary_str) * 1000 if 'K' in str(salary_str) or 'k' in str(salary_str) else float(salary_str)
                except:
                    return None
            
            # 应用薪资处理函数
            self.df['薪资'] = self.df['薪资'].apply(extract_salary_avg)
            
            # 再次去除转换后产生的空值
            self.df = self.df.dropna()
        except Exception as e:
            print(f"数据加载失败: {e}")
            self.df = pd.DataFrame()
            QMessageBox.warning(self, "警告", f"数据加载失败: {str(e)}", QMessageBox.StandardButton.Ok)

    def create_job_count_chart(self):
        """创建岗位类型与关键条件交叉分析热力图"""
        # 检查数据是否为空
        if self.df.empty:
            print("数据为空，无法生成图表")
            return None

        # 提取经验要求、关键词和薪资数据
        exp_salary_data = self.df[['经验要求', '关键词', '薪资']].copy()
        
        # 数据预处理：提取前10个最常见的经验要求
        top_experience = exp_salary_data['经验要求'].value_counts().head(10).index.tolist()
        exp_salary_data = exp_salary_data[exp_salary_data['经验要求'].isin(top_experience)]
        
        # 数据预处理：提取前10个最常见的关键词作为行业标识
        all_keywords = []
        for keywords in exp_salary_data['关键词']:
            if isinstance(keywords, str):
                all_keywords.extend([kw.strip() for kw in keywords.split(',') if kw.strip()])
        
        top_industries = pd.Series(all_keywords).value_counts().head(10).index.tolist()
        
        # 构建热力图数据
        data = []
        for i, experience in enumerate(top_experience):
            exp_data = exp_salary_data[exp_salary_data['经验要求'] == experience]
            
            # 统计每个关键词在该经验要求下的平均薪资
            industry_salary = {}
            industry_count = {}
            
            for _, row in exp_data.iterrows():
                keywords = row['关键词']
                salary = row['薪资']
                
                # 确保salary是数值类型
                if isinstance(salary, (int, float)) and isinstance(keywords, str):
                    for kw in keywords.split(','):
                        kw = kw.strip()
                        if kw in top_industries:
                            if kw not in industry_salary:
                                industry_salary[kw] = 0.0
                                industry_count[kw] = 0
                            industry_salary[kw] += float(salary)
                            industry_count[kw] += 1
            
            # 计算平均薪资并转换为K单位
            for j, industry in enumerate(top_industries):
                if industry in industry_salary and industry_count[industry] > 0:
                    avg_salary = round(industry_salary[industry] / industry_count[industry] / 1000)  # 转换为K单位
                    data.append([i, j, avg_salary])
                else:
                    data.append([i, j, 0])

        # 创建热力图
        heatmap = HeatMap(init_opts=opts.InitOpts(
            theme=ThemeType.DARK, 
            width=f"{self.win_w}px", 
            height=f"{self.win_h}px", 
            bg_color="transparent"
        ))
        
        x_data = top_experience
        y_data = top_industries

        # 添加数据
        heatmap.add_xaxis(x_data)
        heatmap.add_yaxis(
            series_name="平均薪资(K)",
            yaxis_data=y_data,
            value=data,
            itemstyle_opts=opts.ItemStyleOpts(color="#00ffff"),
            label_opts=opts.LabelOpts(
                is_show=True,
                color="#00ffff",
                formatter="{@[2]}K"
            )
        )

        # 全局配置
        max_salary = max([d[2] for d in data]) if data else 10
        heatmap.set_global_opts(
            title_opts=opts.TitleOpts(
                title="岗位类型与关键条件交叉分析热力图",
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
                type_="color",
                min_=0,
                max_=max_salary,
                range_color=["#313695", "#4575b4", "#74add1", "#abd9e9", "#e0f3f8", "#ffffbf", "#fee090", "#fdae61", "#f46d43", "#d73027", "#a50026"],
                orient="horizontal",
                pos_left="center",
                pos_bottom="10%",
                is_calculable=True,
                is_piecewise=False,
                border_width=0
            ),
            tooltip_opts=opts.TooltipOpts(
                trigger="item",
            ),
            xaxis_opts=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(color="#00ffff"),
            ),
            yaxis_opts=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(color="#00ffff"),
            )
            , legend_opts=opts.LegendOpts(
                border_width=0,  # 边框宽度设为0，隐藏外框


            )
        )
        
        return heatmap


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = JobTypeKeyRequirementsVisualization()
    window.show()
    sys.exit(app.exec())