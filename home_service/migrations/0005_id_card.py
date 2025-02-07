from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_service', '0004_service_category_desc'),
    ]

    operations = [
        migrations.CreateModel(
            name='ID_Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card', models.CharField(max_length=30, null=True)),
            ],
        ),
    ]
