# Generated by Django 2.1.3 on 2018-12-11 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db_server', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='monitor_host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_created=True, auto_now_add=True, verbose_name='创建时间')),
                ('name', models.CharField(max_length=128, verbose_name='机器名')),
                ('ip', models.GenericIPAddressField(unique=True, verbose_name='主机地址')),
                ('cpu', models.FloatField(null=True, verbose_name='CPU百分比')),
                ('meminfo', models.FloatField(null=True, verbose_name='内存百分比')),
                ('diskinfo', models.FloatField(null=True, verbose_name='磁盘百分比')),
                ('netinfo', models.FloatField(null=True, verbose_name='网络百分比')),
                ('user', models.CharField(max_length=32, verbose_name='用户名')),
                ('pwd', models.CharField(max_length=256, verbose_name='密码')),
            ],
            options={
                'db_table': 'ddit_monitor_host',
            },
        ),
    ]
