from rest_framework import generics
from .models import Tweet, TwitterAccount
from .serializers import TweetSerializer

# Create your views here.

class ListTweetsView(generics.ListAPIView):
    # GET tweets
    # List all tweets. Only used for debugging
    serializer_class = TweetSerializer

    def get_queryset(self):
        queryset = Tweet.objects.all()
        username = self.request.query_params.get('username', None)
        if username is not None:
            queryset = queryset.filter(user__name__iexact=username)
        return queryset


