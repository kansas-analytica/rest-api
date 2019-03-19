from django.db import models

class Tweets(models.Model):
    created_at = models.DateTimeField()
    id_str = models.CharField(max_length=255, primary_key=True)
    text = models.TextField()
    user_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tweets'


class TwitterAccounts(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    screen_name = models.CharField(max_length=255)
    description = models.TextField()
    date_created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'twitter_accounts'
