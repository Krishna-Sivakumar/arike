# Generated by Django 3.2.12 on 2022-03-03 19:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('care', '0009_auto_20220301_1610'),
    ]

    operations = [
        migrations.CreateModel(
            name='TemporaryLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(default='ep;+Pa\'*OI"?2%DN}#6XNESR0_P_*t', max_length=30)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]