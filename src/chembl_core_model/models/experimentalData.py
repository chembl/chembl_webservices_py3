__author__ = 'mnowotka'

from django.db import models
from chembl_core_model.models import *
from chembl_core_db.db.models.abstractModel import ChemblCoreAbstractModel
from chembl_core_db.db.models.abstractModel import ChemblModelMetaClass
from django.utils import six

# ----------------------------------------------------------------------------------------------------------------------


class AssayType(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    assay_type = ChemblCharField(primary_key=True, max_length=1, help_text='Single character representing assay type')
    assay_desc = ChemblCharField(max_length=250, blank=True, null=True, help_text='Description of assay type')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

# ----------------------------------------------------------------------------------------------------------------------


class RelationshipType(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    relationship_type = ChemblCharField(primary_key=True, max_length=1, help_text='Relationship_type flag used in the assay2target table')
    relationship_desc = ChemblCharField(max_length=250, blank=True, null=True, help_text='Description of relationship_type flags')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

# ----------------------------------------------------------------------------------------------------------------------


class ConfidenceScoreLookup(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    confidence_score = ChemblPositiveIntegerField(primary_key=True, length=1, help_text='0-9 score showing level of confidence in assignment of the precise molecular target of the assay')
    description = ChemblCharField(max_length=100, help_text='Description of the target types assigned with each score')
    target_mapping = ChemblCharField(max_length=30, help_text='Short description of the target types assigned with each score')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

# ----------------------------------------------------------------------------------------------------------------------


class CurationLookup(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    curated_by = ChemblCharField(primary_key=True, max_length=32, help_text='Short description of the level of curation')
    description = ChemblCharField(max_length=100, help_text='Definition of terms in the curated_by field.')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

# ----------------------------------------------------------------------------------------------------------------------


class ActivityStdsLookup(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    std_act_id = ChemblAutoField(primary_key=True, length=9, help_text='Primary key.')
    standard_type = ChemblCharField(max_length=250, help_text='The standard_type that other published_types in the activities table have been converted to.')
    definition = ChemblCharField(max_length=500, blank=True, null=True, help_text='A description/definition of the standard_type.')
    standard_units = ChemblCharField(max_length=100, help_text='The units that are applied to this standard_type and to which other published_units are converted. Note a standard_type may have more than one allowable standard_unit and therefore multiple rows in this table.')
    normal_range_min = models.DecimalField(blank=True, null=True, max_digits=24, decimal_places=12, help_text="The lowest value for this activity type that is likely to be genuine. This is only an approximation, so lower genuine values may exist, but it may be desirable to validate these before using them. For a given standard_type/units, values in the activities table below this threshold are flagged with a data_validity_comment of 'Outside typical range'.")
    normal_range_max = models.DecimalField(blank=True, null=True, max_digits=24, decimal_places=12, help_text="The highest value for this activity type that is likely to be genuine. This is only an approximation, so higher genuine values may exist, but it may be desirable to validate these before using them. For a given standard_type/units, values in the activities table above this threshold are flagged with a data_validity_comment of 'Outside typical range'.")

    class Meta(ChemblCoreAbstractModel.Meta):
        unique_together = (("standard_type", "standard_units"),)

# ----------------------------------------------------------------------------------------------------------------------


class DataValidityLookup(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    data_validity_comment = ChemblCharField(primary_key=True, max_length=30, help_text='Primary key. Short description of various types of errors/warnings applied to values in the activities table.')
    description = ChemblCharField(max_length=200, blank=True, null=True, help_text='Definition of the terms in the data_validity_comment field.')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

# ----------------------------------------------------------------------------------------------------------------------


class BioassayOntology(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    TERM_TYPE_CHOICES = (
        ('ASSAY_FORMAT', 'ASSAY_FORMAT'),
        ('ASSAY_TYPE', 'ASSAY_TYPE'),
        ('BIOASSAY', 'BIOASSAY'),
        ('ENDPOINT', 'ENDPOINT'),
        ('ENDPOINT_CORRELATION', 'ENDPOINT_CORRELATION'),
        ('ENDPOINT_CURVE', 'ENDPOINT_CURVE'),
        ('ENDPOINT_DIRECTION', 'ENDPOINT_DIRECTION'),
        ('ENDPOINT_MOA', 'ENDPOINT_MOA'),
        ('ENDPOINT_PUBCHEM', 'ENDPOINT_PUBCHEM'),
        ('ENDPOINT_RESULT', 'ENDPOINT_RESULT'),
        )

    bao_id = ChemblCharField(primary_key=True, max_length=11, help_text='Bioassay Ontology identifier (BAO version 2.0)')
    label = ChemblCharField(max_length=100, help_text='Bioassay Ontology label for the term (BAO version 2.0)')
    term_type = ChemblCharField(max_length=20, blank=True, null=True, choices=TERM_TYPE_CHOICES)
    bao_version = ChemblCharField(max_length=10)
    parent_bao_id = ChemblCharField(max_length=20, blank=True, null=True)

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

# ----------------------------------------------------------------------------------------------------------------------


class ParameterType(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    parameter_type = ChemblCharField(primary_key=True, max_length=40, help_text='Short name for the type of parameter associated with an assay')
    description = ChemblCharField(max_length=2000, blank=True, null=True, help_text='Description of the parameter type')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

# ----------------------------------------------------------------------------------------------------------------------


class Assays(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    ASSAY_CATEGORY_CHOICES = (
        ('screening', 'screening'),
        ('panel', 'panel'),
        ('confirmatory', 'confirmatory'),
        ('summary', 'summary'),
        ('other', 'other'),
        )

    ASSAY_TEST_TYPE_CHOICES = (
        ('In vivo', 'In vivo'),
        ('In vitro', 'In vitro'),
        ('Ex vivo', 'Ex vivo'),
        )

    assay_id = ChemblAutoField(primary_key=True, length=9, help_text='Unique ID for the assay')
    doc = models.ForeignKey(Docs, on_delete=models.PROTECT,  help_text='Foreign key to documents table')
    description = ChemblIndexedCharField(max_length=4000, db_index=True, blank=True, null=True, help_text='Description of the reported assay')
    assay_type = models.ForeignKey(AssayType, on_delete=models.PROTECT,  blank=True, null=True, db_column='assay_type', help_text='Assay classification, e.g. B=Binding assay, A=ADME assay, F=Functional assay')
    assay_test_type = ChemblCharField(max_length=20, blank=True, null=True, choices=ASSAY_TEST_TYPE_CHOICES, help_text='Type of assay system (i.e., in vivo or in vitro)')
    assay_category = ChemblCharField(max_length=20, blank=True, null=True, choices=ASSAY_CATEGORY_CHOICES, help_text='screening, confirmatory (ie: dose-response), summary, panel or other.')
    assay_organism = ChemblCharField(max_length=250, blank=True, null=True, help_text='Name of the organism for the assay system (e.g., the organism, tissue or cell line in which an assay was performed). May differ from the target organism (e.g., for a human protein expressed in non-human cells, or pathogen-infected human cells).')
    assay_tax_id = ChemblPositiveIntegerField(length=11, blank=True, null=True, help_text='NCBI tax ID for the assay organism.')  # TODO: should be FK to OrganismClass.tax_id
    assay_strain = ChemblCharField(max_length=200, blank=True, null=True, help_text='Name of specific strain of the assay organism used (where known)')
    assay_tissue = ChemblCharField(max_length=100, blank=True, null=True, help_text='Name of tissue used in the assay system (e.g., for tissue-based assays) or from which the assay system was derived (e.g., for cell/subcellular fraction-based assays).')
    assay_cell_type = ChemblCharField(max_length=100, blank=True, null=True, help_text='Name of cell type or cell line used in the assay system (e.g., for cell-based assays).')
    assay_subcellular_fraction = ChemblCharField(max_length=100, blank=True, null=True, help_text='Name of subcellular fraction used in the assay system (e.g., microsomes, mitochondria).')
    target = models.ForeignKey(TargetDictionary, on_delete=models.PROTECT,  blank=True, null=True, db_column='tid', help_text='Target identifier to which this assay has been mapped. Foreign key to target_dictionary. From ChEMBL_15 onwards, an assay will have only a single target assigned.')
    relationship_type = models.ForeignKey(RelationshipType, on_delete=models.PROTECT,  blank=True, null=True, db_column='relationship_type', help_text='Flag indicating of the relationship between the reported target in the source document and the assigned target from TARGET_DICTIONARY. Foreign key to RELATIONSHIP_TYPE table.')
    confidence_score = models.ForeignKey(ConfidenceScoreLookup, on_delete=models.PROTECT,  blank=True, null=True, db_column='confidence_score', help_text='Confidence score, indicating how accurately the assigned target(s) represents the actually assay target. Foreign key to CONFIDENCE_SCORE table. 0 means uncurated/unassigned, 1 = low confidence to 9 = high confidence.')
    curated_by = models.ForeignKey(CurationLookup, on_delete=models.PROTECT,  blank=True, null=True, db_column='curated_by', help_text='Indicates the level of curation of the target assignment. Foreign key to curation_lookup table.')
    activity_count = ChemblPositiveIntegerField(length=9, blank=True, null=True, help_text='Number of activities recorded for this assay')
    assay_source = ChemblCharField(max_length=50, db_index=True, blank=True, null=True)
    src = models.ForeignKey(Source, on_delete=models.PROTECT,  help_text='Foreign key to source table')
    src_assay_id = ChemblCharField(max_length=50, blank=True, null=True, help_text='Identifier for the assay in the source database/deposition (e.g., pubchem AID)')
    chembl = models.OneToOneField(ChemblIdLookup, on_delete=models.PROTECT, help_text='ChEMBL identifier for this assay (for use on web interface etc)')
    updated_on = ChemblDateField(blank=True, null=True)
    updated_by = ChemblCharField(max_length=250, blank=True, null=True)
    orig_description = ChemblCharField(max_length=4000, blank=True, null=True)
    a2t_complex = ChemblNullableBooleanField()
    a2t_multi = ChemblNullableBooleanField()
    mc_tax_id = ChemblPositiveIntegerField(length=11, blank=True, null=True)
    mc_organism = ChemblCharField(max_length=100, blank=True, null=True)
    mc_target_type = ChemblCharField(max_length=28, blank=True, null=True)
    mc_target_name = ChemblCharField(max_length=4000, blank=True, null=True)
    mc_target_accession = ChemblCharField(max_length=255, blank=True, null=True)
    a2t_assay_tax_id = ChemblPositiveIntegerField(length=11, blank=True, null=True)
    a2t_assay_organism = ChemblCharField(max_length=250, blank=True, null=True)
    a2t_updated_on = ChemblDateField(blank=True, null=True)
    a2t_updated_by = ChemblCharField(max_length=100, blank=True, null=True)
    cell = models.ForeignKey(CellDictionary, on_delete=models.PROTECT,  blank=True, null=True, help_text='Foreign key to cell dictionary. The cell type or cell line used in the assay')
    bao_format = models.ForeignKey(BioassayOntology, on_delete=models.PROTECT,  blank=True, null=True, db_column='bao_format', help_text='ID for the corresponding format type in BioAssay Ontology (e.g., cell-based, biochemical, organism-based etc)')
    tissue = models.ForeignKey(TissueDictionary, on_delete=models.PROTECT,  blank=True, null=True, help_text='ID for the corresponding tissue/anatomy in Uberon. Foreign key to tissue_dictionary')
    curation_comment = ChemblCharField(max_length=4000, blank=True, null=True, help_text='Just for prudence!')
    variant = models.ForeignKey(VariantSequences, on_delete=models.PROTECT,  blank=True, null=True, help_text='Foreign key to variant_sequences table. Indicates the mutant/variant version of the target used in the assay (where known/applicable)')
    aidx = ChemblCharField(max_length=600, default='CLD0', help_text='The Depositor Defined Assay Identifier')
    job_id = ChemblPositiveIntegerField(length=38, default=0, help_text='The JOB_ID assigned to this record when first inserted.')
    log_id = ChemblPositiveIntegerField(length=38, default=0)
    ridx = ChemblCharField(max_length=600, default='CLD0', help_text='The Depositor Defined Reference Identifier.')
    tid_fixed = ChemblIntegerField(length=1, blank=True, null=True)

    class Meta(ChemblCoreAbstractModel.Meta):
        pass


class AssayClassification(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    assay_class_id = ChemblPositiveIntegerField(primary_key=True, length=9, help_text='Primary Key')
    l1 = ChemblCharField(max_length=100, blank=True, null=True, help_text='High level classification e.g., by anatomical/therapeutic area')
    l2 = ChemblCharField(max_length=100, blank=True, null=True, help_text='Mid-level classification e.g., by phenotype/biological process')
    l3 = ChemblCharField(max_length=1000, db_index=True, blank=True, null=True, help_text='Fine-grained classification e.g., by assay type')
    class_type = ChemblCharField(max_length=50, blank=True, null=True, help_text='The type of assay being classified e.g., in vivo efficacy')
    bao_id = ChemblCharField(max_length=11, blank=True, null=True, help_text='BAO ID')
    source = ChemblCharField(max_length=50, blank=True, null=True, help_text='Source')
    assays = models.ManyToManyField(Assays, through='AssayClassMap')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass


class AssayClassMap(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    ass_cls_map_id = ChemblPositiveIntegerField(primary_key=True, length=38, help_text='Primary Key')
    assay = models.ForeignKey(Assays, on_delete=models.PROTECT,  blank=True, null=True, help_text='Foreign key to assay. The Assay of the AssayClassification')
    assay_class = models.ForeignKey(AssayClassification, on_delete=models.PROTECT,  blank=True, null=True, help_text='Foreign key to assay_classification. The AssayClassification of the Assay')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass


class AssayParameters(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    assay_param_id = ChemblAutoField(primary_key=True, length=9, help_text='Numeric primary key')
    assay = models.ForeignKey(Assays, on_delete=models.PROTECT,  help_text='Foreign key to assays table. The assay to which this parameter belongs')
    type = ChemblCharField(max_length=250, help_text='The type of parameter being described, according to the original data source')
    relation = ChemblCharField(max_length=50, blank=True, null=True, help_text='The relation symbol for the parameter being described, according to the original data source')
    value = ChemblNoLimitDecimalField(blank=True, null=True, help_text='The value of the parameter being described, according to the original data source. Used for numeric data')
    units = ChemblCharField(max_length=100, blank=True, null=True, help_text='The units for the parameter being described, according to the original data source')
    text_value = ChemblCharField(max_length=4000, blank=True, null=True, help_text='The text value of the parameter being described, according to the original data source. Used for non-numeric/qualitative data')
    standard_type = ChemblCharField(max_length=250, blank=True, null=True, help_text='Standardized form of the TYPE')
    standard_relation = ChemblCharField(max_length=50, blank=True, null=True, help_text='Standardized form of the RELATION')
    standard_value = ChemblNoLimitDecimalField(blank=True, null=True, help_text='Standardized form of the VALUE')
    standard_units = ChemblCharField(max_length=100, blank=True, null=True, help_text='Standardized form of the UNITS')
    standard_text_value = ChemblCharField(max_length=4000, blank=True, null=True, help_text='Standardized form of the TEXT_VALUE')
    comments = ChemblCharField(max_length=4000, blank=True, null=True, help_text='Additional comments describing the parameter')
    standard_type_fixed = ChemblPositiveIntegerField(length=1, default=0, help_text='If set to 1, indicates that the normalized_type has been set manually, and should not be automatically overwritten')
    active = ChemblPositiveIntegerField(length=1, default=1, help_text='If set to 1, indicates that the parameter type is still found in this dataset. 0 is used for parameters that used to be present but are no longer used')

    class Meta(ChemblCoreAbstractModel.Meta):
        unique_together = (("assay", "type"),)

# ----------------------------------------------------------------------------------------------------------------------


class Activities(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    MANUAL_CURATION_FLAG_CHOICES = (
        (0, '0'),
        (1, '1'),
        (2, '2'),
        )

    STANDARD_RELATION_CHOICES = (
        ('>', '>'),
        ('<', '<'),
        ('=', '='),
        ('~', '~'),
        ('<=', '<='),
        ('>=', '>='),
        ('<<', '<<'),
        ('>>', '>>'),
        )

    activity_id = ChemblAutoField(primary_key=True, length=11, help_text='Unique ID for the activity row')
    assay = models.ForeignKey(Assays, on_delete=models.PROTECT,  help_text='Foreign key to the assays table (containing the assay description)')
    doc = models.ForeignKey(Docs, on_delete=models.PROTECT,  blank=True, null=True, help_text='Foreign key to documents table (for quick lookup of publication details - can also link to documents through compound_records or assays table)')
    record = models.ForeignKey(CompoundRecords, on_delete=models.PROTECT,  help_text='Foreign key to the compound_records table (containing information on the compound tested)')
    molecule = models.ForeignKey(MoleculeDictionary, on_delete=models.PROTECT,  blank=True, null=True, db_column='molregno', help_text='Foreign key to compounds table (for quick lookup of compound structure - can also link to compounds through compound_records table)')
    standard_relation = ChemblCharField(max_length=50, db_index=True, blank=True, null=True, novalidate=True, choices=STANDARD_RELATION_CHOICES, help_text='Symbol constraining the activity value (e.g. >, <, =)')
    standard_value = ChemblNoLimitDecimalField(db_index=True, blank=True, null=True, help_text='Same as PUBLISHED_VALUE but transformed to common units: e.g. mM concentrations converted to nM.') # TODO: NUMBER in Oracle
    standard_units = ChemblCharField(max_length=100, db_index=True, blank=True, null=True, help_text="Selected 'Standard' units for data type: e.g. concentrations are in nM.")
    standard_flag = ChemblNullableBooleanField(help_text='Shows whether the standardised columns have been curated/set (1) or just default to the published data (0).')
    standard_type = ChemblCharField(max_length=250, db_index=True, blank=True, null=True, help_text='Standardised version of the published_activity_type (e.g. IC50 rather than Ic-50/Ic50/ic50/ic-50)')
    updated_by = ChemblCharField(max_length=100, blank=True, null=True)
    updated_on = ChemblDateField(blank=True, null=True)
    activity_comment = ChemblCharField(max_length=4000, blank=True, null=True, help_text="Describes non-numeric activities i.e. 'Slighty active', 'Not determined'")
    manual_curation_flag = ChemblPositiveIntegerField(length=1, blank=False, null=True, default=0, choices=MANUAL_CURATION_FLAG_CHOICES) # blank is false because it has default value
    data_validity_comment = models.ForeignKey(DataValidityLookup, on_delete=models.PROTECT,  blank=True, null=True, db_column='data_validity_comment', help_text="Comment reflecting whether the values for this activity measurement are likely to be correct - one of 'Manually validated' (checked original paper and value is correct), 'Potential author error' (value looks incorrect but is as reported in the original paper), 'Outside typical range' (value seems too high/low to be correct e.g., negative IC50 value), 'Non standard unit type' (units look incorrect for this activity type).")
    potential_duplicate = ChemblNullableBooleanField(help_text='When set to 1, indicates that the value is likely to be a repeat citation of a value reported in a previous ChEMBL paper, rather than a new, independent measurement. Note: value of zero does not guarantee that the measurement is novel/independent though')
    original_activity_id = ChemblPositiveIntegerField(length=11, blank=True, null=True) # TODO: should that be FK referencing Activities in future?
    pchembl_value = models.DecimalField(db_index=True, blank=True, null=True, max_digits=4, decimal_places=2, help_text='Negative log of selected concentration-response activity values (IC50/EC50/XC50/AC50/Ki/Kd/Potency)')
    bao_endpoint = models.ForeignKey(BioassayOntology, on_delete=models.PROTECT,  blank=True, null=True, db_column='bao_endpoint', help_text='ID for the corresponding result type in BioAssay Ontology (based on standard_type)')
    uo_units = ChemblCharField(max_length=10, blank=True, null=True, help_text='ID for the corresponding unit in Unit Ontology (based on standard_units)')
    qudt_units = ChemblCharField(max_length=70, blank=True, null=True, help_text='ID for the corresponding unit in QUDT Ontology (based on standard_units)')
    job_id = ChemblPositiveIntegerField(length=38, db_index=True, default=0, help_text='The JOB_ID assigned to this record when first inserted.')
    ridx = ChemblCharField(max_length=600, default='CLD0', help_text='The Depositor defined Reference Identifier')
    toid = ChemblPositiveIntegerField(length=38, blank=True, null=True, help_text='The Test Occassion Identifier')
    upper_value = ChemblNoLimitDecimalField(blank=True, null=True, help_text='Where the activity is a range, this represents the highest value of the range (numerically), while the PUBLISHED_VALUE column represents the lower value')
    standard_upper_value = ChemblNoLimitDecimalField(blank=True, null=True, help_text='Where the activity is a range, this represents the standardised version of the highest value of the range (with the lower value represented by STANDARD_VALUE)')
    src = models.ForeignKey(Source, on_delete=models.PROTECT,  blank=True, null=True, help_text='Foreign key to source table, indicating the source of the activity value')
    type = ChemblCharField(max_length=750, help_text='Type of end-point measurement: e.g. IC50, LD50, %inhibition etc, as it appears in the original dataset')
    relation = ChemblCharField(max_length=150, blank=True, null=True, help_text='Symbol constraining the activity value (e.g. >, <, =), as it appears in the original dataset')
    value = ChemblNoLimitDecimalField(blank=True, null=True, help_text='Datapoint value as it appears in the original dataset.')
    units = ChemblCharField(max_length=300, blank=True, null=True, help_text='Units of measurement as they appear in the original dataset')
    text_value = ChemblCharField(max_length=3000, blank=True, null=True, help_text='Non-numeric value for measurement as in original dataset')
    standard_text_value = ChemblCharField(max_length=3000, blank=True, null=True, help_text='Standardized version of non-numeric measurement')
    # TODO: improper definition make it easier/possible  for the tastypie to create the activity_supplementary_data_by_activity on the web services
    # activity_smids = models.ManyToManyField('ActivitySmid', through='ActivitySuppMap')
    activity_supps = models.ManyToManyField('ActivitySupp', through='ActivitySuppMap')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass


class ActivityProperties(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):
    ap_id = ChemblAutoField(primary_key=True, length=9, help_text='Numeric primary key')
    activity = models.ForeignKey(Activities, on_delete=models.PROTECT,
                              help_text='Foreign key to assays table. The activity to which this property belongs')
    type = ChemblCharField(max_length=250, blank=True, null=False,
                           help_text='The parameter or property type')
    relation = ChemblCharField(max_length=50, blank=True, null=True,
                           help_text='Symbol constraining the value (e.g. >, <, =)')
    value = ChemblNoLimitDecimalField(blank=True, null=True,
                                      help_text='Numberical value for the parameter or property')
    units = ChemblCharField(max_length=100, blank=True, null=True,
                           help_text='Units of measurement')
    text_value = ChemblCharField(max_length=1000, blank=True, null=True,
                           help_text='Non-numerical value of the parameter or property')
    standard_type = ChemblCharField(max_length=250, blank=True, null=True,
                           help_text='Standardised form of the TYPE')
    standard_relation = ChemblCharField(max_length=50, blank=True, null=True,
                           help_text='Standardised form of the RELATION')
    standard_value = ChemblNoLimitDecimalField(blank=True, null=True,
                                      help_text='Standardised form of the VALUE')
    standard_units = ChemblCharField(max_length=100, blank=True, null=True,
                           help_text='Standardised form of the UNITS')
    standard_text_value = ChemblCharField(max_length=1000, blank=True, null=True,
                           help_text='Standardised form of the TEXT_VALUE')
    comments = ChemblCharField(max_length=4000, blank=True, null=True,
                           help_text='A Comment.')
    result_flag = ChemblPositiveIntegerField(length=1, default=0,
                                        help_text='A flag to indicate, if set to 1, that this type is a dependent variable/result (e.g., slope) rather than an independent variable/parameter (0, the default).')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass


class ActivitySmid(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):
    smid = ChemblPositiveIntegerField(primary_key=True, length=11, help_text='Primary Key')
    samid = ChemblPositiveIntegerField(length=11, blank=True, null=True, help_text='The depositors value of SAMID.')
    granular_mapping = ChemblCharField(max_length=1, blank=True, null=True, help_text='G flag to indicate if mapping is completed. If G=1 mapping completed. If G=0 or null then mapping not completed')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass


class ActivitySupp(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):
    as_id = ChemblPositiveIntegerField(primary_key=True, length=11, help_text='Primary Key')
    rgid = ChemblPositiveIntegerField(db_index=True, length=11, blank=True, null=True, help_text='Record Grouping ID, used to group together related data points in this table.')
    smid = models.OneToOneField(ActivitySmid, on_delete=models.PROTECT, db_column='smid', blank=True, null=True, help_text='Foreign key to Activities SMID')
    type = ChemblCharField(db_index=True, max_length=250, blank=False, null=False, help_text='Type of end-point measurement: e.g. IC50, LD50, %inhibition etc, as it appears in the original dataset')
    relation = ChemblCharField(db_index=True, max_length=50, blank=True, null=True, help_text='Symbol constraining the activity value (e.g. >, <, =), as it appears in the original dataset')
    value = ChemblNoLimitDecimalField(db_index=True, blank=True, null=True, help_text='Datapoint value as it appears in the original dataset.')
    units = ChemblCharField(db_index=True, max_length=100, blank=True, null=True, help_text='Units of measurement as they appear in the original dataset')
    text_value = ChemblCharField(db_index=True, max_length=1000, blank=True, null=True, help_text='Non-numeric value for measurement as in original dataset')
    standard_type = ChemblCharField(db_index=True, max_length=250, blank=True, null=True, help_text='Standardised form of the TYPE')
    standard_relation = ChemblCharField(db_index=True, max_length=500, blank=True, null=True, help_text='Standardised form of the RELATION')
    standard_value = ChemblNoLimitDecimalField(db_index=True, blank=True, null=True, help_text='Standardized form of the VALUE')
    standard_units = ChemblCharField(db_index=True, max_length=100, blank=True, null=True, help_text='Standardised form of the UNITS')
    standard_text_value = ChemblCharField(db_index=True, max_length=1000, blank=True, null=True, help_text='Standardised form of the TEXT_VALUE')
    comments = ChemblCharField(max_length=4000, blank=True, null=True, help_text='A Comment.')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass


class ActivitySuppMap(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):
    actsm_id = ChemblPositiveIntegerField(primary_key=True, length=11, help_text='Primary Key')
    activity = models.ForeignKey(Activities, on_delete=models.PROTECT,  blank=False, null=False, help_text='Foreign key to Activities')
    # TODO: improper definition make it easier/possible for the tastypie to create the activity_supplementary_data_by_activity on the web services
    # smid = models.ForeignKey(ActivitySmid, on_delete=models.PROTECT,  db_column='smid', blank=False, null=False, help_text=u'Foreign key to Activities SMID')
    smid = models.ForeignKey(ActivitySupp, on_delete=models.PROTECT,  to_field="smid", db_column="smid")

    class Meta:
        unique_together = (("activity", "smid"),)

# ----------------------------------------------------------------------------------------------------------------------
