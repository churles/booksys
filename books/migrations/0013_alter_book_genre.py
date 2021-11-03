# Generated by Django 3.2.6 on 2021-11-02 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0012_alter_book_genre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='genre',
            field=models.CharField(choices=[('romance', 'Romance'), ("children's book", "Children's Book")], default=("children's book", "Children's Book"), max_length=60),
        ),
    ]
