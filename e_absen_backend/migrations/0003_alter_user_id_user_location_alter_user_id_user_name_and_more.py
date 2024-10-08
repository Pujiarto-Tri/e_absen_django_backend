# Generated by Django 4.2.16 on 2024-09-27 03:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('e_absen_backend', '0002_attendance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_id',
            name='user_location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='e_absen_backend.location'),
        ),
        migrations.AlterField(
            model_name='user_id',
            name='user_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='user_id',
            name='user_payout',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='user_id',
            name='user_role',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='e_absen_backend.role'),
        ),
        migrations.AlterField(
            model_name='user_id',
            name='user_shift',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='e_absen_backend.shift'),
        ),
    ]
