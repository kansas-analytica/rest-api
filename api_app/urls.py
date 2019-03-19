from django.urls import path
from .views import ListTweetsView

urlpatterns = [
    path('tweets/', ListTweetsView.as_view(), name="tweets-all")
]
