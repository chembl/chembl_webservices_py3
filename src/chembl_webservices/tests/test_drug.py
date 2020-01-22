from chembl_webservices.tests import BaseWebServiceTestCase

class DrugTestCase(BaseWebServiceTestCase):

    resource = 'drug'
    id_property = 'molecule_chembl_id'
    resource_expected_count = 13308
    sorting_test_props = ['sc_patent', 'ob_patent']
    mandatory_properties = [
      'applicants',
      'availability_type',
      'black_box',
      'chirality',
      'development_phase',
      'drug_type',
      'first_approval',
      'first_in_class',
      'indication_class',
      'molecule_chembl_id',
      'ob_patent',
      'oral',
      'parenteral',
      'prodrug',
      'research_codes',
      'rule_of_five',
      'sc_patent',
      'synonyms',
      'topical',
      'usan_stem',
      'usan_stem_definition',
      'usan_stem_substem',
      'usan_year',
    ]

    def test_filtered_lists(self):
        drug_list_req = self.get_current_resource_list({
            'first_approval': 1976,
            'usan_stem': '-azosin',
        })
        self.assertGreaterEqual(drug_list_req['page_meta']['total_count'], 1)
