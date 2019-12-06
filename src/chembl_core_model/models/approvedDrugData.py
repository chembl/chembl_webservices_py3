__author__ = 'mnowotka'

from django.db import models
from chembl_core_model.models import *
from chembl_core_db.db.models.abstractModel import ChemblCoreAbstractModel
from chembl_core_db.db.models.abstractModel import ChemblModelMetaClass
from django.utils import six

# ----------------------------------------------------------------------------------------------------------------------


class Products(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    AD_TYPE_CHOICES = (
        ('OTC', 'OTC'),
        ('RX', 'RX'),
        ('DISCN', 'DISCN'),
        )

    NDA_TYPE_CHOICES = (
        ('N', 'N'),
        ('A', 'A'),
        )

    dosage_form = ChemblCharField(max_length=200, blank=True, null=True, help_text='The dosage form of the product (e.g., tablet, capsule etc)')
    route = ChemblCharField(max_length=200, blank=True, null=True, help_text='The administration route of the product (e.g., oral, injection etc)')
    trade_name = ChemblCharField(max_length=200, blank=True, null=True, help_text='The trade name for the product')
    approval_date = ChemblDateField(blank=True, null=True, help_text='The FDA approval date for the product (not necessarily first approval of the active ingredient)')
    ad_type = ChemblCharField(max_length=5, blank=True, null=True, choices=AD_TYPE_CHOICES, help_text='RX = prescription, OTC = over the counter, DISCN = discontinued')
    oral = ChemblNullableBooleanField(help_text='Flag to show whether product is orally delivered')
    topical = ChemblNullableBooleanField(help_text='Flag to show whether product is topically delivered')
    parenteral = ChemblNullableBooleanField(help_text='Flag to show whether product is parenterally delivered')
    information_source = ChemblCharField(max_length=100, blank=True, null=True, help_text='Source of the product information (e.g., Orange Book)')
    black_box_warning = ChemblNullableBooleanField(help_text='Flag to show whether the product label has a black box warning')
    product_class = ChemblCharField(max_length=30, blank=True, null=True)
    applicant_full_name = ChemblCharField(max_length=200, blank=True, null=True, help_text='Name of the company applying for FDA approval')
    innovator_company = ChemblNullableBooleanField(help_text='Flag to show whether the applicant is the innovator of the product')
    product_id = ChemblCharField(primary_key=True, max_length=30, help_text='FDA application number for the product')
    load_date = ChemblDateField(blank=True, null=True, help_text='The date on which one or more of the following fields were created or updated: doasge_form, route, trade_name, approval_date, ad_type, oral, topical, parenteral, information_source, or applicant_full_name). This date is assigned by the EBI parser.')
    removed_date = ChemblDateField(blank=True, null=True, help_text="The date on which this product was first identified (by ebi parser) as having been removed from the information source. The recording of this date was first initiated on 30-JUN-10. Note that a small number of products are removed from OB, but then re-appear... in these cases this field is re-set to 'null' when the product re-appears..")
    nda_type = ChemblCharField(max_length=10, blank=True, null=True, choices=NDA_TYPE_CHOICES, help_text='New Drug Application Type. The type of new drug application approval.  New Drug Applications (NDA or innovator)  are "N".   Abbreviated New Drug Applications (ANDA or generic) are "A".') # TODO: 10 for storing one character sounds strange...
    tmp_ingred_count = ChemblPositiveIntegerField(length=9, blank=True, null=True, help_text='Number of ingredients in the product, to show which are combinations')
    exclude = ChemblIntegerField(length=1, blank=True, null=True, help_text='Non-FDA products, to be excluded')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

# ----------------------------------------------------------------------------------------------------------------------


class AtcClassification(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    who_name = ChemblCharField(max_length=150, blank=True, null=True, help_text='WHO/INN name for the compound')
    level1 = ChemblCharField(max_length=10, blank=True, null=True, help_text='First level of classification')
    level2 = ChemblCharField(max_length=10, blank=True, null=True, help_text='Second level of classification')
    level3 = ChemblCharField(max_length=10, blank=True, null=True, help_text='Third level of classification')
    level4 = ChemblCharField(max_length=10, blank=True, null=True, help_text='Fourth level of classification')
    level5 = ChemblCharField(primary_key=True, max_length=10, help_text='Complete ATC code for compound')
    level1_description = ChemblCharField(max_length=150, blank=True, null=True, help_text='Description of first level of classification')
    level2_description = ChemblCharField(max_length=150, blank=True, null=True, help_text='Description of second level of classification')
    level3_description = ChemblCharField(max_length=150, blank=True, null=True, help_text='Description of third level of classification')
    level4_description = ChemblCharField(max_length=150, blank=True, null=True, help_text='Description of fourth level of classification')
    molecules = models.ManyToManyField(MoleculeDictionary, through='MoleculeAtcClassification')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

# ----------------------------------------------------------------------------------------------------------------------


class UsanStems(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    MAJOR_CLASS_CHOICES = (
        ('GPCR', 'GPCR'),
        ('NR', 'NR'),
        ('PDE', 'PDE'),
        ('ion channel', 'ion channel'),
        ('kinase', 'kinase'),
        ('protease', 'protease'),
        )

    STEM_CLASS_CHOICES = (
        ('Suffix', 'Suffix'),
        ('Prefix', 'Prefix'),
        ('Infix', 'Infix'),
    )

    usan_stem_id = ChemblPositiveIntegerField(primary_key=True, length=9, help_text='Numeric primary key.')
    stem = ChemblCharField(max_length=100, help_text='Stem defined for use in United States Adopted Names.')
    subgroup = ChemblCharField(max_length=100, help_text='More specific subgroup of the stem defined for use in United States Adopted Names.')
    annotation = ChemblCharField(max_length=2000, blank=True, null=True, help_text='Meaning of the stem (e.g., the class of compound it applies to).')
    stem_class = ChemblCharField(max_length=100, blank=True, null=True, choices=STEM_CLASS_CHOICES, help_text='Indicates whether stem is used as a Prefix/Infix/Suffix.') # TODO: 100 is too long for the specified choices
    major_class = ChemblCharField(max_length=100, blank=True, null=True, choices=MAJOR_CLASS_CHOICES, help_text='Protein family targeted by compounds of this class (e.g., GPCR/Ion channel/Protease) where known/applicable.')
    who_extra = ChemblNullableBooleanField(default=False, help_text='Stem not represented in USAN list, but added from WHO INN stem list (where set to 1).')
    downgraded = ChemblNullableBooleanField(default=False, help_text='Stem no longer included in USAN listing (where set to 1).')

    class Meta(ChemblCoreAbstractModel.Meta):
        unique_together = (("stem", "subgroup"),)

# ----------------------------------------------------------------------------------------------------------------------


class HracClassification(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    hrac_class_id = ChemblAutoField(primary_key=True, length=9, help_text='Unique numeric primary key for each level3 code')
    active_ingredient = ChemblCharField(max_length=500, help_text='Name of active ingredient (herbicide) classified by HRAC')
    level1 = ChemblCharField(max_length=2, help_text='HRAC group code - denoting mechanism of action of herbicide')
    level1_description = ChemblCharField(max_length=2000, help_text='Description of mechanism of action provided by HRAC')
    level2 = ChemblCharField(max_length=3, help_text='Indicates a chemical family within a particular HRAC group (number not assigned by HRAC)')
    level2_description = ChemblCharField(max_length=2000, blank=True, null=True, help_text='Description of chemical family provided by HRAC')
    level3 = ChemblCharField(max_length=5, unique=True, help_text='A unique code assigned to each ingredient (based on the level 1 and 2 HRAC classification, but not assigned by HRAC)')
    hrac_code = ChemblCharField(max_length=2, help_text='The official HRAC classification code for the ingredient')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

# ----------------------------------------------------------------------------------------------------------------------


class IracClassification(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    LEVEL1_CHOICES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
        ('M', 'M'),
        ('U', 'U'),
        )

    LEVEL1_DESCRIPTION_CHOICES = (
        ('ENERGY METABOLISM', 'ENERGY METABOLISM'),
        ('GROWTH REGULATION', 'GROWTH REGULATION'),
        ('LIPID SYNTHESIS, GROWTH REGULATION', 'LIPID SYNTHESIS, GROWTH REGULATION'),
        ('MISCELLANEOUS', 'MISCELLANEOUS'),
        ('NERVE ACTION', 'NERVE ACTION'),
        ('NERVE AND MUSCLE ACTION', 'NERVE AND MUSCLE ACTION'),
        ('UNKNOWN', 'UNKNOWN'),
        )

    irac_class_id = ChemblAutoField(primary_key=True, length=9, help_text='Unique numeric primary key for each level4 code')
    active_ingredient = ChemblCharField(max_length=500, help_text='Name of active ingredient (insecticide) classified by IRAC')
    level1 = ChemblCharField(max_length=1, choices=LEVEL1_CHOICES, help_text='Class of action e.g., nerve action, energy metabolism (code not assigned by IRAC)')
    level1_description = ChemblCharField(max_length=2000, choices=LEVEL1_DESCRIPTION_CHOICES, help_text='Description of class of action, as provided by IRAC')
    level2 = ChemblCharField(max_length=3, help_text='IRAC main group code denoting primary site/mechanism of action')
    level2_description = ChemblCharField(max_length=2000, help_text='Description of site/mechanism of action provided by IRAC')
    level3 = ChemblCharField(max_length=6, help_text='IRAC sub-group code denoting chemical class of insecticide')
    level3_description = ChemblCharField(max_length=2000, help_text='Description of chemical class or exemplifying ingredient provided by IRAC')
    level4 = ChemblCharField(max_length=8, unique=True, help_text='A unique code assigned to each ingredient (based on the level 1, 2 and 3 IRAC classification, but not assigned by IRAC)')
    irac_code = ChemblCharField(max_length=3, help_text='The official IRAC classification code for the ingredient')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

# ----------------------------------------------------------------------------------------------------------------------


class FracClassification(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    frac_class_id = ChemblAutoField(primary_key=True, length=9, help_text='Unique numeric primary key for each level5 code')
    active_ingredient = ChemblCharField(max_length=500, help_text='Name of active ingredient (fungicide) classified by FRAC')
    level1 = ChemblCharField(max_length=2, help_text='Mechanism of action code assigned by FRAC')
    level1_description = ChemblCharField(max_length=2000, help_text='Description of mechanism of action')
    level2 = ChemblCharField(max_length=2, help_text='Target site code assigned by FRAC')
    level2_description = ChemblCharField(max_length=2000, blank=True, null=True, help_text='Description of target provided by FRAC')
    level3 = ChemblCharField(max_length=6, help_text='Group number assigned by FRAC')
    level3_description = ChemblCharField(max_length=2000, blank=True, null=True, help_text='Description of group provided by FRAC')
    level4 = ChemblCharField(max_length=7, help_text='Number denoting the chemical group (number not assigned by FRAC)')
    level4_description = ChemblCharField(max_length=2000, blank=True, null=True, help_text='Chemical group name provided by FRAC')
    level5 = ChemblCharField(max_length=8, unique=True, help_text='A unique code assigned to each ingredient (based on the level 1-4 FRAC classification, but not assigned by IRAC)')
    frac_code = ChemblCharField(max_length=4, help_text='The official FRAC classification code for the ingredient')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

# ----------------------------------------------------------------------------------------------------------------------


class PatentUseCodes(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    patent_use_code = ChemblCharField(primary_key=True, max_length=8, help_text='Primary key. Patent use code from FDA Orange Book')
    definition = ChemblCharField(max_length=500, help_text='Definition for the patent use code, from FDA Orange Book.')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

# ----------------------------------------------------------------------------------------------------------------------


class DefinedDailyDose(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    DDD_UNITS_CHOICES = (
        ('LSU', 'LSU'),
        ('MU', 'MU'),
        ('TU', 'TU'),
        ('U', 'U'),
        ('g', 'g'),
        ('mcg', 'mcg'),
        ('mg', 'mg'),
        ('ml', 'ml'),
        ('mmol', 'mmol'),
        ('tablet', 'tablet'),
        )

    atc_code = models.ForeignKey(AtcClassification, on_delete=models.PROTECT,  db_column='atc_code', help_text='ATC code for the compound (foreign key to ATC_CLASSIFICATION table)')
    ddd_value = ChemblPositiveDecimalField(blank=True, null=True, max_digits=9, decimal_places=2, help_text='Value of defined daily dose')
    ddd_units = ChemblCharField(max_length=200, blank=True, null=True, choices=DDD_UNITS_CHOICES, help_text='Units of defined daily dose')
    ddd_admr = ChemblCharField(max_length=1000, blank=True, null=True, help_text='Administration route for dose')
    ddd_comment = ChemblCharField(max_length=2000, blank=True, null=True, help_text='Comment')
    ddd_id = ChemblAutoField(primary_key=True, length=9, help_text='Internal primary key')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

# ----------------------------------------------------------------------------------------------------------------------


class ProductPatents(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    prod_pat_id = ChemblAutoField(primary_key=True, length=9, help_text='Primary key')
    product = models.ForeignKey(Products, on_delete=models.PROTECT,  help_text='Foreign key to products table - FDA application number for the product')
    patent_no = ChemblCharField(max_length=11, help_text='Patent numbers as submitted by the applicant holder for patents covered by the statutory provisions')
    patent_expire_date = ChemblDateField(help_text='Date the patent expires as submitted by the applicant holder including applicable extensions')
    drug_substance_flag = ChemblBooleanField(default=False, help_text='Patents submitted on FDA Form 3542 and listed after August 18, 2003 may have a drug substance flag set to 1, indicating the sponsor submitted the patent as claiming the drug substance')
    drug_product_flag = ChemblBooleanField(default=False, help_text='Patents submitted on FDA Form 3542 and listed after August 18, 2003 may have a drug product flag set to 1, indicating the sponsor submitted the patent as claiming the drug product')
    patent_use_code = models.ForeignKey(PatentUseCodes, on_delete=models.PROTECT,  blank=True, null=True, db_column='patent_use_code', help_text='Code to designate a use patent that covers the approved indication or use of a drug product')
    delist_flag = ChemblBooleanField(default=False, help_text='Sponsor has requested patent be delisted if set to 1.  This patent has remained listed because, under Section 505(j)(5)(D)(i) of the Act, a first applicant may retain eligibility for 180-day exclusivity based on a paragraph IV certification to this patent for a certain period.  Applicants under Section 505(b)(2) are not required to certify to patents where this flag is set to 1')
    in_products = ChemblPositiveIntegerField(length=1, default=0, help_text='Indicates whether the PRODUCT_ID can be found in the PRODUCTS table (where set to 1)')

    class Meta(ChemblCoreAbstractModel.Meta):
        unique_together = (("product", "patent_no", "patent_expire_date", "patent_use_code"),)

# ----------------------------------------------------------------------------------------------------------------------


class MoleculeAtcClassification(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    mol_atc_id = ChemblAutoField(primary_key=True, length=9, help_text='Primary key')
    atc_classification = models.ForeignKey(AtcClassification, on_delete=models.PROTECT,  db_column='level5', help_text='ATC code (foreign key to atc_classification table)')
    molecule = models.ForeignKey(MoleculeDictionary, on_delete=models.PROTECT,  db_column='molregno', help_text='Drug to which the ATC code applies (foreign key to molecule_dictionary table)')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

# ----------------------------------------------------------------------------------------------------------------------


class MoleculeIracClassification(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    mol_irac_id = ChemblAutoField(primary_key=True, length=9, help_text='Primary key.')
    irac_class = models.ForeignKey(IracClassification, on_delete=models.PROTECT,  help_text='Foreign key to the irac_classification table showing the mechanism of action classification for the compound.')
    molecule = models.ForeignKey(MoleculeDictionary, on_delete=models.PROTECT,  db_column='molregno', help_text='Foreign key to the molecule_dictionary table, showing the compound to which the classification applies.')

    class Meta(ChemblCoreAbstractModel.Meta):
        unique_together = (("irac_class", "molecule"),)

# ----------------------------------------------------------------------------------------------------------------------


class MoleculeFracClassification(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    mol_frac_id = ChemblAutoField(primary_key=True, length=9, help_text='Primary key.')
    frac_class = models.ForeignKey(FracClassification, on_delete=models.PROTECT,  help_text='Foreign key to frac_classification table showing the mechanism of action classification of the compound.')
    molecule = models.ForeignKey(MoleculeDictionary, on_delete=models.PROTECT,  db_column='molregno', help_text='Foreign key to molecule_dictionary, showing the compound to which the classification applies.')

    class Meta(ChemblCoreAbstractModel.Meta):
        unique_together = (("frac_class", "molecule"),)

# ----------------------------------------------------------------------------------------------------------------------


class MoleculeHracClassification(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    mol_hrac_id = ChemblAutoField(primary_key=True, length=9, help_text='Primary key')
    hrac_class = models.ForeignKey(HracClassification, on_delete=models.PROTECT,  help_text='Foreign key to hrac_classification table showing the classification for the compound.')
    molecule = models.ForeignKey(MoleculeDictionary, on_delete=models.PROTECT,  db_column='molregno', help_text='Foreign key to molecule_dictionary, showing the compound to which this classification applies.')

    class Meta(ChemblCoreAbstractModel.Meta):
        unique_together = (("hrac_class", "molecule"),)

# ----------------------------------------------------------------------------------------------------------------------


class Formulations(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    product = models.ForeignKey(Products, on_delete=models.PROTECT,  help_text='Unique identifier of the product. FK to PRODUCTS')
    ingredient = ChemblCharField(max_length=200, blank=True, null=True, help_text='Name of the approved ingredient within the product')
    strength = ChemblCharField(max_length=200, blank=True, null=True, help_text='Dose strength')
    record = models.ForeignKey(CompoundRecords, on_delete=models.PROTECT,  help_text='Foreign key to the compound_records table.')
    molecule = models.ForeignKey(MoleculeDictionary, on_delete=models.PROTECT,  blank=True, null=True, db_column='molregno', help_text='Unique identifier of the ingredient FK to MOLECULE_DICTIONARY')
    formulation_id = ChemblAutoField(primary_key=True, length=9, help_text='Primary key.')

    class Meta(ChemblCoreAbstractModel.Meta):
        unique_together = (("record", "product"),)

# ----------------------------------------------------------------------------------------------------------------------

