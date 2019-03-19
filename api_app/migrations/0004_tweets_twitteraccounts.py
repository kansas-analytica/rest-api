# Generated by Django 2.1.7 on 2019-03-19 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('api_app', '0003_auto_20190211_2030'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tweets',
            fields=[
                ('created_at', models.DateTimeField()),
                ('id_str', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('text', models.TextField()),
                ('user_id', models.IntegerField()),
            ],
            options={
                'db_table': 'tweets',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TwitterAccounts',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('screen_name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('date_created', models.DateTimeField()),
            ],
            options={
                'db_table': 'twitter_accounts',
                'managed': False,
            },
        ),
    ]