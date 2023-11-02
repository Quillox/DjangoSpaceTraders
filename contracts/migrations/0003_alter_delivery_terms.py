# Generated by Django 4.2.6 on 2023-11-02 17:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivery',
            name='terms',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deliveries', to='contracts.terms'),
        ),
    ]
