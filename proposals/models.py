# -*- encoding: utf-8 -*-

from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
from django.core.urlresolvers import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _


def validate_pdf(value):
    f = value.file
    if isinstance(f, UploadedFile) and f.content_type != 'application/pdf':
        raise ValidationError(_('Alleen PDF-bestanden zijn toegestaan.'))


class Relation(models.Model):
    order = models.PositiveIntegerField(unique=True)
    description = models.CharField(max_length=200)
    needs_supervisor = models.BooleanField(default=True)

    def __unicode__(self):
        return self.description


class Proposal(models.Model):
    DRAFT = 1
    WMO_DECISION_BY_ETCL = 2
    WMO_DECISION_BY_METC = 3
    STUDY_CREATED = 4
    SESSIONS_STARTED = 5
    TASKS_STARTED = 6
    TASKS_ADDED = 7
    TASKS_ENDED = 8
    SESSIONS_ENDED = 9
    INFORMED_CONSENT_UPLOADED = 10
    SUBMITTED_TO_SUPERVISOR = 40
    SUBMITTED = 50
    DECISION_MADE = 55
    WMO_DECISION_MADE = 60
    STATUSES = (
        (DRAFT, _('Algemene informatie ingevuld')),
        (WMO_DECISION_BY_ETCL, _('WMO: geen beoordeling door METC noodzakelijk')),
        (WMO_DECISION_BY_METC, _('WMO: wordt beoordeeld door METC')),
        (STUDY_CREATED, _('Kenmerken studie toegevoegd')),
        (SESSIONS_STARTED, _('Belasting deelnemer: sessies toevoegen')),
        (TASKS_STARTED, _('Belasting deelnemer: taken toevoegen')),
        (TASKS_ADDED, _('Belasting deelnemer: alle taken toegevoegd')),
        (TASKS_ENDED, _('Belasting deelnemer: afgerond')),
        (SESSIONS_ENDED, _('Belasting deelnemer: afgerond')),
        (INFORMED_CONSENT_UPLOADED, _(u'Informed consent geüpload')),

        (SUBMITTED_TO_SUPERVISOR, _('Opgestuurd ter beoordeling door eindverantwoordelijke')),
        (SUBMITTED, _('Opgestuurd ter beoordeling door ETCL')),

        (DECISION_MADE, _('Aanvraag is beoordeeld door ETCL')),
        (WMO_DECISION_MADE, _('Aanvraag is beoordeeld door METC')),
    )

    # Fields of a proposal
    reference_number = models.CharField(
        max_length=16,
        unique=True)
    date_start = models.DateField(
        _('Wat is de beoogde startdatum van uw studie?'))
    date_end = models.DateField(
        _('Wat is de beoogde einddatum van uw studie?'))
    title = models.CharField(
        _('Wat is de titel van uw studie?'),
        max_length=200,
        unique=True,
        help_text=_('Kies s.v.p. een titel die niet volledig identiek is aan die van eerder ingediende studies.'))
    tech_summary = models.TextField(
        _(u'Schrijf hier een samenvatting van 200-300 woorden, met daarin (a) een duidelijke, \
bondige beschrijving van de onderzoeksvraag of -vragen, en (b) een korte beschrijving van de beoogde methode, \
d.w.z. een mini-versie van de toekomstige Methode-sectie, met informatie over deelnemers, materiaal (taken, stimuli), \
design, en procedure. Het gaat er hier vooral om dat de relatie tussen de onderzoeksvraag of -vragen \
en de beoogde methode voldoende helder is; verderop in deze aanmelding zal voor specifieke ingrediënten \
van de methode meer gedetailleerde informatie worden gevraagd.'))
    other_applicants = models.BooleanField(
        _('Zijn er nog andere UiL OTS-onderzoekers bij deze studie betrokken?'),
        default=False)
    comments = models.TextField(
        _('Ruimte voor eventuele opmerkingen'),
        blank=True)
    allow_in_archive = models.BooleanField(
        _('Mag deze aanvraag ter goedkeuring in het semi-publiekelijk archief?'),
        default=True,
        help_text=_('Dit archief is alleen toegankelijk voor mensen die aan het UiL OTS geaffilieerd zijn.')
    )

    # Fields with respect to informed consent
    informed_consent_pdf = models.FileField(
        _('Upload hier de toestemmingsverklaring (in PDF-formaat)'),
        blank=True,
        validators=[validate_pdf])
    briefing_pdf = models.FileField(
        _('Upload hier de informatiebrief (in PDF-formaat)'),
        blank=True,
        validators=[validate_pdf])
    passive_consent = models.BooleanField(
        _('Maakt uw studie gebruik van passieve informed consent?'),
        default=False,
        help_text=_('Wanneer u kinderen via een instelling (dus ook school) werft en u de ouders niet laat \
ondertekenen, maar in plaats daarvan de leiding van die instelling, dan maakt u gebruik van passieve informed consent. \
U kunt de templates vinden op <link website?>')
    )

    # Status
    status = models.PositiveIntegerField(choices=STATUSES, default=DRAFT)

    # Dates for bookkeeping
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_submitted_supervisor = models.DateTimeField(null=True)
    date_reviewed_supervisor = models.DateTimeField(null=True)
    date_submitted = models.DateTimeField(null=True)
    date_reviewed = models.DateTimeField(null=True)

    # References to other models
    relation = models.ForeignKey(
        Relation,
        verbose_name=_('Wat is uw relatie tot het UiL OTS?'))
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='created_by')
    applicants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Uitvoerende(n)'),
        related_name='applicants')
    supervisor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Eindverantwoordelijke onderzoeker'),
        blank=True,
        null=True,
        help_text=_('Aan het einde van de procedure kunt u deze aanvraag ter verificatie naar uw eindverantwoordelijke sturen. \
Wanneer de verificatie binnen is, krijgt u een e-mail zodat u deze aanvraag kunt afronden.'))
    parent = models.ForeignKey(
        'self',
        null=True,
        verbose_name=_(u'Te kopiëren aanvraag'),
        help_text=_('Dit veld toont enkel aanvragen waar u zelf een medeaanvrager bent.'))

    def save(self, *args, **kwargs):
        """Sets the correct status on save of a Proposal"""
        self.status = self.get_status()
        super(Proposal, self).save(*args, **kwargs)

    def get_status(self):
        """Retrieves the current status for a Proposal"""
        status = self.status
        if hasattr(self, 'wmo'):
            wmo = self.wmo
            if wmo.status == wmo.WAITING:
                status = self.WMO_DECISION_BY_METC
            elif wmo.status == wmo.JUDGED:
                status = self.WMO_DECISION_MADE
            else:
                status = self.WMO_DECISION_BY_ETCL
        if hasattr(self, 'study'):
            status = self.STUDY_CREATED
            if self.study.sessions_number:
                status = self.SESSIONS_STARTED

        session = self.current_session()
        if session:
            status = self.SESSIONS_STARTED
            if session.tasks_number:
                status = self.TASKS_STARTED
            if session.all_tasks_completed():
                status = self.TASKS_ADDED
            if session.tasks_duration:
                status = self.TASKS_ENDED
        if session and session.tasks_duration:
            if self.study.sessions_duration:
                status = self.SESSIONS_ENDED

        if self.informed_consent_pdf:
            status = self.INFORMED_CONSENT_UPLOADED
        if self.date_submitted_supervisor:
            status = self.SUBMITTED_TO_SUPERVISOR
        if self.date_submitted:
            status = self.SUBMITTED
        if self.date_reviewed:
            status = self.DECISION_MADE

        return status

    def continue_url(self):
        session = self.current_session()
        if self.status == self.DRAFT:
            return reverse('proposals:wmo_create', args=(self.id,))
        elif self.status == self.WMO_DECISION_BY_ETCL:
            return reverse('proposals:study_create', args=(self.id,))
        elif self.status == self.WMO_DECISION_BY_METC:
            return reverse('proposals:wmo_update', args=(self.id,))
        elif self.status == self.STUDY_CREATED:
            return reverse('proposals:session_start', args=(self.id,))
        elif self.status == self.SESSIONS_STARTED:
            return reverse('proposals:task_start', args=(session.id,))
        elif self.status == self.TASKS_STARTED:
            return reverse('proposals:task_update', args=(session.current_task().id,))
        elif self.status == self.TASKS_ADDED:
            return reverse('proposals:task_end', args=(session.id,))
        elif self.status == self.TASKS_ENDED:
            return reverse('proposals:session_end', args=(self.id,))
        elif self.status == self.SESSIONS_ENDED:
            return reverse('proposals:consent', args=(self.id,))
        elif self.status == self.INFORMED_CONSENT_UPLOADED:
            return reverse('proposals:submit', args=(self.id,))

        elif self.status == self.WMO_DECISION_MADE:
            return reverse('proposals:my_archive')

    def current_session(self):
        """
        Returns the current (imcomplete) session.
        - If all sessions are completed, the last session is returned.
        - If no sessions have yet been created, None is returned.
        """
        current_session = None
        if hasattr(self, 'study'):
            for session in self.study.session_set.all():
                current_session = session
                if not session.tasks_duration:
                    break
        return current_session

    def __unicode__(self):
        return '%s (%s)' % (self.title, self.created_by)


class Wmo(models.Model):
    NO_WMO = 0
    WAITING = 1
    JUDGED = 2
    WMO_STATUSES = (
        (NO_WMO, _('Geen beoordeling door METC noodzakelijk')),
        (WAITING, _('In afwachting beslissing METC')),
        (JUDGED, _(u'Beslissing METC geüpload')),
    )

    metc = models.NullBooleanField(
        _('Vindt de dataverzameling plaats binnen het UMC Utrecht of andere instelling waar toetsing door een METC verplicht is gesteld?'))
    metc_institution = models.CharField(
        _('Welke instelling?'),
        max_length=200,
        blank=True)
    is_medical = models.NullBooleanField(
        _('Is de onderzoeksvraag medisch-wetenschappelijk van aard (zoals gedefinieerd door de WMO)?'),
        help_text=_('De definitie van medisch-wetenschappelijk onderzoek is: \
Medisch-wetenschappelijk onderzoek is onderzoek dat als doel heeft het beantwoorden van een vraag op het gebied van ziekte en gezondheid \
(etiologie, pathogenese, verschijnselen/symptomen, diagnose, preventie, uitkomst of behandeling van ziekte), door het op systematische wijze vergaren en bestuderen van gegevens. \
Het onderzoek beoogt bij te dragen aan medische kennis die ook geldend is voor populaties buiten de directe onderzoekspopulatie. \
(CCMO-notitie, Definitie medisch-wetenschappelijk onderzoek, 2005, ccmo.nl)'))
    is_behavioristic = models.NullBooleanField(
        _('Worden de deelnemers aan een handeling onderworpen of worden hen gedragsregels opgelegd (zoals gedefinieerd door de WMO)?'),
        help_text=_('Een handeling of opgelegde gedragsregel varieert tussen het afnemen van weefsel bij een deelnemer tot de deelnemer een knop/toets in laten drukken.'))
    metc_application = models.BooleanField(
        _('Uw studie moet beoordeeld worden door de METC, maar dient nog wel bij de ETCL te worden geregistreerd. Is voor deze studie al een METC aanvraag ingediend?'),
        default=False)
    metc_decision = models.BooleanField(
        _('Is de METC al tot een beslissing gekomen?'),
        default=False)
    metc_decision_pdf = models.FileField(
        _('Upload hier de beslissing van het METC (in PDF-formaat)'),
        blank=True,
        validators=[validate_pdf])

    # Status
    status = models.PositiveIntegerField(choices=WMO_STATUSES, default=NO_WMO)

    # References
    proposal = models.OneToOneField(Proposal, primary_key=True)

    def save(self, *args, **kwargs):
        """Sets the correct status on save of a WMO"""
        super(Wmo, self).save(*args, **kwargs)
        self.update_status()
        self.proposal.save()

    def update_status(self):
        if self.metc or (self.is_medical and self.is_behavioristic):
            if not self.metc_decision:
                self.status = self.WAITING
            if self.metc_decision and self.metc_decision_pdf:
                self.status = self.JUDGED
        else:
            self.status = self.NO_WMO

    def __unicode__(self):
        return _('WMO %s, status %s') % (self.proposal.title, self.status)


class AgeGroup(models.Model):
    age_min = models.PositiveIntegerField()
    age_max = models.PositiveIntegerField(blank=True, null=True)
    description = models.CharField(max_length=200)
    needs_details = models.BooleanField(default=False)
    max_net_duration = models.PositiveIntegerField()

    def __unicode__(self):
        if self.age_max:
            return _('%d-%d jaar') % (self.age_min, self.age_max)
        else:
            return _('%d+ jaar') % (self.age_min)


class Setting(models.Model):
    order = models.PositiveIntegerField(unique=True)
    description = models.CharField(max_length=200)
    needs_details = models.BooleanField(default=False)
    requires_review = models.BooleanField(default=False)

    def __unicode__(self):
        return self.description


class Compensation(models.Model):
    order = models.PositiveIntegerField(unique=True)
    description = models.CharField(max_length=200)
    needs_details = models.BooleanField(default=False)
    requires_review = models.BooleanField(default=False)

    def __unicode__(self):
        return self.description


class Recruitment(models.Model):
    order = models.PositiveIntegerField(unique=True)
    description = models.CharField(max_length=200)
    needs_details = models.BooleanField(default=False)
    requires_review = models.BooleanField(default=False)

    def __unicode__(self):
        return self.description


class Study(models.Model):
    age_groups = models.ManyToManyField(
        AgeGroup,
        verbose_name=_('Geef aan binnen welke leeftijdscategorie uw deelnemers vallen, \
er zijn meerdere antwoorden mogelijk'))
    legally_incapable = models.BooleanField(
        _('Maakt uw studie gebruik van <strong>volwassen</strong> wilsonbekwame deelnemers?'),
        default=False)
    has_traits = models.BooleanField(
        _(u'Deelnemers kunnen geïncludeerd worden op bepaalde bijzondere kenmerken. \
Is dit in uw studie bij (een deel van) de deelnemers het geval?'),
        default=False)
    necessity = models.NullBooleanField(
        _('Is het, om de onderzoeksvraag beantwoord te krijgen, noodzakelijk om het geselecteerde type \
deelnemer aan de studie te laten meedoen?'),
        help_text=_('Is het bijvoorbeeld noodzakelijk om kinderen te testen, of zou u de vraag ook kunnen \
beantwoorden door volwassen deelnemers te testen?'))
    necessity_reason = models.TextField(
        _('Leg uit waarom'),
        blank=True)
    recruitment = models.ManyToManyField(
        Recruitment,
        verbose_name=_('Hoe worden de deelnemers geworven?'))
    recruitment_details = models.CharField(
        _('Namelijk'),
        max_length=200,
        blank=True)
    setting = models.ManyToManyField(
        Setting,
        verbose_name=_('Geef aan waar de dataverzameling plaatsvindt'))
    setting_details = models.CharField(
        _('Namelijk'),
        max_length=200,
        blank=True)
    compensation = models.ForeignKey(
        Compensation,
        verbose_name=_('Welke vergoeding krijgt de deelnemer voor zijn/haar deelname aan deze studie?'),
        help_text=_('tekst over dat vergoeding in redelijke verhouding moet zijn met belasting pp. En kinderen geen geld'))
    compensation_details = models.CharField(
        _('Namelijk'),
        max_length=200,
        blank=True)

    # Fields with respect to Sessions
    sessions_number = models.PositiveIntegerField(
        _('Hoeveel sessies telt deze studie?'),
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text=_(u'Wanneer u bijvoorbeeld eerst de deelnemer een taak/aantal taken laat doen tijdens \
een eerste bezoek aan het lab en u laat de deelnemer nog een keer terugkomen om dezelfde taak/taken \
of andere taak/taken te doen, dan spreken we van twee sessies. \
Wanneer u meerdere taken afneemt op dezelfde dag, met pauzes daartussen, dan geldt dat toch als één sessie.'))
    sessions_duration = models.PositiveIntegerField(
        _('De netto duur van uw studie komt op basis van uw opgegeven tijd, uit op <strong>%d minuten</strong>. \
Wat is de totale duur van de gehele studie? Schat de totale tijd die de deelnemers kwijt zijn aan de studie.'),
        null=True,
        help_text=_('Dit is de geschatte totale bruto tijd die de deelnemer kwijt is aan alle sessies \
bij elkaar opgeteld, exclusief reistijd.'))
    stressful = models.NullBooleanField(
        _('Is de studie op onderdelen of als geheel zodanig belastend dat deze <em>ondanks de verkregen informed \
consent </em> vragen zou kunnen oproepen (of zelfs verontwaardiging), bijvoorbeeld bij collega-onderzoekers, \
bij de deelnemers zelf, of bij ouders of andere vertegenwoordigers? Ga bij het beantwoorden van deze vraag uit \
van de volgens u meest kwetsbare c.q. minst belastbare deelnemersgroep, en neem ook de leeftijd van de deelnemers \
in deze inschatting mee.'),
        help_text=mark_safe(_('Dit zou bijvoorbeeld het geval kunnen zijn bij een \'onmenselijk\' lange en uitputtende taak, \
een zeer confronterende vragenlijst, of voortdurend vernietigende feedback, maar ook bij een ervaren inbreuk op de \
privacy, of een ander ervaren gebrek aan respect. Let op, het gaat bij deze vraag om de door de deelnemer ervaren \
belasting tijdens het onderzoek, niet om de opgelopen psychische of fysieke schade door het onderzoek.')),
        default=False)
    stressful_details = models.TextField(
        _('Licht je antwoord toe. Geef concrete voorbeelden van de relevante aspecten van uw studie \
(bijv. representatieve voorbeelden van mogelijk zeer kwetsende woorden of uitspraken in de taak, \
of van zeer confronterende vragen in een vragenlijst), zodat de commissie zich een goed beeld kan vormen.'),
        blank=True)
    risk = models.NullBooleanField(
        _('Zijn de risico\'s op psychische of fysieke schade bij deelname aan de studie <em>meer dan</em> minimaal? \
D.w.z. ligt de kans op en/of omvang van mogelijke fysieke of psychische schade bij de deelnemers duidelijk \
<em>boven</em> het "achtergrondrisico"? Achtergrondrisico is datgene dat gezonde, gemiddelde burgers in de relevante \
leeftijdscategorie normaalgesproken in het dagelijks leven ten deel valt. Ga bij het beantwoorden van deze \
vraag uit van de volgens u meest kwetsbare c.q. minst belastbare deelnemersgroep in uw studie.'),
        help_text=mark_safe(_('Denk bij schade ook aan de gevolgen die het voor de deelnemer of anderen beschikbaar komen \
van bepaalde informatie kan hebben, bijv. op het vlak van zelfbeeld, stigmatisering door anderen, et cetera. \
Het achtergrondrisico omvat bijvoorbeeld ook de risico\'s van \"routine\"-tests, -onderzoeken of -procedures \
die in alledaagse didactische, psychologische of medische contexten plaatsvinden (zoals een eindexamen, een \
rijexamen, een stressbestendigheids-<em>assessment</em>, een intelligentie- of persoonlijkheidstest, of een \
hartslagmeting na fysieke inspanning; dit alles, waar relevant, onder begeleiding van adequaat geschoolde \
specialisten).')),
        default=False)
    risk_details = models.TextField(
        _('Licht toe'),
        blank=True)

    # Fields with respect to Surveys
    has_surveys = models.BooleanField(
        _(u'Worden er vragenlijsten afgenomen bij <em>een ander dan de deelnemer</em>? \
Denk hierbij aan de ouder of voogd van een kind, de leraar van de klas, de arts van een patiënt, etc.'),
        default=False)
    surveys_stressful = models.NullBooleanField(
        _('Is het invullen van deze vragenlijsten belastend? \
Denk hierbij bijv. aan het type vragen dat gesteld wordt en aan de tijd die de persoon kwijt is met het invullen van alle vragenlijsten.'),
        default=False)

    # References
    proposal = models.OneToOneField(Proposal, primary_key=True)

    def save(self, *args, **kwargs):
        """Sets the correct status on Proposal on save of a Study"""
        super(Study, self).save(*args, **kwargs)
        self.proposal.save()

    def net_duration(self):
        """Returns the duration of all Tasks in this Study"""
        return self.session_set.aggregate(models.Sum('tasks_duration'))['tasks_duration__sum']

    def first_session(self):
        """Returns the first Session in this Study"""
        return self.session_set.order_by('order')[0]

    def last_session(self):
        """Returns the last Session in this Study"""
        return self.session_set.order_by('-order')[0]

    def __unicode__(self):
        return _('Study details for proposal %s') % self.proposal.title


class Session(models.Model):
    order = models.PositiveIntegerField()

    # Fields with respect to Tasks
    tasks_number = models.PositiveIntegerField(
        _('Hoeveel taken worden er binnen deze sessie bij de deelnemer afgenomen?'),
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text=_('Wanneer u bijvoorbeeld eerst de deelnemer observeert en de deelnemer vervolgens een vragenlijst afneemt, dan vult u hierboven "2" in. \
Electrodes plakken, sessie-debriefing en kort (< 3 minuten) exit-interview gelden niet als een taak.'))
    tasks_duration = models.PositiveIntegerField(
        _('De totale geschatte netto taakduur van uw sessie komt op basis van uw opgave per taak uit op <strong>%d minuten</strong>. \
Hoe lang duurt <em>de totale sessie</em>, inclusief ontvangst, instructies per taak, pauzes tussen taken, en debriefing? (bij labbezoek dus van binnenkomst tot vertrek)'),
        null=True)

    # References
    study = models.ForeignKey(Study)

    class Meta:
        ordering = ['order']
        unique_together = ('study', 'order')

    def save(self, *args, **kwargs):
        """Sets the correct status on Proposal on save of a Session"""
        super(Session, self).save(*args, **kwargs)
        self.study.proposal.save()

    def delete(self, *args, **kwargs):
        """
        Invalidate the totals on Study level on deletion of a Session.
        """
        study = self.study
        study.sessions_duration = None
        super(Session, self).delete(*args, **kwargs)
        study.save()

    def net_duration(self):
        return self.task_set.aggregate(models.Sum('duration'))['duration__sum']

    def first_task(self):
        tasks = self.task_set.order_by('order')
        return tasks[0] if tasks else None

    def last_task(self):
        tasks = self.task_set.order_by('-order')
        return tasks[0] if tasks else None

    def current_task(self):
        """
        Returns the current (imcomplete) Task.
        - If all Tasks are completed, the last Task is returned.
        - If no Tasks have yet been created, None is returned.
        """
        current_task = None
        for task in self.task_set.all():
            current_task = task
            if not task.name:
                break
        return current_task

    def all_tasks_completed(self):
        result = True
        for task in self.task_set.all():
            result &= task.name != ''
        return result

    def __unicode__(self):
        return _('Sessie {}').format(self.order)


class Survey(models.Model):
    name = models.CharField(_('Naam vragenlijst'), max_length=200)
    minutes = models.PositiveIntegerField(_('Duur (in minuten)'))
    survey_url = models.URLField(_('URL'), blank=True)
    description = models.TextField(_('Korte beschrijving'))
    study = models.ForeignKey(Study)

    def __unicode__(self):
        return self.name


class Registration(models.Model):
    order = models.PositiveIntegerField(unique=True)
    description = models.CharField(max_length=200)
    needs_details = models.BooleanField(default=False)
    needs_kind = models.BooleanField(default=False)
    requires_review = models.BooleanField(default=False)
    age_min = models.PositiveIntegerField(blank=True, null=True)

    def __unicode__(self):
        return self.description


class RegistrationKind(models.Model):
    order = models.PositiveIntegerField(unique=True)
    description = models.CharField(max_length=200)
    needs_details = models.BooleanField(default=False)
    registration = models.ForeignKey(Registration)

    def __unicode__(self):
        return self.description


class Task(models.Model):
    order = models.PositiveIntegerField()
    name = models.CharField(
        _('Wat is de naam van de taak?'),
        max_length=200)
    description = models.TextField(
        _('Wat is de beschrijving van de taak?'))
    duration = models.PositiveIntegerField(
        _('Wat is de duur van deze taak van begin tot eind in <strong>minuten</strong>, dus vanaf het moment dat de taak van start gaat tot en met het einde van de taak (exclusief instructie maar inclusief oefensessie)? \
Indien de taakduur per deelnemer varieert (self-paced taak of task-to-criterion), geef dan het redelijkerwijs te verwachten maximum op.'),
        default=0,
        validators=[MinValueValidator(1)])
    registrations = models.ManyToManyField(
        Registration,
        verbose_name=_('Hoe wordt het gedrag of de toestand van de deelnemer bij deze taak vastgelegd?'))
    registrations_details = models.CharField(
        _('Namelijk'),
        max_length=200,
        blank=True)
    registration_kinds = models.ManyToManyField(
        RegistrationKind,
        verbose_name=_('Kies het soort meting'),
        blank=True)
    registration_kinds_details = models.CharField(
        _('Namelijk'),
        max_length=200,
        blank=True)
    feedback = models.BooleanField(
        _('Krijgt de deelnemer tijdens of na deze taak feedback op zijn/haar gedrag of toestand?'),
        default=False)
    feedback_details = models.TextField(
        _('Beschrijf hoe de feedback wordt gegeven.'),
        blank=True)
    deception = models.BooleanField(
        _('Is er binnen deze sessie sprake van misleiding van de deelnemer, \
d.w.z. het doelbewust verschaffen van inaccurate informatie over het doel en/of belangrijke aspecten van de gang van zaken tijdens de studie? \
Denk aan zaken als een bewust misleidende "cover story" voor het experiment; \
het ten onrechte suggereren dat er met andere deelnemers wordt samengewerkt; \
het onaangekondigd aanbieden van een cruciale geheugentaak of het geven van gefingeerde feedback.'),
        help_text=_('Wellicht ten overvloede: het gaat hierbij niet om fillers.'),
        default=False)
    deception_details = models.TextField(
        'Geef een toelichting en beschrijf hoe en wanneer de deelnemer zal worden gedebrieft.',
        blank=True)

    # References
    session = models.ForeignKey(Session)

    class Meta:
        ordering = ['order']
        unique_together = ('session', 'order')

    def save(self, *args, **kwargs):
        """
        Sets the correct status on Proposal on save of a Task.
        """
        super(Task, self).save(*args, **kwargs)
        self.session.study.proposal.save()

    def delete(self, *args, **kwargs):
        """
        Invalidate the totals on Session/Study level on deletion of a Task.
        """
        session = self.session
        session.tasks_duration = None
        study = self.session.study
        study.sessions_duration = None
        super(Task, self).delete(*args, **kwargs)
        session.save()
        study.save()

    def __unicode__(self):
        return 'Task at {}'.format(self.session)
