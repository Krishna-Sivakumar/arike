# Generated by Django 3.2.12 on 2022-03-07 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_user_date_of_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_of_birth',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]