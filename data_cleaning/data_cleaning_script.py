import pandas as pd
import re
import numpy as np
from datetime import datetime

def clean_zhilian_data(input_file, output_file):
    """
    清洗智联招聘数据
    """
    # 读取CSV文件
    df = pd.read_csv(input_file, encoding='utf-8-sig')
    
    # 1. 去重处理
    print(f"原始数据行数: {len(df)}")
    df = df.drop_duplicates()
    print(f"去重后数据行数: {len(df)}")
    
    # 2. 数据清洗和标准化
    
    # 清理薪资字段 - 确保不出现日期格式，并正确处理"万"单位
    def clean_salary(salary):
        if pd.isna(salary) or salary == '面议':
            return np.nan
        
        # 转换为字符串处理
        salary_str = str(salary)
        
        # 检查是否是日期格式，如果是则返回NaN
        try:
            # 尝试解析为日期，如果成功说明是日期格式
            datetime.strptime(salary_str, '%Y/%m/%d')
            return np.nan  # 如果是日期格式，返回NaN
        except ValueError:
            # 不是日期格式，继续处理
            pass
        
        # 提取薪资范围
        salary_clean = salary_str.replace('·13薪', '').replace('·14薪', '').replace('·15薪', '')
        
        # 处理"万"单位，将其转换为具体数字
        if '万' in salary_clean:
            # 匹配"1-2万"或"1.5-2万"等格式
            match = re.search(r'([\d\.]+)[-~]?([\d\.]+)?万', salary_clean)
            if match:
                low = float(match.group(1))
                high = float(match.group(2)) if match.group(2) else low
                # 转换为元
                low = int(low * 10000)
                high = int(high * 10000)
                return f"{low}-{high}"
        
        # 处理"千"单位
        elif '千' in salary_clean:
            match = re.search(r'([\d\.]+)[-~]?([\d\.]+)?千', salary_clean)
            if match:
                low = float(match.group(1))
                high = float(match.group(2)) if match.group(2) else low
                # 转换为元
                low = int(low * 1000)
                high = int(high * 1000)
                return f"{low}-{high}"
        
        # 处理直接以元为单位的格式
        else:
            match = re.search(r'(\d+)[-~]?(\d+)?', salary_clean.replace('元', ''))
            if match:
                low = match.group(1)
                high = match.group(2) if match.group(2) else low
                # 转换为数字
                try:
                    low = int(low)
                    high = int(high)
                    return f"{low}-{high}"
                except:
                    return np.nan
        
        return np.nan
    
    # 清理学历字段
    def clean_education(edu):
        if pd.isna(edu):
            return edu
        edu = str(edu)
        if '本科' in edu:
            return '本科'
        elif '硕士' in edu:
            return '硕士'
        elif '博士' in edu:
            return '博士'
        elif '大专' in edu:
            return '大专'
        elif '中专' in edu or '中技' in edu:
            return '中专/中技'
        elif '学历不限' in edu or '无' in edu:
            return '不限'
        else:
            return edu
    
    # 清理经验字段
    def clean_experience(exp):
        if pd.isna(exp):
            return exp
        exp = str(exp)
        if '无经验' in exp or '不限' in exp:
            return '无经验'
        elif '1-3年' in exp:
            return '1-3年'
        elif '3-5年' in exp:
            return '3-5年'
        elif '5-10年' in exp or '5年以上' in exp:
            return '5-10年'
        elif '10年以上' in exp:
            return '10年以上'
        elif '1年以下' in exp:
            return '1年以下'
        else:
            return exp
    
    # 清理公司规模字段
    def clean_company_size(size):
        if pd.isna(size):
            return size
        size = str(size)
        if '10000人以上' in size:
            return '10000人以上'
        elif '1000-9999人' in size:
            return '1000-9999人'
        elif '500-999人' in size:
            return '500-999人'
        elif '100-299人' in size:
            return '100-299人'
        elif '20-99人' in size:
            return '20-99人'
        elif '20人以下' in size:
            return '20人以下'
        else:
            return size
    
    # 应用清洗函数
    df['薪资'] = df['薪资'].apply(clean_salary)
    df['学历'] = df['学历'].apply(clean_education)
    df['经验要求'] = df['经验要求'].apply(clean_experience)
    df['公司规模'] = df['公司规模'].apply(clean_company_size)
    
    # 3. 分类处理
    # 根据关键词对职位进行分类
    def classify_job(keyword):
        keyword = str(keyword)
        if 'python' in keyword.lower():
            return 'Python开发'
        elif 'java' in keyword.lower():
            return 'Java开发'
        elif '前端' in keyword:
            return '前端开发'
        elif '后端' in keyword:
            return '后端开发'
        elif '算法' in keyword:
            return '算法工程师'
        elif '大数据' in keyword:
            return '大数据工程师'
        elif '人工智能' in keyword:
            return '人工智能工程师'
        elif '云计算' in keyword:
            return '云计算工程师'
        elif '网络安全' in keyword or '安全' in keyword:
            return '网络安全工程师'
        elif '数据分析师' in keyword:
            return '数据分析师'
        elif '产品经理' in keyword:
            return '产品经理'
        elif '运维' in keyword:
            return '运维工程师'
        elif '系统架构' in keyword:
            return '系统架构师'
        elif '测试' in keyword:
            return '测试工程师'
        else:
            return '其他计算机职位'
    
    df['职位分类'] = df['关键词'].apply(classify_job)
    
    # 4. 地址标准化 - 根据公司名称提取省份或城市
    def extract_location_from_company(company_name):
        if pd.isna(company_name):
            return '西安'
        
        company_name = str(company_name)
        
        # 常见城市列表
        cities = {
            # 陕西省
            '西安': ['西安', '西安市'],
            '咸阳': ['咸阳', '咸阳市'],
            '宝鸡': ['宝鸡', '宝鸡市'],
            '渭南': ['渭南', '渭南市'],
            '铜川': ['铜川', '铜川市'],
            '延安': ['延安', '延安市'],
            '榆林': ['榆林', '榆林市'],
            '汉中': ['汉中', '汉中市'],
            '安康': ['安康', '安康市'],
            '商洛': ['商洛', '商洛市'],
            
            # 其他常见省份/城市
            '北京': ['北京'],
            '上海': ['上海'],
            '广州': ['广州'],
            '深圳': ['深圳'],
            '杭州': ['杭州'],
            '南京': ['南京'],
            '成都': ['成都'],
            '武汉': ['武汉'],
            '重庆': ['重庆'],
            '天津': ['天津'],
            '青岛': ['青岛'],
            '大连': ['大连'],
            '厦门': ['厦门'],
            '苏州': ['苏州'],
            '无锡': ['无锡'],
            '郑州': ['郑州'],
            '长沙': ['长沙'],
            '济南': ['济南'],
            '合肥': ['合肥'],
            '福州': ['福州'],
            '南昌': ['南昌'],
            '石家庄': ['石家庄'],
            '太原': ['太原'],
            '呼和浩特': ['呼和浩特'],
            '沈阳': ['沈阳'],
            '长春': ['长春'],
            '哈尔滨': ['哈尔滨'],
            '南宁': ['南宁'],
            '海口': ['海口'],
            '贵阳': ['贵阳'],
            '昆明': ['昆明'],
            '拉萨': ['拉萨'],
            '兰州': ['兰州'],
            '银川': ['银川'],
            '西宁': ['西宁'],
            '乌鲁木齐': ['乌鲁木齐']
        }
        
        # 遍历城市列表，检查公司名称中是否包含城市关键词
        for city, keywords in cities.items():
            for keyword in keywords:
                if keyword in company_name:
                    return city
        
        # 如果没找到匹配的城市，默认返回西安
        return '西安'
    
    df['地区'] = df['公司名称'].apply(extract_location_from_company)
    
    # 5. 重新排序列
    columns_order = ['职位分类', '关键词', '工作名称', '公司名称', '地区', '学历', '薪资', '经验要求', 
                     '公司性质', '公司规模', '工作类型']
    df = df[columns_order]
    
    # 6. 保存清洗后的数据
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    # 7. 输出统计信息
    print("\n数据清洗完成！")
    print(f"清洗后数据行数: {len(df)}")
    print(f"职位分类统计:")
    print(df['职位分类'].value_counts())
    print(f"\n地区分布统计:")
    print(df['地区'].value_counts())
    print(f"\n数据已保存到: {output_file}")
    
    return df

# 执行数据清洗
if __name__ == "__main__":
    input_file = "zhilian_computer_jobs.csv"
    output_file = "cleaned_zhilian_jobs.csv"
    cleaned_data = clean_zhilian_data(input_file, output_file)