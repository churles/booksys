# Generated by Django 3.2.9 on 2022-02-10 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0032_bookavailability_daterange'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookavailability',
            name='daterange',
            field=models.CharField(blank=True, default='30', max_length=10),
        ),
    ]
