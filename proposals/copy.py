from django.utils import timezone

from .models import Task
from .utils import generate_ref_number


def copy_proposal(self, form):
    parent = form.cleaned_data['parent']
    title = form.cleaned_data['title']

    # Save relationships
    relation = parent.relation
    applicants = parent.applicants.all()  # TODO: what if current user not in applicants?
    copy_wmo = None
    copy_study = None
    if hasattr(parent, 'wmo'):
        copy_wmo = parent.wmo
    if hasattr(parent, 'study'):
        copy_study = parent.study
        copy_age_groups = parent.study.age_groups.all()
        copy_traits = parent.study.traits.all()
        copy_setting = parent.study.setting.all()
        copy_compensation = parent.study.compensation
        copy_recruitment = parent.study.recruitment.all()
        copy_surveys = parent.study.survey_set.all()

    copy_sessions = parent.session_set.all()

    # Create copy and save the this new model, set it to not-submitted
    copy_proposal = parent
    copy_proposal.pk = None
    copy_proposal.reference_number = generate_ref_number(self.request.user)
    copy_proposal.title = title
    copy_proposal.created_by = self.request.user
    copy_proposal.date_created = timezone.now()
    copy_proposal.date_modified = timezone.now()
    copy_proposal.date_submitted_supervisor = None
    copy_proposal.date_reviewed_supervisor = None
    copy_proposal.date_submitted = None
    copy_proposal.date_reviewed = None
    copy_proposal.save()

    # Copy references
    copy_proposal.relation = relation
    copy_proposal.applicants = applicants
    copy_proposal.parent = parent

    # Copy linked models
    if copy_wmo:
        copy_wmo.pk = copy_proposal.pk
        copy_wmo.save()

    if copy_study:
        copy_study.pk = copy_proposal.pk
        copy_study.age_groups = copy_age_groups
        copy_study.traits = copy_traits
        copy_study.setting = copy_setting
        copy_study.compensation = copy_compensation
        copy_study.recruitment = copy_recruitment
        for survey in copy_surveys:
            copy_survey = survey
            copy_survey.pk = None
            copy_survey.study = copy_study
            copy_survey.save()
        copy_study.save()

    for session in copy_sessions:
        copy_session = session
        copy_session.pk = None
        copy_session.proposal = copy_proposal
        copy_session.save()
        for task in Task.objects.filter(session__proposal=parent).prefetch_related('registrations'):  # TODO: this does not seem to work.
            copy_registrations = task.registrations.all()
            copy_task = task
            copy_task.pk = None
            copy_task.session = copy_session
            copy_task.save()
            copy_task.registrations = copy_registrations
            copy_task.save()

    copy_proposal.save()

    return copy_proposal
