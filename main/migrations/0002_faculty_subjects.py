# Generated by Django 5.1.6 on 2025-02-28 13:32

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Subjects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
                ('classes_per_week', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('Faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.faculty')),
            ],
        ),
    ]
