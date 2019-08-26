from django.urls import path
from .views import ListTweetsView
from . import views

urlpatterns = [
    path('tweets/', ListTweetsView.as_view(), name="tweets-all"),
    path('accounts/', views.getAccounts, name="get-accounts"),
    path('vote/<int:uid>/<slug:screenname>/<slug:vote>', views.recordVote, name="record-votes")
]
