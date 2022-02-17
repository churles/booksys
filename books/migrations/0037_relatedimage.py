# Generated by Django 3.2.9 on 2022-02-16 03:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0036_alter_bookavailability_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='RelatedImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, default=None, upload_to='')),
                ('book', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='books.book')),
            ],
            options={
                'ordering': ('book',),
            },
        ),
    ]
