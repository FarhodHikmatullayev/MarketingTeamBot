from django.db import models


class User(models.Model):
    full_name = models.CharField(max_length=221, null=True, blank=True, verbose_name="F.I.SH")
    username = models.CharField(max_length=221, null=True, blank=True, verbose_name="USERNAME")
    phone = models.CharField(max_length=13, null=True, blank=True, verbose_name="TELEFON RAQAM")
    telegram_id = models.BigIntegerField(unique=True, verbose_name="TELEGRAM ID")
    is_active = models.BooleanField(default=False, verbose_name="Is Active?")

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Foydalanuvchilar'

    def __str__(self):
        return self.full_name


class StatusUsers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="FOYDALANUVCHI")
    at_work = models.BooleanField(default=False, null=True, blank=True, verbose_name="ISHDAMI")

    class Meta:
        db_table = "status"
        verbose_name = "User status"
        verbose_name_plural = "Xodimlar statuslari"

    def __str__(self):
        return f"{self.user.full_name} ning statusi"


class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="FOYDALANUVCHI")
    arrival_time = models.DateTimeField(null=True, blank=True, verbose_name="KELGAN VAQTI")
    departure_time = models.DateTimeField(null=True, blank=True, verbose_name="KETGAN VAQTI")
    total_time = models.DurationField(null=True, blank=True, verbose_name="ISHLAGAN VAQTI")

    class Meta:
        db_table = "registrations"
        verbose_name = 'Registration'
        verbose_name_plural = 'Keldi-ketdi registratsiyalari'

    def __str__(self):
        return f"{self.user.full_name} ning registratsiyasi"


class Applications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications', verbose_name="FOYDALANUVCHI")
    description = models.TextField(null=True, blank=True, verbose_name="IZOH")
    created_at = models.DateTimeField(null=True, blank=True, verbose_name="YARATILGAN VAQT")
    is_confirmed = models.BooleanField(null=True, blank=True, verbose_name="TASDIQLANGANMI")
    confirmed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='confirmed_applications', null=True,
                                     blank=True, verbose_name="TASDIQLAGAN SHAXS")
    confirmed_description = models.TextField(null=True, blank=True, verbose_name="TASDIQLASH IZOHI")
    confirmed_at = models.DateTimeField(null=True, blank=True, verbose_name="TASDIQLANGAN VAQT")

    class Meta:
        db_table = 'applications'
        verbose_name = 'Application'
        verbose_name_plural = 'Arizalar'

    def __str__(self):
        return f"{self.user.full_name} ning arizasi"


class Warnings(models.Model):
    text = models.TextField(null=True, blank=True, verbose_name="TEXT")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='varnings', verbose_name="FOYDALANUVCHI")
    warned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='warned_users',
                                  verbose_name="OGOHLANTIRGAN SHAXS")
    created_at = models.DateTimeField(null=True, blank=True, verbose_name="YARATILGAN VAQT")

    class Meta:
        db_table = 'warnings'
        verbose_name = 'Warning'
        verbose_name_plural = 'Ogohlantirishlar'

    def __str__(self):
        return f"{self.user.full_name} uchun ogohlantirish"


class Schedule(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="FOYDALANUVCHI")
    arrival_time = models.CharField(null=True, blank=True, verbose_name="KELISH VAQTI")
    departure_time = models.CharField(null=True, blank=True, verbose_name="KETISH VAQTI")

    class Meta:
        db_table = 'schedule'
        verbose_name = 'Schedule'
        verbose_name_plural = 'Ish grafiklari'

    def __str__(self):
        return f"{self.user.full_name}"
