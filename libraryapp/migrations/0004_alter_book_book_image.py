# Generated by Django 4.0.4 on 2022-07-09 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraryapp', '0003_book'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='book_image',
            field=models.ImageField(upload_to='image'),
        ),
    ]