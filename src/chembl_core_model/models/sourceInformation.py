__author__ = 'mnowotka'

from chembl_core_model.models import *
from chembl_core_db.db.models.abstractModel import ChemblCoreAbstractModel
from chembl_core_db.db.models.abstractModel import ChemblModelMetaClass
from django.utils import six

# ----------------------------------------------------------------------------------------------------------------------


class XrefSource(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    xref_src_db = ChemblCharField(primary_key=True, max_length=60, help_text=u'Name of the source database that is cross-referenced from chembl')
    xref_src_description = ChemblCharField(max_length=300, blank=True, null=True, help_text=u'Longer description of the source database')
    xref_src_url = ChemblCharField(max_length=12000, blank=True, null=True, help_text=u'URL for linking to the source database home page')
    xref_id_url = ChemblCharField(max_length=12000, blank=True, null=True, help_text=u'URL for linking to the source database with a xref_id (substitute id for $$ in url)')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

# ----------------------------------------------------------------------------------------------------------------------


class Source(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    src_id = ChemblAutoField(primary_key=True, length=3, help_text=u'Identifier for each source (used in compound_records and assays tables)')
    src_description = ChemblCharField(max_length=500, blank=True, null=True, help_text=u'Description of the data source')
    src_short_name = ChemblCharField(max_length=20, blank=True, null=True, help_text=u'A short name for each data source, for display purposes')
    default_doc_id = ChemblPositiveIntegerField(length=38, default=0)
    default_loadtype = ChemblPositiveIntegerField(length=38, default=0)

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

# ----------------------------------------------------------------------------------------------------------------------


class Journals(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    journal_id = ChemblAutoField(primary_key=True, length=9)
    title = ChemblCharField(max_length=100, blank=True, null=True)
    iso_abbreviation = ChemblCharField(max_length=50, blank=True, null=True)
    issn_print = ChemblCharField(max_length=20, blank=True, null=True)
    issn_electronic = ChemblCharField(max_length=20, blank=True, null=True)
    publication_start_year = ChemblPositiveIntegerField(length=4, blank=True, null=True)
    nlm_id = ChemblCharField(max_length=15, blank=True, null=True)
    doc_journal = ChemblCharField(max_length=50, blank=True, null=True)

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

    doc_id = ChemblAutoField(primary_key=True, length=9, help_text=u'Unique ID for the document')
    journal = ChemblCharField(max_length=50, db_index=True, blank=True, null=True, help_text=u'Abbreviated journal name for an article')
    year = ChemblPositiveIntegerField(length=4, db_index=True, blank=True, null=True, help_text=u'Year of journal article publication') # TODO: should be date!
    volume = ChemblCharField(max_length=50, db_index=True, blank=True, null=True, help_text=u'Volume of journal article')
    issue = ChemblCharField(max_length=50, db_index=True, blank=True, null=True, help_text=u'Issue of journal article')
    first_page = ChemblCharField(max_length=50, blank=True, null=True, help_text=u'First page number of journal article')
    last_page = ChemblCharField(max_length=50, blank=True, null=True, help_text=u'Last page number of journal article')
    pubmed_id = ChemblPositiveIntegerField(length=11, unique=True, blank=True, null=True, help_text=u'NIH pubmed record ID, where available')
    updated_on = ChemblDateField(blank=True, null=True)
    updated_by = ChemblCharField(max_length=100, blank=True, null=True)
    doi = ChemblCharField(max_length=100, blank=True, null=True, help_text=u'Digital object identifier for this reference')
    chembl = models.OneToOneField(ChemblIdLookup, blank=True, null=False, help_text=u'ChEMBL identifier for this document (for use on web interface etc)') # This combination of null and blank is actually very important!
    title = ChemblCharField(max_length=500, blank=True, null=True, help_text=u'Document title (e.g., Publication title or description of dataset)')
    doc_type = ChemblCharField(max_length=50, choices=DOC_TYPE_CHOICES, help_text=u'Type of the document (e.g., Publication, Deposited dataset)')
    authors = ChemblCharField(max_length=4000, blank=True, null=True, help_text=u'For a deposited dataset, the authors carrying out the screening and/or submitting the dataset.')
    abstract = ChemblTextField(blank=True, null=True, help_text=u'For a deposited dataset, a brief description of the dataset.')
    journal_id = models.ForeignKey(Journals, blank=True, null=True, db_column='journal_id')
    patent_id = ChemblCharField(max_length=20, blank=True, null=True, help_text=u'Patent ID for this document')
    ridx = ChemblCharField(max_length=600, default=u'CLD0', help_text=u'The Depositor Defined Reference Identifier')
    job_id = ChemblPositiveIntegerField(length=38, default=0, help_text=u'The JOB_ID assigned to this record when first inserted.')
    log_id = ChemblPositiveIntegerField(length=38, default=0)
    src_id = ChemblPositiveIntegerField(length=38, default=0, help_text=u'The src_id who owns this document')
    doi_chembl = ChemblCharField(max_length=600, blank=True, null=True)

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

# ----------------------------------------------------------------------------------------------------------------------


class PaperSimilarity(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    sim_id = ChemblAutoField(primary_key=True, length=9)
    doc_1 = models.OneToOneField(Docs, help_text=u'Foreign key to documents table', db_column='doc_id1', related_name=u'to')
    doc_2 = models.ForeignKey(Docs, help_text=u'Foreign key to documents table', db_column='doc_id2', related_name=u'fro')
    pubmed_id1 = ChemblPositiveIntegerField(length=12, blank=True, null=True)
    pubmed_id2 = ChemblPositiveIntegerField(length=12, blank=True, null=True)
    tid_tani = ChemblPositiveDecimalField(blank=True, null=True, max_digits=9, decimal_places=4)
    mol_tani = ChemblPositiveDecimalField(blank=True, null=True, max_digits=9, decimal_places=4)
    avg_tani = ChemblPositiveDecimalField(blank=True, null=True, max_digits=9, decimal_places=4)
    max_tani = ChemblPositiveDecimalField(blank=True, null=True, max_digits=9, decimal_places=4)

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

# ----------------------------------------------------------------------------------------------------------------------

class DocumentTerms(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    id = ChemblAutoField(primary_key=True, length=11)
    term = ChemblCharField(max_length=500)
    documents = models.ManyToManyField('Docs', through="Doc2Term", blank=True)

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

# ----------------------------------------------------------------------------------------------------------------------


class Doc2Term(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    id = ChemblAutoField(primary_key=True, length=11)
    score = ChemblPositiveDecimalField(max_digits=11, decimal_places=6)
    doc = models.ForeignKey(Docs)
    term = models.ForeignKey(DocumentTerms)

    class Meta(ChemblCoreAbstractModel.Meta):
        unique_together = ( ("doc", "term"),  )

# ----------------------------------------------------------------------------------------------------------------------

