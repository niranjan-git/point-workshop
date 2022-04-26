from django import forms
from . import models



class PicodeForm(forms.ModelForm):
    class Meta:
        model = models.Pincode
        fields = ('pincode', 'state', 'city')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = models.City.objects.none()

        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                self.fields['city'].queryset = models.City.objects.filter(state_id=state_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.state.city_set.order_by('name')


# StateModel
# CityModel
# PincodeModel
# ZoneModel
# BranchModel