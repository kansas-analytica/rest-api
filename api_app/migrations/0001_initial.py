# Generated by Django 2.1.5 on 2019-02-04 20:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField()),
                ('tweet_id', models.CharField(max_length=30)),
                ('text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('username', models.CharField(max_length=20)),
                ('screenname', models.CharField(max_length=20)),
                ('location', models.CharField(max_length=50)),
                ('url', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('user_id', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.AddField(
            model_name='tweet',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_app.User'),
        ),
    ]
