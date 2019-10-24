from chembl_webservices.tests import BaseWebServiceTestCase


class ActivityTestCase(BaseWebServiceTestCase):


    resource = 'activity'
    id_property = 'activity_id'
    resource_expected_count = 15504603
    mandatory_properties = [
        'activity_comment',
        'activity_id',
        'assay_chembl_id',
        'assay_description',
        'assay_type',
        'bao_format',
        'bao_label',
        'bao_endpoint',
        'canonical_smiles',
        'data_validity_comment',
        'document_chembl_id',
        'document_journal',
        'document_year',
        'molecule_chembl_id',
        'pchembl_value',
        'potential_duplicate',
        'qudt_units',
        'record_id',
        'standard_flag',
        'standard_relation',
        'standard_type',
        'standard_units',
        'standard_value',
        'src_id',
        'target_pref_name',
        'target_tax_id',
        'target_organism',
        'parent_molecule_chembl_id',
        'uo_units',
        'ligand_efficiency'
    ]
    sorting_test_props = ['assay_type', 'standard_type']



    def test_activity_by_id(self):
        act = self.get_current_resource_by_id('66369')
        self.assertEqual(act['canonical_smiles'], 'NC(=N)c1cccc(C[C@H](NS(=O)(=O)c2ccc3ccccc3c2)C(=O)N4CCOCC4)c1')
        self.assertGreaterEqual(
            self.get_resource_list('target', {'target_components__accession__exact': 'Q13936'})
            ['page_meta']['total_count'], 5
        )

    def assay_type_filter_test_helper(self, assay_type, should_count):
        act_list_req = self.get_current_resource_list({
            'assay_type': assay_type,
        })
        self.assertEqual(act_list_req['page_meta']['total_count'], should_count)
        for act_i in act_list_req[self.get_current_plural()]:
            self.assertEqual(act_i['assay_type'], assay_type)

    def test_assay_type_A(self):
        self.assay_type_filter_test_helper('A', 775430)

    def test_assay_type_B(self):
        self.assay_type_filter_test_helper('B', 3198751)

    def test_assay_type_F(self):
        self.assay_type_filter_test_helper('F', 10774242)

    def test_assay_type_U(self):
        self.assay_type_filter_test_helper('U', 15311)

    def test_assay_type_P(self):
        self.assay_type_filter_test_helper('P', 127430)

    def test_filtered_lists(self):
        act_list_req = self.get_current_resource_list({
            'standard_type': 'Log Ki',
            'standard_value__gte': 5,
        })
        self.assertGreaterEqual(act_list_req['page_meta']['total_count'], 200)

        act_list_req = self.get_current_resource_list({
            'target_chembl_id': 'CHEMBL333',
        })
        self.assertGreaterEqual(act_list_req['page_meta']['total_count'], 10)

        act_list_req = self.get_current_resource_list({
            'target_chembl_id': 'CHEMBL3938',
            'assay_type__iregex': '(B|F)',
        })
        self.assertGreaterEqual(act_list_req['page_meta']['total_count'], 600)
        self.assertLessEqual(act_list_req['page_meta']['total_count'], 800)
        for act_i in act_list_req[self.get_current_plural()]:
            self.assertEqual(act_i['target_chembl_id'], 'CHEMBL3938')
            self.assertIn(act_i['assay_type'], {'B', 'F'})

    def test_slow_filtered_list(self):
        act_list_req = self.get_current_resource_list({
            'target_chembl_id': 'CHEMBL4506',
            'standard_type__in': ','.join(['IC50', 'Ki', 'EC50', 'Kd']),
            'standard_value__isnull': 'false',
            'ligand_efficiency__isnull': 'false'
        })
        self.assertLessEqual(act_list_req['page_meta']['total_count'], 1000)

    def test_activity_assay_description_search(self):
        text_test = 'tg-gates'
        act_list_req = self.get_current_resource_list({
            'assay_description__icontains': text_test.upper()
        })
        upper_ocunt = act_list_req['page_meta']['total_count']
        self.assertGreaterEqual(act_list_req['page_meta']['total_count'], 210700)
        self.assertLessEqual(act_list_req['page_meta']['total_count'], 220000)

        for act_i in act_list_req[self.get_current_plural()]:
            self.assertIn(text_test, act_i['assay_description'].lower())


        act_list_req = self.get_current_resource_list({
            'assay_description__icontains': text_test
        })
        self.assertEquals(act_list_req['page_meta']['total_count'], upper_ocunt,
                          'Upper and lower case search does not match')
        self.assertGreaterEqual(act_list_req['page_meta']['total_count'], 210700)
        self.assertLessEqual(act_list_req['page_meta']['total_count'], 220000)

        for act_i in act_list_req[self.get_current_plural()]:
            self.assertIn(text_test, act_i['assay_description'].lower())
