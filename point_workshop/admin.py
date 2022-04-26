from django.contrib import admin
from . import models
from . import forms

# Register your models here.

admin.site.register(models.State)
admin.site.register(models.City)
admin.site.register(models.Role)
admin.site.register(models.Zone)
admin.site.register(models.Branch)
admin.site.register(models.UserAssignedRole)


@admin.register(models.Pincode)
class PincodeModelAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            kwargs['form'] = forms.PicodeForm
        return super().get_form(request, obj, **kwargs)
