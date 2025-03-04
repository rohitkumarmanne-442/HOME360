from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home_service', '0005_id_card'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_date', models.DateField(null=True)),
                ('book_days', models.CharField(max_length=100, null=True)),
                ('book_hours', models.CharField(max_length=100, null=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home_service.Customer')),
                ('service', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home_service.Service_Man')),
                ('status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home_service.Status')),
            ],
        ),
    ]
