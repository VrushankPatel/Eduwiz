# Generated by Django 2.2.7 on 2020-12-25 05:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='administrator',
            name='dashboard_id',
        ),
        migrations.RemoveField(
            model_name='administrator',
            name='dashboard_pwd',
        ),
    ]