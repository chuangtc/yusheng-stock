import os
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from datetime import datetime,date 

from flask import Flask, request

from pydantic import BaseModel

days=365

columnname=['期別','成交','漲跌','漲跌(%)','成交量(張)','外資買進','外資賣出','外資買賣超',
'外資持有張數','外資持股比率','投信買進','投信賣出','投信買賣超','自營商買進',
'自營商賣出','自營商買賣超','法人合計買進','法人合計賣出','法人合計買賣超']

app = Flask(__name__)


@app.route("/")
def hello_world():
    name = os.environ.get("NAME", "World")
    return "Hello {}!".format(name)


@app.route("/goodinfo")
def goodinfo():
    stockid=request.args.get('stockid',default = '2330', type = str)
    #stockid='2330'
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
    res=requests.get(url,headers=headers,params=payload)
    res.encoding = 'utf8'
    # soup = bs(res.text,'lxml')
    soup = bs(res.text,'html.parser')    
    tr = soup.select('.p4_1 tr')
    df0 = pd.DataFrame(list(map(lambda tr :list(map(lambda td:td.text.strip(),tr.select('td'))),tr)))
    df0.columns=columnname
    df0 = df0[ (df0['期別']!='期別') & (df0['期別'].str.startswith('買進')==False)]
    
    today=date.today()
    year=today.year
    today_str_date2 = f"{year}/{today.month}/{today.day}"
    
    data_str_date1 = f"{year}/{df0['期別'].values[0]}"

    # convert string to date object
    d1 = datetime.strptime(data_str_date1, "%Y/%m/%d")
    d2 = datetime.strptime(today_str_date2, "%Y/%m/%d")

    # difference between dates in timedelta
    delta = d2 - d1
    if((delta.days>0 )& (delta.days<7)):
        data_year=f"{year}"
        data_prev_year=f"{year-1}"
    elif(today.month==1):
        data_year=f"{year-1}"
        data_prev_year=f"{year-2}"        

    prev_month=df0['期別'].values[0][0:2]
    prev_year_bool_ind=False
    for i in range(len(df0.index.values)):
        if((prev_month=="01") & (df0['期別'].values[i][0:2]=="12")):
           prev_year_bool_ind=True 
        prev_month = df0['期別'].values[i][0:2]

        if(prev_year_bool_ind==False):
            df0['期別'].values[i]=(data_year+"/"+df0['期別'].values[i]).replace("/",'-')
        else:
            df0['期別'].values[i]=(data_prev_year+"/"+df0['期別'].values[i]).replace("/",'-')
        
        
        
    df0 = df0[~df0['成交量(張)'].isin([""])]
    df0=df0.apply(pd.to_numeric, errors='ignore')
    df= df0.set_index(['期別'])
    #df= df.sort_index(ascending=False)

    title = "2330 台積電" 
    url=f'https://goodinfo.tw/tw/StockDetail.asp?STOCK_ID={stockid}'
    res=requests.get(url,headers=headers)
    res.encoding = 'utf8'
    # soup = bs(res.text,'lxml')  
    soup = bs(res.text,'html.parser')    
    title = soup.title.text.split(' ')[0]

    html =f"<h1>{title}</h1>"
    html+="  <div style='text_align:right'>"
    html+="    <form action='/goodinfo'>"
    html+="      <lable for=stockid>Stockid:</lable>"
    html+="      <input type='text' id='stockid' name='stockid'><br/>"
    html+="      <input type=submit value='Submit'>"
    html+="    </form>"
    html+="  </div>"
    html+="<table border='1'>"
    html+="<tr>"
    html+=f"<td>期別</td>"
    for i in range(len(columnname)-1):
        html+=f"<td>{list(df.columns.values)[i]}</td>"
    html+="</tr>"
    for i in range(len(df.index)):
        html+="<tr>"
        html+=f"<td>{df.index[i]}</td>"
        for j in range(len(columnname)-1):
            html+=f"<td>{df.iat[i, j]}</td>"
        html+="</tr>"
        
    html+="</table>"
    #print(df.head(20))
    #print( f"{html}" )
    return f"{html}"


if __name__ == "__main__":
    #app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

    goodinfo()    