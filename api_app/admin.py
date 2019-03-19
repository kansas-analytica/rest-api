from django.contrib import admin
from .models import Tweets, TwitterAccounts

# Register your models here.

admin.site.register(Tweets)
admin.site.register(TwitterAccounts)
