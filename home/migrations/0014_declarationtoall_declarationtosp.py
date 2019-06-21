# Generated by Django 2.1.5 on 2019-04-22 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_feesrecord'),
    ]

    operations = [
        migrations.CreateModel(
            name='declarationtoall',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school_id', models.PositiveIntegerField()),
                ('declared_on', models.CharField(max_length=10)),
                ('message', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='declarationtosp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school_id', models.PositiveIntegerField()),
                ('declared_on', models.CharField(max_length=10)),
                ('message', models.TextField()),
                ('people_type', models.CharField(max_length=12)),
                ('Enroll', models.PositiveIntegerField()),
                ('std', models.PositiveIntegerField()),
            ],
        ),
    ]
