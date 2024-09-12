# Generated by Django 5.1.1 on 2024-09-12 09:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0005_registration_total_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applications',
            name='confirmed_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='TASDIQLANGAN VAQT'),
        ),
        migrations.AlterField(
            model_name='applications',
            name='confirmed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='confirmed_applications', to='project.user', verbose_name='TASDIQLAGAN SHAXS'),
        ),
        migrations.AlterField(
            model_name='applications',
            name='confirmed_description',
            field=models.TextField(blank=True, null=True, verbose_name='TASDIQLASH IZOHI'),
        ),
        migrations.AlterField(
            model_name='applications',
            name='created_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='YARATILGAN VAQT'),
        ),
        migrations.AlterField(
            model_name='applications',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='IZOH'),
        ),
        migrations.AlterField(
            model_name='applications',
            name='is_confirmed',
            field=models.BooleanField(blank=True, null=True, verbose_name='TASDIQLANGANMI'),
        ),
        migrations.AlterField(
            model_name='applications',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='project.user', verbose_name='FOYDALANUVCHI'),
        ),
        migrations.AlterField(
            model_name='registration',
            name='arrival_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='KELGAN VAQTI'),
        ),
        migrations.AlterField(
            model_name='registration',
            name='departure_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='KETGAN VAQTI'),
        ),
        migrations.AlterField(
            model_name='registration',
            name='total_time',
            field=models.DurationField(blank=True, null=True, verbose_name='ISHLAGAN VAQTI'),
        ),
        migrations.AlterField(
            model_name='registration',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.user', verbose_name='FOYDALANUVCHI'),
        ),
        migrations.AlterField(
            model_name='statususers',
            name='at_work',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='ISHDAMI'),
        ),
        migrations.AlterField(
            model_name='statususers',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='project.user', verbose_name='FOYDALANUVCHI'),
        ),
        migrations.AlterField(
            model_name='user',
            name='full_name',
            field=models.CharField(blank=True, max_length=221, null=True, verbose_name='F.I.SH'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=13, null=True, verbose_name='TELEFON RAQAM'),
        ),
        migrations.AlterField(
            model_name='user',
            name='telegram_id',
            field=models.BigIntegerField(unique=True, verbose_name='TELEGRAM ID'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, max_length=221, null=True, verbose_name='USERNAME'),
        ),
        migrations.AlterField(
            model_name='warnings',
            name='created_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='YARATILGAN VAQT'),
        ),
        migrations.AlterField(
            model_name='warnings',
            name='text',
            field=models.TextField(blank=True, null=True, verbose_name='TEXT'),
        ),
        migrations.AlterField(
            model_name='warnings',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='varnings', to='project.user', verbose_name='FOYDALANUVCHI'),
        ),
        migrations.AlterField(
            model_name='warnings',
            name='warned_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='warned_users', to='project.user', verbose_name='OGOHLANTIRGAN SHAXS'),
        ),
    ]
