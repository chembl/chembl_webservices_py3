from chembl_webservices.tests import BaseWebServiceTestCase


class AssayTestCase(BaseWebServiceTestCase):

    resource = 'assay'
    id_property = 'assay_chembl_id'
    resource_expected_count = 1221311
    sorting_test_props = ['assay_organism', 'assay_category', 'assay_strain']
    mandatory_properties = [
        'assay_category',
        'assay_cell_type',
        'assay_chembl_id',
        'assay_organism',
        'assay_strain',
        'assay_subcellular_fraction',
        'assay_tax_id',
        'assay_test_type',
        'assay_tissue',
        'assay_type',
        'assay_type_description',
        'bao_format',
        'bao_label',
        'cell_chembl_id',
        'confidence_description',
        'confidence_score',
        'description',
        'document_chembl_id',
        'relationship_description',
        'relationship_type',
        'src_assay_id',
        'src_id',
        'target_chembl_id',
    ]

    def test_assay_by_id(self):
        self.assertEqual(self.get_current_resource_by_id('CHEMBL1217643')['assay_organism'], 'Homo sapiens')
        self.assertEqual(len(self.get_current_resource_list_by_ids(['CHEMBL1217643', 'CHEMBL1217644'])), 2)

    def test_bioactivities(self):
        self.assertEqual(
            self.get_resource_list('activity', {'assay_chembl_id__exact': 'CHEMBL1217643'})
            ['page_meta']['total_count'], 1
        )

    def test_filtered_lists(self):
        assay_list_req = self.get_current_resource_list({
            'assay_oragism': 'Sus scrofa',
            'assay_type': 'B',
        })
        self.assertGreaterEqual(assay_list_req['page_meta']['total_count'], 200)

        assay_list_req = self.get_current_resource_list({
            'target_chembl_id': 'CHEMBL333',
        })
        self.assertGreaterEqual(assay_list_req['page_meta']['total_count'], 10)

        assay_list_req = self.get_current_resource_list({
            'target_chembl_id': 'CHEMBL3938',
            'assay_type__iregex': '(B|F)',
        })
        self.assertGreaterEqual(assay_list_req['page_meta']['total_count'], 50)
        self.assertLessEqual(assay_list_req['page_meta']['total_count'], 100)
        for act_i in assay_list_req[self.get_current_plural()]:
            self.assertEqual(act_i['target_chembl_id'], 'CHEMBL3938')
            self.assertIn(act_i['assay_type'], {'B', 'F'})


    def test_filtered_lists_icontains(self):
        assay_list_req_1 = self.get_current_resource_list({
            'description__icontains': 'insulin',
            'assay_type': 'B',
        })
        assay_list_req_2 = self.get_current_resource_list([
            ('description__icontains', 'insulin'),
            ('description__icontains', 'inhibitor'),
            ('assay_type', 'B'),
        ])
        self.assertGreaterEqual(assay_list_req_1['page_meta']['total_count'], 100)
        self.assertGreaterEqual(assay_list_req_1['page_meta']['total_count'], assay_list_req_2['page_meta']['total_count'])
        self.assertGreaterEqual(assay_list_req_2['page_meta']['total_count'], 1)

    def test_bao_format(self):
        assay_list_req = self.get_current_resource_list_by_ids(['CHEMBL615111', 'CHEMBL615112', 'CHEMBL615113'])
        self.assertEqual(len(assay_list_req), 3)
        for assay_i in assay_list_req:
            self.assertEqual(assay_i['bao_format'], 'BAO_0000019')
