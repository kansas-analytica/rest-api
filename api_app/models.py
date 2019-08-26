from django.db import models

class Tweet(models.Model):
    created_at = models.DateTimeField()
    id_str = models.CharField(max_length=255, primary_key=True)
    text = models.TextField()
    user = models.ForeignKey('TwitterAccount', on_delete=models.CASCADE)

    def __str__(self):
        return "{} - {}".format(self.user.name, self.id_str)

    class Meta:
        managed = False
        db_table = 'tweets'


class TwitterAccount(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    screen_name = models.CharField(max_length=255)
    description = models.TextField()
    date_created = models.DateTimeField()

    followers = models.IntegerField()
    following = models.IntegerField()
    # statuses_count = models.IntegerField()
    image_url = models.CharField(max_length=300, blank=True, null=True)

    last_updated = models.DateTimeField()

    def __str__(self):
        return self.screen_name

    class Meta:
        managed = False
        db_table = 'twitter_accounts'
