from selenium import webdriver
import requests
import time
import json
import csv
import re

driver = webdriver.Chrome()
time.sleep(2)
driver.get('https://www.macromicro.me/charts/39415/global-coal-prices')
time.sleep(2)
#cookies
cookie_list = driver.get_cookies()
c = 'PHPSESSID=' + cookie_list[9]['value']
#取得token
p = re.compile(r'<p data-stk="(.*?)">')
B = p.findall(driver.page_source)
driver.close()
#'Accept-Encoding': 'gzip, deflate, br',
request_headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding':'utf-8',
    'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Authorization': 'Bearer ' + B[0],
    'Cookie': c,
    'Host': 'www.macromicro.me',
    'Referer': 'https://www.macromicro.me/charts/39415/global-coal-prices',
    'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}
url = 'https://www.macromicro.me/charts/data/39415'
r = requests.get(url, headers=request_headers)
print(r.text)

with open('data.json','w+') as f:
    f.write(r.text)


#讀取json檔
with open('data.json') as f:
    data = json.load(f)
    #'ICE-Newcastle煤 (L)'
    n1 = (data['data']['c:39415']['s'][0])
    #'ICE-Rotterdam煤 (L)'
    n2 = (data['data']['c:39415']['s'][1])
    #'中國-動力煤期貨 (R)'
    n3 = (data['data']['c:39415']['s'][2])
    #'中國-焦煤期貨 (R)'
    n4 = (data['data']['c:39415']['s'][3])

#取得最大值
m = max([len(n1),len(n2),len(n3),len(n4)])

#寫入csv
with open('output.csv', 'w+', newline='',encoding='utf_8_sig') as csvfile:
    # 以逗點分隔欄位，建立 CSV 檔寫入器
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['時間', 'ICE-Newcastle煤 (L)', '時間','ICE-Rotterdam煤 (L)','時間','中國-動力煤期貨 (R)','時間','中國-焦煤期貨 (R)'])
    for i in range(m):
        if i > len(n1)-1:
            d1 = ''
            v1 = ''
        else:
            d1 = n1[i][0]
            v1 = n1[i][1]
            
        if i > len(n2)-1:
            d2 = ''
            v2 = ''
        else:
            d2 = n2[i][0]
            v2 = n2[i][1]
            
        if i > len(n3)-1:
            d3 = ''
            v3 = ''
        else:
            d3 = n3[i][0]
            v3 = n3[i][1]
        if i > len(n4)-1:
            d4 = ''
            v4 = ''
        else:
            d4 = n4[i][0]
            v4 = n4[i][1]
            
        d = [d1,v1,d2,v2,d3,v3,d4,v4]
        writer.writerow(d)