# Generated by Django 2.1.3 on 2018-12-11 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db_server', '0004_monitor_host_on_line'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='host_info',
            name='Display',
        ),
        migrations.AddField(
            model_name='monitor_host',
            name='update_at',
            field=models.DateTimeField(auto_created=True, auto_now=True, verbose_name='更新时间'),
        ),
    ]