# ----------------------------------------------------------------------- #
#   DOGEGIE: An Intelligent-Agent for Cryptocurrency Decision Support
#
#   Authors:
#   ARCONADO, Kristine N.                   BERSE, Nikko R.
#   DALAY, Jeremy Tristen A.                FAUSTINO, Kyle C.
# ----------------------------------------------------------------------- #

from tkinter import *
from PIL import Image, ImageTk
from functools import partial
from datetime import date, timedelta
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from elements.tkinter_custom_button import TkinterCustomButton as tkButton
import modules.dogegie as dg
import modules.connect as cn


# Chart and Prediction Window
def new_window(btn):
    app.withdraw()

    global window
    window = Toplevel(app)
    window.title('DOGEGIE')
    window.geometry('1024x661+300+85')
    window['bg'] = "#212528"
    window.resizable(0,0)

    def return_to_main():
        window.destroy()
        app.deiconify()
    window.protocol("WM_DELETE_WINDOW", return_to_main)
    

    # Navbar
    navbar_canvas = Canvas(window, width=1024, height=48, highlightthickness=0, bg="#4A70D2")
    navbar_canvas.place(x=0, y=0)

    # Logo Label
    image1 = Image.open("images/dogegie-label.png")
    image1 = image1.resize((112,33),Image.ANTIALIAS)
    test = ImageTk.PhotoImage(image1, master=navbar_canvas)
    home = Button(navbar_canvas, image=test, command=return_to_main, bd=0, bg="#4A70D2", activebackground="#4A70D2")
    home.image = test
    navbar_canvas.create_window(20,9, window=home, anchor=NW)


    # Content Canvas
    content = Canvas(window, width=968, height=577, highlightthickness=0, bg='#212528')
    content.place(x=28, y=64)
    
    # Data
    today = date.today()
    df = cn.get_by_date('*','doge_realtime',today.strftime("%d/%m/%Y"))
    

    #---------- Btn1: Live&Historical Chart ----------#
    def btn1():
        content.delete('all')
        navbar_canvas.delete('btn')


        # Dogecoin
        dogecoin_lbl = Label(content, text='Dogecoin', font=('Century Gothic',30,'bold'), bg='#212528', fg='white')
        content.create_window(105, 23, window=dogecoin_lbl)

        doge_lbl = Label(content, text='DOGE', font=('Century Gothic',22), bg='#212528', fg='#B7B5B5')
        content.create_window(253, 26.5, window=doge_lbl)

        today_lbl = Label(content, text=today.strftime("%B %d, %Y"), font=('arial', 17), bg='#212528', fg='white')
        content.create_window(890, 26.5, window=today_lbl)


        # Table
        tbl_canvas = Canvas(content, width=952, height=76, highlightthickness=0, bg='#212528')#"#292F34"
        content.create_window(482, 100, window=tbl_canvas)

        image1 = Image.open("images/tbl-bg.png")
        image1 = image1.resize((954,76),Image.ANTIALIAS)
        test = ImageTk.PhotoImage(image1, master=tbl_canvas)
        tbl = Label(tbl_canvas, image=test, bg='#212528')
        tbl.image = test
        tbl_canvas.create_image(0,0, image=test, anchor=NW)

        # Labels
        col = [
            "Current Price", "24hr High", "24hr Low",
            "Market Cap", "Total Supply", "Volume"
        ]

        x=91
        for item in col:
            tbl_canvas.create_text(x,20, text=item, fill="#425393", font=('yu gothic ui', 13, "bold"))
            x+=155

        col = [
            df.iat[-1,2], df.iat[-1,4], df.iat[-1,5],
            df.iat[-1,6], df.iat[-1,8], df.iat[-1,7]
        ]

        y = 47
        x = 91
        for item in col:
            tbl_canvas.create_text(x, y, text=item, fill="#425393", font=('yu gothic ui', 20, "bold"), tags=('row'))
            x+=155


        # Graph
        bg = Image.open("images/grph-bg1.png")
        bg = bg.resize((954, 418), Image.ANTIALIAS)
        test = ImageTk.PhotoImage(bg, master=content)
        label3 = Label(content, image=test, bg='#212528')
        label3.image = test
        content.create_image(6,150, anchor=NW,image=test)

        global graph_canvas
        graph_canvas = Canvas(content, width=882, height=285, highlightthickness=0, bg="#425393")
        content.create_window(484, 339, window=graph_canvas)


        def btn_selected(i):
            clear()

            if i == 0:
                # ----- Display DOGEGIE ------ #
                dg = Image.open("images/doge-chat4.png")
                dg = dg.resize((405, 60), Image.ANTIALIAS)
                test = ImageTk.PhotoImage(dg, master=content)
                dg = Label(content, image=test, bg='#4A70D2')
                dg.image = test
                content.create_image(500,500, anchor=NW,image=test, tags=('label'))

                dogegie = cn.get_by_date('Decision', 'doge_decide', today.strftime("%d/%m/%Y"))
                dogegie = dogegie.iat[-1,0]
                content.create_text(675,529, text=dogegie, fill="#2c2f67", font=('Segoe UI Black', 14), tags=('label'))

                data = df
                data['time'] = pd.to_datetime(data['time']).dt.strftime("%H:%M")
                data['day_price'] = pd.to_numeric(data['day_price'])
                df2 = data[['time','day_price']]
                x = 'time'
            
            else:
                if i == 1:
                    days = 3
                elif i == 2:
                    days = 7
                elif i == 3:
                    days = 30
                else:
                    days = 365
                
                past = today - timedelta(days=days)
                data = pd.DataFrame()
                
                for j in range(days):
                    df_temp = cn.get_by_date('*', 'doge_histo', past.strftime("%d/%m/%Y"))
                    df_temp['Date'] = pd.to_datetime(df_temp['Date']).dt.strftime("%d/%m/%Y")
                    data = pd.concat([data, df_temp], ignore_index=True)
                    past = today - timedelta(days=days-(j+1))
                
                data = pd.concat([data,get_today()], ignore_index=True)

                if days == 365 or days == 30:
                    data['Date'] = pd.to_datetime(data['Date']).dt.strftime("%Y/%m/%d")
                else:
                    data['Date'] = pd.to_datetime(data['Date']).dt.strftime("%Y %b %d")
                data['Close'] = pd.to_numeric(data['Close'])
                df2 = data[['Date','Close']]
                x = 'Date'
                
            graph(df2, i, 10, 3.2, x, 450, 135)

            try:
                past = today - timedelta(days=days)
                lbl = Label(content, text=past.strftime("%B %d, %Y")+" - "+today.strftime("%B %d, %Y"), 
                            font=('arial', 15), bg='#4A70D2', fg='white')
                content.create_window(775, 530, window=lbl, tags=('label',))
            except Exception:
                pass
        
        
        # Buttons
        btns_canvas = Canvas(content, width=267, height=36, highlightthickness=0, bg="#4A70D2")#
        btns_canvas.place(x=45, y=513)

        btn_text = ["1D", "3D", "1W", "1M", "1Y"]

        x = 3
        for i in range(len(btn_text)):
            Button(btns_canvas, text=btn_text[i], font=('yu gothic ui', 10, "bold"), padx=7, bg="#212528", 
                    fg="white", relief="flat", command=partial(btn_selected, i)).place(x=x, y=3)
            x+=48
        btn_selected(0)


        # Next Window
        bg = Image.open("images/btn2.png")
        bg = bg.resize((198, 31), Image.ANTIALIAS)
        test = ImageTk.PhotoImage(bg, master=navbar_canvas)
        to_btn2 = Button(navbar_canvas, image=test, bg="#4A70D2", command=btn2,
                    relief="flat", activebackground="#4A70D2", bd=0)
        to_btn2.image = test
        navbar_canvas.create_window(912,24, window=to_btn2, tags=('btn'))
    
    
    #---------- Btn2: Predicted Prices ---------------#
    def btn2():
        content.delete('all')
        navbar_canvas.delete('btn')


        # Predicted Prices
        predict_lbl = Label(content, text='Predicted Prices', font=('Century Gothic',30,'bold'), bg='#212528', fg='white')
        content.create_window(161, 22, window=predict_lbl)

        today = date.today()
        
        def predicted(i):
            global db_data
            clear()

            if i == 0:
                col = "Date, Predicted_Price"
                x = "Predicted_Price"
                txt = "Closing"
            elif i == 1:
                col = "Date, Predicted_High"
                x = "Predicted_High"
                txt = "High"
            else:
                col = "Date, Predicted_Low"
                x = "Predicted_Low"
                txt = "Low"

            db_data = cn.get_all(col, "doge_pred")
            db_data[x] = pd.to_numeric(db_data[x])
            db_data['Date'] = pd.to_datetime(db_data['Date']).dt.strftime("%b %d")


            # Graph
            bg = Image.open("images/predict-grph2.png")
            bg = bg.resize((954, 511), Image.ANTIALIAS)
            test = ImageTk.PhotoImage(bg, master=content)
            label3 = Label(content, image=test, bg='#212528')
            label3.image = test
            content.create_image(6,56, anchor=NW,image=test)

            global graph_canvas
            graph_canvas = Canvas(content, width=635, height=393, highlightthickness=0, bg="#425393")
            content.create_window(355,290, window=graph_canvas)

            global price_canvas
            price_canvas = Canvas(content, width=220, height=393, highlightthickness=0, bg="#425393")
            content.create_window(818,290, window=price_canvas)


            def create_grph(days):
                data = db_data.head(days)
                col = txt

                if col == 'Closing':
                    col = 'Close'
                
                df_today = get_today()[['Date', col]]
                df_today['Date'] = pd.to_datetime(df_today['Date']).dt.strftime("%b %d")
                df_today = df_today.rename(columns={col: x})
                data = pd.concat([df_today, data], ignore_index=True)
                data[x] = pd.to_numeric(data[x])
                #print(data)

                graph(data, 0, 6.7, 4.3, 'Date', 330, 182)

                # Price panel
                price_canvas.create_text(112,23, fill="white", text=txt, font=('yu gothic ui bold',15))

                y = 75
                for i in range(1, len(data)):
                    date_lbl = data.iat[(i), 0]
                    price_lbl = '{: .6f}'.format(data.iat[(i), 1])
                    price_canvas.create_text(45,y, text=date_lbl, fill="white", font=('yu gothic ui bold',15))
                    price_canvas.create_text(150,y, text=price_lbl, fill="white", font=('yu gothic ui bold',15))

                    y+=40


            # Slider
            slider_canvas = Canvas(content, width=400, height=40, highlightthickness=0, bg='#4A70D2')#
            content.create_window(245, 529, window=slider_canvas)

            days = 1
            current_value = DoubleVar()

            def get_current_value():
                return '{: .2f}'.format(current_value.get())

            def slider_changed(event):
                clear()
                days = int(round(float(get_current_value())))
                ddate = today+timedelta(days=days)

                create_grph(days)

                if days == 1:
                    ddate_lbl = Label(content, text=ddate.strftime("%B %d, %Y"), font=('arial', 15), bg='#4A70D2', fg='white')
                    content.create_window(820, 532, window=ddate_lbl, tags=('label',))
                else:
                    yesterday = today + timedelta(days=1)
                    ddate_lbl = Label(content, text=yesterday.strftime("%B %d, %Y")+" - "+ddate.strftime("%B %d, %Y"), 
                            font=('arial', 15), bg='#4A70D2', fg='white')
                    content.create_window(775, 532, window=ddate_lbl, tags=('label',))
        

            Label(slider_canvas,text='Days:', font=('yu gothic ui',18, "bold"), bg='#4A70D2' , fg='white').place(x=14, y=5)

            Scale(slider_canvas, from_=1, to=7, orient='horizontal', sliderrelief='flat', variable=current_value, bg='#4A70D2',
                    command=slider_changed,length=300, fg='white', troughcolor='#212528', highlightthickness=0).place(x=85, y=0)


            ddate = today+timedelta(days=days)
            date_lbl = Label(content, text=ddate.strftime("%B %d, %Y"), font=('arial', 15), bg='#4A70D2', fg='white')
            content.create_window(820, 532, window=date_lbl, tags=('label',))
            create_grph(days)


        btn_text = ["Closing", "High", "Low"]
        x=415
        for i in range(len(btn_text)):
            btn_data = tkButton(master=content, text=btn_text[i], text_font=('yu gothic ui', 14, "bold"), fg_color="#DCE3FF",
                            bg_color="#212528", width=134, hover_color="#b9d9ff", text_color="#425393",
                            command=partial(predicted, i))
            content.create_window(x,22, window=btn_data)
            x+=155
        predicted(0)


        # Next Window
        bg = Image.open("images/btn1.png")
        bg = bg.resize((303, 31), Image.ANTIALIAS)
        test = ImageTk.PhotoImage(bg, master=navbar_canvas)
        to_btn2 = Button(navbar_canvas, image=test, bg='#4A70D2', command=btn1, 
                    relief="flat", activebackground='#4A70D2', bd=0)
        to_btn2.image = test
        navbar_canvas.create_window(860,24, window=to_btn2, tags=('btn'))

        
    # clear
    def clear():
        try:
            content.delete('label')
            graph_canvas.delete('all')
            price_canvas.delete('all')
        except Exception:
            pass

    # today
    def get_today():
        df_today = df.tail(1)
        df_today = df_today.rename(columns={'date': 'Date', 
                                            'day_price': 'Close',
                                            'day_open': 'Open',
                                            'day_high': 'High',
                                            'day_low': 'Low'
                                            })
        df_today['Date'] = pd.to_datetime(df_today['Date']).dt.strftime("%d/%m/%Y")
        
        return df_today
    
    # Create Graph
    def graph(df2, i, w, h, plot, x, y):
        figure2 = plt.Figure(figsize=(w, h), dpi=100, facecolor="#425393")
        ax2 = figure2.add_subplot(111)

        if i == 3 or i == 4:
            df2.plot(x=plot, kind='line', legend=True, ax=ax2, color="#4ad29f", fontsize=10)
        else:
            df2.plot(x=plot, kind='line', legend=True, ax=ax2, color="#4ad29f", marker='o',fontsize=10)

        ax2.set_facecolor("#425393")
        ax2.xaxis.label.set_color('w')
        ax2.yaxis.grid(color="#5E6FAF",linewidth=1)

        for label in ax2.xaxis.get_ticklabels():
            label.set_color('w')
        for label in ax2.yaxis.get_ticklabels():
            label.set_color('w')

        ax2.spines['bottom'].set_color("#202D42")
        ax2.spines['top'].set_color("#425393")
        ax2.spines['left'].set_color("#202D42")
        ax2.spines['right'].set_color("#425393")

        line2 = FigureCanvasTkAgg(figure2, graph_canvas)
        line2 = line2.get_tk_widget()
        graph_canvas.create_window(x, y, window=line2, tags=('graph',))
    
    
    if btn == 0:
        btn1()
    else:
        btn2()


# Main APP
app = Tk()
app.title('DOGEGIE')
app.geometry('1024x661+300+85')
app['bg'] = "#4A70D2"
app.resizable(0,0)

logo_canvas = Canvas(app, width=400, height=279, highlightthickness=0, bg="#4A70D2")
logo_canvas.place(x=312, y=108)


# Logo
image1 = Image.open("images/dogegie-logo.png")
image1 = image1.resize((400,279),Image.ANTIALIAS)
test = ImageTk.PhotoImage(image1, master=logo_canvas)
label1 = Label(logo_canvas, image=test)
label1.image = test
logo_canvas.create_image(0,0, anchor=NW,image=test)


# Buttons
btns = ["SEE DOGECOIN LIVE CHART AND HISTORICAL DATA", "SEE DOGECOIN PREDICTED PRICES"]
y = 435
for i in range(2):
    Button(app, width=45, height=2, text=btns[i], bg="#212528", fg="white", activebackground="#212528",
        activeforeground="white", bd=0, command=partial(new_window, i)).place(x=355, y=y)
    y+=65

# Start App
app.mainloop()