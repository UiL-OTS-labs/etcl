from django.db import models
from django.core.validators import MaxValueValidator
from django.utils.translation import ugettext_lazy as _

from studies.models import Study


class Observation(models.Model):
    days = models.PositiveIntegerField(
        _('Op hoeveel dagen wordt er geobserveerd?'))
    mean_hours = models.DecimalField(
        _('Hoeveel uur wordt er gemiddeld per dag geobserveerd?'),
        max_digits=4,
        decimal_places=2,
        validators=[MaxValueValidator(24)])
    is_anonymous = models.BooleanField(
        _('Wordt er anoniem geobserveerd?'),
        help_text=_('Zoals zou kunnen voorkomen op fora en de onderzoeker ook een account heeft.'),
        default=False)
    is_in_target_group = models.BooleanField(
        _('Doet de onderzoeker zich voor als behorende tot de doelgroep?'),
        default=False)
    is_nonpublic_space = models.BooleanField(
        _('Wordt er geobserveerd in een niet-openbare ruimte?'),
        help_text=_('Bijvoorbeeld er wordt geobserveerd bij iemand thuis, \
tijdens een hypotheekgesprek of tijdens politieverhoren.'),
        default=False)
    has_advanced_consent = models.BooleanField(
        _('Vindt de informed consent van tevoren plaats?'),
        default=True)

    # References
    study = models.OneToOneField(Study)


class Location(models.Model):
    name = models.CharField(_('Locatie'), max_length=200)
    registration = models.TextField(_('Hoe wordt het gedrag geregistreerd?'))
    observation = models.ForeignKey(Observation)

    def __unicode__(self):
        return self.name
