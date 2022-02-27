# Generated by Django 3.2.12 on 2022-02-27 11:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('care', '0007_ward_number'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='district',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='care.district'),
        ),
        migrations.AddField(
            model_name='user',
            name='facility',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='care.facility'),
        ),
        migrations.AddField(
            model_name='user',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(default=1234567891, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('PN', 'Primary Nurse'), ('SN', 'Secondary Nurse'), ('DA', 'District Admin')], default='DA', max_length=2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
