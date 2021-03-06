# Generated by Django 2.0 on 2019-03-31 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_userprofile_teacher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='grade',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(blank=True, default='image/default.png', null=True, upload_to='image/%Y/%m'),
        ),
    ]
