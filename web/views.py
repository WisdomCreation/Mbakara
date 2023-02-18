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
import subprocess
from web.models import user_data
from .forms import webForm
import logging
import coloredlogs
from .trading_bot.utils import show_eval_result, switch_k_backend_device, get_stock_data
from .trading_bot.methods import evaluate_model
from .trading_bot.agent import Agent
import yfinance as yf
import pandas as pd
import numpy as np

import altair as alt
import seaborn as sns

def show_graph(symbol , model_name):

    # model_name = 'model_dqn_GOOG_50'
    # test_stock = 'data/GOOG_2019.csv'
    window_size = 10
    debug = True
    agent = Agent(window_size, pretrained=True, model_name=model_name)

    df = yf.download(tickers = symbol , period="1y" , interval="1d" )
    df = df.reset_index()
    test_stock = list(df['Adj Close'])
    # filter out the desired features
    df = df[['Date', 'Adj Close']]
    # rename feature column names
    df = df.rename(columns={'Adj Close': 'actual', 'Date': 'date'})
    # convert dates from object to DateTime type
    dates = df['date']
    dates = pd.to_datetime(dates, infer_datetime_format=True)
    df['date'] = dates
    coloredlogs.install(level='DEBUG')
    switch_k_backend_device()

    test_data = test_stock
    initial_offset = test_data[1] - test_data[0]

    test_result, history = evaluate_model(agent, test_data, window_size, debug)
    show_eval_result(model_name, test_result, initial_offset)

    coloredlogs.install(level='DEBUG')
    switch_k_backend_device()

    test_data = test_stock
    initial_offset = test_data[1] - test_data[0]

    test_result, history = evaluate_model(agent, test_data, window_size, debug)
    show_eval_result(model_name, test_result, initial_offset)
    chart = visualize(df, history, title=test_stock)
    print(chart)
    return chart


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


def visualize(df, history, title="trading session"):
    # add history to dataframe
    position = [history[0][0]] + [x[0] for x in history]
    actions = ['HOLD'] + [x[1] for x in history]
    df['position'] = position
    df['action'] = actions
    
    # specify y-axis scale for stock prices
    scale = alt.Scale(domain=(min(min(df['actual']), min(df['position'])) - 50, max(max(df['actual']), max(df['position'])) + 50), clamp=True)
    
    # plot a line chart for stock positions
    actual = alt.Chart(df).mark_line(
        color='green',
        opacity=0.5
    ).encode(
        x='date:T',
        y=alt.Y('position', axis=alt.Axis(format='$.2f', title='Price'), scale=scale)
    ).interactive(
        bind_y=False
    )
    
    # plot the BUY and SELL actions as points
    points = alt.Chart(df).transform_filter(
        alt.datum.action != 'HOLD'
    ).mark_point(
        filled=True
    ).encode(
        x=alt.X('date:T', axis=alt.Axis(title='Date')),
        y=alt.Y('position', axis=alt.Axis(format='$.2f', title='Price'), scale=scale),
        color='action'
    ).interactive(bind_y=False)

    # merge the two charts
    chart = alt.layer(actual, points, title=title).properties(height=300, width=1000)
    return chart


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

@login_required(login_url="signin")
def trading(request):
    context = {}
    context['form'] = webForm()
    if request.method == "POST":
        try:
            obj = user_data.objects.filter(username = request.user.username)
            for o in obj:
                api_key = o.api_key
                acc_id = o.acc_id
                run_trading = o.run_trading
                run_scanner = o.run_scanner
                amount = o.amount
                trading_model = o.trading_model
                trading_symbols = o.trading_symbols
            if request.POST.get("api_key") != "":
                api_key = request.POST.get("api_key")
            if request.POST.get("acc_id") != "":
                acc_id = request.POST.get("acc_id")
            if request.POST.get("run_trading") != "":
                run_trading = request.POST.get("run_trading")
            if request.POST.get("run_scanner") != "":
                run_scanner = request.POST.get("run_scanner")
            if request.POST.get("amount") != "":
                amount = request.POST.get("amount")
            if request.POST.get("trading_model") != "":
                trading_model = request.POST.get("trading_model")
            if request.POST.get("trading_symbols") != "":
                trading_symbols = request.POST.get("trading_symbols")
            obj = user_data.objects.filter(username = request.user.username).update(api_key = api_key , acc_id = acc_id , run_scanner = run_scanner , run_trading = run_trading , trading_model = trading_model , trading_symbols = trading_symbols , amount = amount)
            messages.warning(request, "Your Data is Store")
            return render(request, "index.html")        
        except:
            messages.warning(request, "Invalid Entries")
            return render(request, "index.html")        
    return render( request, "trading.html", context)

@login_required(login_url="signin" )
def scanner(request):
    context = {}
    context['form'] = webForm()
    if request.method == "POST":
        try:
            obj = user_data.objects.filter(username = request.user.username)
            for o in obj:
                scanner_models = o.scanner_models
                scanner_symbols = o.scanner_symbols
                run_scanner = o.run_scanner
            if request.POST.get("scanner_models") != "":
                scanner_models = request.POST.get("scanner_models")
            if request.POST.get("scanner_symbols") != "":
                scanner_symbols = request.POST.get("scanner_symbols")
            if request.POST.get("run_scanner") != "":
                run_scanner = request.POST.get("run_scanner")
            obj = user_data.objects.filter(username = request.user.username).update(scanner_models = scanner_models , scanner_symbols = scanner_symbols , run_scanner = run_scanner)
            messages.warning(request, "Your Data is Store")
            return render(request, "index.html")        
        except:
            messages.warning(request, "Invalid Entries")
            return render(request, "index.html")        
    return render( request, "scanner.html", context)


@login_required(login_url="signin")
def graph(request):
    context = {}
    context['form'] = webForm()
    if request.method == "POST":
        chart = show_graph(symbol= request.POST.get("symbol"), model_name= request.POST.get("model"))
        # chart.save("ss.html")
        # plot = chart.to_html()
        # plot = chart.to_dict()
        return render( request, "fig.html", context)
        # return render(request, 'graph.html',
        #                 context={'plot_div': plot})

    return render( request, "graph.html", context)




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
            obj = user_data()
            obj.username = username
            obj.acc_id = 1
            obj.save()
            print("ADDEd")
            # cursor.execute("INSERT INTO user_config (username) VALUES (?)" , username)
            messages.success(request , "your Accont has been Successfuly Created.")
            df = pd.DataFrame(columns=["datetime" , 'stock_name' ,  "order_type" , "stock_price" ,  "quantity" , "amount" , "profit_loss" ])
            file_name = str("data\\") + str(username) + str(".csv")
            df.to_csv(file_name)
            user = user_data(username = username)
            user.save()
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
            active_user = username
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
