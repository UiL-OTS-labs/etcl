# -*- encoding: utf-8 -*-

from django import forms
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from braces.forms import UserKwargModelFormMixin

from core.forms import ConditionalModelForm
from core.models import YES_NO_DOUBT, YES, NO, DOUBT
from core.utils import YES_NO, get_users_as_list
from .models import Proposal, Wmo, Relation
from .utils import check_local_facilities


class ProposalForm(UserKwargModelFormMixin, ConditionalModelForm):
    class Meta:
        model = Proposal
        fields = [
            'relation', 'supervisor',
            'other_applicants', 'applicants',
            'other_stakeholders', 'stakeholders',
            'date_start', 'title',
            'summary', 'pre_assessment_pdf',
            'funding', 'funding_details', 'funding_name'
        ]
        widgets = {
            'relation': forms.RadioSelect(),
            'other_applicants': forms.RadioSelect(choices=YES_NO),
            'other_stakeholders': forms.RadioSelect(choices=YES_NO),
            'summary': forms.Textarea(attrs={'cols': 50}),
            'funding': forms.CheckboxSelectMultiple()
        }
        error_messages = {
            'title': {
                'unique': _('Er bestaat al een studie met deze titel.'),
            },
        }

    def __init__(self, *args, **kwargs):
        """
        - Remove empty label from relation field
        - Don't allow to pick yourself or a superuser as supervisor, unless you already are
        - Add a None-option for supervisor
        - Don't allow to pick a superuser as applicant
        - If this is a practice Proposal, limit the relation choices
        - Remove summary for preliminary assessment Proposals
        - Set pre_assessment_pdf required for preliminary assessment Proposals, otherwise remove
        """
        in_course = kwargs.pop('in_course', False)
        is_pre_assessment = kwargs.pop('is_pre_assessment', False)

        super(ProposalForm, self).__init__(*args, **kwargs)
        self.fields['relation'].empty_label = None

        applicants = get_user_model().objects.all()

        supervisors = applicants.exclude(pk=self.user.pk)

        instance = kwargs.get('instance')

        # If you are already defined as a supervisor, we have to set it to you
        if instance is not None and instance.supervisor == self.user:
            supervisors = [self.user]

        self.fields['supervisor'].choices = [(None, _('Selecteer...'))] + get_users_as_list(supervisors)
        self.fields['applicants'].choices = get_users_as_list(applicants)

        if in_course:
            self.fields['relation'].queryset = Relation.objects.filter(check_in_course=True)
            self.fields['supervisor'].label = _('Docent')
            self.fields['supervisor'].help_text = _('Vul hier de docent van \
de cursus in waarbinnen je deze portal moet doorlopen. De docent kan na afloop \
de studie inkijken in de portal. De studie zal niet in het semipublieke archief \
van het UiL OTS worden opgenomen.')

        if is_pre_assessment:
            self.fields['relation'].queryset = Relation.objects.filter(check_pre_assessment=True)
            self.fields['pre_assessment_pdf'].required = True
            del self.fields['summary']
            del self.fields['funding']
            del self.fields['funding_details']
            del self.fields['funding_name']
        else:
            del self.fields['pre_assessment_pdf']

    def clean(self):
        """
        Check for conditional requirements:
        - If relation needs supervisor, make sure supervisor is set
        - If other_applicants is checked, make sure applicants are set
        - If other_stakeholders is checked, make sure stakeholders is not empty
        - Maximum number of words for summary
        """
        cleaned_data = super(ProposalForm, self).clean()

        relation = cleaned_data.get('relation')
        if relation and relation.needs_supervisor and not cleaned_data.get('supervisor'):
            error = forms.ValidationError(_('U dient een eindverantwoordelijke op te geven.'), code='required')
            self.add_error('supervisor', error)

        if cleaned_data.get('other_applicants') and len(cleaned_data.get('applicants')) == 1:
            error = forms.ValidationError(_('U heeft geen andere onderzoekers geselecteerd.'), code='required')
            self.add_error('applicants', error)

        self.check_dependency(cleaned_data, 'other_stakeholders', 'stakeholders')
        self.check_dependency_multiple(cleaned_data, 'funding', 'needs_details', 'funding_details')
        self.check_dependency_multiple(cleaned_data, 'funding', 'needs_name', 'funding_name')


class ProposalStartPracticeForm(forms.Form):
    practice_reason = forms.ChoiceField(
        label=_('Ik vul de portal in'),
        choices=Proposal.PRACTICE_REASONS,
        widget=forms.RadioSelect())


class ProposalCopyForm(UserKwargModelFormMixin, forms.ModelForm):
    class Meta:
        model = Proposal
        fields = ['parent', 'is_revision', 'title']
        widgets = {
            'is_revision': forms.RadioSelect(choices=YES_NO),
        }
        error_messages = {
            'title': {
                'unique': _('Er bestaat al een studie met deze titel.'),
            },
        }

    def __init__(self, *args, **kwargs):
        """
        Filters the Proposals to only show those where:
        - the current User is an applicant.
        - the Proposal is not a preliminary assessment or practice Proposal.
        """
        super(ProposalCopyForm, self).__init__(*args, **kwargs)
        self.fields['parent'].queryset = Proposal.objects. \
            filter(applicants=self.user, is_pre_assessment=False, in_course=False, is_exploration=False)


class ProposalConfirmationForm(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = ['date_confirmed', 'confirmation_comments']


class WmoForm(ConditionalModelForm):
    class Meta:
        model = Wmo
        fields = [
            'metc', 'metc_details', 'metc_institution',
            'is_medical', 'is_behavioristic',
        ]
        widgets = {
            'metc': forms.RadioSelect(),
            'is_medical': forms.RadioSelect(),
            'is_behavioristic': forms.RadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        """
        - Remove empty label from is_medical/is_behavioristic field and reset the choices
        """
        super(WmoForm, self).__init__(*args, **kwargs)
        self.fields['is_medical'].empty_label = None
        self.fields['is_medical'].choices = YES_NO_DOUBT
        self.fields['is_behavioristic'].empty_label = None
        self.fields['is_behavioristic'].choices = YES_NO_DOUBT

    def clean(self):
        """
        Check for conditional requirements:
        - If metc is checked, make sure institution is set and details are filled out
        - If metc is not checked, check if is_medical or is_behavioristic is set
        """
        cleaned_data = super(WmoForm, self).clean()

        self.check_dependency(cleaned_data, 'metc', 'metc_details', f1_value=YES)
        self.check_dependency(cleaned_data, 'metc', 'metc_institution',
                              f1_value=YES,
                              error_message=_('U dient een instelling op te geven.'))
        self.check_dependency_list(cleaned_data, 'metc', 'is_medical', f1_value_list=[NO, DOUBT])
        self.check_dependency_list(cleaned_data, 'metc', 'is_behavioristic', f1_value_list=[NO, DOUBT])


class WmoCheckForm(forms.ModelForm):
    class Meta:
        model = Wmo
        fields = [
            'metc', 'is_medical', 'is_behavioristic',
        ]
        widgets = {
            'metc': forms.RadioSelect(),
            'is_medical': forms.RadioSelect(),
            'is_behavioristic': forms.RadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        """
        - Remove empty label from is_medical/is_behavioristic field and reset the choices
        """
        super(WmoCheckForm, self).__init__(*args, **kwargs)
        self.fields['is_medical'].empty_label = None
        self.fields['is_medical'].choices = YES_NO_DOUBT
        self.fields['is_behavioristic'].empty_label = None
        self.fields['is_behavioristic'].choices = YES_NO_DOUBT


class WmoApplicationForm(ConditionalModelForm):
    class Meta:
        model = Wmo
        fields = [
            'metc_application', 'metc_decision', 'metc_decision_pdf',
        ]
        widgets = {
            'metc_application': forms.RadioSelect(choices=YES_NO),
            'metc_decision': forms.RadioSelect(choices=YES_NO),
        }

    def clean(self):
        """
        Check for conditional requirements:
        - If metc_decision has been checked, make sure the file is added
        """
        cleaned_data = super(WmoApplicationForm, self).clean()

        self.check_dependency(cleaned_data, 'metc_decision', 'metc_decision_pdf')


class StudyStartForm(forms.ModelForm):
    study_name_1 = forms.CharField(label=_('Naam traject 1'), max_length=15, required=False)
    study_name_2 = forms.CharField(label=_('Naam traject 2'), max_length=15, required=False)
    study_name_3 = forms.CharField(label=_('Naam traject 3'), max_length=15, required=False)
    study_name_4 = forms.CharField(label=_('Naam traject 4'), max_length=15, required=False)
    study_name_5 = forms.CharField(label=_('Naam traject 5'), max_length=15, required=False)

    class Meta:
        model = Proposal
        fields = [
            'studies_similar', 'studies_number',
            'study_name_1', 'study_name_2', 'study_name_3', 'study_name_4', 'study_name_5'
        ]
        widgets = {
            'studies_similar': forms.RadioSelect(choices=YES_NO),
        }

    def __init__(self, *args, **kwargs):
        """
        - Set the Proposal for later reference
        - Set initial data for the study_name fields
        """
        self.proposal = kwargs.pop('proposal', None)

        super(StudyStartForm, self).__init__(*args, **kwargs)

        for n, study in enumerate(self.proposal.study_set.all()):
            study_name = 'study_name_' + str(n + 1)
            self.fields[study_name].initial = study.name

    def clean(self):
        """
        Check for conditional requirements:
        - If studies_similar is not set, add a required error
        - If studies_similar is set to False, make sure studies_number is set (and higher than 2)
        - If studies_number is set, make sure the corresponding name fields are filled.
        """
        cleaned_data = super(StudyStartForm, self).clean()

        if cleaned_data['studies_similar'] is None:
            self.add_error('studies_similar', _('Dit veld is verplicht.'))
        elif not cleaned_data['studies_similar']:
            nr_studies = cleaned_data['studies_number']
            if cleaned_data['studies_number'] < 2:
                self.add_error('studies_number', _('Als niet dezelfde trajecten worden doorlopen, moeten er minstens twee verschillende trajecten zijn.'))
            for n in xrange(nr_studies):
                if n >= 5:
                    break
                study_name = 'study_name_' + str(n + 1)
                if not cleaned_data[study_name]:
                    self.add_error(study_name, _('Dit veld is verplicht.'))


class ProposalDataManagementForm(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = []


class ProposalSubmitForm(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = ['comments', 'inform_local_staff']
        widgets = {
            'inform_local_staff': forms.RadioSelect(choices=YES_NO),
        }

    def __init__(self, *args, **kwargs):
        """
        - Mark the label of inform_local_staff as safe
        - Check if the inform_local_staff question should be asked
        """
        self.proposal = kwargs.pop('proposal', None)

        super(ProposalSubmitForm, self).__init__(*args, **kwargs)

        self.fields['inform_local_staff'].label = mark_safe(self.fields['inform_local_staff'].label)

        if not check_local_facilities(self.proposal):
            del self.fields['inform_local_staff']

    def clean(self):
        """
        Check if the Proposal is complete:
        - Do all Studies have informed consent/briefing?
        - If the inform_local_staff question is asked, it is required
        """
        cleaned_data = super(ProposalSubmitForm, self).clean()

        if not self.instance.is_pre_assessment and not self.instance.is_practice():
            for study in self.instance.study_set.all():
                if study.passive_consent:
                    if not study.director_consent_declaration:
                        self.add_error('comments', _('Toestemmingsverklaring voor traject {} nog niet toegevoegd.').format(study.order))
                    if not study.director_consent_information:
                        self.add_error('comments', _('Informatiebrief voor traject {} nog niet toegevoegd.').format(study.order))
                    if not study.parents_information:
                        self.add_error('comments', _('Informatiebrief voor traject {} nog niet toegevoegd.').format(study.order))
                else:
                    if not study.informed_consent:
                        self.add_error('comments', _('Toestemmingsverklaring voor traject {} nog niet toegevoegd.').format(study.order))
                    if not study.briefing:
                        self.add_error('comments', _('Informatiebrief voor traject {} nog niet toegevoegd.').format(study.order))

        if check_local_facilities(self.proposal) and cleaned_data['inform_local_staff'] is None:
            self.add_error('inform_local_staff', _('Dit veld is verplicht.'))
