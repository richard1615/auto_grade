
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
