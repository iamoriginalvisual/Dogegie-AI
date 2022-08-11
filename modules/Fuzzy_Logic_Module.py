import numpy as np

#fuzzification open left
def open_left(x,alpha,beta):
    if x<alpha:
        return 1 
    if alpha<x and x<=beta:
        return (beta-x)/(beta-alpha)
    else:
        return 0 

#fuzzification open right
def open_right(x, alpha, beta):
    if x<alpha:
        return 0
    if alpha<x and x<=beta:
        return (x-alpha)/(beta-alpha)
    else:
        return 1

#fuzzification open left
def triangular(x,a,b,c):
    return max(min((x-a)/(b-a), (c-x)/(c-b)),0)

#fuzzy partition
def a_partition(x):
    low = med = high = 0;

    if x>0 and x<25:
        low = open_left(x,25,50)
    if x>20 and x<80:   
        med = triangular(x, 20, 50, 80)
    if x>75 and x<100:
        high = open_right(x, 75, 80)

    return low,med,high

def b_partition(x):
    low = high = 0;
    if x>0 and x<55:
        high = open_left(x,45,55)
    if x<45 and x<100:
        low = open_right(x, 45,55)
    if x<0:
        high = 1
    if x>100:
        low = 1

    return low,high 

def f_partition(x):
    bn = bl = hl = sl = sn = 0;

    if x>0 and  x<25:
        bn = open_left(x,20,25)
    if x>20 and x<50:   
        bl = triangular(x, 20, 25, 50)
    if x>25 and x<75:
        hl = triangular(x, 25, 50, 75)
    if x>50 and x<80:
        sl = triangular(x, 50, 75, 80)
    if x>75 and x<100:
        sn = open_right(x, 75, 80)

    return bn, bl, hl, sl, sn;

#compare rules
def compare(a,b,c,d):
    tc = 0

    arr  = np.array([a,b,c,d])
    values = np.unravel_index(np.where(arr!=0, arr, arr.max()+1).argmin(), arr.shape)

    if len(values) != 0:
        tc = min(values)
    
    return tc  


#rules
def rule(r_lw,r_md,r_hi,s_lw,s_md,s_hi,m_lw,m_hi,p_lw,p_hi):

    #if MACD HIGH and RSI LOW and SO LOW and PRED HIGH THEN BUY NOW
    bn_a = min(m_hi,r_lw,s_lw,p_hi)
    #if MACD HIGH and RSI MED and SO MED and PRED HIGH THEN BUY NOW
    bn_b = min(m_hi,r_md,s_md,p_hi)
    #if MACD HIGH and RSI LOW and SO MED and PRED LOW THEN BUY NOW
    bn_c = min(m_hi,r_lw,s_md,p_lw)
    #if MACD HIGH and RSI MED and SO LOW and PRED LOW THEN BUY NOW
    bn_d = min(m_hi,r_md,s_lw,p_lw)
    #compare rules

    bn = compare(bn_a,bn_b,bn_c,bn_d)

    #if MACD HIGH and RSI LOW and SO LOW and PRED LOW THEN BUY LATER
    bl_a = min(m_hi,r_lw,s_lw,p_lw)
    #if MACD HIGH and RSI MED and SO LOW and PRED HIGH THEN BUY LATER
    bl_b = min(m_hi,r_md,s_lw,p_hi)
    #if MACD HIGH and RSI LOW and SO MED and PRED HIGH THEN BUY LATER 
    bl_c = min(m_hi,r_lw,s_md,p_hi)

    bl = compare(bl_a,bl_b,bl_c,0)

    #if MACD HIGH and RSI MED and SO MED and PRED LOW THEN HOLD
    hl_a = min(m_hi,r_md,s_md,p_lw)
    #if MACD LOW and RSI MED and SO MED and PRED HIGH THEN HOLD
    hl_b = min(m_lw,r_md,s_md,p_hi)

    hl = compare(hl_a,hl_b,0,0)

    #if MACD LOW and RSI HIGH and SO HIGH and PRED LOW THEN SELL LATER
    sl_a = min(m_hi,r_hi,s_hi,p_lw)
    #if MACD LOW and RSI MED and SO HIGH and PRED HIGH THEN SELL LATER
    sl_b = min(m_lw,r_md,s_hi,p_hi)
    #if MACD LOW and RSI HIGH and SO MED and PRED HIGH THEN SELL LATER
    sl_c = min(m_lw,r_hi,s_md,p_hi)

    sl = compare(sl_a,sl_b,sl_c,0)

    #if MACD LOW and RSI HIGH and SO HIGH and PRED HIGH THEN SELL NOW
    sn_a = min(m_lw,r_hi,s_hi,p_hi)    
    #if MACD LOW and RSI MED and SO MED and PRED LOW THEN SELL NOW    
    sn_b = min(m_lw,r_md,s_md,p_lw)
    #if MACD LOW and RSI MED and SO HIGH and PRED LOW THEN SELL NOW
    sn_c = min(m_lw,r_md,s_hi,p_lw)
    #if MACD LOW and RSI HIGH and SO MED and PRED LOW THEN SELL NOW
    sn_d = min(m_lw,r_hi,s_md,p_lw)

    sn = compare(sn_a,sn_b,sn_c,sn_d)

    return bn,bl,hl,sl,sn
  

#defuzzification
def area_tr(mu, a, b, c):
    x1 = mu*(b-a) + a
    x2 = c - mu*(c-b)
    d1 = (c-a)
    d2 = x2-x1
    a = (1/2)*mu*(d1+d2)
    return a

def area_ol(mu, alpha, beta):
    x_ol = beta -mu*(beta-alpha)
    return 1/2*mu*(beta+x_ol),beta/2

def area_or(mu, alpha, beta):
    x_or = (beta-alpha)*mu+alpha
    a_or = (1/2)*mu*(100-alpha)+(100-x_or)
    return a_or, (100-alpha)/2+alpha

def defuzzify(bn,bl,hl,sl,sn):
    ar_bn = ar_bl = ar_hl = ar_sl = ar_sn = c_bn = c_bl = c_hl = c_sl = c_sn = 0

    if sn != 0:
        ar_sn, c_sn = area_or(sn,75,80)
    if sl != 0:
        ar_sl = area_tr(sl,50,75,80)
        c_sl = 75
    if hl != 0:
        ar_hl = area_tr(hl,25,50,75)
        c_hl = 50
    if bl != 0:
        ar_bl = area_tr(bl,20,25,50)
        c_bl = 25
    if bn !=0:
        ar_bn,c_bn = area_ol(bn,20,25)
    
    numerator = ar_sn*c_sn + ar_sl*c_sl + ar_hl*c_hl + ar_bl*c_bl + ar_bn*c_bn
    denominator = ar_sn + ar_sl + ar_hl + ar_bl + ar_bn
    
    if denominator == 0:
        print("No rule exists to give result")
        return 0
    else:
        crisp_output = numerator/denominator
        return crisp_output