from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_service', '0002_auto_20200704_1446'),
    ]

    operations = [
        migrations.AddField(
            model_name='service_man',
            name='service_name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
