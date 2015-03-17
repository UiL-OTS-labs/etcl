from django.conf import settings
from django.db import models

class Proposal(models.Model):
    DRAFT = 0 
    WMO_IN_PROGRESS = 1
    WMO_FINISHED = 2
    STATUSES = (
        (DRAFT, 'draft'),
        (WMO_IN_PROGRESS, 'wmo_'),
        (WMO_FINISHED, 'wmo_finished'),
        (2, 'participant_groups'),
        (3, 'experiments'),
        (4, 'concept'),
        (5, 'submitted'),
    )

    # Fields
    name = models.CharField(
        'Titel studie', 
        max_length=200, 
        help_text='Een studie wordt als volgt gedefinieerd: proefpersonen worden aan eenzelfde handeling of reeks handelingen onderworpen. \
Dus proefpersonen binnen de studie, ongeacht de groep (controle of  experimentele groep), doen allemaal dezelfde taak/taken. \
Wanneer het om herhaalde metingen gaat en de procedure verandert per meetmoment, moeten er verschillende aanvragen worden ingediend \
bij de commissie via deze webportal. Ook wanneer de taken onveranderd blijven, maar de proefpersonen kruisen een leeftijdscategorie \
(--link leeftijdscategorieen--), moeten er meerdere aanvragen ingediend worden. Vragen 6 en 7 gaan hierover. \
Het is handig voor het overzicht en het aanvraagproces om in de titel van de studie de leeftijdscategorie te vermelden.')
    tech_summary = models.TextField(
        'Samenvatting',
        help_text='Schrijf hier een samenvatting van max. 500 woorden. \
Deze samenvatting moet in ieder geval bestaan uit een duidelijke beschrijving van deonderzoeksvraag, de proefpersonen. \
Geef een helder beeld van de procedure en een beschrijving van de stimuli (indien daar sprake van is), \
het aantal taken en de methode waarmee het gedrag van de proefpersoon wordt vastgelegd \
(bijv.: reactietijden; knoppenbox; schriftelijke vragenlijst; interview; etc.).')
    longitudinal = models.BooleanField(
        'Is uw studie een longitudinale studie?',
        default=False)
    supervisor_name = models.CharField(
        'Naam eindverantwoordelijke',
        max_length=200, 
        help_text='De eindverantwoordelijke is een onderzoeker die de graad van doctor behaald heeft. \
Wanneer een student de aanvraag doet, dan is de eindverantwoordelijke de begeleidende onderzoeker met in ieder geval een doctorstitel.')
    supervisor_email = models.EmailField(
        'E-mailadres eindverantwoordelijke',
        help_text='Aan het einde van de procedure kunt u deze aanvraag ter verificatie naar uw eindverantwoordelijke sturen. \
Wanneer de verificatie binnen is, krijgt u een e-mail zodat u deze aanvraag kunt afronden.')
    status = models.PositiveIntegerField(choices=STATUSES)

    # Dates 
    date_submitted = models.DateTimeField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    # References
    applicants = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name='Uitvoerende(n)')
    parent = models.ForeignKey('self', null=True)

    def denormalize_status(self):
        """Sets the correct status on save of a Proposal"""
        if not self.status: 
            self.status = self.DRAFT
        if self.Wmo.metc: 
            self.status = self.WMO_IN_PROGRESS
        else:
            self.status = self.WMO_FINISHED

    def __unicode__(self):
        return 'Proposal %s' % self.name

class Wmo(models.Model):
    metc = models.NullBooleanField(
        'Vindt de studie plaats binnen het UMC Utrecht, of een andere instelling waarbij de METC verplicht betrokken wordt?', 
        default=False)
    metc_institution = models.CharField(
        'Instelling',
        max_length=200,
        blank=True)
    is_medical = models.NullBooleanField(
        'Is de onderzoeksvraag medisch-wetenschappelijk van aard?', 
        default=False)
    is_behavioristic = models.NullBooleanField(
        'Worden de proefpersonen aan een handeling onderworpen of worden hen gedragsregels opgelegd?', 
        help_text='Een handeling of opgelegde gedragsregel varieert tussen het afnemen van weefsel bij een proefpersoon tot de proefpersoon een knop/toets in laten drukken.',
        default=False)
    metc_decision = models.BooleanField(
        'Is uw onderzoek al in behandeling genomen door een METC?',
        default=False)
    metc_decision_pdf = models.FileField(
        'Upload hier de beslissing van het METC')

    # References
    proposal = models.OneToOneField(Proposal, primary_key=True)

    def __unicode__(self):
        return 'Wmo %s' % self.proposal.name

class AgeGroup(models.Model):
    age_min = models.PositiveIntegerField()
    age_max = models.PositiveIntegerField(blank=True, null=True)
    description = models.CharField(max_length=200)

    def __unicode__(self):
        if self.age_max: 
            return '%d-%d' % (self.age_min, self.age_max)
        else:
            return '%d+' % (self.age_min)

class Trait(models.Model):
    order = models.PositiveIntegerField(unique=True)
    description = models.CharField(max_length=200)
    needs_details = models.BooleanField(default=False)

    def __unicode__(self):
        return self.description

class Survey(models.Model):
    name = models.CharField(max_length=200)
    minutes = models.PositiveIntegerField()

    def __unicode__(self):
        return self.name

class Setting(models.Model):
    order = models.PositiveIntegerField(unique=True)
    description = models.CharField(max_length=200)
    needs_details = models.BooleanField(default=False)

    def __unicode__(self):
        return self.description

class Recruitment(models.Model):
    order = models.PositiveIntegerField(unique=True)
    description = models.CharField(max_length=200)
    needs_details = models.BooleanField(default=False)

    def __unicode__(self):
        return self.description

class Study(models.Model): 
    age_groups = models.ManyToManyField(
        AgeGroup, 
        verbose_name='Geef hieronder aan binnen welke leeftijdscategorie uw proefpersonen vallen, er zijn meerdere antwoorden zijn mogelijk')
    traits = models.ManyToManyField(
        Trait, 
        verbose_name='Worden de beoogde proefpersonen op bijzondere kenmerken geselecteerden die mogelijk een negatief effect hebben \
op de kwetsbaarheid of verminderde belastbaarheid van de proefpersoon? Indien u twee (of meer) groepen voor ogen heeft, \
hoeft u over de controlegroep (die dus geen bijzondere kenmerken heeft) niet in het hoofd te nemen bij het beantwoorden van de ze vraag')
    traits_details = models.CharField(
        'Namelijk', 
        max_length=200,
        blank=True)
    necessity = models.NullBooleanField(
        'Is het noodzakelijk om deze geselecteerde groep proefpersonen aan de door jou opgelegde handeling te onderwerpen om de onderzoeksvraag beantwoord te krijgen? \
Is het bijvoorbeeld noodzakelijk om kinderen te testen, of zou je de vraag ook kunnen beantwoorden door volwassen proefpersonen te testen?',
        default=True)
    necessity_reason = models.TextField(
        'Leg uit waarom',
        blank=True)
    setting = models.ManyToManyField(
        Setting,
        verbose_name='Geef aan waar de studie plaatsvindt')
    setting_details = models.CharField(
        'Namelijk', 
        max_length=200,
        blank=True)
    surveys = models.ManyToManyField(Survey)
    risk_physical = models.NullBooleanField(
        'Is er een kans dat de proefpersoon fysiek letsel oploopt?',
        default=False)
    risk_psychological = models.NullBooleanField(
        'Is er een kans dat de proefpersoon psychisch letsel oploopt?',
        default=False)
    compensation = models.CharField(
        'Welke vergoeding krijgt de proefpersoon voor verrichte taken?',
        max_length=200,
        help_text='tekst over dat vergoeding in redelijke verhouding moet zijn met belasting pp. En kinderen geen geld')
    recruitment = models.ManyToManyField(
        Recruitment,
        verbose_name='Hoe worden de proefpersonen geworven?')
    recruitment_details = models.CharField(
        'Namelijk', 
        max_length=200, 
        blank=True)

    # References
    proposal = models.OneToOneField(Proposal, primary_key=True)

    def __unicode__(self):
        return 'Experiment settings for proposal %s' % self.proposal.name

class Action(models.Model): 
    order = models.PositiveIntegerField(unique=True)
    description = models.CharField(max_length=200)
    info_text = models.TextField()

    def __unicode__(self):
        return self.description

class Registration(models.Model): 
    order = models.PositiveIntegerField(unique=True)
    description = models.CharField(max_length=200)
    needs_details = models.BooleanField(default=False)

    def __unicode__(self):
        return self.description

class Task(models.Model): 
    name = models.CharField(
        'Naam van de taak', 
        max_length=200)
    procedure = models.NullBooleanField(
        'Welk onderdeel, of welke combinatie van onderdelen, van de procedure zouden door de proefpersonen als \
belastend/onaangenaam ervaren kunnen worden?')
    duration = models.PositiveIntegerField(
        'Wat is de duur van de taak, waarbij de proefpersoon een handeling moet verrichten, van begin tot eind, \
dus vanaf het moment dat de taak van start gaat tot en met het einde van de taak?')
    actions = models.ManyToManyField(Action)
    registrations = models.ManyToManyField(Registration)
    registrations_details = models.CharField(max_length=200, blank=True)

    # References
    proposal = models.ForeignKey(Proposal)

class Faq(models.Model):
    order = models.PositiveIntegerField(unique=True)
    question = models.TextField()
    answer = models.TextField()

    class Meta: 
        verbose_name = 'FAQ'

    def __unicode__(self):
        return self.question

class Member(models.Model): 
    title = models.CharField(max_length=200, blank=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    role = models.CharField(max_length=200)

    def __unicode__(self):
        return '%s %s' % (self.first_name, self.last_name)

class Meeting(models.Model):
    date = models.DateField()
    deadline = models.DateField()

    def __unicode__(self):
        return '%s' % (self.date)
