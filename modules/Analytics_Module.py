import pandas as pd
import numpy as np
import modules.connect as cn
from datetime import datetime

def start_analytics(df,c_price,c_high,c_low):
    df_a = df[['Close']]
    rt_a = pd.DataFrame()
    rt_a['Close'] = c_price
    df_a = pd.concat([df_a,rt_a])
    df_a['Close'] = pd.to_numeric(df_a['Close'])

    ot = pd.DataFrame()
    ot['Close'] = c_price
    ot['High'] = c_high
    ot['Low'] = c_low
    df_b = pd.concat([df,ot], ignore_index=True)

    macd = get_macd(df_a, 26, 12, 9)
    rsi = get_rsi(df_a['Close'], 14)
    so = get_so(df_b)

    return macd,rsi,so

#Moving Average Convergence Divergence (MACD) computation
def get_macd(price,slow, fast, smooth):
    exp1 = price.ewm(span = fast, adjust = False).mean()
    exp2 = price.ewm(span = slow, adjust = False).mean()
    macd = pd.DataFrame(exp1 - exp2).rename(columns = {'Close':'macd'})
    signal = pd.DataFrame(macd.ewm(span = smooth, adjust = False).mean()).rename(columns = {'macd':'signal'})
    hist = pd.DataFrame(((signal['signal'] - macd['macd'])/signal['signal']) * 100 + 50).rename(columns = {0:'hist'})
    return hist.iat[-1,0]

#Relative Strength Index (RSI) computation
def get_rsi (data, time_window):
    diff = data.diff(1).dropna()
    up_chg = 0 * diff
    down_chg = 0 * diff
    up_chg[diff > 0] = diff[ diff>0 ]
    down_chg[diff < 0] = diff[ diff < 0 ]
    up_chg_avg   = up_chg.ewm(com=time_window-1 , min_periods=time_window).mean()
    down_chg_avg = down_chg.ewm(com=time_window-1 , min_periods=time_window).mean()
    
    rs = abs(up_chg_avg/down_chg_avg)
    rsi = 100 - 100/(1+rs)
    rsi = rsi.iat[-1]
    return rsi

    #Stochastic Oscillator computation
def get_so (data):
    data['14-high'] = data['High'].rolling(14).max()
    data['14-low'] = data['Low'].rolling(14).min()
    data['%K'] = (data['Close'] - data['14-low'])*100/(data['14-high'] - data['14-low'])
    data['%D'] = data['%K'].rolling(3).mean()
    so = pd.to_numeric(data.iat[-1,5])*100 
    return so 