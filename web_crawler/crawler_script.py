import re
import requests
import time
import csv
import sys

# 配置标准输出编码为UTF-8
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception as e:
    print(f"设置stdout编码时出错: {e}")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    'Cookie': 'x-zp-client-id=728d6122-1014-4446-95b6-8631411f9557; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkchannel=%7B%22prop%22%3A%7B%22_sa_channel_landing_url%22%3A%22%22%7D%7D; Hm_lvt_7fa4effa4233f03d11c7e2c710749600=1764079430; HMACCOUNT=6B601562DE21CB95; x-zp-device-sn=cd45ea586b2c4a38824cbe860bb89480; LastCity=%E7%A6%8F%E5%B7%9E; LastCity%5Fid=681; zp_passport_deepknow_sessionId=408b22aas89e0c48b7a9882526c5bf528ae3; at=3481f17ee81c44a5b394e7d87ce16eca; rt=19647502cb9145d59a9dff91ead3e1e9; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221235544394%22%2C%22first_id%22%3A%2219abb53e006651-054fa4fa4fa4fa4-26061b51-1327104-19abb53e00791d%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTlhYmI1M2UwMDY2NTEtMDU0ZmE0ZmE0ZmE0ZmE0LTI2MDYxYjUxLTEzMjcxMDQtMTlhYmI1M2UwMDc5MWQiLCIkaWRlbnRpdHlfbG9naW5faWQiOiIxMjM1NTQ0Mzk0In0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%221235544394%22%7D%2C%22%24device_id%22%3A%2219abb53e006651-054fa4fa4fa4fa4-26061b51-1327104-19abb53e00791d%22%7D; locationInfo_search={%22code%22:%22%22}; selectCity_search=489; Hm_lpvt_7fa4effa4233f03d11c7e2c710749600=1764080003'
}

# 定义20个计算机相关专业关键词列表
keywords = [
    '计算机',
    '人工智能',
    '前端',
    '后端',
    'python',
    'java',
    '数据分析师',
    '算法工程师',
    '大数据工程师',
    '云计算工程师',
    '网络安全工程师',
    '数据库管理员',
    '系统架构师',
    '移动开发工程师',
    'UI设计师',
    '产品经理',
    '运维工程师',
    '测试工程师',
    '机器学习工程师',
    '区块链工程师'
]

# 打开CSV文件准备写入数据
with open('zhilian_computer_jobs.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    writer = csv.writer(csvfile)
    # 写入表头
    writer.writerow(['关键词', '工作名称', '公司名称', '地区', '学历', '薪资', '经验要求', '公司性质', '公司规模', '工作类型'])

    for keyword in keywords:
        print(f"正在搜索关键词: {keyword}")
        found_any_data = False  # 标记是否找到了数据
        
        for page in range(1, 20):  # 每个关键词爬取10页
            # 按照你提供的URL格式来构造
            url = f"https://sou.zhaopin.com/?jl=854&kw={keyword}&p={page}"
            print(f"正在爬取关键词'{keyword}'第 {page} 页...")
            time.sleep(1)
            # 停顿1秒
            
            try:
                response = requests.get(url, headers=headers).text
                
                # 先检查能匹配到多少个职位
                names = re.findall(r'"matchInfo":.*?"name":"(.*?)"', response)
                companyNames = re.findall(r'"companyName":"(.*?)"', response)
                cityDistricts = re.findall(r'"cityDistrict":"(.*?)"', response)
                educations = re.findall(r'"education":"(.*?)"', response)
                salary60s = re.findall(r'"salary60":"(.*?)"', response)
                workingExps = re.findall(r'"workingExp":"(.*?)"', response)
                properties = re.findall(r'"property":"(.*?)"', response)
                companySizes = re.findall(r'"companySize":"(.*?)"', response)
                workTypes = re.findall(r'"workType":"(.*?)"', response)
                
                # 输出各字段匹配到的数量
                print(f"关键词'{keyword}'第{page}页匹配到数据数量: 名称({len(names)}), 公司({len(companyNames)}), 地区({len(cityDistricts)}), "
                      f"学历({len(educations)}), 薪资({len(salary60s)}), 经验({len(workingExps)}), "
                      f"公司性质({len(properties)}), 公司规模({len(companySizes)}), 工作类型({len(workTypes)})")
                
                # 检查是否找到了数据
                if len(names) > 0:
                    found_any_data = True
                elif page == 1:
                    # 如果第一页就没有数据，跳出循环，尝试下一个关键词
                    print(f"关键词'{keyword}'第一页未找到数据，跳转到下一个关键词")
                    break
                
                # 以最少的字段数量为准，避免索引越界
                min_count = min(len(names), len(companyNames), len(cityDistricts), len(educations),
                               len(salary60s), len(workingExps), len(properties), len(companySizes),
                               len(workTypes))
                
                # 写入每一行数据
                for i in range(min_count):
                    # 添加关键词作为第一列
                    row = [keyword]
                    # 添加其他字段数据
                    row_data = [names[i], companyNames[i], cityDistricts[i], educations[i],
                               salary60s[i], workingExps[i], properties[i], companySizes[i],
                               workTypes[i]]
                    
                    # 清理数据中的特殊字符
                    clean_data = []
                    for item in row_data:
                        # 处理可能存在的转义字符和特殊符号
                        if isinstance(item, str):
                            # 替换常见的转义字符
                            item = item.replace('\\n', ' ').replace('\\r', ' ').replace('\\t', ' ')
                            # 去除首尾空白字符
                            item = item.strip()
                        clean_data.append(item)
                    
                    # 合并关键词和清理后的数据
                    full_row = [row[0]] + clean_data
                    writer.writerow(full_row)
                    
                print(f"关键词'{keyword}'第 {page} 页数据写入完成，共写入 {min_count} 条数据")
                
                # 如果当前页没有数据，跳出循环
                if min_count == 0 and page > 1:
                    break
                    
            except Exception as e:
                print(f"处理关键词'{keyword}'第 {page} 页时出现错误: {e}")
                continue
        
        if not found_any_data:
            print(f"关键词'{keyword}'未找到任何数据")

print("所有数据爬取完成！")
input("按Enter键退出...")