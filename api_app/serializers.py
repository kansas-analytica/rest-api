from rest_framework import serializers
from .models import Tweet, TwitterAccount

class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = ("id_str", "created_at", "text", "user_id")
        depth = 1

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = TwitterAccount
		fields = ("screen_name", "description", "date_created", "followers", "following", "image_url", "last_updated")

# class UserTweetSerializer(serializers.Serializer):
# 	
