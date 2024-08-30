import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# 初始化 WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# 打开目标网页
url = 'https://iftp.chinamoney.com.cn/english/bdInfo/'
driver.get(url)

# 选择 Bond Type 为 Treasury Bond
bond_type_select = Select(driver.find_element(By.ID, "Bond_Type_select"))
bond_type_select.select_by_value("100001")  # 100001 是 Treasury Bond 的值

# 选择 Issue Year 为 2023
issue_year_select = Select(driver.find_element(By.ID, "Issue_Year_select"))
issue_year_select.select_by_value("2023")

# 点击 Search 按钮
search_button = driver.find_element(By.XPATH, '//a[@onclick="searchData()"]')
search_button.click()

# 等待页面加载完成
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//ul[@id="pagi-bond-market"]//span[@class="page-total"]'))
)

# 获取表格内容的函数
def get_table_data():
    rows = driver.find_elements(By.XPATH, '//div[@id="sheet-bond-market"]//tbody/tr')
    page_data = []
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, 'td')
        row_data = [cell.text.strip() for cell in cells]
        if all(row_data):  # 确保行中所有字段都不为空
            page_data.append(row_data)
    return page_data

# 获取总页数
total_pages = int(driver.find_element(By.XPATH, '//ul[@id="pagi-bond-market"]//span[@class="page-total"]').text)
all_data = []

# 循环遍历所有页面并抓取数据
for page in range(total_pages):
    # 抓取当前页面的数据
    current_page_data = get_table_data()
    if current_page_data:
        all_data.extend(current_page_data[:len(current_page_data)//2])
    else:
        print("No data found on this page, exiting loop.")
        break

    # 尝试点击“下一页”按钮
    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//li[@class="page-btn page-next"]/a'))
        )
        next_button.click()
        WebDriverWait(driver, 10).until(
            EC.staleness_of(next_button)  # 等待当前页面完全消失
        )
    except Exception as e:
        print(f"No more pages or an error occurred: {e}")
        break

# 将数据转换为DataFrame
df = pd.DataFrame(all_data, columns=["ISIN", "Bond Code", "Issuer", "Bond Type", "Issue Date", "Latest Rating"])

# 去除空行
df = df.dropna(how='all')
#
# # 去除重复数据
# df.drop_duplicates(inplace=True)

# 保存为CSV文件
csv_file_name = "bond_data_cleaned1.csv"
df.to_csv(csv_file_name, index=False, encoding='utf-8-sig')

# 关闭浏览器
driver.quit()

print(f"Data has been saved to {csv_file_name}")
