"""webapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path , include
import web.views as views

admin.site.site_header = "Mbakara630 Admin"
admin.site.site_title = "Mbakara630 Admin Portal"
admin.site.index_title = "Welcome to Mbakara630 Researcher Portal"

urlpatterns = [
    path('admin/', admin.site.urls),
    path("" , views.home , name="home"),
    path("index" , views.home , name="home"),
    path("scanner" , views.scanner , name="scanner"),
    path("graph" , views.graph , name="graph"),
    path("trading" , views.trading , name="trading"),
    # path("account" , views.account , name="account"),
    path("log" , views.log , name="log"),
    path("signup" , views.signup , name = "signup"), 
    path("signin" , views.signin , name = "signin"),
    path("signout" , views.signout , name = "signout"),
]
