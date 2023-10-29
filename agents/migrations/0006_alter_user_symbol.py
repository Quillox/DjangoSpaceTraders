# Generated by Django 4.2.6 on 2023-10-29 17:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agents', '0005_user_symbol'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='symbol',
            field=models.ForeignKey(help_text='The symbol of the SpaceTraders agent associated with this user.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='django_user', to='agents.agent'),
        ),
    ]
