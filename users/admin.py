from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    list_display = ('id','name', 'documento', 'email', 'rol', 'is_staff', 'is_active')
    list_filter = ('rol', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('documento', 'password')}),
        ('Personal info', {'fields': ('name', 'email', 'rol')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('documento', 'name', 'email', 'rol', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )
    search_fields = ('documento', 'name', 'email')
    ordering = ('name',)
    filter_horizontal = ()

# Registrar el modelo de usuario con la clase UserAdmin personalizada
admin.site.register(User, UserAdmin)
