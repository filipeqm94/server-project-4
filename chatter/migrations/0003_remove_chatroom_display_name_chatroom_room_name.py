# Generated by Django 4.0.1 on 2022-01-23 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatter', '0002_alter_chatmessage_chat_alter_chatroom_user_one_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatroom',
            name='display_name',
        ),
        migrations.AddField(
            model_name='chatroom',
            name='room_name',
            field=models.TextField(default=1, unique=True),
            preserve_default=False,
        ),
    ]
