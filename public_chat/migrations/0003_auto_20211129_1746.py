# Generated by Django 3.2.9 on 2021-11-29 09:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('public_chat', '0002_alter_publicchatroom_users'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publicchatroom',
            name='users',
        ),
        migrations.RemoveField(
            model_name='publicchatroommessage',
            name='room',
        ),
        migrations.RemoveField(
            model_name='publicchatroommessage',
            name='user',
        ),
        migrations.DeleteModel(
            name='PublicChatRoomMessageManager',
        ),
        migrations.DeleteModel(
            name='PublicChatRoom',
        ),
        migrations.DeleteModel(
            name='PublicChatRoomMessage',
        ),
    ]