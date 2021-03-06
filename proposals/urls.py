from django.conf.urls import url, include

from .views.proposal_views import MyConceptsView, MyPracticeView, \
    MySubmittedView, MyCompletedView, MySupervisedView, MyProposalsView, \
    ProposalCreate, ProposalUpdate, ProposalDelete, ProposalStart, \
    ProposalDataManagement, ProposalSubmit, ProposalSubmitted, \
    ProposalConfirmation, ProposalCopy, ProposalCopyRevision, \
    ProposalDifference, ProposalAsPdf, EmptyPDF, ProposalCreatePreAssessment, \
    ProposalUpdatePreAssessment, ProposalStartPreAssessment, \
    ProposalSubmitPreAssessment, ProposalSubmittedPreAssessment, \
    ProposalCreatePractice, ProposalUpdatePractice, ProposalStartPractice, \
    HideFromArchiveView, ProposalsExportView, ProposalStartPreApproved, \
    ProposalCreatePreApproved, ProposalSubmittedPreApproved, \
    ProposalSubmitPreApproved, ProposalUpdatePreApproved, ProposalArchiveView, \
    ProposalCopyAmendment

from .views.study_views import StudyStart, StudyConsent
from .views.wmo_views import WmoCreate, WmoUpdate, \
    WmoApplication, WmoCheck, check_wmo, \
    WmoCreatePreAssessment, WmoUpdatePreAssessment

app_name = 'proposals'

urlpatterns = [
    # List views
    url(r'^archive/', include([
        url(r'^export/(?P<pk>\d+)?$', ProposalsExportView.as_view(),
            name='archive_export'),
        url(r'^hide/(?P<pk>\d+)/$', HideFromArchiveView.as_view(),
            name='archive_hide'),
        # WARNING! This one needs to be LAST in the list. (Django goes
        # through the list and picks the first one that fits, and the regex
        # will always fit for the other 2 URL's, effectively superseding them
        # if it's above them).
        url(r'^(?P<committee>\w+)/$', ProposalArchiveView.as_view(),
            name='archive'),
    ])),

    url(r'^my_concepts/$', MyConceptsView.as_view(), name='my_concepts'),
    url(r'^my_practice/$', MyPracticeView.as_view(), name='my_practice'),
    url(r'^my_submitted/$', MySubmittedView.as_view(), name='my_submitted'),
    url(r'^my_completed/$', MyCompletedView.as_view(), name='my_completed'),
    url(r'^my_supervised/$', MySupervisedView.as_view(), name='my_supervised'),
    url(r'^my_archive/$', MyProposalsView.as_view(), name='my_archive'),

    # Proposal
    url(r'^create/', include([
        url(r'^$', ProposalCreate.as_view(), name='create'),
        url(r'^pre/$', ProposalCreatePreAssessment.as_view(),
            name='create_pre'),
        url(r'^practice/(?P<reason>\d+)/$', ProposalCreatePractice.as_view(),
            name='create_practice'),
        url(r'^pre_approved/$', ProposalCreatePreApproved.as_view(),
            name='create_pre_approved'),
    ])),
    url(r'^update/(?P<pk>\d+)/', include([
        url(r'^$', ProposalUpdate.as_view(), name='update'),
        url(r'^pre/$', ProposalUpdatePreAssessment.as_view(),
            name='update_pre'),
        url(r'^practice/$', ProposalUpdatePractice.as_view(),
            name='update_practice'),
        url(r'^pre_approved/$', ProposalUpdatePreApproved.as_view(),
            name='update_pre_approved'),
    ])),
    url(r'^delete/(?P<pk>\d+)/$', ProposalDelete.as_view(), name='delete'),

    url(r'^start/', include([
        url(r'^$', ProposalStart.as_view(), name='start'),
        url(r'^pre/$', ProposalStartPreAssessment.as_view(), name='start_pre'),
        url(r'^practice/$', ProposalStartPractice.as_view(),
            name='start_practice'),
        url(r'^pre_approved/$', ProposalStartPreApproved.as_view(),
            name='start_pre_approved'),
    ])),
    url(r'^data_management/(?P<pk>\d+)/', include([
        url(r'^$', ProposalDataManagement.as_view(), name='data_management'),
    ])),
    url(r'^submit/(?P<pk>\d+)/', include([
        url(r'^$', ProposalSubmit.as_view(), name='submit'),
        url(r'^pre/$', ProposalSubmitPreAssessment.as_view(),
            name='submit_pre'),
        url(r'^pre_approved/$', ProposalSubmitPreApproved.as_view(),
            name='submit_pre_approved'),
    ])),

    url(r'^submitted/(?P<pk>\d+)/', include([
        url(r'^$', ProposalSubmitted.as_view(), name='submitted'),
        url(r'^pre/$', ProposalSubmittedPreAssessment.as_view(),
            name='submitted_pre'),
        url(r'^pre_approved/$', ProposalSubmittedPreApproved.as_view(),
            name='submitted_pre_approved')
    ])),

    url(r'^confirm/(?P<pk>\d+)/$', ProposalConfirmation.as_view(),
        name='confirmation'),

    url(r'^study_start/(?P<pk>\d+)/$', StudyStart.as_view(),
        name='study_start'),
    url(r'^consent/(?P<pk>\d+)/$', StudyConsent.as_view(), name='consent'),

    url(r'^copy/', include([
        url(r'^$', ProposalCopy.as_view(), name='copy'),
        url(r'^revision/$', ProposalCopyRevision.as_view(),
            name='copy_revision'),
        url(r'^amendment/$', ProposalCopyAmendment.as_view(),
            name='copy_amendment'),
    ])),
    url(r'^diff/(?P<pk>\d+)/$', ProposalDifference.as_view(), name='diff'),

    url(r'^pdf/(?P<pk>\d+)/$', ProposalAsPdf.as_view(), name='pdf'),
    url(r'^pdf_empty/$', EmptyPDF.as_view(), name='empty_pdf'),

    # WMO
    url(r'^wmo/create/(?P<pk>\d+)/', include([
        url(r'^$', WmoCreate.as_view(), name='wmo_create'),
        url(r'^pre/$', WmoCreatePreAssessment.as_view(), name='wmo_create_pre'),
    ])),
    url(r'^wmo/update/(?P<pk>\d+)/', include([
        url(r'^$', WmoUpdate.as_view(), name='wmo_update'),
        url(r'^pre/$', WmoUpdatePreAssessment.as_view(), name='wmo_update_pre'),
    ])),
    url(r'^wmo/application/(?P<pk>\d+)/$', WmoApplication.as_view(),
        name='wmo_application'),
    url(r'^wmo/check/$', WmoCheck.as_view(), name='wmo_check'),
    url(r'^wmo/check_js/$', check_wmo, name='check_wmo'),
]
