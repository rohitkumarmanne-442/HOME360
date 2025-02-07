from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_service', '0008_service_category_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='report_status',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
