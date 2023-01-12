import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import sys

days=365
stockid=2330
url='https://goodinfo.tw/StockInfo/ShowBuySaleChart.asp'
payload={
    'STOCK_ID':f'{stockid}',
    'CHT_CAT':'DATE',
    'SHEET':'買賣張數',
    'STEP':'DATA',
    'PERIOD':days
}
Refererurl = f'https://goodinfo.tw/StockInfo/ShowBuySaleChart.asp?STOCK_ID={stockid}&CHT_CAT=DATE'
headers={
 'Referer':Refererurl,
 'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
}
columnname=['期別','成交','漲跌','漲跌(%)','成交量(張)','外資買進','外資賣出','外資買賣超',
'外資持有張數','外資持股比率','投信買進','投信賣出','投信買賣超','自營商買進',
'自營商賣出','自營商買賣超','法人合計買進','法人合計賣出','法人合計買賣超']
res=requests.get(url,headers=headers,params=payload)
res.encoding = 'utf8'
soup = bs(res.text,'lxml')
tr = soup.select('.p4_1 tr')
df0 = pd.DataFrame(list(map(lambda tr :list(map(lambda td:td.text.strip(),tr.select('td'))),tr)))
df0.columns=columnname
df0 = df0[ (df0['期別']!='期別') & (df0['期別'].str.startswith('買進')==False)]
df0['期別']=("2022/"+df0['期別']).str.replace("/",'-')
df0 = df0[~df0['成交量(張)'].isin([""])]
df0=df0.apply(pd.to_numeric, errors='ignore')
df= df0.set_index(['期別'])
#df= df.sort_index(ascending=False)
print(df.head(20))