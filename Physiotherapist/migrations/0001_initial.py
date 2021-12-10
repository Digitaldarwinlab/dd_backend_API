# Generated by Django 3.2.3 on 2021-05-20 10:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='pp_physiotherapist_master',
            fields=[
                ('pp_pm_id', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, serialize=False, to='Auth.user')),
                ('first_name', models.CharField(max_length=50)),
                ('middle_name', models.CharField(blank=True, max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('Doctor_type', models.IntegerField()),
                ('Address_1', models.CharField(max_length=150)),
                ('Address_2', models.CharField(blank=True, max_length=150)),
                ('Address_3', models.CharField(blank=True, max_length=150)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
                ('mobile_no', models.CharField(max_length=15)),
                ('whatsapp_no', models.CharField(max_length=15)),
                ('landline', models.CharField(max_length=15)),
                ('regd_no_1', models.CharField(max_length=50)),
                ('regd_no_2', models.CharField(blank=True, max_length=50)),
                ('degree', models.CharField(max_length=50)),
                ('expertise_1', models.CharField(max_length=50)),
                ('expertise_2', models.CharField(blank=True, max_length=50)),
                ('expertise_3', models.CharField(blank=True, max_length=50)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField(blank=True)),
                ('status_flag', models.IntegerField()),
                ('roleId', models.IntegerField()),
            ],
            options={
                'db_table': 'pp_physiotherapist_master',
            },
        ),
    ]