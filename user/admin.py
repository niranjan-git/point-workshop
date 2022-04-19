from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User , Role

# Register your models here.


admin.site.register(Role)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password', 'last_login', 'roles')}),
        ('Permissions', {'fields': (
            'is_active', 
            'is_staff', 
            'is_superuser',
            'groups', 
            'user_permissions',
        )}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2')
            }
        ),
    )


    ordering = ('email',)
    list_display = ('email', 'is_staff', 'is_active')
    search_fields = ('email',)
    
    

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)
