# Generated by Django 3.2.6 on 2021-11-03 06:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0015_genre'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='genre',
            options={'ordering': ('title',)},
        ),
    ]
