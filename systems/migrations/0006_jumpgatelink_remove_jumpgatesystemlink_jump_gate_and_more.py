# Generated by Django 4.2.6 on 2023-10-30 20:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('systems', '0005_alter_tradegood_symbol'),
    ]

    operations = [
        migrations.CreateModel(
            name='JumpGateLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='systems.waypoint')),
                ('jump_gate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jump_gate_link', to='systems.waypoint')),
            ],
        ),
        migrations.RemoveField(
            model_name='jumpgatesystemlink',
            name='jump_gate',
        ),
        migrations.RemoveField(
            model_name='jumpgatesystemlink',
            name='system',
        ),
        migrations.DeleteModel(
            name='JumpGate',
        ),
        migrations.DeleteModel(
            name='JumpGateSystemLink',
        ),
    ]
