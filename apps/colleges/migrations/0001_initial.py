# Generated by Django 2.0 on 2019-03-17 19:16

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CollegeOrg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='学院名称')),
                ('desc', models.TextField(verbose_name='学院描述')),
                ('click_nums', models.IntegerField(default=0, verbose_name='点击数')),
                ('fav_nums', models.IntegerField(default=0, verbose_name='收藏数')),
                ('image', models.ImageField(upload_to='college_org/%Y/%m', verbose_name='封面图')),
                ('address', models.CharField(max_length=150, verbose_name='学院地址')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'verbose_name': '学院机构',
                'verbose_name_plural': '学院机构',
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='讲师名称')),
                ('work_years', models.IntegerField(default=0, verbose_name='工作年限')),
                ('address', models.CharField(max_length=150, verbose_name='办公地址')),
                ('points', models.CharField(max_length=50, verbose_name='教学特点')),
                ('click_nums', models.IntegerField(default=0, verbose_name='点击数')),
                ('fav_nums', models.IntegerField(default=0, verbose_name='收藏数')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now)),
                ('college_org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='colleges.CollegeOrg', verbose_name='所属学院')),
            ],
            options={
                'verbose_name': '讲师',
                'verbose_name_plural': '讲师',
            },
        ),
    ]