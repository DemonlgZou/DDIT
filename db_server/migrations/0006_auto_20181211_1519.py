# Generated by Django 2.1.3 on 2018-12-11 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db_server', '0005_auto_20181211_1503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monitor_host',
            name='on_line',
            field=models.CharField(max_length=256, null=True, verbose_name='状态'),
        ),
        migrations.AlterField(
            model_name='monitor_host',
            name='pwd',
            field=models.CharField(max_length=256, null=True, verbose_name='密码'),
        ),
        migrations.AlterField(
            model_name='monitor_host',
            name='user',
            field=models.CharField(max_length=32, null=True, verbose_name='用户名'),
        ),
    ]