from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='commandqueue',
            name='machine_id',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
    ]
