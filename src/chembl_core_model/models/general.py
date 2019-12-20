__author__ = 'mnowotka'

from chembl_core_db.db.customFields import *
from chembl_core_db.db.models.abstractModel import ChemblCoreAbstractModel
from chembl_core_db.db.models.abstractModel import ChemblModelMetaClass
from django.utils import six

# ----------------------------------------------------------------------------------------------------------------------


class Version(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    name = models.CharField(primary_key=True, max_length=20, help_text='Name of release version')
    creation_date = ChemblDateField(blank=True, null=True, help_text='Date database created')
    comments = models.CharField(max_length=2000, blank=True, null=True, help_text='Description of release version')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

# ----------------------------------------------------------------------------------------------------------------------


class ChemblIdLookup(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    ENTITY_TYPE_CHOICES = (
        ('ASSAY', 'ASSAY'),
        ('CELL', 'CELL'),
        ('COMPOUND', 'COMPOUND'),
        ('DOCUMENT', 'DOCUMENT'),
        ('TARGET', 'TARGET'),
        ('TISSUE', 'TISSUE'),
        )

    STATUS_CHOICES = (
        ('ACTIVE', 'ACTIVE'),
        ('INACTIVE', 'INACTIVE'),
        ('OBS', 'OBS'),
        )

    chembl_id = models.CharField(primary_key=True, max_length=20, help_text='ChEMBL identifier')
    entity_type = models.CharField(max_length=50, choices=ENTITY_TYPE_CHOICES, help_text='Type of entity (e.g., COMPOUND, ASSAY, TARGET)')
    entity_id = ChemblIntegerField(length=9, help_text='Primary key for that entity in corresponding table (e.g., molregno for compounds, tid for targets)')
    status = models.CharField(max_length=10, default='ACTIVE', choices=STATUS_CHOICES, help_text='Indicates whether the status of the entity within the database - ACTIVE, INACTIVE (downgraded), OBS (obsolete/removed).')

    class Meta(ChemblCoreAbstractModel.Meta):
        unique_together = (("entity_id", "entity_type"),)

# ----------------------------------------------------------------------------------------------------------------------


