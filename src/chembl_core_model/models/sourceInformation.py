__author__ = 'mnowotka'

from django.db import models
from chembl_core_model.models import *
from chembl_core_db.db.models.abstractModel import ChemblCoreAbstractModel
from chembl_core_db.db.models.abstractModel import ChemblModelMetaClass
from django.utils import six

# ----------------------------------------------------------------------------------------------------------------------


class XrefSource(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    xref_src_db = models.CharField(primary_key=True, max_length=60, help_text='Name of the source database that is cross-referenced from chembl')
    xref_src_description = models.CharField(max_length=300, blank=True, null=True, help_text='Longer description of the source database')
    xref_src_url = models.CharField(max_length=12000, blank=True, null=True, help_text='URL for linking to the source database home page')
    xref_id_url = models.CharField(max_length=12000, blank=True, null=True, help_text='URL for linking to the source database with a xref_id (substitute id for $$ in url)')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

# ----------------------------------------------------------------------------------------------------------------------


class Source(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    src_id = ChemblAutoField(primary_key=True, length=3, help_text='Identifier for each source (used in compound_records and assays tables)')
    src_description = models.CharField(max_length=500, blank=True, null=True, help_text='Description of the data source')
    src_short_name = models.CharField(max_length=20, blank=True, null=True, help_text='A short name for each data source, for display purposes')
    default_doc_id = ChemblPositiveIntegerField(length=38, default=0)
    default_loadtype = ChemblPositiveIntegerField(length=38, default=0)

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

# ----------------------------------------------------------------------------------------------------------------------


class Journals(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    journal_id = ChemblAutoField(primary_key=True, length=9)
    title = models.CharField(max_length=100, blank=True, null=True)
    iso_abbreviation = models.CharField(max_length=50, blank=True, null=True)
    issn_print = models.CharField(max_length=20, blank=True, null=True)
    issn_electronic = models.CharField(max_length=20, blank=True, null=True)
    publication_start_year = ChemblPositiveIntegerField(length=4, blank=True, null=True)
    nlm_id = models.CharField(max_length=15, blank=True, null=True)
    doc_journal = models.CharField(max_length=50, blank=True, null=True)

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

# ----------------------------------------------------------------------------------------------------------------------


class Docs(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    DOC_TYPE_CHOICES = (
        ('PUBLICATION', 'PUBLICATION'),
        ('BOOK', 'BOOK'),
        ('DATASET', 'DATASET'),
        ('PATENT', 'PATENT'),
        )

    doc_id = ChemblAutoField(primary_key=True, length=9, help_text='Unique ID for the document')
    journal = models.CharField(max_length=50, db_index=True, blank=True, null=True, help_text='Abbreviated journal name for an article')
    year = ChemblPositiveIntegerField(length=4, db_index=True, blank=True, null=True, help_text='Year of journal article publication') # TODO: should be date!
    volume = models.CharField(max_length=50, db_index=True, blank=True, null=True, help_text='Volume of journal article')
    issue = models.CharField(max_length=50, db_index=True, blank=True, null=True, help_text='Issue of journal article')
    first_page = models.CharField(max_length=50, blank=True, null=True, help_text='First page number of journal article')
    last_page = models.CharField(max_length=50, blank=True, null=True, help_text='Last page number of journal article')
    pubmed_id = ChemblPositiveIntegerField(length=11, unique=True, blank=True, null=True, help_text='NIH pubmed record ID, where available')
    updated_on = ChemblDateField(blank=True, null=True)
    updated_by = models.CharField(max_length=100, blank=True, null=True)
    doi = models.CharField(max_length=100, blank=True, null=True, help_text='Digital object identifier for this reference')
    chembl = models.OneToOneField(ChemblIdLookup, on_delete=models.PROTECT, blank=True, null=False, help_text='ChEMBL identifier for this document (for use on web interface etc)') # This combination of null and blank is actually very important!
    title = models.CharField(max_length=500, blank=True, null=True, help_text='Document title (e.g., Publication title or description of dataset)')
    doc_type = models.CharField(max_length=50, choices=DOC_TYPE_CHOICES, help_text='Type of the document (e.g., Publication, Deposited dataset)')
    authors = models.CharField(max_length=4000, blank=True, null=True, help_text='For a deposited dataset, the authors carrying out the screening and/or submitting the dataset.')
    abstract = ChemblTextField(blank=True, null=True, help_text='For a deposited dataset, a brief description of the dataset.')
    journal_id = models.ForeignKey(Journals, on_delete=models.PROTECT,  blank=True, null=True, db_column='journal_id')
    patent_id = models.CharField(max_length=20, blank=True, null=True, help_text='Patent ID for this document')
    ridx = models.CharField(max_length=600, default='CLD0', help_text='The Depositor Defined Reference Identifier')
    job_id = ChemblPositiveIntegerField(length=38, default=0, help_text='The JOB_ID assigned to this record when first inserted.')
    log_id = ChemblPositiveIntegerField(length=38, default=0)
    src_id = ChemblPositiveIntegerField(length=38, default=0, help_text='The src_id who owns this document')
    doi_chembl = models.CharField(max_length=600, blank=True, null=True)

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

# ----------------------------------------------------------------------------------------------------------------------


class PaperSimilarity(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    sim_id = ChemblAutoField(primary_key=True, length=9)
    doc_1 = models.OneToOneField(Docs, on_delete=models.PROTECT, help_text='Foreign key to documents table', db_column='doc_id1', related_name='to')
    doc_2 = models.ForeignKey(Docs, on_delete=models.PROTECT,  help_text='Foreign key to documents table', db_column='doc_id2', related_name='fro')
    pubmed_id1 = ChemblPositiveIntegerField(length=12, blank=True, null=True)
    pubmed_id2 = ChemblPositiveIntegerField(length=12, blank=True, null=True)
    tid_tani = ChemblPositiveDecimalField(blank=True, null=True, max_digits=9, decimal_places=4)
    mol_tani = ChemblPositiveDecimalField(blank=True, null=True, max_digits=9, decimal_places=4)
    avg_tani = ChemblPositiveDecimalField(blank=True, null=True, max_digits=9, decimal_places=4)
    max_tani = ChemblPositiveDecimalField(blank=True, null=True, max_digits=9, decimal_places=4)

    class Meta(ChemblCoreAbstractModel.Meta):
        pass
