# Generated by Django 3.2.12 on 2022-03-03 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20220303_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name of User'),
        ),
    ]
