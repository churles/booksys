# Generated by Django 3.2.9 on 2022-02-09 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0030_book_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='slug',
            field=models.SlugField(blank=b'I01\n'),
        ),
    ]
