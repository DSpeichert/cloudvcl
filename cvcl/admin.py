from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import *

admin.site.register(Assignment)
admin.site.register(Environment)
admin.site.register(EnvironmentDefinition)
admin.site.register(Flavor)
admin.site.register(Image)
admin.site.register(Course)
admin.site.register(Vm)
admin.site.register(VmDefinition)


class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('is_instructor',)
    list_filter = UserAdmin.list_filter + ('is_instructor',)
    fieldsets = UserAdmin.fieldsets
    fieldsets[2][1]['fields'] = ('is_active', 'is_instructor', 'is_staff', 'is_superuser',
                                  'groups', 'user_permissions',)


admin.site.register(User, CustomUserAdmin)
