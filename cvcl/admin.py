from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import AdminSite
from django.contrib import admin
from .models import *


class CloudVCLAdminSite(AdminSite):
    site_header = 'Cloud Virtual Computing Lab'
    site_title = 'Cloud VCL'


admin_site = CloudVCLAdminSite(name='myadmin')
admin_site.register(Flavor)
admin_site.register(Image)


@admin.register(Assignment, site=admin_site)
class CustomAssignmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'environment_definition', 'is_current')
    list_display_links = ('course', 'environment_definition')
    list_filter = ('course', 'environment_definition',)


@admin.register(Course, site=admin_site)
class CustomCourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'instructor',)
    list_display_links = ('instructor',)
    list_filter = ('instructor',)


@admin.register(Environment, site=admin_site)
class CustomEnvironmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'assignment', 'course',)
    list_display_links = ('user', 'assignment', 'course',)
    list_filter = ('assignment',)


@admin.register(User, site=admin_site)
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


class VmDefinitionInline(admin.TabularInline):
    model = VmDefinition
    extra = 1


@admin.register(EnvironmentDefinition, site=admin_site)
class CustomEnvironmentDefinitionAdmin(admin.ModelAdmin):
    list_display = ('name', 'instructor',)
    list_display_links = ('instructor',)
    list_filter = ('instructor',)
    inlines = [
        VmDefinitionInline,
    ]


@admin.register(Vm, site=admin_site)
class CustomVmAdmin(admin.ModelAdmin):
    list_display = ('environment', 'uuid', 'name', 'user', 'assignment', 'course',)
    list_display_links = ('environment', 'user', 'assignment', 'course',)
    list_filter = ('environment__assignment', 'environment__assignment__course')


@admin.register(VmDefinition, site=admin_site)
class VmDefinition(admin.ModelAdmin):
    list_display = ('name', 'image', 'flavor',)
    list_display_links = ('image', 'flavor',)
    list_filter = ('image', 'flavor',)
