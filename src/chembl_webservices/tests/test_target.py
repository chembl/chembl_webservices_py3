from chembl_webservices.tests import BaseWebServiceTestCase


class TargetTestCase(BaseWebServiceTestCase):

    resource = 'target'
    id_property = 'target_chembl_id'
    resource_expected_count = 12482
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
