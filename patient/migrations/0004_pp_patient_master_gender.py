# Generated by Django 3.2.4 on 2021-06-12 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0003_pp_otp'),
    ]

    operations = [
        migrations.AddField(
            model_name='pp_patient_master',
            name='gender',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]