from django.contrib import admin
from .models import Tweet, TwitterAccount

# Register your models here.

admin.site.register(Tweet)
admin.site.register(TwitterAccount)
