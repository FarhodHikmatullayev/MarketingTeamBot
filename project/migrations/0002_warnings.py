# Generated by Django 5.1 on 2024-08-20 10:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Warnings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='varnings', to='project.user')),
                ('warned_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='warned_users', to='project.user')),
            ],
            options={
                'verbose_name': 'Warning',
                'verbose_name_plural': 'Ogohlantirishlar',
                'db_table': 'warnings',
            },
        ),
    ]
