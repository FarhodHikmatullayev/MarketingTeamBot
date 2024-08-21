from django.contrib import admin
from .models import User, Applications, Registration, StatusUsers


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(StatusUsers)
class StatusUsersAdmin(admin.ModelAdmin):
    pass


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    pass


@admin.register(Applications)
class ApplicationsAdmin(admin.ModelAdmin):
    pass
