# Generated by Django 4.1.5 on 2023-02-04 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignment_submissions', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='score',
            field=models.IntegerField(default=0),
        ),
    ]
