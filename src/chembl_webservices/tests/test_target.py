from chembl_webservices.tests import BaseWebServiceTestCase


class TargetTestCase(BaseWebServiceTestCase):

    resource = 'target'
    id_property = 'target_chembl_id'
    resource_expected_count = 13382
    sorting_test_props = ['pref_name']

    def test_target_by_id(self):
        self.assertEqual(self.get_resource_by_id('target', 'CHEMBL2476')['target_type'], 'SINGLE PROTEIN')
        self.assertGreaterEqual(
            self.get_resource_list('target', {'target_components__accession__exact': 'Q13936'})
            ['page_meta']['total_count'], 5
        )
        self.assertEqual(len(self.get_resource_list_by_ids('target', ['CHEMBL240', 'CHEMBL1927'])), 2)

    def test_targets(self):
        self.assertGreaterEqual(
            self.get_resource_list('target')
            ['page_meta']['total_count'], 10000
        )

    def test_bioactivities(self):
        self.assertGreaterEqual(
            self.get_resource_list('activity', {'target_chembl_id__exact': 'CHEMBL240'})
            ['page_meta']['total_count'], 10000
        )

    def test_nested_property_filtering(self):
        # target_synonym is resolved to a nested property inside the target components
        self.assertGreaterEqual(
            self.get_current_resource_list({'target_synonym__iexact': 'CDKN5'})
            ['page_meta']['total_count'], 6
        )


#
#
#     def test_target_resource(self):
#         target = new_client.target
#         count = len(target.all())
#         self.assertTrue(count)
#         self.assertTrue(target.filter(organism="Homo sapiens").filter(target_type="SINGLE PROTEIN").exists())
#         self.assertTrue(target.filter(target_components__accession="Q13936").exists())
#         self.assertEqual(len(target.filter(target_components__accession="Q13936")), 3)
#         self.assertNotEqual(target.all().order_by('species_group_flag')[0]['target_chembl_id'],target.all().order_by('-species_group_flag')[0]['target_chembl_id'])
#         self.assertNotEqual(target.all().order_by('target_chembl_id')[0]['target_chembl_id'],target.all().order_by('-target_chembl_id')[0]['target_chembl_id'])
#         self.assertEqual( [t['pref_name'] for t in target.get(['CHEMBL1927', 'CHEMBL1929', 'CHEMBL1930'])],
#         ['Thioredoxin reductase 1',
#          'Xanthine dehydrogenase',
#          'Vitamin k epoxide reductase complex subunit 1 isoform 1'])
#         random_index = 8888  # randint(0, count - 1)
#         random_elem = target.all()[random_index]
#         self.assertIsNotNone(random_elem, "Can't get {0} element from the list".format(random_index))
#         self.assertIn('organism', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('tax_id', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('pref_name', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('species_group_flag', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('target_chembl_id', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('target_type', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('target_components', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         has_components = target.get('CHEMBL247')
#         target_component = has_components['target_components'][0]
#         self.assertIn('accession', target_component, 'One of required fields not found in resource {0}'.format(target_component))
#         self.assertIn('component_id', target_component, 'One of required fields not found in resource {0}'.format(target_component))
#         self.assertIn('component_type', target_component, 'One of required fields not found in resource {0}'.format(target_component))
#         self.assertIn('relationship', target_component, 'One of required fields not found in resource {0}'.format(target_component))
#         self.assertIn('component_description', target_component, 'One of required fields not found in resource {0}'.format(target_component))
#         self.assertIn('target_component_synonyms', target_component, 'One of required fields not found in resource {0}'.format(target_component))
#         synonym = target_component['target_component_synonyms'][0]
#         self.assertIn('component_synonym', synonym, 'One of required fields not found in  resource {0}'.format(synonym))
#         self.assertIn('syn_type', synonym, 'One of required fields not found in  resource {0}'.format(synonym))
#         gene_name = 'GABRB2'
#         targets_for_gene = target.filter(target_components__target_component_synonyms__component_synonym__icontains=gene_name)
#         self.assertEqual(len(targets_for_gene), 14)
#         shortcut = target.filter(target_synonym__icontains=gene_name)
#         self.assertListEqual([x for x in targets_for_gene], [x for x in shortcut])
#         only_components = target.filter(target_synonym__icontains=gene_name).only(['target_components'])
#         first = only_components[0]
#         self.assertEqual(list(first.keys()), ['target_components'])
#
#         gene_name = 'flap'
#         targets_for_gene = target.filter(target_components__target_component_synonyms__component_synonym__icontains=gene_name)
#         self.assertEqual(len(targets_for_gene), 5)
#         shortcut = target.filter(target_synonym__icontains=gene_name)
#         self.assertListEqual([x for x in targets_for_gene], [x for x in shortcut])
#         with_x_refs = target.get('CHEMBL2074')
#         self.assertIn('cross_references', with_x_refs, 'No cross references')
#         x_refs = with_x_refs['cross_references']
#         self.assertTrue(len(x_refs))
#         single_ref = x_refs[0]
#         self.assertIn('xref_id', single_ref, 'No xref_id in cross reference')
#         self.assertIn('xref_name', single_ref, 'No xref_name in cross reference')
#         self.assertIn('xref_src', single_ref, 'No xref_src in cross reference')
#         target.set_format('xml')
#         parseString(target.all()[0])
#         with self.assertRaisesRegex(HttpBadRequest, 'Related Field got invalid lookup: contains'):
#             len(target.search('trypsin').filter(target_type__contains='Single').filter(organism_contains='Sus scrofa'))
#
