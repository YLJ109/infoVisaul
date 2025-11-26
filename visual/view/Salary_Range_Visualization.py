# 薪资区间分布可视化
# 桑基图
import sys
import pandas as pd
from PyQt6.QtWidgets import QApplication, QMessageBox
import pyecharts.options as opts
from pyecharts.charts import Sankey
from pyecharts.globals import ThemeType
from visual.view.Code_Template import CodeTemplate


class SalaryRangeVisualization(CodeTemplate):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("薪资区间分布")

    def load_data(self):
        """加载数据"""
        try:
            # 读取CSV文件
            self.df = pd.read_csv(self.data_path, encoding='utf-8')
            # 数据加载成功，无需打印信息
            
            # 检查是否有薪资列
            if '薪资' not in self.df.columns:
                print("错误：数据中没有找到'薪资'列")
                self.df = pd.DataFrame()
                return
                
            # 清理数据，去除空值
            original_count = len(self.df)
            self.df = self.df.dropna(subset=['薪资'])
            # 已去除空薪资数据
            
            # 处理薪资范围数据，提取平均值作为代表
            def extract_salary_avg(salary_str):
                if pd.isna(salary_str):
                    return None
                try:
                    # 分割薪资范围字符串
                    parts = str(salary_str).split('-')
                    if len(parts) == 2:
                        low = int(parts[0])
                        high = int(parts[1])
                        return (low + high) / 2  # 返回平均值
                    else:
                        # 如果不是范围格式，尝试直接转换为整数
                        return int(salary_str)
                except:
                    return None
            
            # 应用薪资处理函数
            self.df['薪资'] = self.df['薪资'].apply(extract_salary_avg)
            
            # 再次去除转换后产生的空值
            original_count = len(self.df)
            self.df = self.df.dropna()
            # 已转换为数值类型并完成样本数据处理
            
        except Exception as e:
            print(f"数据加载失败: {e}")
            self.df = pd.DataFrame()
            QMessageBox.warning(self, "警告", f"数据加载失败: {str(e)}", QMessageBox.StandardButton.Ok)

    def create_job_count_chart(self):
        """创建薪资区间分布桑基图"""
        # 检查数据是否为空
        if self.df.empty:
            print("数据为空，无法生成图表")
            return None

        # 开始创建图表

        # 定义薪资区间
        salary_ranges = [
            (0, 5000),
            (5000, 8000),
            (8000, 12000),
            (12000, 18000),
            (18000, 25000),
            (25000, 35000),
            (35000, 50000),
            (50000, float('inf'))
        ]
        
        range_labels = [
            "0-5k",
            "5k-8k",
            "8k-12k",
            "12k-18k",
            "18k-25k",
            "25k-35k",
            "35k-50k",
            "50k以上"
        ]

        # 按薪资区间统计数量
        range_counts = []
        for min_sal, max_sal in salary_ranges:
            if max_sal == float('inf'):
                count = len(self.df[(self.df['薪资'] >= min_sal)])
            else:
                count = len(self.df[(self.df['薪资'] >= min_sal) & (self.df['薪资'] < max_sal)])
            range_counts.append(count)
        # 各区间统计完成

        # 检查是否有数据
        if sum(range_counts) == 0:
            print("警告：所有薪资区间都没有数据")
            return None

        # 构造桑基图数据
        nodes = [
            {"name": "总计"},
        ]
        
        # 添加薪资区间节点
        for label in range_labels:
            nodes.append({"name": label})
            
        # 构造链接关系
        links = []
        total = sum(range_counts)
        
        # 从总计到各薪资区间的链接
        for i, (label, count) in enumerate(zip(range_labels, range_counts)):
            if count > 0:  # 只添加有数据的链接
                links.append({
                    "source": "总计",
                    "target": label,
                    "value": count
                })

        # 创建桑基图
        sankey = Sankey(init_opts=opts.InitOpts(theme=ThemeType.DARK, width=f"{self.win_w-40}px", height=f"{self.win_h-40}px", bg_color=self.web_bg_color))  # 科技感背景色

        sankey.add(
            series_name="薪资区间分布",
            nodes=nodes,
            links=links,
            linestyle_opt=opts.LineStyleOpts(opacity=0.2, curve=0.5, color="source"),
            label_opts=opts.LabelOpts(position="right", color="#00ffff"),  # 科技感青蓝色
        )

        # 全局配置
        sankey.set_global_opts(
            title_opts=opts.TitleOpts(
                title="薪资区间分布桑基图",
                title_textstyle_opts=opts.TextStyleOpts(font_size=18, font_weight="bold", font_family="微软雅黑", color="#00ffff")  # 科技感青蓝色
            ),
            tooltip_opts=opts.TooltipOpts(trigger="item", trigger_on="mousemove", background_color="rgba(0, 0, 0, 0.7)", border_color="#00ffff", border_width=1)  # 科技感青蓝色边框
        )

        return sankey


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SalaryRangeVisualization()
    window.show()
    sys.exit(app.exec())