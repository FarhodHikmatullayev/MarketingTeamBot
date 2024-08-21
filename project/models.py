from django.db import models


class User(models.Model):
    full_name = models.CharField(max_length=221, null=True, blank=True)
    username = models.CharField(max_length=221, null=True, blank=True)
    phone = models.CharField(max_length=13, null=True, blank=True)
    telegram_id = models.BigIntegerField(unique=True)

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Foydalanuvchilar'

    def __str__(self):
        return self.full_name


class StatusUsers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    at_work = models.BooleanField(default=False, null=True, blank=True)

    class Meta:
        db_table = "status"
        verbose_name = "User status"
        verbose_name_plural = "Xodimlar statuslari"

    def __str__(self):
        return f"{self.user.full_name} ning statusi"


class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    arrival_time = models.DateTimeField(null=True, blank=True)
    departure_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "registrations"
        verbose_name = 'Registration'
        verbose_name_plural = 'Keldi-ketdi registratsiyalari'

    def __str__(self):
        return f"{self.user.full_name} ning registratsiyasi"


class Applications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    is_confirmed = models.BooleanField(null=True, blank=True)
    confirmed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='confirmed_applications', null=True,
                                     blank=True)
    confirmed_description = models.TextField(null=True, blank=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'applications'
        verbose_name = 'Application'
        verbose_name_plural = 'Arizalar'

    def __str__(self):
        return f"{self.user.full_name} ning arizasi"


class Warnings(models.Model):
    text = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='varnings')
    warned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='warned_users')
    created_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'warnings'
        verbose_name = 'Warning'
        verbose_name_plural = 'Ogohlantirishlar'

    def __str__(self):
        return f"{self.user.full_name} uchun ogohlantirish"
