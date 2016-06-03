# -*- encoding: utf-8 -*-

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from core.models import YES_NO_DOUBT
from core.validators import validate_pdf_or_doc
from proposals.models import Proposal


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


class Trait(models.Model):
    order = models.PositiveIntegerField(unique=True)
    description = models.CharField(max_length=200)
    needs_details = models.BooleanField(default=False)

    class Meta:
        ordering = ['order']

    def __unicode__(self):
        return self.description


class Compensation(models.Model):
    order = models.PositiveIntegerField(unique=True)
    description = models.CharField(max_length=200)
    needs_details = models.BooleanField(default=False)
    requires_review = models.BooleanField(default=False)

    class Meta:
        ordering = ['order']

    def __unicode__(self):
        return self.description


class Recruitment(models.Model):
    order = models.PositiveIntegerField(unique=True)
    description = models.CharField(max_length=200)
    needs_details = models.BooleanField(default=False)
    requires_review = models.BooleanField(default=False)

    class Meta:
        ordering = ['order']

    def __unicode__(self):
        return self.description


class Study(models.Model):
    OBSERVATION = 0
    INTERVENTION = 1
    SESSIONS = 2
    DESIGNS = (
        (OBSERVATION, _('Observatieonderzoek')),
        (INTERVENTION, _('Interventieonderzoek')),
        (SESSIONS, _('Taakonderzoek')),
    )

    order = models.PositiveIntegerField()
    name = models.CharField(
        _('Naam traject'),
        max_length=15,
        blank=True)

    age_groups = models.ManyToManyField(
        AgeGroup,
        verbose_name=_(u'Uit welke leeftijdscategorie(ën) bestaat uw deelnemersgroep?'),
        help_text=_(u'De beoogde leeftijdsgroep kan zijn 5-7 jarigen. Dan moet u hier hier 4-5 én 6-11 invullen.'))
    legally_incapable = models.NullBooleanField(
        _('Maakt uw studie gebruik van wils<u>on</u>bekwame (volwassen) \
deelnemers?'),
        help_text=_('Wilsonbekwame volwassenen zijn volwassenen die waarvan \
redelijkerwijs mag worden aangenomen dat ze onvoldoende kunnen inschatten \
wat hun eventuele deelname allemaal behelst, en/of waarvan anderszins mag \
worden aangenomen dat informed consent niet goed gerealiseerd kan worden \
(bijvoorbeeld omdat ze niet goed hun eigen mening kunnen geven). \
Hier dient in ieder geval altijd informed consent van een relevante \
vertegenwoordiger te worden verkregen.'))
    legally_incapable_details = models.TextField(
        _('Licht toe'),
        blank=True)
    has_traits = models.NullBooleanField(
        _(u'Deelnemers kunnen geïncludeerd worden op bepaalde bijzondere kenmerken. \
Is dit in uw studie bij (een deel van) de deelnemers het geval?'))
    traits = models.ManyToManyField(
        Trait,
        blank=True,
        verbose_name=_('Selecteer de bijzondere kenmerken van uw proefpersonen'))
    traits_details = models.CharField(
        _('Namelijk'),
        max_length=200,
        blank=True)
    necessity = models.CharField(
        _('Is het, om de onderzoeksvraag beantwoord te krijgen, noodzakelijk om het geselecteerde type \
deelnemer aan de studie te laten meedoen?'),
        help_text=_('Is het bijvoorbeeld noodzakelijk om kinderen te testen, of zou u de vraag ook kunnen \
beantwoorden door volwassen deelnemers te testen?'),
        max_length=1,
        choices=YES_NO_DOUBT,
        blank=True)
    necessity_reason = models.TextField(
        _('Leg uit waarom'),
        blank=True)
    recruitment = models.ManyToManyField(
        Recruitment,
        verbose_name=_('Hoe worden de deelnemers geworven?'))
    recruitment_details = models.TextField(
        _('Licht toe'),
        blank=True)
    compensation = models.ForeignKey(
        Compensation,
        verbose_name=_('Welke vergoeding krijgt de deelnemer voor zijn/haar deelname?'),
        help_text=_(u'Het standaard bedrag voor vergoeding aan de deelnemers \
is €10,- per uur. Minderjarigen mogen geen geld ontvangen, maar wel een \
cadeautje.'),
        null=True)
    compensation_details = models.CharField(
        _('Namelijk'),
        max_length=200,
        blank=True)

    # Fields with respect to experimental design
    has_intervention = models.BooleanField(
        _('Interventieonderzoek'),
        default=False)
    has_observation = models.BooleanField(
        _('Observatieonderzoek'),
        default=False)
    has_sessions = models.BooleanField(
        _('Taakonderzoek'),
        default=False)

    # Fields with respect to informed consent
    informed_consent = models.FileField(
        _('Upload hier de toestemmingsverklaring (in .pdf of .doc(x)-formaat)'),
        blank=True,
        validators=[validate_pdf_or_doc])
    briefing = models.FileField(
        _('Upload hier de informatiebrief (in .pdf of .doc(x)-formaat)'),
        blank=True,
        validators=[validate_pdf_or_doc])
    passive_consent = models.BooleanField(
        _('Maakt u gebruik van passieve informed consent?'),
        default=False,
        help_text=mark_safe(_('Wanneer u kinderen via een instelling \
(dus ook school) werft en u de ouders niet laat ondertekenen, maar in \
plaats daarvan de leiding van die instelling, dan maakt u gebruik van \
passieve informed consent. U kunt de templates vinden op \
<a href="https://etcl.wp.hum.uu.nl/toestemmingsverklaringen/" \
target="_blank">de ETCL-website</a>.')))

    # Fields with respect to Sessions
    sessions_number = models.PositiveIntegerField(
        _('Hoeveel sessies met taakonderzoek zullen de deelnemers doorlopen?'),
        null=True,
        validators=[MinValueValidator(1)],
        help_text=_(u'Wanneer u bijvoorbeeld eerst de deelnemer een taak/aantal taken laat doen tijdens \
een eerste bezoek aan het lab en u laat de deelnemer nog een keer terugkomen om dezelfde taak/taken \
of andere taak/taken te doen, dan spreken we van twee sessies. \
Wanneer u meerdere taken afneemt op dezelfde dag, met pauzes daartussen, dan geldt dat toch als één sessie.'))
    deception = models.CharField(
        _('Is er binnen bovenstaand onderzoekstraject sprake van \
misleiding van de deelnemer?'),
        help_text=_('Misleiding is het doelbewust verschaffen van inaccurate \
informatie over het doel en/of belangrijke aspecten van de gang van zaken \
tijdens de studie. Denk aan zaken als een bewust misleidende "cover story" \
voor het experiment; het ten onrechte suggereren dat er met andere \
deelnemers wordt samengewerkt; het onaangekondigd aanbieden van een cruciale \
geheugentaak of het geven van gefingeerde feedback. Wellicht ten overvloede: \
het gaat hierbij niet om fillers.'),
        max_length=1,
        choices=YES_NO_DOUBT,
        blank=True)
    deception_details = models.TextField(
        _('Geef een toelichting en beschrijf hoe en wanneer de deelnemer \
zal worden gedebrieft.'),
        blank=True)
    negativity = models.CharField(
        _('Bevat bovenstaand onderzoekstraject elementen die \
<em>tijdens</em> de deelname niet-triviale negatieve emoties kunnen opwekken? \
Denk hierbij bijvoorbeeld aan emotioneel indringende vragen, kwetsende \
uitspraken, negatieve feedback, frustrerende, zware, (heel) lange en/of \
(heel) saaie taken.'),
        max_length=1,
        choices=YES_NO_DOUBT,
        blank=True)
    negativity_details = models.TextField(
        _('Licht uw antwoord toe.'),
        blank=True)
    stressful = models.CharField(
        _('Bevat bovenstaand onderzoekstraject elementen die tijdens de \
deelname zodanig belastend zijn dat deze <em>ondanks de verkregen \
informed consent</em> vragen zou kunnen oproepen (of zelfs \
verontwaardiging), bijvoorbeeld bij collega-onderzoekers, bij de deelnemers \
zelf, of bij ouders of andere vertegenwoordigers?'),
        help_text=mark_safe(_('Dit zou bijvoorbeeld het geval kunnen zijn \
bij een \'onmenselijk\' lange en uitputtende taak, een zeer confronterende \
vragenlijst, of voortdurend vernietigende feedback, maar ook bij een ervaren \
inbreuk op de privacy, of een ander ervaren gebrek aan respect. \
Let op, het gaat bij deze vraag om de door de deelnemer ervaren belasting \
tijdens het onderzoek, niet om de opgelopen psychische of fysieke schade \
door het onderzoek.')),
        max_length=1,
        choices=YES_NO_DOUBT,
        blank=True)
    stressful_details = models.TextField(
        _('Licht uw antwoord toe. Geef concrete voorbeelden van de relevante \
aspecten van uw studie (bijv. representatieve voorbeelden van mogelijk zeer \
kwetsende woorden of uitspraken in de taak, of van zeer confronterende \
vragen in een vragenlijst), zodat de commissie zich een goed beeld kan \
vormen.'),
        blank=True)
    risk = models.CharField(
        _('Zijn de risico\'s op psychische, fysieke, of andere (bijv. \
economische, juridische) schade door deelname aan bovenstaand \
onderzoekstraject <em>meer dan</em> minimaal? \
D.w.z. ligt de kans op en/of omvang van mogelijke schade \
bij de deelnemers duidelijk <em>boven</em> het "achtergrondrisico"?'),
        help_text=mark_safe(_('Achtergrondrisico is datgene dat gezonde, \
gemiddelde burgers in de relevante leeftijdscategorie normaalgesproken \
in het dagelijks leven ten deel valt. \
Denk bij schade ook aan de gevolgen die het voor de deelnemer of \
anderen beschikbaar komen van bepaalde informatie kan hebben, bijv. \
op het vlak van zelfbeeld, stigmatisering door anderen, economische \
schade door data-koppeling, et cetera. Het achtergrondrisico voor \
psychische en fysieke schade omvat bijvoorbeeld ook de risico\'s van \
"routine"-tests, -onderzoeken of -procedures die in alledaagse didactische, \
psychologische of medische contexten plaatsvinden (zoals een eindexamen, \
een rijexamen, een stressbestendigheids-<em>assessment</em>, een \
intelligentie- of persoonlijkheidstest, of een hartslagmeting na fysieke \
inspanning; dit alles, waar relevant, onder begeleiding van adequaat \
geschoolde specialisten).')),
        max_length=1,
        choices=YES_NO_DOUBT,
        blank=True)
    risk_details = models.TextField(
        _('Licht toe'),
        max_length=200,
        blank=True)

    # Fields with respect to Surveys
    has_surveys = models.BooleanField(
        _(u'Worden er vragenlijsten afgenomen bij <em>een ander dan de deelnemer</em>? \
Denk hierbij aan de ouder of voogd van een kind, de leraar van de klas, de arts van een patiënt, etc.'),
        default=False)
    surveys_stressful = models.CharField(
        _('Is het invullen van deze vragenlijsten belastend? \
Denk hierbij bijv. aan het type vragen dat gesteld wordt en aan de tijd die de persoon kwijt is met het invullen van alle vragenlijsten.'),
        max_length=1,
        choices=YES_NO_DOUBT,
        blank=True)

    # References
    proposal = models.ForeignKey(Proposal)

    class Meta:
        ordering = ['order']
        unique_together = ('proposal', 'order')

    def net_duration(self):
        """Returns the duration of all Tasks in this Study"""
        result = self.session_set.aggregate(models.Sum('tasks_duration'))['tasks_duration__sum']
        return result or 0

    def first_session(self):
        """Returns the first Session in this Study"""
        return self.session_set.order_by('order')[0]

    def last_session(self):
        """Returns the last Session in this Study"""
        return self.session_set.order_by('-order')[0]

    def __unicode__(self):
        return _('Study details for proposal %s') % self.proposal.title


class Survey(models.Model):
    name = models.CharField(_('Naam vragenlijst'), max_length=200)
    duration = models.PositiveIntegerField(_('Duur (in minuten)'))
    url = models.CharField(_('URL'), blank=True, max_length=200)
    description = models.TextField(_('Korte beschrijving'))
    study = models.ForeignKey(Study)

    def __unicode__(self):
        return self.name
