# Generated by Django 2.0 on 2019-03-31 21:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('colleges', '0004_teacher_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='user',
        ),
    ]
