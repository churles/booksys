# Generated by Django 3.2.9 on 2022-02-09 07:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0028_rename_description_book_synopsis'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='availability',
        ),
        migrations.RemoveField(
            model_name='book',
            name='price',
        ),
        migrations.RemoveField(
            model_name='book',
            name='stock',
        ),
        migrations.CreateModel(
            name='BookAvailability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('availability', models.CharField(choices=[('rent', 'RENT'), ('sale', 'SALE')], default='rent', max_length=10)),
                ('price', models.IntegerField(default=None)),
                ('stock', models.IntegerField(default=None)),
                ('book', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='books.book')),
            ],
            options={
                'ordering': ('book',),
            },
        ),
    ]
