# Generated by Django 3.2.12 on 2022-04-02 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QAS', '0003_auto_20220402_1917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notice',
            name='file_id',
            field=models.IntegerField(null=True, unique=True, verbose_name='文件编号'),
        ),
    ]
