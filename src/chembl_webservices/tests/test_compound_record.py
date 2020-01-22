from chembl_webservices.tests import BaseWebServiceTestCase


class CompoundRecordTestCase(BaseWebServiceTestCase):

    resource = 'compound_record'
    id_property = 'record_id'
    resource_expected_count = 2425876
    sorting_test_props = ['compound_name']
    mandatory_properties = [
      'compound_key',
      'compound_name',
      'document_chembl_id',
      'molecule_chembl_id',
      'record_id',
      'src_id',
    ]

    def test_filtered_lists(self):
        records_req = self.get_current_resource_list({
            'compound_name__istartswith': '2-Acetoxy',
            'compound_key__icontains': 'ASA',
            'document_chembl_id': 'CHEMBL1123757',
        })
        self.assertGreaterEqual(records_req['page_meta']['total_count'], 1)

        records_req = self.get_current_resource_list({
            'document_chembl_id': 'CHEMBL1126670',
        })
        self.assertGreaterEqual(records_req['page_meta']['total_count'], 20)

        records_req = self.get_current_resource_list({
            'compound_name__iendswith': 'propionamide',
        })
        self.assertGreaterEqual(records_req['page_meta']['total_count'], 6000)

        records_req = self.get_current_resource_list({
            'molecule_chembl_id': 'CHEMBL409',
        })
        self.assertGreaterEqual(records_req['page_meta']['total_count'], 70)
