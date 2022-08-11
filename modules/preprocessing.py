import modules.connect as cn 
import pandas as pd
from datetime import datetime as dt

def get_dataset():
    today = dt.now().strftime("%d/%m/%Y")

    cols = "day_price,day_open,day_high,day_low"

    histo = cn.get_all('*','doge_histo')
    #print("1. From Histo:\n",histo)
    curr = cn.get_by_date(cols,'doge_realtime',today)

    c_prc = pd.to_numeric(curr.iat[-1,0])
    c_opn = pd.to_numeric(curr.iat[-1,1])
    c_high= pd.to_numeric(curr.iat[-1,2])
    c_low= pd.to_numeric(curr.iat[-1,3])
    #print("\n2. From Realtime: *Last Row or Recent:\n",c_prc,c_opn,c_high,c_low)

    lag = pd.Series(histo.High)
    lag.index = lag.index + 1
    lag = pd.concat([pd.Series(histo.at[0,'High']), lag])
    lag = lag.drop(len(lag)-1)
    h_lag = pd.to_numeric(histo.iloc[-1]['High'])
    histo['H-Lag'] = lag
    #print("\n3. Histo with added High Lag:\n",histo)

    lag = pd.Series(histo.Low)
    lag.index = lag.index + 1
    lag = pd.concat([pd.Series(histo.at[0,'Low']), lag])
    lag = lag.drop(len(lag)-1)
    l_lag = pd.to_numeric(histo.iloc[-1]['Low'])
    histo['L-Lag'] = lag
    #print("\n4. Histo with added Low Lag:\n",histo)
    return histo,c_prc,c_opn,c_high,c_low,h_lag,l_lag


