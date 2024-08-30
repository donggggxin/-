import re

def reg_search(text, regex_list):
    results = []
    # 遍历正则表达式字典列表
    for regex_dict in regex_list:
        result_dict = {}
        # 遍历每个字典中的键值对
        for key, pattern in regex_dict.items():
            # 根据键值对构建正则表达式
            compiled_pattern = re.compile(pattern)
            # 在文本中搜索匹配项
            matches = compiled_pattern.findall(text)
            if matches:
                # 如果是日期匹配项，则进行格式化
                if key == '换股期限':
                    formatted_dates = [f"{year}-{month.zfill(2)}-{day.zfill(2)}" for year, month, day in matches]
                    result_dict[key] = formatted_dates
                elif key == '标的证券':
                    # 股票代码应为单个字符串
                    result_dict[key] = matches[0]
                else:
                    # 如果找到匹配项，添加到结果字典中
                    result_dict[key] = matches
            else:
                # 如果没有找到匹配项，添加None或空列表
                result_dict[key] = None
        # 将结果字典添加到结果列表中
        results.append(result_dict)
    return results

# 示例文本
text = '''
标的证券：本期发行的证券为可交换为发行人所持中国长江电力股份
有限公司股票（股票代码：600900.SH，股票简称：长江电力）的可交换公司债券。
换股期限：本期可交换公司债券换股期限自可交换公司债券发行结束
之日起满 12 个月后的第一个交易日起至可交换债券到期日止，即 2023 年 6 月 2
日至 2027 年 6 月 1 日止。
'''

# 正则表达式列表
regex_list = [
    {
        '标的证券': r'股票代码：(\d{6}\.\w+)',
        '换股期限': r'(\d{4})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日'
    }
]

# 调用函数并打印结果
result = reg_search(text, regex_list)
print(result)
