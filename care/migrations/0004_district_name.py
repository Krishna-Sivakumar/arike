# Generated by Django 3.2.12 on 2022-02-27 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('care', '0003_auto_20220227_1029'),
    ]

    operations = [
        migrations.AddField(
            model_name='district',
            name='name',
            field=models.CharField(default='nothing', max_length=100),
            preserve_default=False,
        ),
    ]
