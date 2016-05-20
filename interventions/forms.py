from django import forms
from django.utils.translation import ugettext as _

from core.forms import ConditionalModelForm
from core.utils import YES_NO, get_users_as_list
from .models import Intervention


class InterventionForm(ConditionalModelForm):
    class Meta:
        model = Intervention
        fields = [
            'setting', 'setting_details', 'supervision',
            'period', 'amount_per_week', 'duration',
            'has_prepost', 'prepost_experimenter', 'prepost_description',
            'pre_duration', 'pre_registrations', 'pre_registrations_details', 'pre_registration_kinds', 'pre_registration_kinds_details',
            'post_duration', 'post_registrations', 'post_registrations_details', 'post_registration_kinds', 'post_registration_kinds_details',
            'experimenter', 'description',
            'has_controls', 'controls_description',
            ]
        widgets = {
            'setting': forms.CheckboxSelectMultiple(),
            'supervision': forms.RadioSelect(choices=YES_NO),
            'has_prepost': forms.RadioSelect(choices=YES_NO),
            'pre_registrations': forms.CheckboxSelectMultiple(),
            'pre_registration_kinds': forms.CheckboxSelectMultiple(),
            'post_registrations': forms.CheckboxSelectMultiple(),
            'post_registration_kinds': forms.CheckboxSelectMultiple(),
            'has_controls': forms.RadioSelect(choices=YES_NO),
        }

    def __init__(self, *args, **kwargs):
        """
        - Sets the choices for experimenters to the applicants of the Proposal
        - Sets initial data for has_observation and has_sessions
        """
        self.study = kwargs.pop('study', None)
        super(InterventionForm, self).__init__(*args, **kwargs)
        applicants = get_users_as_list(self.study.proposal.applicants.all())
        self.fields['prepost_experimenter'].choices = applicants

    def clean(self):
        """
        Check for conditional requirements:
        - If a setting which needs details has been checked, make sure the details are filled
        - If has_controls is True, has_controls_details is required
        - If has_recording is True and recording_same_experimenter is set to False check:
        -- Whether the recording_experimenter has been set.
        -- Whether the recording_experimenter is someone else than the experimenter.
        """
        cleaned_data = super(InterventionForm, self).clean()

        self.check_dependency_multiple(cleaned_data, 'setting', 'needs_details', 'setting_details')
        # TODO: this doesn't work as supervision is a boolean value
        self.check_dependency_multiple(cleaned_data, 'setting', 'needs_supervision', 'supervision')

        self.check_dependency(cleaned_data, 'has_prepost', 'prepost_experimenter')
        self.check_dependency(cleaned_data, 'has_prepost', 'prepost_description')
        self.check_dependency(cleaned_data, 'has_prepost', 'pre_duration')
        self.check_dependency(cleaned_data, 'has_prepost', 'pre_registrations')
        self.check_dependency_multiple(cleaned_data, 'pre_registrations', 'needs_kind', 'pre_registration_kinds')
        self.check_dependency_multiple(cleaned_data, 'pre_registrations', 'needs_details', 'pre_registrations_details')
        self.check_dependency_multiple(cleaned_data, 'pre_registration_kinds', 'needs_details', 'pre_registration_kinds_details')
        self.check_dependency(cleaned_data, 'has_prepost', 'post_duration')
        self.check_dependency(cleaned_data, 'has_prepost', 'post_registrations')
        self.check_dependency_multiple(cleaned_data, 'post_registrations', 'needs_kind', 'post_registration_kinds')
        self.check_dependency_multiple(cleaned_data, 'post_registrations', 'needs_details', 'post_registrations_details')
        self.check_dependency_multiple(cleaned_data, 'post_registration_kinds', 'needs_details', 'post_registration_kinds_details')

        self.check_dependency(cleaned_data, 'has_controls', 'controls_description')
