# Generated by Django 3.2.6 on 2021-11-20 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_reviewlike'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reviewlike',
            options={'ordering': ('review',)},
        ),
        migrations.AddField(
            model_name='reviewlike',
            name='value',
            field=models.CharField(default='Unlike', max_length=60),
        ),
    ]
