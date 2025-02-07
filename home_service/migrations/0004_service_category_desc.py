from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_service', '0003_service_man_service_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='service_category',
            name='desc',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
