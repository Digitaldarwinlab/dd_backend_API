# Generated by Django 3.2.3 on 2021-06-01 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0002_rename_patient_family_historyy_pp_patient_master_patient_family_history'),
    ]

    operations = [
        migrations.CreateModel(
            name='pp_otp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('otp', models.IntegerField()),
                ('created_at', models.TimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'pp_otp',
            },
        ),
    ]
