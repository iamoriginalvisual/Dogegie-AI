import pandas as pd
import os
import numpy as np
import modules.connect as cn
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score,mean_squared_error
import statsmodels.api as sm
from datetime import datetime
from datetime import timedelta

def get_analysis(X,Y,mdl):

    date = datetime.now().strftime("%d/%m/%Y")

    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size = 0.2,train_size = 0.8 ,shuffle=False)

    analysis = linear_model.LinearRegression()
    analysis.fit(x_train,y_train)
    y_prediction =  analysis.predict(x_test)

    act_pred = pd.DataFrame()
    act_pred['Actual'] = y_test
    act_pred['Prediction'] = y_prediction


    """
    plt.plot(act_pred.index, y_test, label = "Actual")
    plt.plot(act_pred.index, y_prediction, label = "Predicted")
    plt.gcf().autofmt_xdate(rotation=90)
    plt.xticks(size=7)
    plt.title(mdl+ ' Actual vs Predicted')
    plt.plot()
    plt.legend()
    
    os.getcwd()
    plt.savefig(mdl+' line plot.png', dpi=350)
    plt.clf()
    """

    score = round(r2_score(y_test,y_prediction)*100,4)
    mse = round(mean_squared_error(y_test,y_prediction),10)
    rmse = round(np.sqrt(mean_squared_error(y_test,y_prediction)),10)
    
    print("\nAnalysis "+mdl+":\nR2-score: ",score,"\nMean Squared Error: ",mse,"\nRoot Mean Squared Error: ",rmse)
    print(act_pred)

    row = (str(date), mdl,str(score), str(mse), str(rmse))
    cn.add_analysis(row)

def Average(lst):
    return sum(lst) / len(lst)

def get_reg(data,r_cur,r_opn,r_high,r_low,h_lag,l_lag):

    data.set_index('Date',inplace=True)
    
    X = data[['Open','High','Low']]
    Y = data['Close']

    X1 = data[['Close', 'Open', 'H-Lag']]
    Y1 = data['High']

    X2 = data[['Close', 'Open', 'L-Lag']]
    Y2 = data['Low']

    regr = linear_model.LinearRegression()
    regr.fit(X,Y)

    reg_high = linear_model.LinearRegression()
    reg_high.fit(X1, Y1)

    reg_low = linear_model.LinearRegression()
    reg_low.fit(X1, Y2)

    cn.delete_row('doge_pred')
    arr = []
    arr_p = pd.DataFrame(columns =['Date','Close Prediction', 'High Prediciton', 'Low Prediction'])
    
    for i in range(0,7,1):

        pred = float(regr.predict([[r_opn,r_high,r_low]]))
        pred_h = float(reg_high.predict([[r_cur,r_opn,h_lag]]))
        pred_l = float(reg_low.predict([[r_cur, r_opn,l_lag]]))

        day = datetime.today() + timedelta(days=i+1)
        date = day.strftime("%d/%m/%Y")
        arr_p = arr_p.append({'Date':date,'Close Prediction':pred,'High Prediciton':pred_h,'Low Prediction':pred_l},ignore_index=True)
        row = (str(date), str(pred), str(pred_h), str(pred_l))
        
        cn.add_pred(row)

        a = ((r_cur - pred)/r_cur)*100 + 50 
        arr.append(float(a))

        r_opn = float(r_cur)
        r_cur = float(pred)
        h_lag = r_high
        l_lag = r_low
        r_high = pred_h
        r_low = pred_l

    arr_p['Date'] = pd.to_datetime(arr_p['Date'])
    arr_p.set_index('Date',inplace=True)
    print("\nPrediction:\n",arr_p)
    get_analysis(X,Y,'Price Prediction Model')
    get_analysis(X1,Y1,'High Prediction Model')
    get_analysis(X2,Y2,'Low Prediction Model')

    return Average(arr)