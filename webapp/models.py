from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class user_data(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    user_token_file = models.TextField()
    # user_
    model_name = models.CharField(max_length=100)
    amount = models.IntegerField(max_length=8)
    symbols = models.TextField()
    scanner_symbols = models.TextField()


