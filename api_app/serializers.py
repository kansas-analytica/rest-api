from rest_framework import serializers
from .models import Tweet, TwitterAccount

class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = ("id_str", "created_at", "text", "user_id")
