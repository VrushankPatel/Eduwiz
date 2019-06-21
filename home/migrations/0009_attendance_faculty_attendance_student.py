# Generated by Django 2.1.5 on 2019-04-15 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_auto_20190415_1021'),
    ]

    operations = [
        migrations.CreateModel(
            name='attendance_faculty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school_id', models.PositiveIntegerField()),
                ('date', models.CharField(max_length=10)),
                ('Enroll', models.PositiveIntegerField()),
                ('present', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='attendance_student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school_id', models.PositiveIntegerField()),
                ('date', models.CharField(max_length=10)),
                ('std', models.PositiveIntegerField()),
                ('Enroll', models.PositiveIntegerField()),
                ('present', models.BooleanField(default=False)),
            ],
        ),
    ]
