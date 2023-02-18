from django.shortcuts import redirect, render , HttpResponse
from django.urls import path , include
from django.contrib.auth.models import User
from django.contrib import messages 
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
import plotly.graph_objs as go
import pandas as pd
import requests
from datetime import timedelta , date
import numpy as np
import sqlite3
# from ..scanner.roi import criteria_scanner
import subprocess
connection = sqlite3.connect("db.sqlite3" , check_same_thread=False)

# print(connection.total_changes)

cursor = connection.cursor()
# cursor.execute("CREATE TABLE user (id INTEGER PRIMARY KEY AUTOINCREMENT,user_name TEXT, model_name TEXT,symbols TEXT, amount INTEGER)")

# query="ALTER TABLE user ADD user_name VARCHAR(100)"
# cursor.execute(query)
# print("NEW COLUMN ADDED..")



class scan():
    def __init__(self):
        self.api_url = str
        self.Symbol = "AAPL"
        self.api_key = "26eff02f62994365a02a513f06924270"
        self.df = pd.DataFrame
        self.Interval = "1day"

        today = date.today()
        end_date = today.strftime("%Y-%m-%d")
        self.start_date = today - timedelta(days=1825)
        self.end_date = today
    def Get_Data(self):
        self.api_url = f"https://api.twelvedata.com/time_series?symbol={self.Symbol}&interval={self.Interval}&apikey={self.api_key}&dp=5&start_date={self.start_date}&end_date={self.end_date}"
        data = requests.get(self.api_url).json()
        df = pd.DataFrame(data = data['values'])
        df['open'] = df['open'].astype(float)
        df['high'] = df['high'].astype(float)
        df['close'] = df['close'].astype(float)
        df['low'] = df['low'].astype(float)
        df['volume'] = df['volume'].astype(float)
        df = df[df['volume']!=0]
        df.reset_index(drop=True , inplace=True)
        self.df = df
        return df


# Create your views here.
@login_required(login_url="signin" )
def home(request):
    ob = scan()
    df = ob.Get_Data()    
    dfpl = df[0:50]

    fig = go.Figure(data=[go.Candlestick(x=dfpl['datetime'], 
                    open=dfpl['open'],
                    high=dfpl['high'],
                    low=dfpl['low'],
                    close=dfpl['close'],
                    increasing_line_color= 'green', decreasing_line_color= 'red')
                    ])

    plot = fig.to_html()
    return render(request, 'index.html', 
                    context={'plot_div': plot})


    return render(request , "index.html")

# @login_required(login_url="signin")
def scanner(request):
    if request.method == "POST":
    #     start_stop = request.POST.get("start_stop")
    #     if start_stop == "true":
    #         start_stop = True
    #     else:
    #         start_stop = False
    #     mini_stock_price = request.POST.get("mini_stock_price")
    #     mini_last_days = request.POST.get("mini_last_days")
    #     roi_per_month = request.POST.get("roi_per_month")
    #     print(roi_per_month , mini_last_days , mini_stock_price , start_stop)
    #     messages.success(request , "ROI Scanner is Updated, Thanks!")
    #     # subprocess.call(['python roi.py'])
    #     username = request.user.username
    #     file_name = str("data\\") + str("user_data") + str(".csv")
    #     df = pd.read_csv(file_name , index_col=0)
    #     ind = df['username'].where(df['username'] == username).dropna()
    #     if len(ind) !=0:
    #         n = ind.index[0]
    #     else:
    #         n = len(df["username"])

    #     df.at[n , "roi_per_month"] = float(roi_per_month)
    #     df.at[n , "last_days"] = int(mini_last_days)
    #     df.at[n , "stock_price"] = float(mini_stock_price)
    #     df.to_csv(file_name)

    #     return render(request , "index.html" )
    # else:
    #     username = request.user.username
    #     file_name = str("data\\") + str("user_data") + str(".csv")
    #     df = pd.read_csv(file_name , index_col=0)
    #     ind = df['username'].where(df['username'] == username).dropna()
    #     if len(ind) !=0:            
    #         n = ind.index[0]
    #         print(df.iloc[n]['last_days'] , type(df.iloc[n]['last_days']))
    #         if df.iloc[n]['last_days'] != 0:
    #             json_obj = {
    #                 "username" : request.user.username,
    #                 "roi_mini_stock_price" : df.iloc[n]['stock_price'],
    #                 "roi_last_days" : df.iloc[n]['last_days'],
    #                 "roi_per_month" : df.iloc[n]['roi_per_month'] 
    #                 }

    #             # start_scaning = criteria_scanner(json_obj)
    #             # start_scaning.start()
        pass
    return render(request , "scanner.html")
    # data.objects.create(roi = {"start_stop" : True , "stock_price" : mini_stock_price , "last_days" : mini_last_days , "roi" : roi_per_month} , pu = {"start_stop" : True , "stock_price" : mini_stock_price , "last_days" : mini_last_days , "roi" : roi_per_month}).save()



# @login_required(login_url="signin")
def account(request):
    if request.method == "POST":
    #     start_stop = request.POST.get("start_stop")
    #     if start_stop == "true":
    #         start_stop = True
    #     else:
    #         start_stop = False
    #     time_frame = request.POST.get("time_frame")
    #     gained = request.POST.get("gained")
    #     # data(roi = {"stock_price" : 50 , "last_days" : 12 }).save
    #     username = request.user.username
    #     file_name = str("data\\") + str("user_data") + str(".csv")
    #     df = pd.read_csv(file_name , index_col=0)
    #     ind = df['username'].where(df['username'] == username).dropna()
    #     if len(ind) !=0:
    #         n = ind.index[0]
    #     else:
    #         n = len(df["username"])
    #     df.at[n , "pu_time_frame"] = time_frame
    #     df.at[n , "pu_gained"] = gained
    #     df.to_csv(file_name)
    #     json_obj = {
    #         "username" : request.user.username,
    #         "pu_time_frame" : df.iloc[n]['pu_time_frame'],
    #         "pu_gained" : df.iloc[n]['pu_gained'],
    #         }
    #     messages.success(request , "Purple Unicorn Scanner is Updated, Thanks!")
    #     return render(request , "index.html" )
    # else:
    #     username = request.user.username
    #     file_name = str("data\\") + str("user_data") + str(".csv")
    #     df = pd.read_csv(file_name , index_col=0)
    #     ind = df['username'].where(df['username'] == username).dropna()
    #     if len(ind) !=0:            
    #         n = ind.index[0]
    #         if df.iloc[n]['pu_time_frame'] != 0:
    #             json_obj = {
    #                 "username" : request.user.username,
    #                 "pu_time_frame" : df.iloc[n]['pu_time_frame'],
    #                 "pu_gained" : df.iloc[n]['pu_gained'],
    #                 }
        pass
    return render(request , "account.html")

@login_required(login_url="signin")
def log(request):
    file_name = str("data\\") + str(request.user.username) + str(".csv")
    print(file_name)
    DataFrame = pd.read_csv(file_name , index_col=0)
    return render(request, 'log.html', {'df': DataFrame })
    # return render(request , "log.html")

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        if User.objects.filter(username=username).exists():
            messages.warning(request , "User Already Exists!")
            return render(request , "signin.html")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        if password1 == password2:
            myuser = User.objects.create_user(username , email , password1)
            myuser.save()
            # cursor.execute("INSERT INTO user_config (username) VALUES (?)" , username)
            messages.success(request , "your Accont has been Successfuly Created.")
            df = pd.DataFrame(columns=["datetime" , 'stock_name' , "Purple_Unicorn" , "pu_time_frame" , "pu_gained" , "roi_per_month" , "last_days" , "stock_price"])            
            file_name = str("data\\") + str(username) + str(".csv")
            df.to_csv(file_name)
            cursor.execute("INSERT INTO user (user_name) VALUES (?)" , (username,))
            cursor.close()
            return render(request , "signin.html")
        else:
            messages.warning(request , "Password Not Match")
        return render(request , "signup.html")

    return render(request , "signup.html")

def signin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(username = email , password = password)

        if user is not None:
            login(request , user)
            username = user.username
            messages.success(request , "Login successfly")
            return render(request , "index.html" , {"username" : username})
        else:
            messages.warning(request , "no user exists with these credentials")
            return render(request , "signin.html")
    return render(request , "signin.html")

def signout(request):
    logout(request)
    messages.success(request , "logged Out Successfuly!")
    return redirect("home")
