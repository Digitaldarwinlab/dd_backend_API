# Generated by Django 3.2.4 on 2021-06-23 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0004_pp_patient_master_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pp_patient_master',
            name='email',
            field=models.EmailField(max_length=150, unique=True),
        ),
    ]