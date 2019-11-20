from chembl_webservices.tests import BaseWebServiceTestCase


class TargetTestCase(BaseWebServiceTestCase):

    resource = 'protein_class'
    id_property = 'protein_class_id'
    resource_expected_count = 857
    sorting_test_props = ['l1', 'l2', 'l3']
    mandatory_properties = [
        'l1',
        'l2',
        'l3',
        'l4',
        'l5',
        'l6',
        'l7',
        'l8',
        'protein_class_id',
    ]

    def test_filtered_list(self):
        req_res_1 = self.get_current_resource_list({
            'l1': 'Enzyme'
        })
        req_res_2 = self.get_current_resource_list({
            'l2': 'Kinase'
        })
        req_res_3 = self.get_current_resource_list({
            'l3': 'Protein Kinase'
        })
        req_res_4 = self.get_current_resource_list({
            'l4': 'CAMK protein kinase group'
        })
        req_res_5 = self.get_current_resource_list({
            'l5': 'CAMK protein kinase CAMK1 family'
        })
        req_res_6 = self.get_current_resource_list({
            'l6': 'CAMK protein kinase AMPK subfamily'
        })
        self.assertGreaterEqual(req_res_1['page_meta']['total_count'], req_res_2['page_meta']['total_count'])
        self.assertGreaterEqual(req_res_2['page_meta']['total_count'], req_res_3['page_meta']['total_count'])
        self.assertGreaterEqual(req_res_3['page_meta']['total_count'], req_res_4['page_meta']['total_count'])
        self.assertGreaterEqual(req_res_4['page_meta']['total_count'], req_res_5['page_meta']['total_count'])
        self.assertGreaterEqual(req_res_5['page_meta']['total_count'], req_res_6['page_meta']['total_count'])

    def test_protein_class_traversing(self):
        prot_class_req = self.get_current_resource_list({
            'l3__icontains': 'Bromodomain'
        })
        bromodomain_id = prot_class_req[self.get_current_plural()][0]['protein_class_id']

        target_component_req = self.get_resource_list('target_component', {
            'protein_classifications__protein_classification_id': bromodomain_id
        })
        print(target_component_req)
        print(self.get_current_plural())
        bromodomain_family_target_ids = [
            target_component['targets']
            for target_component in target_component_req[self.get_plural('target_component')]
        ]
        bromodomain_family_target_ids = [
            item['target_chembl_id'] for sublist in bromodomain_family_target_ids for item in sublist
        ]
        bromodomain_family_targets = self.get_resource_list_by_ids('target', bromodomain_family_target_ids)

        bromodomain_family_gene_names = []
        for target in bromodomain_family_targets:
            for component in target['target_components']:
                for synonym in component['target_component_synonyms']:
                    if synonym['syn_type'] == "GENE_SYMBOL":
                        bromodomain_family_gene_names.append(synonym['component_synonym'])

        self.assertIn('BRD1', bromodomain_family_gene_names)
        self.assertIn('BRD2', bromodomain_family_gene_names)
        self.assertIn('BRD3', bromodomain_family_gene_names)
        self.assertIn('BRD4', bromodomain_family_gene_names)
        self.assertIn('BRDT', bromodomain_family_gene_names)
