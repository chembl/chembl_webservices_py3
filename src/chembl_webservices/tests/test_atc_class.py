from chembl_webservices.tests import BaseWebServiceTestCase


class ATCClassTestCase(BaseWebServiceTestCase):

    resource = 'atc_class'
    id_property = 'level5'
    resource_expected_count = 4886
    sorting_test_props = ['level4', 'level4_description', 'level5']
    mandatory_properties = [
        'level1',
        'level1_description',
        'level2',
        'level2_description',
        'level3',
        'level3_description',
        'level4',
        'level4_description',
        'level5',
        'who_name',
    ]

    def test_filtered_lists(self):
        atc_list_h = self.get_current_resource_list({'level1': 'H'})
        atc_list_h03 = self.get_current_resource_list({'level2': 'H03'})
        atc_list_h03a = self.get_current_resource_list({'level3': 'H03A'})
        atc_list_h03aa = self.get_current_resource_list({'level4': 'H03AA'})
        atc_list_h03aa03 = self.get_current_resource_list({'level5': 'H03AA03'})

        self.assertGreaterEqual(atc_list_h['page_meta']['total_count'], atc_list_h03['page_meta']['total_count'])
        self.assertGreaterEqual(atc_list_h03['page_meta']['total_count'], atc_list_h03a['page_meta']['total_count'])
        self.assertGreaterEqual(atc_list_h03a['page_meta']['total_count'], atc_list_h03aa['page_meta']['total_count'])
        self.assertGreaterEqual(
            atc_list_h03aa['page_meta']['total_count'], atc_list_h03aa03['page_meta']['total_count']
        )

        doc_data = self.get_current_resource_by_id('H03AA03')
        self.assertEqual(doc_data['who_name'], 'combinations of levothyroxine and liothyronine')
