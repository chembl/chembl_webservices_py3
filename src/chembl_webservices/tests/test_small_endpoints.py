from chembl_webservices.tests import BaseWebServiceTestCase


class BindingSiteTestCase(BaseWebServiceTestCase):

    resource = 'binding_site'
    id_property = 'site_id'
    resource_expected_count = 11089
    sorting_test_props = ['site_name']
    mandatory_properties = [
        'site_name',
        'site_components'
    ]

class BiotherapeuticTestCase(BaseWebServiceTestCase):

    resource = 'biotherapeutic'
    id_property = 'molecule_chembl_id'
    resource_expected_count = 22925
    sorting_test_props = ['helm_notation']
    mandatory_properties = [
        'molecule_chembl_id',
        'helm_notation'
    ]

class GoSlimTestCase(BaseWebServiceTestCase):

    resource = 'go_slim'
    id_property = 'go_id'
    resource_expected_count = 309
    sorting_test_props = ['pref_name']
    mandatory_properties = [
        'aspect',
        'class_level',
        'go_id',
        'parent_go_id',
        'path',
        'pref_name',
    ]


class MetabolismTestCase(BaseWebServiceTestCase):

    resource = 'metabolism'
    id_property = 'met_id'
    resource_expected_count = 1245
    sorting_test_props = ['metabolite_name']
    mandatory_properties = [
        'drug_chembl_id',
        'enzyme_name',
        'substrate_name',
        'metabolite_name',
        'met_comment',
        'met_conversion',
        'met_id',
        'metabolism_refs',
        'metabolite_chembl_id',
        'organism',
        'pathway_id',
        'pathway_key',
        'substrate_chembl_id',
        'target_chembl_id',
        'tax_id',
    ]


class TissueTestCase(BaseWebServiceTestCase):

    resource = 'tissue'
    id_property = 'tissue_chembl_id'
    resource_expected_count = 707
    sorting_test_props = ['pref_name']
    mandatory_properties = [
        'tissue_chembl_id',
        'pref_name',
        'uberon_id',
    ]


class TargetRelationsTestCase(BaseWebServiceTestCase):

    resource = 'target_relation'
    id_property = 'target_chembl_id'
    resource_expected_count = 9578
    sorting_test_props = []
    mandatory_properties = [
        'target_chembl_id',
        'relationship',
        'related_target_chembl_id',
    ]


class CellLineTestCase(BaseWebServiceTestCase):

    resource = 'cell_line'
    id_property = 'cell_chembl_id'
    resource_expected_count = 1830
    sorting_test_props = ['cell_source_tissue', 'cell_source_organism']
    mandatory_properties = [
      'cell_chembl_id',
      'cell_description',
      'cell_id',
      'cell_name',
      'cell_source_organism',
      'cell_source_tax_id',
      'cell_source_tissue',
      'cellosaurus_id',
    ]


class DrugIndicationTestCase(BaseWebServiceTestCase):

    resource = 'drug_indication'
    id_property = 'drugind_id'
    resource_expected_count = 55385
    sorting_test_props = ['mesh_heading', 'efo_term']
    mandatory_properties = [
      'drugind_id',
      'efo_id',
      'efo_term',
      'indication_refs',
      'max_phase_for_ind',
      'mesh_heading',
      'mesh_id',
    ]


class DocumentSimilarityTestCase(BaseWebServiceTestCase):

    resource = 'document_similarity'
    id_property = 'document_1_chembl_id'
    resource_expected_count = 756389
    sorting_test_props = ['tid_tani', 'mol_tani']
    mandatory_properties = [
      'document_1_chembl_id',
      'document_2_chembl_id',
      'mol_tani',
      'tid_tani',
    ]


class CompoundStructuralAlertTestCase(BaseWebServiceTestCase):

    resource = 'compound_structural_alert'
    id_property = 'cpd_str_alert_id'
    resource_expected_count = 3690638
    sorting_test_props = ['alert__alertset__priority']
    mandatory_properties = [
      'alert',
      'cpd_str_alert_id',
      'molecule_chembl_id',
    ]


class OrganismTestCase(BaseWebServiceTestCase):

    resource = 'organism'
    id_property = 'oc_id'
    resource_expected_count = 3959
    sorting_test_props = ['l1', 'l2', 'l3']
    mandatory_properties = [
      'l1',
      'l2',
      'l3',
      'oc_id',
      'tax_id',
    ]

class MoleculeFormTestCase(BaseWebServiceTestCase):

    resource = 'molecule_form'
    id_property = 'molecule_chembl_id'
    resource_expected_count = 1865157
    mandatory_properties = [
      'is_parent',
      'molecule_chembl_id',
      'parent_chembl_id',
    ]

class SourceTestCase(BaseWebServiceTestCase):

    resource = 'source'
    id_property = 'src_id'
    resource_expected_count = 47
    mandatory_properties = [
      'src_description',
      'src_id',
      'src_short_name',
    ]

class TargetComponentTestCase(BaseWebServiceTestCase):

    resource = 'target_component'
    id_property = 'component_id'
    resource_expected_count = 9756
    mandatory_properties = [
      'accession',
      'component_id',
      'component_type',
      'description',
      'go_slims.go_id',
      'organism',
      'protein_classifications.protein_classification_id',
      'sequence',
      'target_component_synonyms.component_synonym',
      'target_component_synonyms.syn_type',
      'target_component_xrefs.xref_id',
      'target_component_xrefs.xref_name',
      'target_component_xrefs.xref_src_db',
      'targets.target_chembl_id',
      'tax_id',
    ]

class ChemblIdLookUpTestCase(BaseWebServiceTestCase):

    resource = 'chembl_id_lookup'
    id_property = 'chembl_id'
    resource_expected_count = 3687036
    mandatory_properties = [
      'chembl_id',
      'entity_type',
      'resource_url',
      'status',
    ]
