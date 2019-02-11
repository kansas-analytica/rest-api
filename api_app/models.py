from django.db import models

# Create your models here.
class User(models.Model):
	username = models.CharField(max_length=20)
	screenname = models.CharField(max_length=20)
	location = models.CharField(max_length=50)
	url = models.CharField(max_length=40)
	description = models.TextField()
	user_id = models.IntegerField(primary_key=True)


class Tweet(models.Model):
	created_on = models.DateTimeField()
	tweet_id = models.CharField(max_length=30)
	text = models.TextField()
	user = models.ForeignKey(User, on_delete=models.CASCADE)


