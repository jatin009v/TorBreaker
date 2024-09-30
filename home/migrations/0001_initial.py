# Generated by Django 5.0.4 on 2024-04-06 00:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pipeline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('sequenceno', models.IntegerField(default=1)),
                ('cmd', models.TextField(default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ActiveScan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('is_completed', models.BooleanField(default=False)),
                ('pipeline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.pipeline')),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vulnerability_type', models.CharField(default='', max_length=100)),
                ('is_vulnerable', models.BooleanField(default=False)),
                ('payload', models.TextField(default='', max_length=255)),
                ('endpoint', models.CharField(default='', max_length=100)),
                ('url', models.CharField(default='', max_length=255)),
                ('active_scan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.activescan')),
            ],
        ),
    ]
