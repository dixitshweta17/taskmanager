from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from user.models import User

# Register your models here.
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        (_("Personal info"), {"fields": ("first_name","last_name", "role")}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'groups', 'user_permissions',)}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ("first_name","last_name",'email', 'password1', 'password2', 'role', 'is_active', 'is_staff', 'is_superuser'),
            },
        ),
    )
    list_display = ['email', "first_name","last_name", 'role', 'is_staff', 'is_superuser', 'is_active']
    search_fields = ('email', "first_name","last_name", 'role')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups',)

admin.site.register(User, UserAdmin)