import pandas as pd
import numpy as np
import modules.connect as cn
import modules.preprocessing as pre
import modules.Regression_Module as rm
import modules.Analytics_Module as am
import modules.Fuzzy_Logic_Module as fz
from datetime import datetime as dt

def interpret(x):
    
    pred = cn.get_all('*','doge_pred')
    min_p = pred
    max_p = pred
    min_p = min_p[pred.Predicted_Price == min_p.Predicted_Price.min()]

    max_p = max_p[pred.Predicted_Price == max_p.Predicted_Price.min()]

    bn, bl, hl, sl, sn = fz.f_partition(x)
    arr = np.array([bn, bl, hl, sl, sn])
 
    tc = max(arr)

    res = [i for i, j in enumerate(arr) if j == tc]
 
    check = res[0]

    if check == 0:
        dscn = 'BUY NOW'
    elif check == 1:
        date = min_p.iloc[0]['Date']
        date = pd.to_datetime(date).strftime("%B %d, %Y")
        dscn = 'BUY LATER on '+date
    elif check == 2:
        dscn = 'HOLD'
    elif check == 3:
        date = max_p.iloc[0]['Date']
        date = pd.to_datetime(date).strftime("%B %d, %Y")
        dscn = 'SELL LATER on '+date
    elif check == 4:
        dscn = 'SELL NOW'
    else:
        dscn = 'NO available decision'
    
    return dscn

def doge_decide():
    data,r_cur,r_opn,r_high,r_low,h_lag,l_lag = pre.get_dataset()

    avg = rm.get_reg(data,r_cur,r_opn,r_high,r_low,h_lag,l_lag)

    macd,rsi,so = am.start_analytics(data,r_cur,r_high,r_low)
    
    print("\nMACD: ",macd,"\nRSI: ",rsi,"\nSO: ",so,"\nPrediciton Average",avg)
    r_lw,r_md,r_hi = fz.a_partition(rsi)
    s_lw,s_md,s_hi = fz.a_partition(so)
    m_lw,m_hi = fz.b_partition(macd)
    p_lw,p_hi = fz.b_partition(avg)
    print("\nFuzzy Values:\nRSI:",r_lw,r_md,r_hi,"\nSO: ",s_lw,s_md,s_hi,"\nMACD: ",m_lw,m_hi,"\nPrediciton Average",p_lw,p_hi)
    bn,bl,hl,sl,sn = fz.rule(r_lw,r_md,r_hi,s_lw,s_md,s_hi,m_lw,m_hi,p_lw,p_hi)
    print("\nRules: ",bn,bl,hl,sl,sn)
    crisp_f = fz.defuzzify(bn,bl,hl,sl,sn)
    print("\nCrisp Value: ",crisp_f)
    des = interpret(crisp_f)
    return macd,rsi,so,avg,des


