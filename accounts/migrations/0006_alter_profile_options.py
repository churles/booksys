# Generated by Django 3.2.9 on 2022-02-26 02:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_profile_coverphoto'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ('account',)},
        ),
    ]
