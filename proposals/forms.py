from django import forms

from .models import Wmo, Study, Task

yes_no_doubt = [(True, "ja"), (False, "nee"), (None, "twijfel")]

class WmoForm(forms.ModelForm):
    class Meta:
        model = Wmo
        fields = ['metc', 'metc_institution', 'is_medical', 'is_behavioristic', 'metc_decision']
        widgets = {
            'metc': forms.RadioSelect(choices=yes_no_doubt),
            'is_medical': forms.RadioSelect(choices=yes_no_doubt),
            'is_behavioristic': forms.RadioSelect(choices=yes_no_doubt),
        }

class StudyForm(forms.ModelForm):
    class Meta:
        model = Study
        fields = ['age_groups', 'traits', 'traits_details', 'necessity', 'necessity_reason', 'setting', 'setting_details', \
            'risk_physical', 'risk_psychological', 'compensation', 'recruitment', 'recruitment_details']
        widgets = {
            'age_groups': forms.CheckboxSelectMultiple(),
            'traits': forms.CheckboxSelectMultiple(),
            'necessity': forms.RadioSelect(choices=yes_no_doubt),
            'risk_physical': forms.RadioSelect(choices=yes_no_doubt),
            'setting': forms.CheckboxSelectMultiple(),
            'risk_psychological': forms.RadioSelect(choices=yes_no_doubt),
            'recruitment': forms.CheckboxSelectMultiple(),
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'procedure', 'duration', 'actions', 'registrations', 'registrations_details']
        widgets = {
            'procedure': forms.RadioSelect(choices=yes_no_doubt),
            'actions': forms.CheckboxSelectMultiple(),
            'registrations': forms.CheckboxSelectMultiple(),
        }
