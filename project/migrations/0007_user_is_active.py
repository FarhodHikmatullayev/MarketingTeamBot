# Generated by Django 5.1.1 on 2024-09-21 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0006_alter_applications_confirmed_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='Is Active?'),
        ),
    ]
