from chembl_webservices.tests import BaseWebServiceTestCase

class DocumentTestCase(BaseWebServiceTestCase):

    resource = 'document'
    id_property = 'document_chembl_id'
    resource_expected_count = 76076
    sorting_test_props = ['title']
    mandatory_properties = [
      'abstract',
      'doc_type',
      'document_chembl_id',
      'doi',
      'title',
    ]

    def test_filtered_lists(self):
        doc_list_req = self.get_current_resource_list({
            'doc_type': 'PUBLICATION',
            'year__gt': 1985,
        })
        self.assertGreaterEqual(doc_list_req['page_meta']['total_count'], 66000)
