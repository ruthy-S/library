# Generated by Django 4.1.1 on 2022-10-15 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraryapp', '0008_remove_issuebook_reqbook_issuebook_book_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermember',
            name='user_address',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='usermember',
            name='user_designation',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='usermember',
            name='user_gender',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='usermember',
            name='user_mobile',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
