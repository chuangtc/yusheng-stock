import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import sys

days=365
stockid=2330
url=f'https://goodinfo.tw/tw/StockDetail.asp?STOCK_ID={stockid}'
Refererurl = f'https://goodinfo.tw/StockInfo/ShowBuySaleChart.asp?STOCK_ID={stockid}&CHT_CAT=DATE'
headers={
 'Referer':Refererurl,
 'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
}
res=requests.get(url,headers=headers)
#res=requests.get(url,headers=headers)

res.encoding = 'utf8'
soup = bs(res.text,'lxml')
print(soup.title.text.split(' ')[0])


# tr = soup.select('.p4_1 tr')
# df0 = pd.DataFrame(list(map(lambda tr :list(map(lambda td:td.text.strip(),tr.select('td'))),tr)))
# df0.columns=columnname
# df0 = df0[ (df0['期別']!='期別') & (df0['期別'].str.startswith('買進')==False)]
# df0['期別']=("2022/"+df0['期別']).str.replace("/",'-')
# df0 = df0[~df0['成交量(張)'].isin([""])]
# df0=df0.apply(pd.to_numeric, errors='ignore')
# df= df0.set_index(['期別'])
# #df= df.sort_index(ascending=False)
# print(df.head(20))