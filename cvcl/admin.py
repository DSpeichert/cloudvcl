from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import AdminSite
from django.contrib import admin
from .models import *


class CloudVCLAdminSite(AdminSite):
    site_header = 'Cloud Virtual Computing Lab'
    site_title = 'Cloud VCL'


admin_site = CloudVCLAdminSite(name='myadmin')


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


@admin.register(Flavor, site=admin_site)
class CustomFlavorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'vcpus', 'ram', 'swap', 'disk',)
    list_filter = ('vcpus', 'ram', 'swap', 'disk',)
    readonly_fields = ('vcpus', 'ram', 'swap', 'disk',)


@admin.register(Image, site=admin_site)
class CustomImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'size', 'min_ram', 'min_disk',)
    list_filter = ('min_ram', 'min_disk',)
    readonly_fields = ('min_ram', 'min_disk',)


@admin.register(User, site=admin_site)
class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('is_instructor', 'usage_instances', 'limit_instances', 'usage_vcpus',
                                             'limit_vcpus', 'usage_ram', 'limit_ram', 'usage_disk', 'limit_disk',)
    list_filter = UserAdmin.list_filter + ('is_instructor',)
    fieldsets = UserAdmin.fieldsets + (
        ('Instructor Data', {'fields': ('is_instructor',
                                        'limit_instances',
                                        'limit_vcpus',
                                        'limit_ram',
                                        'limit_disk',
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
class CustomVmDefinitionAdmin(admin.ModelAdmin):
    list_display = ('name', 'image', 'flavor',)
    list_display_links = ('name', 'image', 'flavor',)
    list_filter = ('image', 'flavor',)


@admin.register(IPOwnerHistory, site=admin_site)
class CustomIPOwnerHistoryAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'end_at', 'ip_address', 'user', 'vm',)
    list_display_links = ('ip_address', 'user', 'vm',)
