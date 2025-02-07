from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_service', '0006_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='service_man',
            name='experience',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
