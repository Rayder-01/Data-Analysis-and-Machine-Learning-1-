import datetime
import pandas as pd

import mplfinance as mpl

import yfinance as yf

#設定爬蟲時間
start = datetime.datetime.now() - datetime.timedelta(days=360)
end = datetime.date.today()

#設定爬蟲股票代號
sid = '2330'  

#取得股票資料
stock_yf = yf.download(sid+'.TW', start, end)
print(stock_yf.tail(10))

# ==============================  周K線圖  ======================================

#1:必須將索引值轉換成pandas默認的類型
stock_yf.index = pd.to_datetime(stock_yf.index)

#2:進行頻率轉換日K---周K,首先讓所有指標都為最後一天的價格
# 周'W',月'M',季度'Q'
day = 'W'
period_week_data = stock_yf.resample(day).last()

#分別對於開盤、收盤、最高價、最低價進行處理
period_week_data['Open'] = stock_yf['Open'].resample(day).first()
#處理最高和最低價       
period_week_data['High'] = stock_yf['High'].resample(day).max()
#最低價
period_week_data['Low'] = stock_yf['Low'].resample(day).min()
#收盤價
period_week_data['Close'] = stock_yf['Close'].resample(day).min()
#成交量 這一周每天成交量的和
period_week_data['Volume'] = stock_yf['Volume'].resample(day).sum()

#其中存在的缺失值
period_week_data.dropna(inplace=True)

mpl.plot(period_week_data, type='candle', style='charles',
        title='',
        ylabel='',
        ylabel_lower='',
        volume=True,
        figscale=1,
        figratio=(12,6)
        )
mpl.show()
