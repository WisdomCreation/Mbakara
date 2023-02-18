from django.db import models
# Create your models here.
class user_data(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    token_path = models.TextField(null=True) 
    run_trading = models.BooleanField(null=True)
    run_scanner = models.BooleanField(null=True)
    buy_more = models.BooleanField(null=True)
    api_key = models.CharField(max_length=225 , null=True)
    redirect_url = models.CharField(max_length=225 , null=True)
    acc_id = models.IntegerField(null=True)
    trading_model = models.CharField(max_length=100 , null=True)
    amount = models.IntegerField(null=True)
    trading_symbols = models.TextField(null=True)
    scanner_symbols = models.TextField(null=True)
    scanner_models = models.TextField(null=True) 
    