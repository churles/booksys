# Generated by Django 3.2.9 on 2021-12-10 08:19

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('books', '0025_bookrented'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BookRented',
            new_name='BookRent',
        ),
    ]
