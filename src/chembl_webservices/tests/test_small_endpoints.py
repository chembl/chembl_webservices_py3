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


class DocumentTermRelationsTestCase(BaseWebServiceTestCase):

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
