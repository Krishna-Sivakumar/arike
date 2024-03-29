# Generated by Django 3.2.12 on 2022-03-06 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('care', '0017_treatmentnotes_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitdetails',
            name='palliative_phase',
            field=models.CharField(choices=[('stable', 'stable'), ('unstable', 'unstable'), ('deteriorating', 'deteriorating'), ('dying', 'dying')], max_length=100),
        ),
        migrations.AlterField(
            model_name='visitdetails',
            name='systemic_examination',
            field=models.CharField(choices=[('cardiovascular', 'cardiovascular'), ('gastrointestinal', 'gastrointestinal'), ('central nervous system', 'central nervous system'), ('respiratory', 'respiratory'), ('genital-urinary', 'genital-urinary')], max_length=100),
        ),
    ]
