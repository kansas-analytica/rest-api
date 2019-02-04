
from django.contrib.auth.models import User, Tweet
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = ('username', 'screenname', 'location', 'url', 'description', 'user_id')
