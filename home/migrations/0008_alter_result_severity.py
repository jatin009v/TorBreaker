# Generated by Django 5.0.4 on 2024-05-03 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_result_website'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='severity',
            field=models.CharField(choices=[('low', 'low'), ('medium', 'medium'), ('high', 'high'), ('critical', 'critical')], default='low', max_length=10),
        ),
    ]
