__author__ = 'mnowotka'

import datetime
from django.db import models
from chembl_core_model.models import *
from chembl_core_db.db.customFields import BlobField, ChemblCharField
from chembl_core_db.db.customManagers import CompoundMolsManager
from chembl_core_db.db.models.abstractModel import ChemblCoreAbstractModel
from chembl_core_db.db.models.abstractModel import ChemblModelMetaClass
from django.utils import six
from django.conf import settings

try:
    COMPOUND_MOLS_TABLE = settings.COMPOUND_MOLS_TABLE
except AttributeError:
    COMPOUND_MOLS_TABLE = None

try:
    CTAB_COLUMN = settings.CTAB_COLUMN
except AttributeError:
    CTAB_COLUMN = None

# ----------------------------------------------------------------------------------------------------------------------


class MoleculeBrowseDrugs(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    AVAILABILITY_TYPE_CHOICES = (
        (-2, -2),
        (-1, -1),
        (0, 0),
        (1, 1),
        (2, 2),
        )

    CHIRALITY_CHOICES = (
        (-1, -1),
        (0, 0),
        (1, 1),
        (2, 2),
        )

    DEVELOPMENT_PHASE_CHOICES = (
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        )

    parent = models.OneToOneField('MoleculeDictionary', primary_key=True, db_column='parent_molregno')
    chembl = models.OneToOneField(ChemblIdLookup, blank=True, null=False, help_text=u'ChEMBL identifier for this compound (for use on web interface etc)')
    synonyms = ChemblCharField(max_length=4000, blank=True, null=True)
    development_phase = ChemblPositiveIntegerField(length=1, blank=True, null=True, choices=DEVELOPMENT_PHASE_CHOICES)
    research_codes = ChemblCharField(max_length=600, blank=True, null=True)
    applicants = ChemblCharField(max_length=2000, blank=True, null=True)
    usan_stem = ChemblCharField(max_length=600, blank=True, null=True)
    usan_year = ChemblPositiveIntegerField(length=4, blank=True, null=True)
    first_approval = ChemblPositiveIntegerField(length=4, blank=True, null=True)
    atc_code = ChemblCharField(max_length=2000, blank=True, null=True)
    drug_type = ChemblIntegerField(length=2, blank=True, null=True)
    rule_of_five = ChemblNullableBooleanField()
    first_in_class = ChemblNullableBooleanField()
    chirality = ChemblIntegerField(length=1, blank=True, null=True, choices=CHIRALITY_CHOICES)
    prodrug = ChemblNullableBooleanField()
    oral = ChemblNullableBooleanField()
    parenteral = ChemblNullableBooleanField()
    topical = ChemblNullableBooleanField()
    black_box = ChemblNullableBooleanField()
    availability_type = ChemblIntegerField(length=1, blank=True, null=True, choices=AVAILABILITY_TYPE_CHOICES)
    usan_stem_definition = ChemblCharField(max_length=2000, blank=True, null=True)
    indication_class = ChemblCharField(max_length=2000, blank=True, null=True)
    usan_stem_substem = ChemblCharField(max_length=300, blank=True, null=True)
    atc_code_description = ChemblCharField(max_length=2000, blank=True, null=True)
    ob_patent = ChemblCharField(max_length=120, blank=True, null=True)
    sc_patent = ChemblCharField(max_length=180, blank=True, null=True)
    withdrawn_year = ChemblPositiveIntegerField(length=4, blank=True, null=True)
    withdrawn_country = ChemblCharField(max_length=2000, blank=True, null=True)
    withdrawn_reason = ChemblCharField(max_length=2000, blank=True, null=True)
    withdrawn_class = ChemblCharField(max_length=1000, blank=True, null=True)

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

# ----------------------------------------------------------------------------------------------------------------------


class ResearchStem(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    res_stem_id = ChemblAutoField(primary_key=True, length=9, help_text=u'Primary key. Unique ID for each research code stem.')
    research_stem = ChemblCharField(max_length=20, unique=True, blank=True, null=True, help_text=u'The actual stem/prefix used in the research code.')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

# ----------------------------------------------------------------------------------------------------------------------


class StructuralAlertSets(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    alert_set_id = ChemblPositiveIntegerField(primary_key=True, length=9, help_text=u'Unique ID for the structural alert set')
    set_name = ChemblCharField(max_length=100, unique=True, help_text=u'Name (or origin) of the structural alert set')
    priority = ChemblPositiveIntegerField(length=2, help_text=u'Priority assigned to the structural alert set for display on the ChEMBL interface (priorities >=4 are shown by default).')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

# ----------------------------------------------------------------------------------------------------------------------


class BioComponentSequences(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    component_id = ChemblAutoField(primary_key=True, length=9, help_text=u'Primary key. Unique identifier for each of the molecular components of biotherapeutics in ChEMBL (e.g., antibody chains, recombinant proteins, synthetic peptides).')
    component_type = ChemblCharField(max_length=50, help_text=u"Type of molecular component (e.g., 'PROTEIN','DNA','RNA').") # TODO: add constraint, is always PROTEIN now... this should be similar to compound sequences!!!
    description = ChemblCharField(max_length=200, blank=True, null=True, help_text=u'Description/name of molecular component.')
    sequence = ChemblTextField(blank=True, null=True, help_text=u'Sequence of the biotherapeutic component.')
    sequence_md5sum = ChemblCharField(max_length=32, blank=True, null=True, help_text=u'MD5 checksum of the sequence.')
    tax_id = ChemblPositiveIntegerField(length=11, blank=True, null=True, help_text=u'NCBI tax ID for the species from which the sequence is derived. May be null for humanized monoclonal antibodies, synthetic peptides etc.')
    organism = ChemblCharField(max_length=150, blank=True, null=True, help_text=u'Name of the species from which the sequence is derived.')
    updated_on = ChemblDateField(blank=True, null=True)
    updated_by = ChemblCharField(max_length=100, blank=True, null=True)
    insert_date = ChemblDateField(blank=True, null=True)
    accession = ChemblCharField(max_length=25, blank=True, null=True)
    db_source = ChemblCharField(max_length=25, blank=True, null=True)
    db_version = ChemblCharField(max_length=10, blank=True, null=True)

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

# ----------------------------------------------------------------------------------------------------------------------


class MoleculeDictionary(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    AVAILABILITY_TYPE_CHOICES = (
        (-2, '-2'),
        (-1, '-1'),
        (0, '0'),
        (1, '1'),
        (2, '2'),
        )

    CHIRALITY_CHOICES = (
        (-1, '-1'),
        (0, '0'),
        (1, '1'),
        (2, '2'),
        )

    MAX_PHASE_CHOICES = (
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        )

    MOLECULE_TYPE_CHOICES = (
        ('Antibody', 'Antibody'),
        ('Cell', 'Cell'),
        ('Enzyme', 'Enzyme'),
        ('Oligonucleotide', 'Oligonucleotide'),
        ('Oligosaccharide', 'Oligosaccharide'),
        ('Protein', 'Protein'),
        ('Small molecule', 'Small molecule'),
        ('Unclassified', 'Unclassified'),
        ('Unknown', 'Unknown'),
        )

    NOMERGE_REASON_CHOICES = (
        ('GSK', 'GSK'),
        ('PARENT', 'PARENT'),
        ('PDBE', 'PDBE'),
        ('SALT', 'SALT'),
        )

    STRUCTURE_TYPE_CHOICES = (
        ('NONE', 'NONE'),
        ('MOL', 'MOL'),
        ('SEQ', 'SEQ'),
        ('BOTH', 'BOTH'),
        )

    @property
    def compoundImage(self):
        if hasattr(self, 'compoundimages'):
            return self.compoundimages
        return None

    @property
    def compoundMol(self):
        if hasattr(self, 'compoundmols'):
            return self.compoundmols
        return None

    @property
    def compoundProperty(self):
        if hasattr(self, 'compoundproperties'):
            return self.compoundproperties
        return None

    @property
    def compoundStructure(self):
        if hasattr(self, 'compoundstructures'):
            return self.compoundstructures
        return None

    @property
    def moleculeHierarchy(self):
        if hasattr(self, 'moleculehierarchy'):
            return self.moleculehierarchy
        return None

    molregno = ChemblAutoField(primary_key=True, length=9, help_text=u'Internal Primary Key for the molecule')
    pref_name = ChemblCharField(max_length=255, db_index=True, blank=True, null=True, help_text=u'Preferred name for the molecule')
    chembl = models.OneToOneField(ChemblIdLookup, blank=True, null=False, help_text=u'ChEMBL identifier for this compound (for use on web interface etc)') # This combination of null and blank is actually very important!
    max_phase = ChemblPositiveIntegerField(length=1, db_index=True, default=0, choices=MAX_PHASE_CHOICES, help_text=u'Maximum phase of development reached for the compound (4 = approved). Null where max phase has not yet been assigned.')
    therapeutic_flag = ChemblBooleanField(db_index=True, default=False, help_text=u'Indicates that a drug has a therapeutic application (as opposed to e.g., an imaging agent, additive etc).')
    dosed_ingredient = ChemblBooleanField(default=False, help_text=u'Indicates that the drug is dosed in this form (e.g., a particular salt)')
    structure_key = ChemblCharField(max_length=27, db_index=True, unique=True, blank=True, null=True, help_text=u'Unique key for the structure/sequence (e.g., inchi_key or sequence md5sum) to help enforce non-redundancy.')
    structure_type = ChemblCharField(max_length=10, default='MOL', choices=STRUCTURE_TYPE_CHOICES, novalidate_default=True, help_text=u'Indications whether the molecule has a small molecule structure or a protein sequence (MOL indicates an entry in the compound_structures table, SEQ indications an entry in the protein_therapeutics table, NONE indicates an entry in neither table, e.g., structure unknown)')
    chebi_id = ChemblPositiveIntegerField(length=9, unique=True, blank=True, null=True, help_text=u'Assigned ChEBI ID for the compound, where it is a small molecule.')
    chebi_par_id = ChemblPositiveIntegerField(length=9, blank=True, null=True, help_text=u'Preferred ChEBI ID for the compound (where different from assigned)')
    insert_date = ChemblDateField(blank=False, null=True, default=datetime.date.today) # blank is false because it has default value
    molfile_update = ChemblDateField(blank=True, null=True)
    downgraded = ChemblBooleanField(default=False)
    downgrade_reason = ChemblCharField(max_length=2000, blank=True, null=True)
    replacement_mrn = ChemblPositiveIntegerField(length=9, blank=True, null=True)
    checked_by = ChemblCharField(max_length=2000, blank=True, null=True)
    nomerge = ChemblBooleanField(default=False, help_text=u"Flag to show that this entry shouldn't be merged with others of the same structure (when set to 1)")
    nomerge_reason = ChemblCharField(max_length=200, blank=True, null=True, choices=NOMERGE_REASON_CHOICES, help_text=u'Reason for entry not being merged with others of the same structure (e.g., known to be a stereoisomer)')
    molecule_type = ChemblCharField(max_length=30, blank=True, null=True, choices=MOLECULE_TYPE_CHOICES, help_text=u'Type of molecule (Small molecule, Protein, Antibody, Oligosaccharide, Oligonucleotide, Cell, Unknown)')
    first_approval = ChemblPositiveIntegerField(length=4, blank=True, null=True, help_text=u'Earliest known approval year for the molecule') # TODO: should be date!
    oral = ChemblBooleanField(default=False, help_text=u'Indicates whether the drug is known to be administered orally.')
    parenteral = ChemblBooleanField(default=False, help_text=u'Indicates whether the drug is known to be administered parenterally')
    topical = ChemblBooleanField(default=False, help_text=u'Indicates whether the drug is known to be administered topically.')
    black_box_warning = ChemblNullBooleanField(default=0, help_text=u'Indicates that the drug has a black box warning')
    natural_product = ChemblNullBooleanField(default=(-1), help_text=u'Indicates whether the compound is natural product-derived (currently curated only for drugs)')
    first_in_class = ChemblNullBooleanField(default=(-1), help_text=u'Indicates whether this is known to be the first compound of its class (e.g., acting on a particular target).')
    chirality = ChemblIntegerField(length=1, default=(-1), choices=CHIRALITY_CHOICES, help_text=u'Shows whether a drug is dosed as a racemic mixture (0), single stereoisomer (1) or is an achiral molecule (2)')
    prodrug = ChemblNullBooleanField(default=(-1), help_text=u'Indicates that the molecule is a pro-drug (see molecule hierarchy for active component, where known)')
    inorganic_flag = ChemblNullBooleanField(default=0, help_text=u'Indicates whether the molecule is inorganic (i.e., containing only metal atoms and <2 carbon atoms)')
    usan_year = ChemblPositiveIntegerField(length=4, blank=True, null=True, help_text=u'The year in which the application for a USAN/INN name was made')
    availability_type = ChemblIntegerField(length=1, blank=True, null=True, choices=AVAILABILITY_TYPE_CHOICES, help_text=u'The availability type for the drug (0 = discontinued, 1 = prescription only, 2 = over the counter)')
    usan_stem = ChemblCharField(max_length=50, blank=True, null=True, help_text=u'Where the compound has been assigned a USAN name, this indicates the stem, as described in the USAN_STEM table.')
    polymer_flag = ChemblNullableBooleanField(help_text=u'Indicates whether a molecule is a small molecule polymer (e.g., polistyrex)')
    usan_substem = ChemblCharField(max_length=50, blank=True, null=True, help_text=u'Where the compound has been assigned a USAN name, this indicates the substem')
    usan_stem_definition = ChemblCharField(max_length=1000, blank=True, null=True, help_text=u'Definition of the USAN stem')
    indication_class = ChemblCharField(max_length=1000, blank=True, null=True, help_text=u'Indication class(es) assigned to a drug in the USP dictionary')
    products = models.ManyToManyField('Products', through="Formulations", blank=True)
    docs = models.ManyToManyField('Docs', through="CompoundRecords", blank=True)
    assays = models.ManyToManyField('Assays', through="Activities", blank=True)
    withdrawn_flag = ChemblBooleanField(default=False, help_text="Flag indicating whether the drug has been withdrawn in at least one country (not necessarily in the US)")
    withdrawn_year = ChemblPositiveIntegerField(length=4, blank=True, null=True, help_text=u'Year the drug was first withdrawn in any country')
    withdrawn_country = ChemblCharField(max_length=2000, blank=True, null=True, help_text=u'List of countries/regions where the drug has been withdrawn')
    withdrawn_reason = ChemblCharField(max_length=2000, blank=True, null=True, help_text=u'Reasons for withdrawal (e.g., safety)')
    withdrawn_class = ChemblCharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return 'Molecule {0} ({1}) {2}'.format(self.molregno, self.chembl_id, self.pref_name)

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

# ----------------------------------------------------------------------------------------------------------------------


class ResearchCompanies(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    co_stem_id = ChemblAutoField(primary_key=True, length=9, help_text=u'Primary key.')
    res_stem = models.ForeignKey(ResearchStem, blank=True, null=True, help_text=u'Foreign key to research_stem table.')
    company = ChemblCharField(max_length=100, blank=True, null=True, help_text=u'Name of current company associated with this research code stem.')
    country = ChemblCharField(max_length=50, blank=True, null=True, help_text=u'Country in which the company uses this research code stem.') # TODO: should have a constraint
    previous_company = ChemblCharField(max_length=100, blank=True, null=True, help_text=u'Previous name of the company associated with this research code stem (e.g., if the company has undergone acquisitions/mergers).')

    class Meta(ChemblCoreAbstractModel.Meta):
        unique_together = (("res_stem", "company"),)

# ----------------------------------------------------------------------------------------------------------------------


class StructuralAlerts(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    alert_id = ChemblPositiveIntegerField(primary_key=True, length=9, help_text=u'Primary key. Unique identifier for the structural alert')
    alertset = models.ForeignKey(StructuralAlertSets, db_column='alert_set_id', help_text=u'Foreign key to structural_alert_sets table indicating which set this particular alert comes from')
    alert_name = ChemblCharField(max_length=100, help_text=u'A name for the structural alert')
    smarts = ChemblCharField(max_length=4000, help_text=u'SMARTS defining the structural feature that is considered to be an alert')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass # unique_together = (("alert_set", "alert_name", "smarts"),)

# ----------------------------------------------------------------------------------------------------------------------


class CompoundProperties(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    MOLECULAR_SPECIES_CHOICES = (
        ('ACID', 'ACID'),
        ('BASE', 'BASE'),
        ('ZWITTERION', 'ZWITTERION'),
        ('NEUTRAL', 'NEUTRAL'),
        )

    NUM_RO5_VIOLATIONS_CHOICES = (
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        )

    RO3_PASS_CHOICES = (
        ('Y', 'Y'),
        ('N', 'N'),
        )

    molecule = models.OneToOneField(MoleculeDictionary, primary_key=True, db_column='molregno', help_text=u'Foreign key to compounds table (compound structure)')
    mw_freebase = ChemblPositiveDecimalField(db_index=True, blank=True, null=True, decimal_places=2, max_digits=9, help_text=u'Molecular weight of parent compound')
    alogp = models.DecimalField(db_index=True, blank=True, null=True, decimal_places=2, max_digits=9, help_text=u'Calculated ALogP')
    hba = ChemblPositiveIntegerField(length=3, db_index=True, blank=True, null=True, help_text=u'Number hydrogen bond acceptors')
    hbd = ChemblPositiveIntegerField(length=3, db_index=True, blank=True, null=True, help_text=u'Number hydrogen bond donors')
    psa = ChemblPositiveDecimalField(db_index=True, blank=True, null=True, decimal_places=2, max_digits=9, help_text=u'Polar surface area')
    rtb = ChemblPositiveIntegerField(length=3, db_index=True, blank=True, null=True, help_text=u'Number rotatable bonds')
    ro3_pass = ChemblCharField(max_length=3, blank=True, null=True, choices=RO3_PASS_CHOICES, help_text=u'Indicates whether the compound passes the rule-of-three (mw < 300, logP < 3 etc)')
    num_ro5_violations = ChemblPositiveIntegerField(length=1, db_index=True, blank=True, null=True, choices=NUM_RO5_VIOLATIONS_CHOICES, help_text=u"Number of violations of Lipinski's rule-of-five, using HBA and HBD definitions")
    acd_most_apka = models.DecimalField(blank=True, null=True, max_digits=9, decimal_places=2, help_text=u'The most acidic pKa calculated using ACDlabs v12.01')
    acd_most_bpka = ChemblPositiveDecimalField(blank=True, null=True, max_digits=9, decimal_places=2, help_text=u'The most basic pKa calculated using ACDlabs v12.01')
    acd_logp = models.DecimalField(blank=True, null=True, max_digits=9, decimal_places=2, help_text=u'The calculated octanol/water partition coefficient using ACDlabs v12.01')
    acd_logd = models.DecimalField(blank=True, null=True, max_digits=9, decimal_places=2, help_text=u'The calculated octanol/water distribution coefficient at pH7.4 using ACDlabs v12.01')
    molecular_species = ChemblCharField(max_length=50, blank=True, null=True, choices=MOLECULAR_SPECIES_CHOICES, help_text=u'Indicates whether the compound is an acid/base/neutral')
    full_mwt = ChemblPositiveDecimalField(blank=True, null=True, max_digits=9, decimal_places=2, help_text=u'Molecular weight of the full compound including any salts')
    aromatic_rings = ChemblPositiveIntegerField(length=3, blank=True, null=True, help_text=u'Number of aromatic rings')
    heavy_atoms = ChemblPositiveIntegerField(length=3, blank=True, null=True, help_text=u'Number of heavy (non-hydrogen) atoms')
    qed_weighted = ChemblPositiveDecimalField(blank=True, null=True, max_digits=3, decimal_places=2, help_text=u'Weighted quantitative estimate of drug likeness (as defined by Bickerton et al., Nature Chem 2012)')
    updated_on = ChemblDateField(blank=True, null=True, help_text=u'Shows date properties were last recalculated')
    mw_monoisotopic = ChemblPositiveDecimalField(blank=True, null=True, max_digits=11, decimal_places=4, help_text=u'Monoisotopic parent molecular weight')
    full_molformula = ChemblCharField(max_length=100, blank=True, null=True, help_text=u'Molecular formula for the full compound (including any salt)')
    hba_lipinski = ChemblPositiveIntegerField(length=3, blank=True, null=True, help_text=u"Number of hydrogen bond acceptors calculated according to Lipinski's original rules (i.e., N + O count))")
    hbd_lipinski = ChemblPositiveIntegerField(length=3, blank=True, null=True, help_text=u"Number of hydrogen bond donors calculated according to Lipinski's original rules (i.e., NH + OH count)")
    num_lipinski_ro5_violations = ChemblPositiveIntegerField(length=1, blank=True, null=True, choices=NUM_RO5_VIOLATIONS_CHOICES, help_text=u"Number of violations of Lipinski's rule of five using HBA_LIPINSKI and HBD_LIPINSKI counts")

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

# ----------------------------------------------------------------------------------------------------------------------


class CompoundRecords(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    SRC_COMPOUND_ID_VERSION_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        )

    record_id = ChemblAutoField(primary_key=True, length=9, help_text=u'Unique ID for a compound/record')
    molecule = models.ForeignKey(MoleculeDictionary, blank=True, null=True, db_column='molregno', help_text=u'Foreign key to compounds table (compound structure)')
    doc = models.ForeignKey(Docs, help_text=u'Foreign key to documents table')
    compound_key = ChemblCharField(max_length=250, db_index=True, blank=True, null=True, help_text=u'Key text identifying this compound in the scientific document')
    compound_name = ChemblCharField(max_length=4000, blank=True, null=True, help_text=u'Name of this compound recorded in the scientific document')
    filename = ChemblCharField(max_length=250, blank=True, null=True)
    updated_by = ChemblCharField(max_length=100, blank=True, null=True)
    updated_on = ChemblDateField(blank=True, null=True)
    src = models.ForeignKey(Source, help_text=u'Foreign key to source table')
    src_compound_id = ChemblCharField(max_length=150, db_index=True, blank=True, null=True, help_text=u'Identifier for the compound in the source database (e.g., pubchem SID)')
    removed = ChemblNullBooleanField(default=0)
    src_compound_id_version = ChemblPositiveIntegerField(length=3, blank=True, null=True, choices=SRC_COMPOUND_ID_VERSION_CHOICES)
    curated = ChemblBooleanField(default=False, help_text=u'Can be marked as curated if the entry has been mapped to a molregno other than that given by the original structure, and hence care should be taken when updating')
    load_date = ChemblDateField(blank=True, null=True, default=datetime.date.today)
    ridx = ChemblCharField(max_length=600, default=u'CLD0', help_text=u'The Depositor Defined Reference Identifier.')
    cidx = ChemblCharField(max_length=600, default=u'CLD0', help_text=u'The Depositor Defined Compound Identifier.')
    job_id = ChemblPositiveIntegerField(length=38, default=0, help_text=u'The JOB_ID assigned to this record when first inserted.')
    log_id = ChemblPositiveIntegerField(length=38, default=0)
    molregno_fixed = ChemblIntegerField(length=38, blank=True, null=True, help_text=u"The molregno associated with this record has been fixed by curators: Do not update automatically. null = not fixed. '1' = Fixed")
    molregno_comment = ChemblCharField(max_length=3000, blank=True, null=True, help_text=u'The reason why this molregno is associated with this record')
    molregno_sv = ChemblNoLimitDecimalField(blank=True, null=True, help_text=u'The version of the standardizer protocol used')
    products = models.ManyToManyField('Products', through="Formulations", blank=True)
    assays = models.ManyToManyField('Assays', through="Activities", blank=True)

    def __str__(self):
        return 'Compound Record {0} for Molecule {1}, name {2}, key {3}'.format(
            self.record_id, self.molecule.chembl_id if self.molecule else '', self.compound_name, self.compound_key)

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

# ----------------------------------------------------------------------------------------------------------------------


class MoleculeHierarchy(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    molecule = models.OneToOneField(MoleculeDictionary, primary_key=True, db_column='molregno', help_text=u'Foreign key to compounds table. This field holds a list of all of the ChEMBL compounds with associated data (e.g., activity information, approved drugs). Parent compounds that are generated only by removing salts, and which do not themselves have any associated data will not appear here.')
    parent_molecule = models.ForeignKey(MoleculeDictionary, db_index=True, blank=True, null=True, related_name=u'parent', db_column='parent_molregno', help_text=u'Represents parent compound of molregno in first field (i.e., generated by removing salts). Where molregno and parent_molregno are same, the initial ChEMBL compound did not contain a salt component, or else could not be further processed for various reasons (e.g., inorganic mixture). Compounds which are only generated by removing salts will appear in this field only. Those which, themselves, have any associated data (e.g., activity data) or are launched drugs will also appear in the molregno field.')
    active_molecule = models.ForeignKey(MoleculeDictionary, blank=True, null=True, related_name=u'active', db_column='active_molregno', help_text=u"Where a compound is a pro-drug, this represents the active metabolite of the 'dosed' compound given by parent_molregno. Where parent_molregno and active_molregno are the same, the compound is not currently known to be a pro-drug. ")

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

# ----------------------------------------------------------------------------------------------------------------------


class MoleculeSynonyms(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    molecule = models.ForeignKey(MoleculeDictionary, db_column='molregno', help_text=u'Foreign key to molecule_dictionary')
    synonyms = ChemblCharField(max_length=200, db_index=True, blank=True, null=True, help_text=u'Synonym for the compound')
    syn_type = ChemblCharField(max_length=50, help_text=u'Type of name/synonym (e.g., TRADE_NAME, RESEARCH_CODE, USAN)')
    molsyn_id = ChemblAutoField(primary_key=True, length=9, help_text=u'Primary key.')
    res_stem = models.ForeignKey(ResearchStem, blank=True, null=True, help_text=u'Foreign key to the research_stem table. Where a synonym is a research code, this links to further information about the company associated with that code.')
    molecule_synonym = ChemblCharField(max_length=200, blank=True, null=True, help_text=u'Synonym for the compound')

    class Meta(ChemblCoreAbstractModel.Meta):
        unique_together = (("molecule", "synonyms", "syn_type"),)

# ----------------------------------------------------------------------------------------------------------------------


class RecordSynonyms(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    rec_syn_id = ChemblAutoField(primary_key=True, length=9, help_text=u'Primary key.')
    record = models.ForeignKey(CompoundRecords)
    record_synonym = ChemblCharField(max_length=200, blank=True, null=True, help_text=u'Synonym for the compound record')
    syn_type = ChemblCharField(max_length=50, help_text=u'Type of name/synonym (e.g., TRADE_NAME, RESEARCH_CODE, USAN)')
    res_stem = models.ForeignKey(ResearchStem, blank=True, null=True, help_text=u'Foreign key to the research_stem table. Where a synonym is a research code, this links to further information about the company associated with that code.')
    canonical_synonym = ChemblCharField(max_length=200, blank=True, null=True, help_text=u'Canonical synonym for the compound record')
    removed = ChemblNullBooleanField(default=0, help_text="Indicates whether the synonym has been removed (1) from the database")

    class Meta(ChemblCoreAbstractModel.Meta):
        unique_together = (("record", "record_synonym", "syn_type"),)

# ----------------------------------------------------------------------------------------------------------------------


class Biotherapeutics(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    molecule = models.OneToOneField(MoleculeDictionary, primary_key=True, db_column='molregno', help_text=u'Foreign key to molecule_dictionary')
    description = ChemblCharField(max_length=2000, blank=True, null=True, help_text=u'Description of the biotherapeutic.')
    helm_notation = ChemblCharField(max_length=4000, blank=True, null=True, help_text=u'Sequence notation generated according to the HELM standard (http://www.openhelm.org/home). Currently for peptides only')
    bio_component_sequences = models.ManyToManyField('BioComponentSequences', through="BiotherapeuticComponents", blank=True)

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

# ----------------------------------------------------------------------------------------------------------------------


class CompoundStructuralAlerts(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    cpd_str_alert_id = ChemblPositiveIntegerField(primary_key=True, length=9, help_text=u'Primary key.')
    molecule = models.ForeignKey(MoleculeDictionary, db_column='molregno', help_text=u'Foreign key to the molecule_dictionary. The compound for which the structural alert has been found.')
    alert = models.ForeignKey(StructuralAlerts, help_text=u'Foreign key to the structural_alerts table. The particular alert that has been identified in this compound.')

    class Meta(ChemblCoreAbstractModel.Meta):
        unique_together = ( ("molecule", "alert"),  )

# ----------------------------------------------------------------------------------------------------------------------


class CompoundXref(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    molecule = models.ForeignKey(MoleculeDictionary, db_column='molregno', help_text=u'Foreign key to compounds table')
    xref_src_db = models.ForeignKey(XrefSource, db_column='xref_src_db', help_text=u'Name of the database that this cross reference links to')
    xref_id = ChemblCharField(max_length=330, unique=True, help_text=u'Identifier for the entry in the cross-referenced database')
    xref_name = ChemblCharField(max_length=150, blank=True, null=True, help_text=u'Name for the entry in the cross-referenced database, where applicable')
    cmpd_xref_id = ChemblPositiveIntegerField(primary_key=True, length=9)

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

# ----------------------------------------------------------------------------------------------------------------------


class CompoundImages(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    molecule = models.OneToOneField(MoleculeDictionary, primary_key=True, db_column='molregno')
    png = BlobField(blank=True, null=True)
    png_500 = BlobField(blank=True, null=True)

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

# ----------------------------------------------------------------------------------------------------------------------


class CompoundMols(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    objects = CompoundMolsManager()

    molecule = models.OneToOneField(MoleculeDictionary, primary_key=True, db_column='molregno')
    ctab = BlobField(blank=True, null=True, db_column=CTAB_COLUMN) if CTAB_COLUMN else BlobField(blank=True, null=True)

    class Meta(ChemblCoreAbstractModel.Meta):
        if COMPOUND_MOLS_TABLE:
            db_table = COMPOUND_MOLS_TABLE

# ----------------------------------------------------------------------------------------------------------------------


class CompoundStructures(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    molecule = models.OneToOneField(MoleculeDictionary, primary_key=True, db_column='molregno', help_text=u'Internal Primary Key for the compound structure and foreign key to molecule_dictionary table')
    molfile = ChemblTextField(blank=True, null=True, help_text=u'MDL Connection table representation of compound')
    standard_inchi = ChemblCharField(max_length=4000, db_index=True, unique=True, blank=True, null=True, help_text=u'IUPAC standard InChI for the compound')
    standard_inchi_key = ChemblCharField(max_length=27, db_index=True, help_text=u'IUPAC standard InChI key for the compound')
    canonical_smiles = ChemblCharField(max_length=4000, db_index=True, blank=True, null=True, help_text=u'Canonical smiles, generated using pipeline pilot')
    structure_exclude_flag = ChemblBooleanField(default=False, help_text=u'Indicates whether the structure for this compound should be hidden from users (e.g., organometallic compounds with bad valence etc)')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

# ----------------------------------------------------------------------------------------------------------------------


class BiotherapeuticComponents(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    biocomp_id = ChemblAutoField(primary_key=True, length=9, help_text=u'Primary key.')
    biotherapeutics = models.ForeignKey(Biotherapeutics, db_column='molregno', help_text=u'Foreign key to the biotherapeutics table, indicating which biotherapeutic the component is part of.')
    component = models.ForeignKey(BioComponentSequences, help_text=u'Foreign key to the bio_component_sequences table, indicating which component is part of the biotherapeutic.')

    class Meta(ChemblCoreAbstractModel.Meta):
        unique_together = (("biotherapeutics", "component"),)

# ----------------------------------------------------------------------------------------------------------------------


class RecordDrugProperties(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    AVAILABILITY_TYPE_CHOICES = (
        (-2, '-2'),
        (-1, '-1'),
        (0, '0'),
        (1, '1'),
        (2, '2'),
        )

    CHIRALITY_CHOICES = (
        (-1, '-1'),
        (0, '0'),
        (1, '1'),
        (2, '2'),
        )

    MAX_PHASE_CHOICES = (
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        )

    MOLECULE_TYPE_CHOICES = (
        ('Antibody', 'Antibody'),
        ('Cell', 'Cell'),
        ('Enzyme', 'Enzyme'),
        ('Oligonucleotide', 'Oligonucleotide'),
        ('Oligosaccharide', 'Oligosaccharide'),
        ('Protein', 'Protein'),
        ('Small molecule', 'Small molecule'),
        ('Unclassified', 'Unclassified'),
        ('Unknown', 'Unknown'),
        )

    record = models.OneToOneField(CompoundRecords, primary_key=True)
    max_phase = ChemblPositiveIntegerField(length=1, db_index=True, default=0, choices=MAX_PHASE_CHOICES, help_text=u'Maximum phase of development reached for the compound (4 = approved). Null where max phase has not yet been assigned.')
    molecule_type = ChemblCharField(max_length=30, blank=True, null=True, choices=MOLECULE_TYPE_CHOICES, help_text=u'Type of molecule (Small molecule, Protein, Antibody, Oligosaccharide, Oligonucleotide, Cell, Unknown)')
    first_approval = ChemblPositiveIntegerField(length=4, blank=True, null=True, help_text=u'Earliest known approval year for the molecule') # TODO: should be date!
    oral = ChemblNullableBooleanField(default=False, help_text=u'Indicates whether the drug is known to be administered orally.')
    parenteral = ChemblNullableBooleanField(default=False, help_text=u'Indicates whether the drug is known to be administered parenterally')
    topical = ChemblNullableBooleanField(default=False, help_text=u'Indicates whether the drug is known to be administered topically.')
    black_box_warning = ChemblNullableBooleanField(default=0, help_text=u'Indicates that the drug has a black box warning')
    first_in_class = ChemblNullBooleanField(default=(-1), help_text=u'Indicates whether this is known to be the first compound of its class (e.g., acting on a particular target).')
    chirality = ChemblIntegerField(length=1, default=(-1), choices=CHIRALITY_CHOICES, help_text=u'Shows whether a drug is dosed as a racemic mixture (0), single stereoisomer (1) or is an achiral molecule (2)')
    prodrug = ChemblNullableBooleanField(default=False, help_text=u'Indicates that the molecule is a pro-drug (see molecule hierarchy for active component, where known)')
    therapeutic_flag = ChemblNullableBooleanField(db_index=True, default=False, help_text=u'Indicates that a drug has a therapeutic application (as opposed to e.g., an imaging agent, additive etc).')
    natural_product = ChemblNullBooleanField(default=(-1), help_text=u'Indicates whether the compound is natural product-derived (currently curated only for drugs)')
    inorganic_flag = ChemblNullableBooleanField(default=0, help_text=u'Indicates whether the molecule is inorganic (i.e., containing only metal atoms and <2 carbon atoms)')
    applicants = ChemblCharField(max_length=1000, blank=True, null=True)
    usan_stem = ChemblCharField(max_length=50, blank=True, null=True, help_text=u'Where the compound has been assigned a USAN name, this indicates the stem, as described in the USAN_STEM table.')
    usan_year = ChemblPositiveIntegerField(length=4, blank=True, null=True, help_text=u'The year in which the application for a USAN/INN name was made')
    availability_type = ChemblIntegerField(length=1, blank=True, null=True, choices=AVAILABILITY_TYPE_CHOICES, help_text=u'The availability type for the drug (0 = discontinued, 1 = prescription only, 2 = over the counter)')
    usan_substem = ChemblCharField(max_length=50, blank=True, null=True, help_text=u'Where the compound has been assigned a USAN name, this indicates the substem')
    indication_class = ChemblCharField(max_length=1000, blank=True, null=True, help_text=u'Indication class(es) assigned to a drug in the USP dictionary')
    usan_stem_definition = ChemblCharField(max_length=1000, blank=True, null=True, help_text=u'Definition of the USAN stem')
    polymer_flag = ChemblNullableBooleanField(help_text=u'Indicates whether a molecule is a small molecule polymer (e.g., polistyrex)')
    withdrawn_flag = ChemblPositiveIntegerField(length=1, blank=True, null=True)
    withdrawn_year = ChemblPositiveIntegerField(length=4, blank=True, null=True)
    withdrawn_country = ChemblCharField(max_length=1000, blank=True, null=True)
    withdrawn_reason = ChemblCharField(max_length=1000, blank=True, null=True)
    withdrawn_class = ChemblCharField(max_length=1000, blank=True, null=True)

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

# ----------------------------------------------------------------------------------------------------------------------

