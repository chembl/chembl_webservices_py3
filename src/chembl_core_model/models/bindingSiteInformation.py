__author__ = 'mnowotka'

from django.db import models
from chembl_core_model.models import *
from chembl_core_db.db.models.abstractModel import ChemblCoreAbstractModel
from chembl_core_db.db.models.abstractModel import ChemblModelMetaClass
from django.utils import six

# ----------------------------------------------------------------------------------------------------------------------


class Domains(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    DOMAIN_TYPE_CHOICES = (
        ('Pfam-A', 'Pfam-A'),
        ('Pfam-B', 'Pfam-B'),
        )

    domain_id = ChemblAutoField(primary_key=True, length=9, help_text=u'Primary key. Unique identifier for each domain.')
    domain_type = ChemblCharField(max_length=20, choices=DOMAIN_TYPE_CHOICES, help_text=u'Indicates the source of the domain (e.g., Pfam).')
    source_domain_id = ChemblCharField(max_length=20, help_text=u'Identifier for the domain in the source database (e.g., Pfam ID such as PF00001).')
    domain_name = ChemblCharField(max_length=20, blank=True, null=True, help_text=u'Name given to the domain in the source database (e.g., 7tm_1).')
    domain_description = ChemblCharField(max_length=500, blank=True, null=True, help_text=u'Longer name or description for the domain.')
    component_sequences = models.ManyToManyField('ComponentSequences', through="ComponentDomains", blank=True)

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

# ----------------------------------------------------------------------------------------------------------------------


class ComponentDomains(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    compd_id = ChemblAutoField(primary_key=True, length=9, help_text=u'Primary key.')
    domain = models.ForeignKey(Domains, blank=True, null=True, help_text=u'Foreign key to the domains table, indicating the domain that is contained in the associated molecular component.')
    component = models.ForeignKey(ComponentSequences, help_text=u'Foreign key to the component_sequences table, indicating the molecular_component that has the given domain.')
    start_position = ChemblPositiveIntegerField(length=5, blank=True, null=True, help_text=u'Start position of the domain within the sequence given in the component_sequences table.')
    end_position = ChemblPositiveIntegerField(length=5, blank=True, null=True, help_text=u'End position of the domain within the sequence given in the component_sequences table.')

    class Meta(ChemblCoreAbstractModel.Meta):
        unique_together = (("domain", "component", "start_position"),)

# ----------------------------------------------------------------------------------------------------------------------


class BindingSites(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    site_id = ChemblAutoField(primary_key=True, length=9, help_text=u'Primary key. Unique identifier for a binding site in a given target.')
    site_name = ChemblCharField(max_length=200, blank=True, null=True, help_text=u'Name/label for the binding site.')
    target = models.ForeignKey(TargetDictionary, blank=True, null=True, db_column='tid', help_text=u'Foreign key to target_dictionary. Target on which the binding site is found.')
    domains = models.ManyToManyField('Domains', through="SiteComponents", blank=True)

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

# ----------------------------------------------------------------------------------------------------------------------


class SiteComponents(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    sitecomp_id = ChemblAutoField(primary_key=True, length=9, help_text=u'Primary key.')
    site = models.ForeignKey(BindingSites, help_text=u'Foreign key to binding_sites table.')
    component = models.ForeignKey(ComponentSequences, blank=True, null=True, help_text=u'Foreign key to the component_sequences table, indicating which molecular component of the target is involved in the binding site.')
    domain = models.ForeignKey(Domains, blank=True, null=True, help_text=u'Foreign key to the domains table, indicating which domain of the given molecular component is involved in the binding site (where not known, the domain_id may be null).')
    site_residues = ChemblCharField(max_length=2000, blank=True, null=True, help_text=u'List of residues from the given molecular component that make up the binding site (where not know, will be null).')

    class Meta(ChemblCoreAbstractModel.Meta):
        unique_together = (("site", "component", "domain"),)

# ----------------------------------------------------------------------------------------------------------------------


