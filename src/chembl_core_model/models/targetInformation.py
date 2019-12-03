__author__ = 'mnowotka'

import datetime
from django.db import models
from chembl_core_model.models import *
from chembl_core_db.db.models.abstractModel import ChemblCoreAbstractModel
from chembl_core_db.db.models.abstractModel import ChemblModelMetaClass
from django.utils import six

# ----------------------------------------------------------------------------------------------------------------------


class TargetType(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    target_type = ChemblCharField(primary_key=True, max_length=30, help_text=u'Target type (as used in target dictionary)')
    target_desc = ChemblCharField(max_length=250, blank=True, null=True, help_text=u'Description of target type')
    parent_type = ChemblCharField(max_length=25, blank=True, null=True, help_text=u"Higher level classification of target_type, allowing grouping of e.g., all 'PROTEIN' targets, all 'NON-MOLECULAR' targets etc.")

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

# ----------------------------------------------------------------------------------------------------------------------


class OrganismClass(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    oc_id = ChemblAutoField(primary_key=True, length=9, help_text=u'Internal primary key')
    tax_id = ChemblPositiveIntegerField(length=11, unique=True, blank=True, null=True, help_text=u'NCBI taxonomy ID for the organism (corresponding to tax_ids in assay2target and target_dictionary tables)')
    l1 = ChemblCharField(max_length=200, blank=True, null=True, help_text=u'Highest level classification (e.g., Eukaryotes, Bacteria, Fungi etc)')
    l2 = ChemblCharField(max_length=200, blank=True, null=True, help_text=u'Second level classification')
    l3 = ChemblCharField(max_length=200, blank=True, null=True, help_text=u'Third level classification')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

# ----------------------------------------------------------------------------------------------------------------------


class OrganismSynonyms(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    tax = models.ForeignKey(OrganismClass, primary_key=True, to_field='tax_id', help_text=u'NCBI tax_id for organism')
    synonyms = ChemblCharField(max_length=3000, help_text=u'Synonyms for this NCBI tax_id')
    source = ChemblCharField(max_length=600, help_text=u'The name of the source of this synonym')

    class Meta(ChemblCoreAbstractModel.Meta):
        unique_together = (("tax", "synonyms", "source"),)

# ----------------------------------------------------------------------------------------------------------------------


class ProteinFamilyClassification(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    protein_class_id = ChemblAutoField(primary_key=True, length=9, help_text=u'Primary key. Unique identifier for each classification.')
    protein_class_desc = ChemblCharField(max_length=810, unique=True, help_text=u'Concatenated description of each classification for searching purposes etc.')
    l1 = ChemblCharField(max_length=100, help_text=u'First level classification (e.g., Enzyme, Transporter, Ion Channel).')
    l2 = ChemblCharField(max_length=100, blank=True, null=True, help_text=u'Second level classification.')
    l3 = ChemblCharField(max_length=100, blank=True, null=True, help_text=u'Third level classification.')
    l4 = ChemblCharField(max_length=100, blank=True, null=True, help_text=u'Fourth level classification.')
    l5 = ChemblCharField(max_length=100, blank=True, null=True, help_text=u'Fifth level classification.')
    l6 = ChemblCharField(max_length=100, blank=True, null=True, help_text=u'Sixth level classification.')
    l7 = ChemblCharField(max_length=100, blank=True, null=True, help_text=u'Seventh level classification.')
    l8 = ChemblCharField(max_length=100, blank=True, null=True, help_text=u'Eighth level classification.')

    class Meta(ChemblCoreAbstractModel.Meta):
        unique_together = (("l1", "l2", "l3", "l4", "l5", "l6", "l7", "l8"),)

# ----------------------------------------------------------------------------------------------------------------------


class ProteinClassification(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    CLASS_LEVEL_CHOICES = (
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        )

    protein_class_id = ChemblAutoField(primary_key=True, length=9, help_text=u'Primary key. Unique identifier for each protein family classification.')
    parent_id = ChemblPositiveIntegerField(length=9, blank=True, null=True, help_text=u'Protein_class_id for the parent of this protein family.')
    pref_name = ChemblCharField(max_length=500, blank=True, null=True, help_text=u'Preferred/full name for this protein family.')
    short_name = ChemblCharField(max_length=50, blank=True, null=True, help_text=u'Short/abbreviated name for this protein family (not necessarily unique).')
    protein_class_desc = ChemblCharField(max_length=410, help_text=u'Concatenated description of each classification for searching purposes etc.')
    definition = ChemblCharField(max_length=4000, blank=True, null=True, help_text=u'Definition of the protein family.')
    downgraded = ChemblBooleanField(default=False)
    replaced_by = ChemblPositiveIntegerField(length=9, blank=True, null=True)
    class_level = ChemblPositiveIntegerField(length=9, choices=CLASS_LEVEL_CHOICES, help_text=u'Level of the class within the hierarchy (level 1 = top level classification)')
    sort_order = ChemblPositiveIntegerField(length=2, blank=True, null=True)
    component_sequences = models.ManyToManyField('ComponentSequences', through="ComponentClass", blank=True)

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

# ----------------------------------------------------------------------------------------------------------------------


class GoClassification(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    ASPECT_CHOICES = (
        ('C', 'C'),
        ('F', 'F'),
        ('P', 'P'),
        )

    CLASS_LEVEL_CHOICES = (
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        )

    go_id = ChemblCharField(primary_key=True, max_length=10, help_text=u'Primary key. Gene Ontology identifier for the GO slim term')
    parent_go_id = ChemblCharField(max_length=10, blank=True, null=True, help_text=u'Gene Ontology identifier for the parent of this GO term in the ChEMBL Drug Target GO slim')
    pref_name = ChemblCharField(max_length=200, blank=True, null=True, help_text=u'Gene Ontology name')
    class_level = ChemblPositiveIntegerField(length=1, blank=True, null=True, choices=CLASS_LEVEL_CHOICES, help_text=u'Indicates the level of the term in the slim (L1 = highest)')
    aspect = ChemblCharField(max_length=1, blank=True, null=True, choices=ASPECT_CHOICES, help_text=u'Indicates which aspect of the Gene Ontology the term belongs to (F = molecular function, P = biological process, C = cellular component)')
    path = ChemblCharField(max_length=1000, blank=True, null=True, help_text=u'Indicates the full path to this term in the GO slim')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

# ----------------------------------------------------------------------------------------------------------------------


class ComponentSequences(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    COMPONENT_TYPE_CHOICES = (
        ('PROTEIN', 'PROTEIN'),
        ('DNA', 'DNA'),
        ('RNA', 'RNA'),
        )

    DB_SOURCE_CHOICES = (
        ('SWISS-PROT', 'SWISS-PROT'),
        ('TREMBL', 'TREMBL'),
        ('Manual', 'Manual'),
        )

    component_id = ChemblAutoField(primary_key=True, length=9, help_text=u'Primary key. Unique identifier for the component.')
    component_type = ChemblCharField(max_length=50, blank=True, null=True, choices=COMPONENT_TYPE_CHOICES, help_text=u"Type of molecular component represented (e.g., 'PROTEIN','DNA','RNA').")
    accession = ChemblCharField(max_length=25, unique=True, blank=True, null=True, help_text=u'Accession for the sequence in the source database from which it was taken (e.g., UniProt accession for proteins).')
    sequence = ChemblTextField(blank=True, null=True, help_text=u'A representative sequence for the molecular component, as given in the source sequence database (not necessarily the exact sequence used in the assay).')
    sequence_md5sum = ChemblCharField(max_length=32, blank=True, null=True, help_text=u'MD5 checksum of the sequence.')
    description = ChemblCharField(max_length=200, blank=True, null=True, help_text=u'Description/name for the molecular component, usually taken from the source sequence database.')
    tax_id = ChemblPositiveIntegerField(length=11, blank=True, null=True, help_text=u'NCBI tax ID for the sequence in the source database (i.e., species that the protein/nucleic acid sequence comes from).') # TODO: should be FK to Organism class
    organism = ChemblCharField(max_length=150, blank=True, null=True, help_text=u'Name of the organism the sequence comes from.')
    db_source = ChemblCharField(max_length=25, blank=True, null=True, choices=DB_SOURCE_CHOICES, help_text=u'The name of the source sequence database from which sequences/accessions are taken. For UniProt proteins, this field indicates whether the sequence is from SWISS-PROT or TREMBL.')
    db_version = ChemblCharField(max_length=10, blank=True, null=True, help_text=u'The version of the source sequence database from which sequences/accession were last updated.')
    insert_date = ChemblDateField(blank=False, null=True, default=datetime.date.today) # blank is false because it has default value
    updated_on = ChemblDateField(blank=True, null=True)
    updated_by = ChemblCharField(max_length=100, blank=True, null=True)

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

# ----------------------------------------------------------------------------------------------------------------------


class VariantSequences(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    ISOFORM_CHOICES = (
        (1, '1'),
        (2, '2'),
        (4, '4'),
        )

    VERSION_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        )

    variant_id = ChemblPositiveIntegerField(primary_key=True, length=9, help_text=u'Primary key, numeric ID for each sequence variant.')
    mutation = ChemblCharField(max_length=2000, blank=True, null=True, help_text=u'Details of variant(s) used, with residue positions adjusted to match provided sequence.')
    accession = ChemblCharField(max_length=25, blank=True, null=True, help_text=u'UniProt accesion for the representative sequence used as the base sequence (without variation).')
    version = ChemblPositiveIntegerField(length=9, blank=True, null=True, choices=VERSION_CHOICES, help_text=u'Version of the UniProt sequence used as the base sequence.')
    isoform = ChemblPositiveIntegerField(length=9, blank=True, null=True, choices=ISOFORM_CHOICES, help_text=u'Details of the UniProt isoform used as the base sequence where relevant.')
    sequence = ChemblTextField(blank=True, null=True, help_text=u'Variant sequence formed by adjusting the UniProt base sequence with the specified mutations/variations.')
    organism = ChemblCharField(max_length=200, blank=True, null=True, help_text=u'Organism from which the sequence was obtained.')

    class Meta(ChemblCoreAbstractModel.Meta):
        # unique_together = (("mutation", "accession"),)
        pass

# ----------------------------------------------------------------------------------------------------------------------


class TargetDictionary(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    TARGET_PARENT_TYPE_CHOICES = (
        ('MOLECULAR', 'MOLECULAR'),
        ('NON-MOLECULAR', 'NON-MOLECULAR'),
        ('PROTEIN', 'PROTEIN'),
        ('UNDEFINED', 'UNDEFINED'),
        )

    tid = ChemblAutoField(primary_key=True, length=9, help_text=u'Unique ID for the target')
    target_type = models.ForeignKey(TargetType, blank=True, null=True, db_column='target_type', help_text=u'Describes whether target is a protein, an organism, a tissue etc. Foreign key to TARGET_TYPE table.')
    pref_name = ChemblCharField(max_length=200, db_index=True, help_text=u'Preferred target name: manually curated')
    tax_id = ChemblPositiveIntegerField(length=11, db_index=True, blank=True, null=True, help_text=u'NCBI taxonomy id of target') # TODO: should be FK to OrganismClass.tax_id
    organism = ChemblCharField(max_length=150, db_index=True, blank=True, null=True, help_text=u'Source organism of molecuar target or tissue, or the target organism if compound activity is reported in an organism rather than a protein or tissue')
    updated_on = ChemblDateField(blank=True, null=True)
    updated_by = ChemblCharField(max_length=100, blank=True, null=True)
    chembl = models.ForeignKey(ChemblIdLookup, blank=True, null=False, help_text=u'ChEMBL identifier for this target (for use on web interface etc)') # This combination of null and blank is actually very important!
    insert_date = ChemblDateField(blank=False, null=True, default=datetime.date.today) # blank is false because it has default value
    target_parent_type = ChemblCharField(max_length=100, blank=True, null=True, choices=TARGET_PARENT_TYPE_CHOICES)
    species_group_flag = ChemblBooleanField(default=False, help_text=u"Flag to indicate whether the target represents a group of species, rather than an individual species (e.g., 'Bacterial DHFR'). Where set to 1, indicates that any associated target components will be a representative, rather than a comprehensive set.")
    downgraded = ChemblBooleanField(default=False, help_text=u'Flag to indicate that the target is downgraded (if equal to 1)')
    component_sequences = models.ManyToManyField('ComponentSequences', through="TargetComponents")
    docs = models.ManyToManyField('Docs', through="Assays")

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

# ----------------------------------------------------------------------------------------------------------------------


class TargetPredictions(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    pred_id = ChemblAutoField(primary_key=True, length=11, help_text=u'Unique ID for the prediction')
    molecule = models.ForeignKey('MoleculeDictionary', db_column='parent_molregno', help_text=u'Foreign key to the molecule_dictionary, indicating the molecule to which the predictions belong.')
    molecule_chembl_id = ChemblCharField(max_length=20, db_column='chembl_id', blank=True, null=True)
    target = models.ForeignKey(TargetDictionary, db_column='tid', help_text=u'Foreign key to the target_dictionary, indicating the target to which the predictions belong.')
    target_chembl_id = ChemblCharField(max_length=60)
    target_accession = ChemblCharField(max_length=60)
    probability = ChemblPositiveDecimalField(max_digits=12, decimal_places=11)
    in_training = ChemblCharField(max_length=60)
    value = ChemblPositiveIntegerField(length=5)

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

# ----------------------------------------------------------------------------------------------------------------------


class ComponentClass(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    component = models.ForeignKey(ComponentSequences, help_text=u'Foreign key to component_sequences table.')
    protein_class = models.ForeignKey(ProteinClassification, help_text=u'Foreign key to the protein_classification table.')
    comp_class_id = ChemblAutoField(primary_key=True, length=9, help_text=u'Primary key.')

    class Meta(ChemblCoreAbstractModel.Meta):
        unique_together = (("component", "protein_class"),)

# ----------------------------------------------------------------------------------------------------------------------


class ComponentSynonyms(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    SYN_TYPE_CHOICES = (
        ('HGNC_SYMBOL', 'HGNC_SYMBOL'),
        ('GENE_SYMBOL', 'GENE_SYMBOL'),
        ('UNIPROT', 'UNIPROT'),
        ('MANUAL', 'MANUAL'),
        ('OTHER', 'OTHER'),
        ('EC_NUMBER', 'EC_NUMBER'),
        )

    compsyn_id = ChemblAutoField(primary_key=True, length=9, help_text=u'Primary key.')
    component = models.ForeignKey(ComponentSequences, help_text=u'Foreign key to the component_sequences table. The component to which this synonym applies.')
    component_synonym = ChemblCharField(max_length=500, blank=True, null=True, help_text=u'The synonym for the component.')
    syn_type = ChemblCharField(max_length=20, blank=True, null=True, choices=SYN_TYPE_CHOICES, help_text=u'The type or origin of the synonym (e.g., GENE_SYMBOL).')

    class Meta(ChemblCoreAbstractModel.Meta):
        unique_together = (("component", "component_synonym", "syn_type"),)

# ----------------------------------------------------------------------------------------------------------------------


class ComponentXref(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    comp_xref_id = ChemblAutoField(primary_key=True, length=9, help_text=u'Primary key.')
    component = models.ForeignKey(ComponentSequences, help_text=u'Foreign key to component_sequences table.')
    xref_src_db = ChemblCharField(max_length=150)
    xref_id = ChemblCharField(max_length=300)
    xref_name = ChemblCharField(max_length=3000, blank=True, null=True)

    class Meta(ChemblCoreAbstractModel.Meta):
        unique_together = (("component", "xref_src_db", "xref_id"),)


# ----------------------------------------------------------------------------------------------------------------------


class CellDictionary(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    cell_id = ChemblAutoField(primary_key=True, length=9, help_text=u'Primary key. Unique identifier for each cell line in the target_dictionary.')
    cell_name = ChemblCharField(max_length=50, help_text=u'Name of each cell line (as used in the target_dicitonary pref_name).')
    cell_description = ChemblCharField(max_length=200, blank=True, null=True, help_text=u'Longer description (where available) of the cell line.')
    cell_source_tissue = ChemblCharField(max_length=50, blank=True, null=True, help_text=u'Tissue from which the cell line is derived, where known.')
    cell_source_organism = ChemblCharField(max_length=150, blank=True, null=True, help_text=u'Name of organism from which the cell line is derived.')
    cell_source_tax_id = ChemblPositiveIntegerField(length=11, blank=True, null=True, help_text=u'NCBI tax ID of the organism from which the cell line is derived.') # TODO: should be FK to organism class
    clo_id = ChemblCharField(max_length=11, blank=True, null=True, help_text=u'ID for the corresponding cell line in Cell Line Ontology')
    efo_id = ChemblCharField(max_length=12, blank=True, null=True, help_text=u'ID for the corresponding cell line in Experimental Factory Ontology')
    cellosaurus_id = ChemblCharField(max_length=15, blank=True, null=True, help_text=u'ID for the corresponding cell line in Cellosaurus Ontology')
    downgraded = ChemblNullableBooleanField(default=False, help_text=u'Indicates the cell line has been removed (if set to 1)')
    cl_lincs_id = ChemblCharField(max_length=8, blank=True, null=True, help_text=u'Cell ID used in LINCS (Library of Integrated Network-based Cellular Signatures)')
    chembl = models.OneToOneField(ChemblIdLookup, blank=True, null=True, help_text=u'ChEMBL identifier for the cell (used in web interface etc)')
    curator_comment = ChemblCharField(max_length=6000, blank=True, null=True)

    class Meta(ChemblCoreAbstractModel.Meta):
        unique_together = (("cell_name", "cell_source_tax_id"),)

# ----------------------------------------------------------------------------------------------------------------------


class ProteinClassSynonyms(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    SYN_TYPE_CHOICES = (
        ('CHEMBL', 'CHEMBL'),
        ('CONCEPT_WIKI', 'CONCEPT_WIKI'),
        ('UMLS', 'UMLS'),
        ('CW_XREF', 'CW_XREF'),
        ('MESH_XREF', 'MESH_XREF'),
        )

    protclasssyn_id = ChemblAutoField(primary_key=True, length=9, help_text=u'Primary key.')
    protein_class = models.ForeignKey(ProteinClassification, help_text=u'Foreign key to the PROTEIN_CLASSIFICATION table. The protein_class to which this synonym applies.')
    protein_class_synonym = ChemblCharField(max_length=1000, blank=True, null=True, help_text=u'The synonym for the protein class.')
    syn_type = ChemblCharField(max_length=20, blank=True, null=True, choices=SYN_TYPE_CHOICES, help_text=u'The type or origin of the synonym (e.g., ChEMBL, Concept Wiki, UMLS).')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass # unique_together = ( ("protein_class", "protein_class_synonym", "syn_type"),  )

# ----------------------------------------------------------------------------------------------------------------------


class TissueDictionary(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    tissue_id = ChemblAutoField(primary_key=True, length=9, help_text=u'Primary key, numeric ID for each tissue.')
    uberon_id = ChemblCharField(max_length=15, blank=True, null=True, help_text=u'Uberon ontology identifier for this tissue.')
    pref_name = ChemblCharField(max_length=200, help_text=u'Name for the tissue (in most cases Uberon name).')
    efo_id = ChemblCharField(max_length=20, blank=True, null=True, help_text=u'Experimental Factor Ontology identifier for the tissue.')
    chembl = models.OneToOneField(ChemblIdLookup, help_text=u'ChEMBL identifier for this tissue (for use on web interface etc)')
    bto_id = ChemblCharField(max_length=20, blank=True, null=True, help_text=u'BRENDA Tissue Ontology identifier for the tissue.')
    caloha_id = ChemblCharField(max_length=7, blank=True, null=True, help_text=u'Swiss Institute for Bioinformatics CALOHA Ontology identifier for the tissue.')

    class Meta(ChemblCoreAbstractModel.Meta):
        unique_together = (("uberon_id", "efo_id"),)

# ----------------------------------------------------------------------------------------------------------------------


class ComponentGo(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    comp_go_id = ChemblAutoField(primary_key=True, length=9, help_text=u'Primary key')
    component = models.ForeignKey(ComponentSequences, help_text=u'Foreign key to COMPONENT_SEQUENCES table. The protein component this GO term applies to')
    go = models.ForeignKey(GoClassification, help_text=u'Foreign key to the GO_CLASSIFICATION table. The GO term that this protein is mapped to')

    class Meta(ChemblCoreAbstractModel.Meta):
        unique_together = (("component", "go"),)

# ----------------------------------------------------------------------------------------------------------------------


class TargetComponents(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    HOMOLOGUE_CHOICES = (
        (0, '0'),
        (1, '1'),
        (2, '2'),
        )

    RELATIONSHIP_CHOICES = (
        ('SINGLE PROTEIN', 'SINGLE PROTEIN'),
        ('PROTEIN SUBUNIT', 'PROTEIN SUBUNIT'),
        ('RNA SUBUNIT', 'RNA SUBUNIT'),
        ('GROUP MEMBER', 'GROUP MEMBER'),
        ('RNA', 'RNA'),
        ('INTERACTING PROTEIN', 'INTERACTING PROTEIN'),
        ('COMPARATIVE PROTEIN', 'COMPARATIVE PROTEIN'),
        ('FUSION PROTEIN', 'FUSION PROTEIN'),
        ('UNCURATED', 'UNCURATED'),
        )

    STOICHIOMETRY_CHOICES = (
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (12, '12'),
        )

    target = models.ForeignKey(TargetDictionary, db_column='tid', help_text=u'Foreign key to the target_dictionary, indicating the target to which the components belong.')
    component = models.ForeignKey(ComponentSequences, help_text=u'Foreign key to the component_sequences table, indicating which components belong to the target.')
    relationship = ChemblCharField(max_length=20, default=u'UNCURATED', choices=RELATIONSHIP_CHOICES)
    stoichiometry = ChemblPositiveIntegerField(length=3, blank=True, null=True, choices=STOICHIOMETRY_CHOICES)
    targcomp_id = ChemblAutoField(primary_key=True, length=9, help_text=u'Primary key.')
    homologue = ChemblPositiveIntegerField(length=1, default=0, choices=HOMOLOGUE_CHOICES, help_text=u'Indicates that the given component is a homologue of the correct component (e.g., from a different species) when set to 1. This may be the case if the sequence for the correct protein/nucleic acid cannot be found in sequence databases. A value of 2 indicates that the sequence given is a representative of a species group, e.g., an E. coli protein to represent the target of a broad-spectrum antibiotic.')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

# ----------------------------------------------------------------------------------------------------------------------


class TargetRelations(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    RELATIONSHIP_CHOICES = (
        ('EQUIVALENT TO', 'EQUIVALENT TO'),
        ('OVERLAPS WITH', 'OVERLAPS WITH'),
        ('SUBSET OF', 'SUBSET OF'),
        ('SUPERSET OF', 'SUPERSET OF'),
        )

    target = models.ForeignKey(TargetDictionary, related_name=u'to', db_column='tid', help_text=u'Identifier for target of interest (foreign key to target_dictionary table)')
    relationship = ChemblCharField(max_length=20, choices=RELATIONSHIP_CHOICES, help_text=u'Relationship between two targets (e.g., SUBSET OF, SUPERSET OF, OVERLAPS WITH)')
    related_target = models.ForeignKey(TargetDictionary, related_name=u'fro', db_column='related_tid', help_text=u'Identifier for the target that is related to the target of interest (foreign key to target_dicitionary table)')
    targrel_id = ChemblAutoField(primary_key=True, length=9, help_text=u'Primary key')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

# ----------------------------------------------------------------------------------------------------------------------


class TargetXref(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    target = models.ForeignKey(TargetDictionary, db_column='tid', help_text=u'Foreign key to target_dictionary table')
    xref_src_db = models.ForeignKey(XrefSource, db_column='xref_src_db', help_text=u'Name of the database that this cross-reference links to')
    xref_id = ChemblCharField(max_length=300, unique=True, help_text=u'Identifier for the entry in the cross-referenced database')
    xref_name = ChemblCharField(max_length=3000, blank=True, null=True, help_text=u'Name for the entry in the cross-referenced database, where applicable')
    targ_xref_id = ChemblPositiveIntegerField(primary_key=True, length=9)

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

# ----------------------------------------------------------------------------------------------------------------------


