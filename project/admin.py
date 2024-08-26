from django.contrib import admin
from .models import User, Applications, Registration, StatusUsers


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'username', 'phone', 'telegram_id')
    search_fields = ('username', 'phone', 'telegram_id')


@admin.register(StatusUsers)
class StatusUsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'user__full_name', 'at_work')
    search_fields = ('user__full_name',)


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user__full_name', 'arrival_time', 'departure_time', 'total_time')
    search_fields = ('user__full_name',)
    list_filter = ('arrival_time', 'departure_time')
    readonly_fields = ('arrival_time', 'departure_time', 'total_time')
    date_hierarchy = 'arrival_time'


@admin.register(Applications)
class ApplicationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user__full_name', 'is_confirmed', 'confirmed_by', 'created_at', 'confirmed_at')
    readonly_fields = ('confirmed_at', 'created_at')
    list_filter = ('confirmed_at', 'created_at')
    date_hierarchy = 'created_at'
    search_fields = ('user__full_name', 'confirmed_by__full_name')
