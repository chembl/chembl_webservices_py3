from chembl_webservices.tests import BaseWebServiceTestCase


class BindingSiteTestCase(BaseWebServiceTestCase):

    resource = 'binding_site'
    id_property = 'site_id'
    resource_expected_count = 9522
    sorting_test_props = ['site_name']
    mandatory_properties = [
        'site_name',
        'site_components'
    ]

class BiotherapeuticTestCase(BaseWebServiceTestCase):

    resource = 'biotherapeutic'
    id_property = 'molecule_chembl_id'
    resource_expected_count = 22920
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
    resource_expected_count = 655
    sorting_test_props = ['pref_name']
    mandatory_properties = [
        'tissue_chembl_id',
        'pref_name',
        'uberon_id',
    ]


class TargetRelationsTestCase(BaseWebServiceTestCase):

    resource = 'target_relation'
    id_property = 'target_chembl_id'
    resource_expected_count = 7670
    sorting_test_props = []
    mandatory_properties = [
        'target_chembl_id',
        'relationship',
        'related_target_chembl_id',
    ]


class DocumentTermTestCase(BaseWebServiceTestCase):

    resource = 'document_term'
    # TODO: check if this is a required index
    id_property = None
    resource_expected_count = 361150
    sorting_test_props = ['term_text']
    mandatory_properties = [
        'document_chembl_id',
        'score',
        'term_text',
    ]


class CellLineTestCase(BaseWebServiceTestCase):

    resource = 'cell_line'
    id_property = 'cell_chembl_id'
    resource_expected_count = 1670
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
    resource_expected_count = 29457
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
    resource_expected_count = 561129
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
    resource_expected_count = 5655561
    sorting_test_props = ['alert__alertset__priority']
    mandatory_properties = [
      'alert',
      'cpd_str_alert_id',
      'molecule_chembl_id',
    ]


class OrganismTestCase(BaseWebServiceTestCase):

    resource = 'organism'
    id_property = 'oc_id'
    resource_expected_count = 3847
    sorting_test_props = ['l1', 'l2', 'l3']
    mandatory_properties = [
      'l1',
      'l2',
      'l3',
      'l4_synonyms',
      'oc_id',
      'tax_id',
    ]

class MoleculeFormTestCase(BaseWebServiceTestCase):

    resource = 'molecule_form'
    id_property = 'molecule_chembl_id'
    resource_expected_count = 1798168
    mandatory_properties = [
      'is_parent',
      'molecule_chembl_id',
      'parent_chembl_id',
    ]
