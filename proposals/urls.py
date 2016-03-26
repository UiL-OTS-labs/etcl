from django.conf.urls import url

from .views.base_views import HomeView, check_requires
from .views.proposal_views import ProposalsView, MyConceptsView, MySubmittedView, MyCompletedView, MyProposalsView, \
    ProposalCreate, ProposalUpdate, ProposalDelete, ProposalStart, ProposalConsent, ProposalSubmit, ProposalSubmitted, \
    DetailView, ProposalCopy, ProposalAsPdf, EmptyPDF
from .views.session_views import SessionStart, SessionEnd
from .views.study_views import StudyCreate, StudyUpdate, StudyDesign, StudySurvey, check_necessity_required
from .views.wmo_views import WmoCreate, WmoUpdate, WmoCheck, check_wmo

urlpatterns = [
    # Home
    url(r'^$', HomeView.as_view(), name='home'),

    # List views
    url(r'^proposals-all/$', ProposalsView.as_view(), name='archive'),
    url(r'^concepts/$', MyConceptsView.as_view(), name='my_concepts'),
    url(r'^submitted/$', MySubmittedView.as_view(), name='my_submitted'),
    url(r'^completed/$', MyCompletedView.as_view(), name='my_completed'),
    url(r'^proposals/$', MyProposalsView.as_view(), name='my_archive'),

    # Proposal
    url(r'^create/$', ProposalCreate.as_view(), name='create'),
    url(r'^update/(?P<pk>\d+)/$', ProposalUpdate.as_view(), name='update'),
    url(r'^delete/(?P<pk>\d+)/$', ProposalDelete.as_view(), name='delete'),
    url(r'^show/(?P<pk>\d+)/$', DetailView.as_view(), name='detail'),

    url(r'^copy/$', ProposalCopy.as_view(), name='copy'),
    url(r'^start/$', ProposalStart.as_view(), name='start'),
    url(r'^consent/(?P<pk>\d+)/$', ProposalConsent.as_view(), name='study_consent'),
    url(r'^submit/(?P<pk>\d+)/$', ProposalSubmit.as_view(), name='submit'),
    url(r'^submitted/$', ProposalSubmitted.as_view(), name='submitted'),

    url(r'^pdf/(?P<pk>\d+)/$', ProposalAsPdf.as_view(), name='pdf'),
    url(r'^pdf_empty/$', EmptyPDF.as_view(), name='empty_pdf'),

    # WMO
    url(r'^wmo/create/(?P<pk>\d+)/$', WmoCreate.as_view(), name='wmo_create'),
    url(r'^wmo/update/(?P<pk>\d+)/$', WmoUpdate.as_view(), name='wmo_update'),
    url(r'^wmo/check/$', WmoCheck.as_view(), name='wmo_check'),
    url(r'^wmo/check_js/$', check_wmo, name='check_wmo'),

    # Study
    url(r'^study/create/(?P<pk>\d+)/$', StudyCreate.as_view(), name='study_create'),
    url(r'^study/update/(?P<pk>\d+)/$', StudyUpdate.as_view(), name='study_update'),
    url(r'^study/design/(?P<pk>\d+)/$', StudyDesign.as_view(), name='study_design'),
    url(r'^study/survey/(?P<pk>\d+)/$', StudySurvey.as_view(), name='study_survey'),

    # Session(s)
    url(r'^session/start/(?P<pk>\d+)/$', SessionStart.as_view(), name='session_start'),
    url(r'^session/end/(?P<pk>\d+)/$', SessionEnd.as_view(), name='session_end'),

    # Checks on conditional fields
    url(r'^check_requires/$', check_requires, name='check_requires'),
    url(r'^check_necessity_required/$', check_necessity_required, name='check_necessity_required'),
]
