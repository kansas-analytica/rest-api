from rest_framework import generics
from .models import Tweet, TwitterAccount
from .serializers import TweetSerializer
from django.http import JsonResponse, HttpResponse
import tweepy                       # For filling in data
import MySQLdb                      # For filling in data
from datetime import datetime       # For filling in data

# Environment variables, for patching missingness in data as-needed. hastily thrown in here
CONSUMER_KEY='EN1KxGBUKz1yHTQsD75chAdZ5'
CONSUMER_SECRET='dpUgQ0DBDBcHcn6pUtUDdgOK7VYQlNcgxKkTFCDZx5nikNPv1X'
ACCESS_TOKEN='47129106-ZgrslW1F8UnzjoR34rHm1xv5vhNWr61dwHX0xPrJb'
ACCESS_TOKEN_SECRET='SMfTKVnoGdO7j5b3gum7E0tWOnV958euKuOlQvC7Gzsn5'

DB_HOST='localhost'
DB_USER='root'
DB_PASS='kuteam02'
DB_NAME='kansasanalytica'

# How many tweets return on a /accounts/ call?
TWEETS_RETURN_LENGTH = 10

# Setup Tweepy
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
twitter = tweepy.API(auth)

# Utility - Connect to database (avoids timeout issues)
def connectToDB():
    db = MySQLdb.connect(host=DB_HOST,user=DB_USER,passwd=DB_PASS,db=DB_NAME, charset="utf8")
    KA = db.cursor()  # Cursor object kfor interacting with the Kansas Analytica database
    return (db, KA)

# Add a tweet to the database (given a row in the data file)
def add_tweet_to_db(user_id, db, KA):
    try:
        statuses = twitter.user_timeline(user_id=user_id, count=5, tweet_mode="extended")
        tweets = {}
        i = 0
        print("Found {} tweets to add...".format(len(statuses)))
        for status in statuses:
            # print("[Tweet] {}".format(status.full_text))

            # Timestamp formatting
            # t_time = datetime.strptime(status.created_at, '%a %b %d %H:%M:%S %z %Y')
            t_time = datetime.strftime(status.created_at, '%Y-%m-%d %H:%M:%S')

            #Insert the account into the verified_accounts_tweets table
            query = "INSERT IGNORE INTO tweets (id_str, created_at, text, user_id) VALUES (%s, %s, %s, %s)"
            values = (status.id_str, t_time, status.full_text.encode('utf-8', errors='ignore'), int(status.user.id_str))
            # Execute query and commit to database
            KA.execute(query, values)
            db.commit()
        return True
    except Exception as e:
        print("[Error] - Assuming account is protected. More info below. Passing...")
        print(e)
    return False


class ListTweetsView(generics.ListAPIView):
    # GET tweets
    # List all tweets. Only used for debugging
    serializer_class = TweetSerializer

    def get_queryset(self):
        queryset = Tweet.objects.all()
        username = self.request.query_params.get('username', None)
        if username is not None:
            queryset = queryset.filter(user__screen_name__iexact=username).order_by('?')[:3]
        return queryset

# Grab 5 tweets from the given twitter account
def fillTweets(account):
    data = {}
    tweets = Tweet.objects.filter(user_id=account.id)[:4]
    for index, tweet in enumerate(tweets):
        data[index] = {'id_str': tweet.id_str,
                        'user_id': tweet.user_id,
                        'text': tweet.text,
                        'created_at': tweet.created_at}
    return data

# Doing this because tried adding statuses_count to TwitterAccount django model once and there were issues
#   and I really don't feel like jacking with it because I want to be done with this shit
def getStatusesCount(account_id, db, KA):
    KA.execute("SELECT statuses_count FROM twitter_accounts WHERE id={}".format(account_id))
    statuses_count = KA.fetchone()
    return int(statuses_count[0])

# Update the user's statuses count since we added this retroactively
def updateStatusesCount(account, db, KA):
    try:
        user = twitter.get_user(account.id)
        # db_user = TwitterAccount.objects.get(id=account.id)
        # db_user.statuses_count = user.statuses_count
        # db_user.save()
        query = "UPDATE twitter_accounts SET statuses_count = {} WHERE id ={}".format(user.statuses_count, account.id)
        KA.execute(query)
        db.commit()

        return user.statuses_count
    except Exception as e:
        print("Error updating status count for {} [{}]. Passing...".format(account.screen_name, account.id))
        pass

# Returns an account
# ENDPOINT : api.kansasanalytica.com/accounts/
def getAccounts(request):
    data = {}
    accounts = TwitterAccount.objects.all().order_by('?')[:TWEETS_RETURN_LENGTH]
    db, KA = connectToDB()
    for index, account in enumerate(accounts):
        statuses_count = getStatusesCount(account.id, db, KA)
        data[index] = {'id': account.id,
                        'name': account.name,
                        'screen_name': account.screen_name,
                        'description': account.description,
                        'date_created': account.date_created,
                        'followers': account.followers,
                        'following': account.following,
                        "statuses_count": statuses_count,
                        'last_updated': account.last_updated,
                        'image_url': account.image_url,
                        'tweets': fillTweets(account)}

        # Added Statuses count so need to retroactively backfill
        if statuses_count == 0:
            statuses_count = updateStatusesCount(account, db, KA)
            data[index]["statuses_count"] = statuses_count

        # Begins logic for fixing missingness in the data whenever an account has less than 3 tweets.
        numTweets = len(data[index]['tweets'])
        if numTweets < 3:
            print("Only found {} tweets for user {}. Getting more...".format(numTweets, data[index]['screen_name']))
            finished = add_tweet_to_db(account.id, db, KA)
            data[index]['tweets'] = fillTweets(account)

        # print("STATUSES COUNT : {}".format(data[index]['statuses_count']))

    return JsonResponse(data, safe=False)


# Captures response data
# user_id is the voter
# account_id is the account the user is voting on
# /vote/{user_id}/{account_id}/{vote}
def recordVote(request, uid, screenname, vote):
    db, KA = connectToDB()
    print("Recording vote from user {} for account {}: {}".format(uid, screenname, vote))

    query = "INSERT INTO votes (uid, id, vote) VALUES (%s, %s, %s)"
    values = (uid, screenname, vote)
    KA.execute(query, values)
    db.commit()

    return HttpResponse(status=200)
