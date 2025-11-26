# 数据文件路径
import os

# 获取当前文件所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 数据文件路径
data_path = os.path.join(current_dir, "static", "data", "cleaned_zhilian_jobs.csv")
# ECharts JS 文件路径
echarts_js_path = os.path.join(current_dir,"static", "js", "echarts.min.js")
os.environ["QTWEBENGINE_DISABLE_GPU"] = "1"