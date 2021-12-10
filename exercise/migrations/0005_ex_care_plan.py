# Generated by Django 3.2.4 on 2021-06-19 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercise', '0004_alter_ex_excercise_joints_mapping_flex_field_1'),
    ]

    operations = [
        migrations.CreateModel(
            name='ex_care_plan',
            fields=[
                ('pp_cp_id', models.AutoField(primary_key=True, serialize=False)),
                ('careplan_code', models.CharField(max_length=50)),
                ('patient_details', models.JSONField(blank=True, default=None, null=True)),
                ('exercise_details', models.JSONField(blank=True, default=None, null=True)),
                ('status_flag', models.IntegerField()),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('created_by', models.IntegerField(blank=True, default=None, null=True)),
                ('last_update_date', models.DateField(auto_now_add=True)),
                ('last_updated_by', models.IntegerField(blank=True, default=None, null=True)),
            ],
        ),
    ]
