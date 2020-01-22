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
    resource_expected_count = 1865157
    mandatory_properties = [
      'is_parent',
      'molecule_chembl_id',
      'parent_chembl_id',
    ]


#     def test_source_resource(self):
#         source = new_client.source
#         count = len(source.all())
#         self.assertTrue(count)
#         self.assertTrue(source.filter(src_short_name="ATLAS").exists())
#         self.assertEqual( [src['src_id'] for src in source.all().order_by('src_id')[0:5]], [1,2,3,4,5])
#         random_index = 5#randint(0, count - 1)
#         random_elem = source.all()[random_index]
#         self.assertIsNotNone(random_elem, "Can't get {0} element from the list".format(random_index))
#         self.assertIn('src_description', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('src_id', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('src_short_name', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         source.set_format('xml')
#         parseString(source.filter(src_short_name="DRUGS")[0])



#
#     def test_target_prediction_resource(self):
#         target_prediction = new_client.target_prediction
#         count = len(target_prediction.all())
#         self.assertTrue(count)
#         self.assertTrue(set(["P15823", "P43140", "P23944", "P35368", "P18130"]).issubset(set(tar['target_accession'] for tar in target_prediction.filter(molecule_chembl_id='CHEMBL2'))))
#         self.assertTrue(all(float(tar['probability']) >= 0.9 for tar in target_prediction.filter(molecule_chembl_id='CHEMBL3').filter(probability__gte=0.9)))
#         self.assertEqual(len(target_prediction.filter(molecule_chembl_id='CHEMBL4').filter(probability__lte=0.5)), 95)
#         self.assertEqual(target_prediction.filter(molecule_chembl_id='CHEMBL5').order_by('probability')[0]['target_chembl_id'], "CHEMBL5080")
#         random_index = 7878
#         random_elem = target_prediction.all()[random_index]
#         self.assertIsNotNone(random_elem, "Can't get {0} element from the list".format(random_index))
#         self.assertIn('in_training', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('molecule_chembl_id', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('pred_id', random_elem,
#                       'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('probability', random_elem,
#                       'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('target_accession', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('target_chembl_id', random_elem,
#                       'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('value', random_elem,
#                       'One of required fields not found in resource {0}'.format(random_elem))
#         target_prediction.set_format('xml')
#         parseString(target_prediction.filter(molecule_chembl_id='CHEMBL6').filter(value=1)[0])


#
#
#     def test_target_component_resource(self):
#         target_component = new_client.target_component
#         count = len(target_component.all())
#         self.assertTrue(count)
#         self.assertTrue('sequence' in target_component.get(1295))
#         self.assertEqual([targcomp['component_id'] for targcomp in target_component.all().order_by('component_id')[0:5]],
#             [1, 2, 3, 4, 5])
#         has_synonyms = target_component.get(375)
#         self.assertIn('target_component_synonyms', has_synonyms, 'One of required fields not found in resource {0}'.format(has_synonyms))
#         synonym = has_synonyms['target_component_synonyms'][0]
#         self.assertIn('component_synonym', synonym, 'One of required fields not found in resource {0}'.format(synonym))
#         self.assertIn('syn_type', synonym, 'One of required fields not found in resource {0}'.format(synonym))
#         target_component.set_format('xml')
#         random_index = 5432  # randint(0, count - 1)
#         random_elem = target_component.all()[random_index]
#         self.assertIsNotNone(random_elem, "Can't get {0} element from the list".format(random_index))
#         self.assertIn('accession', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('sequence', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('component_id', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('component_type', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('description', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('go_slims', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('organism', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('tax_id', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         parseString(target_component.all()[0])



#
#     def test_chembl_id_lookup_resource(self):
#         chembl_id_lookup = new_client.chembl_id_lookup
#         count = len(chembl_id_lookup.all())
#         self.assertTrue(count)
#         self.assertTrue(chembl_id_lookup.filter(entity_type="TARGET").exists())
#         random_index = 5678  # randint(0, count - 1)
#         random_elem = chembl_id_lookup.all()[random_index]
#         self.assertNotEqual(chembl_id_lookup.all().order_by('chembl_id')[0]['chembl_id'], chembl_id_lookup.all().order_by('-chembl_id')[0]['chembl_id'])
#         self.assertNotEqual(chembl_id_lookup.all().order_by('entity_type')[0]['chembl_id'], chembl_id_lookup.all().order_by('-entity_type')[0]['chembl_id'])
#         self.assertNotEqual(chembl_id_lookup.all().order_by('status')[0]['chembl_id'], chembl_id_lookup.all().order_by('-status')[0]['chembl_id'])
#         self.assertIsNotNone(random_elem, "Can't get {0} element from the list".format(random_index))
#         self.assertIn('chembl_id', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('entity_type', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('status', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('resource_url', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         chembl_id_lookup.set_format('xml')
#         parseString(chembl_id_lookup.filter(entity_type="COMPOUND").filter(status="ACTIVE")[0])
#