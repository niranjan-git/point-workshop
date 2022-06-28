from django.contrib import admin
from import_export.admin import ExportActionMixin, ImportExportMixin
from . import models
from . import forms

# Register your models here.

# admin.site.register(models.State)
# admin.site.register(models.City)
# admin.site.register(models.Role)
# admin.site.register(models.Zone)
# admin.site.register(models.ZoneStateMap)
# admin.site.register(models.Branch)
# admin.site.register(models.UserAssignedRole)

# admin.site.register(models.Batch)
# admin.site.register(models.Participant)
# admin.site.register(models.EnrolledParticipant)


@admin.register(models.Batch)
class BatchModelAdmin(ImportExportMixin, ExportActionMixin, admin.ModelAdmin):
    list_display = ('name', 'is_active', 'st_date', 'en_date', 'remarks')
    fields = ('name', ('st_date', 'en_date'), 'remarks', 'is_active')
    ordering = ('name',)

    list_filter = ('is_active', 'st_date', 'en_date')

    search_fields = ['name', 'remarks']



@admin.register(models.Branch)
class BranchModelAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('zone', 'branch_code', 'branch_name', 'remarks')
    fields = ('branch_code', 'branch_name', 'remarks')
    ordering = ('zone',)

    list_filter = ('zone',)

    search_fields = ['zone', 'branch_code', 'branch_name', 'remarks']



@admin.register(models.City)
class CityModelAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('state', 'city_code', 'city_name')
    fields = ('state', 'city_code', 'city_name')
    ordering = ('state',)

    list_filter = ('state',)

    search_fields = ['state', 'city_code', 'city_name']



@admin.register(models.State)
class StateModelAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('state_code', 'state_name')
    fields = ('state_code', 'state_name')
    ordering = ('state_code',)

    # list_filter = ('state_code',)

    search_fields = ['state_code', 'state_name']


@admin.register(models.Zone)
class ZoneModelAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('zone_code', 'zone_name', 'remarks')
    fields = ('zone_code', 'zone_name', 'remarks')
    ordering = ('zone_code',)

    search_fields = ['zone_code', 'zone_name', 'remarks']


@admin.register(models.ZoneStateMap)
class ZoneStateMapModelAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('zone', 'state')
    fields = ('zone', 'state')
    ordering = ('zone',)
    list_filter = ('zone',)

    search_fields = ['zone', 'state']



@admin.register(models.Participant)
class ParticipantModelAdmin(ImportExportMixin, ExportActionMixin, admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_no', 'zone', 'branch', 'is_active')
    fields = ('name', 'email', 'phone_no', 'branch', 'is_active')
    ordering = ('name',)

    list_filter = ('is_active', 'branch')

    search_fields = ['name', 'email', 'phone_no', 'branch']

    def zone(self, obj):
        return obj.branch.zone
    zone.short_description = 'Zone'



@admin.register(models.EnrolledParticipant)
class EnrolledParticipantModelAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('batch', 'participant')
    fields = ('batch', 'participant')
    ordering = ('batch',)

    list_filter = ('batch',)

    search_fields = ['batch', 'participant']


@admin.register(models.Role)
class RoleModelAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('role_short_name', 'role_full_name')
    fields = ('role_short_name', 'role_full_name')
    ordering = ('role_short_name',)

    search_fields = ['role_short_name', 'role_full_name']


@admin.register(models.UserAssignedRole)
class UserAssignedRoleModelAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('name', 'user', 'role', 'zone', 'branch', 'user_status')
    fields = ('user', 'role', 'zone', 'branch')
    ordering = ('user',)
    list_filter = ('role', 'zone', 'branch')

    search_fields = ['user', 'role', 'zone', 'branch']

    def user_status(self, obj):
        return obj.user.is_active
    user_status.short_description = 'Active'

    def name(self, obj):
        return obj.user.name
    name.short_description = 'Name'