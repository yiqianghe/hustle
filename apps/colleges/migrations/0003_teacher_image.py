# Generated by Django 2.0 on 2019-03-24 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('colleges', '0002_auto_20190324_1512'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='image',
            field=models.ImageField(default='', upload_to='teacher/%Y/%m', verbose_name='讲师封面'),
        ),
    ]
