from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import *

admin.site.register(Environment)
admin.site.register(EnvironmentDefinition)
admin.site.register(Flavor)
admin.site.register(Image)
admin.site.register(Vm)
admin.site.register(VmDefinition)


@admin.register(Assignment)
class CustomAssignmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'course',)
    list_filter = ('course',)


@admin.register(Course)
class CustomCourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'instructor',)
    list_filter = ('instructor',)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('is_instructor',)
    list_filter = UserAdmin.list_filter + ('is_instructor',)
    fieldsets = UserAdmin.fieldsets + (
        ('Instructor Data', {'fields': ('is_instructor',
                                        'limit_instances',
                                        'limit_cpus',
                                        'limit_ram',
                                        'images',
                                        )
                             }
         ),
    )
