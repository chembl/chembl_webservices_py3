__author__ = 'mnowotka'

import datetime
from django.db import models
from chembl_core_model.models import *
from chembl_core_db.db.models.abstractModel import ChemblCoreAbstractModel
from chembl_core_db.db.models.abstractModel import ChemblModelMetaClass
from django.utils import six

# ----------------------------------------------------------------------------------------------------------------------


class ActionType(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    action_type = ChemblCharField(primary_key=True, max_length=50, help_text=u'Primary key. Type of action of the drug e.g., agonist, antagonist')
    description = ChemblCharField(max_length=200, help_text=u'Description of how the action type is used')
    parent_type = ChemblCharField(max_length=50, blank=True, null=True, help_text=u'Higher-level grouping of action types e.g., positive vs negative action')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

# ----------------------------------------------------------------------------------------------------------------------


class DrugMechanism(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    CURATION_STATUS_CHOICES = (
        ('COMPLETE', 'COMPLETE'),
        ('PARTIAL', 'PARTIAL'),
        )

    mec_id = ChemblAutoField(primary_key=True, length=9, help_text=u'Primary key for each drug mechanism of action')
    record = models.ForeignKey(CompoundRecords, help_text=u'Record_id for the drug (foreign key to compound_records table)')
    molecule = models.ForeignKey(MoleculeDictionary, blank=True, null=True, db_column='molregno', help_text=u'Molregno for the drug (foreign key to molecule_dictionary table)')
    mechanism_of_action = ChemblCharField(max_length=250, blank=True, null=True, help_text=u"Description of the mechanism of action e.g., 'Phosphodiesterase 5 inhibitor'")
    target = models.ForeignKey(TargetDictionary, blank=True, null=True, db_column='tid', help_text=u'Target associated with this mechanism of action (foreign key to target_dictionary table)')
    site = models.ForeignKey(BindingSites, blank=True, null=True, help_text=u'Binding site for the drug within the target (where known) - foreign key to binding_sites table')
    action_type = models.ForeignKey(ActionType, blank=True, null=True, db_column='action_type', help_text=u'Type of action of the drug on the target e.g., agonist/antagonist etc (foreign key to action_type table)')
    direct_interaction = ChemblNullableBooleanField(help_text=u'Flag to show whether the molecule is believed to interact directly with the target (1 = yes, 0 = no)')
    molecular_mechanism = ChemblNullableBooleanField(help_text=u'Flag to show whether the mechanism of action describes the molecular target of the drug, rather than a higher-level physiological mechanism e.g., vasodilator (1 = yes, 0 = no)')
    disease_efficacy = ChemblNullableBooleanField(help_text=u'Flag to show whether the target assigned is believed to play a role in the efficacy of the drug in the indication(s) for which it is approved (1 = yes, 0 = no)')
    mechanism_comment = ChemblCharField(max_length=500, blank=True, null=True, help_text=u'Additional comments regarding the mechanism of action')
    selectivity_comment = ChemblCharField(max_length=100, blank=True, null=True, help_text=u'Additional comments regarding the selectivity of the drug')
    binding_site_comment = ChemblCharField(max_length=100, blank=True, null=True, help_text=u'Additional comments regarding the binding site of the drug')
    curated_by = ChemblCharField(max_length=20)
    date_added = ChemblDateField(default=datetime.date.today)
    date_removed = ChemblDateField(blank=True, null=True)
    downgraded = ChemblBooleanField(default=False)
    downgrade_reason = ChemblCharField(max_length=200, blank=True, null=True)
    curator_comment = ChemblCharField(max_length=500, blank=True, null=True)
    curation_status = ChemblCharField(max_length=10, default=u'PARTIAL', choices=CURATION_STATUS_CHOICES, help_text=u'Show whether the curation for this row is complete')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

# ----------------------------------------------------------------------------------------------------------------------


class DrugIndication(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    MAX_PHASE_FOR_IND_CHOICES = (
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        )

    drugind_id = ChemblPositiveIntegerField(primary_key=True, length=9, help_text=u'Primary key')
    record = models.ForeignKey(CompoundRecords, help_text=u'Foreign key to compound_records table. Links to the drug record to which this indication applies')
    molecule = models.ForeignKey(MoleculeDictionary, blank=True, null=True, db_column='molregno', help_text=u'Molregno corresponding to the record_id in the compound_records table')
    max_phase_for_ind = ChemblPositiveIntegerField(length=1, blank=True, null=True, choices=MAX_PHASE_FOR_IND_CHOICES, help_text=u'The maximum phase of development that the drug is known to have reached for this particular indication')
    mesh_id = ChemblCharField(max_length=7, help_text=u'Medical Subject Headings (MeSH) disease identifier corresponding to the indication')
    mesh_heading = ChemblCharField(max_length=200, help_text=u'Medical Subject Heading term for the MeSH disease ID')
    efo_id = ChemblCharField(max_length=20, blank=True, null=True, help_text=u'Experimental Factor Ontology (EFO) disease identifier corresponding to the indication')
    efo_term = ChemblCharField(max_length=200, blank=True, null=True, help_text=u'Experimental Factor Ontology term for the EFO ID')

    class Meta(ChemblCoreAbstractModel.Meta):
        unique_together = ( ("record", "mesh_id", "efo_id"),  )

# ----------------------------------------------------------------------------------------------------------------------


class LigandEff(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    activity = models.OneToOneField(Activities, primary_key=True, help_text=u'Link key to activities table')
    bei = ChemblPositiveDecimalField(blank=True, null=True, max_digits=9, decimal_places=2, help_text=u'Binding Efficiency Index = p(XC50) *1000/MW_freebase')
    sei = ChemblPositiveDecimalField(blank=True, null=True, max_digits=9, decimal_places=2, help_text=u'Surface Efficiency Index = p(XC50)*100/PSA')
    le = ChemblPositiveDecimalField(blank=True, null=True, max_digits=9, decimal_places=2, help_text=u'Ligand Efficiency = deltaG/heavy_atoms  [from the Hopkins DDT paper 2004]')
    lle = models.DecimalField(blank=True, null=True, max_digits=9, decimal_places=2, help_text=u'Lipophilic Ligand Efficiency = -logKi-ALogP. [from Leeson NRDD 2007]')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

# ----------------------------------------------------------------------------------------------------------------------


class PredictedBindingDomains(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    CONFIDENCE_CHOICES = (
        ('high', 'high'),
        ('medium', 'medium'),
        ('low', 'low'),
        )

    PREDICTION_METHOD_CHOICES = (
        ('Manual', 'Manual'),
        ('Multi domain', 'Multi domain'),
        ('Single domain', 'Single domain'),
        )

    predbind_id = ChemblAutoField(primary_key=True, length=9, help_text=u'Primary key.')
    activity = models.ForeignKey(Activities, blank=True, null=True, help_text=u'Foreign key to the activities table, indicating the compound/assay(+target) combination for which this prediction is made.')
    site = models.ForeignKey(BindingSites, blank=True, null=True, help_text=u'Foreign key to the binding_sites table, indicating the binding site (domain) that the compound is predicted to bind to.')
    prediction_method = ChemblCharField(max_length=50, blank=True, null=True, choices=PREDICTION_METHOD_CHOICES, help_text=u"The method used to assign the binding domain (e.g., 'Single domain' where the protein has only 1 domain, 'Multi domain' where the protein has multiple domains, but only 1 is known to bind small molecules in other proteins).")
    confidence = ChemblCharField(max_length=10, blank=True, null=True, choices=CONFIDENCE_CHOICES, help_text=u'The level of confidence assigned to the prediction (high where the protein has only 1 domain, medium where the compound has multiple domains, but only 1 known small molecule-binding domain).')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass

# ----------------------------------------------------------------------------------------------------------------------


class MechanismRefs(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    REF_TYPE_CHOICES = (
        ('ClinicalTrials', 'ClinicalTrials'),
        ('DOI', 'DOI'),
        ('DailyMed', 'DailyMed'),
        ('Expert', 'Expert'),
        ('FDA', 'FDA'),
        ('ISBN', 'ISBN'),
        ('IUPHAR', 'IUPHAR'),
        ('InterPro', 'InterPro'),
        ('KEGG', 'KEGG'),
        ('Other', 'Other'),
        ('PMC', 'PMC'),
        ('Patent', 'Patent'),
        ('PubChem', 'PubChem'),
        ('PubMed', 'PubMed'),
        ('UniProt', 'UniProt'),
        ('Wikipedia', 'Wikipedia'),
        )

    mecref_id = ChemblAutoField(primary_key=True, length=9, help_text=u'Primary key')
    mechanism = models.ForeignKey(DrugMechanism, db_column='mec_id', help_text=u'Foreign key to drug_mechanism table - indicating the mechanism to which the references refer')
    ref_type = ChemblCharField(max_length=50, choices=REF_TYPE_CHOICES, help_text=u"Type/source of reference (e.g., 'PubMed','DailyMed')")
    ref_id = ChemblCharField(max_length=200, blank=True, null=True, help_text=u'Identifier for the reference in the source (e.g., PubMed ID or DailyMed setid)')
    ref_url = ChemblCharField(max_length=400, blank=True, null=True, help_text=u'Full URL linking to the reference')
    downgraded = ChemblNullableBooleanField()
    downgrade_reason = ChemblCharField(max_length=4000, blank=True, null=True)

    class Meta(ChemblCoreAbstractModel.Meta):
        unique_together = (("mechanism", "ref_type", "ref_id"),)

# ----------------------------------------------------------------------------------------------------------------------


class IndicationRefs(six.with_metaclass(ChemblModelMetaClass, ChemblCoreAbstractModel)):

    REF_TYPE_CHOICES = (
        ('ATC', 'ATC'),
        ('ClinicalTrials', 'ClinicalTrials'),
        ('DailyMed', 'DailyMed'),
        ('FDA', 'FDA'),
        )

    indref_id = ChemblPositiveIntegerField(primary_key=True, length=9, help_text=u'Primary key')
    drug_indication = models.ForeignKey(DrugIndication, db_column='drugind_id', help_text=u'Foreign key to the DRUG_INDICATION table, indicating the drug-indication link that this reference applies to')
    ref_type = ChemblCharField(max_length=50, choices=REF_TYPE_CHOICES, help_text=u'Type/source of reference')
    ref_id = ChemblCharField(max_length=2000, help_text=u'Identifier for the reference in the source')
    ref_url = ChemblCharField(max_length=4000, help_text=u'Full URL linking to the reference')

    class Meta(ChemblCoreAbstractModel.Meta):
        pass # unique_together = (("drug_indication", "ref_type", "ref_id"),)

# ----------------------------------------------------------------------------------------------------------------------


