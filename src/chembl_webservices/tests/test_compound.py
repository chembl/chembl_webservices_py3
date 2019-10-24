from chembl_webservices.tests import BaseWebServiceTestCase


class CompoundTestCase(BaseWebServiceTestCase):

    resource = 'molecule'
    id_property = 'molecule_chembl_id'
    resource_expected_count = 1879206
    sorting_test_props = ['pref_name']

    def test_compound_by_id(self):
        self.assertEqual(
            self.get_current_resource_by_id('CHEMBL1')['molecule_structures']['standard_inchi_key'],
            'GHBOEFUAGSHXPO-XZOTUCIWSA-N'
        )

        self.assertEqual(
            len(self.get_current_resource_list_by_ids(['CHEMBL{0}'.format(x) for x in range(1, 6)])),
            5
        )
        self.assertEqual(
            len(self.get_current_resource_list_by_ids(['CHEMBL{0}'.format(x) for x in range(1, 301)])),
            170
        )

    def test_compound_by_inchi(self):
        self.assertEqual(
            self.get_current_resource_list(
                {'molecule_structures__standard_inchi_key__exact': 'QFFGVLORLPOAEC-SNVBAGLBSA-N'}
            )['molecules'][0]['molecule_properties']['full_molformula'], 'C19H21ClFN3O3'
        )

    def test_compound_flexmatch(self):
        self.assertEqual(
            self.get_current_resource_list(
                {
                    'molecule_structures__canonical_smiles__flexmatch':
                    'COc1ccc2[C@@H]3[C@H](COc2c1)C(C)(C)OC4=C3C(=O)C(=O)C5=C4OC(C)(C)[C@@H]6COc7cc(OC)ccc7[C@H]56'
                }
            )['molecules'][0]['molecule_structures']['standard_inchi_key'], 'GHBOEFUAGSHXPO-UWXQAFAOSA-N'
        )
        req = self.get_current_resource_list(
            {
                'molecule_structures__canonical_smiles__flexmatch':
                'C\C(=C\C(=O)O)\C=C\C=C(/C)\C=C\C1=C(C)CCCC1(C)C'
            }
        )
        self.assertGreaterEqual(
            req['page_meta']['total_count'], 9
        )
        self.assertIn('ISOTRETINOIN', [c['pref_name'] for c in req['molecules']])

        req = self.get_current_resource_list(
            {
                'molecule_structures__canonical_smiles__flexmatch':
                'COC1(CN2CCC1CC2)C#CC(C#N)(c3ccccc3)c4ccccc4'
            }
        )
        self.assertEqual(
            req['page_meta']['total_count'], 1
        )
        self.assertEqual(
            req['molecules'][0]['molecule_structures']['standard_inchi_key'], 'MMAOIAFUZKMAOY-UHFFFAOYSA-N'
        )

        req = self.get_current_resource_list(
            {
                'molecule_structures__canonical_smiles__flexmatch':
                'CN1C\C(=C/c2ccc(C)cc2)\C3=C(C1)C(C(=C(N)O3)C#N)c4ccc(C)cc4'
            }
        )
        self.assertEqual(
            req['page_meta']['total_count'], 1
        )
        self.assertEqual(
            req['molecules'][0]['molecule_chembl_id'], 'CHEMBL319317'
        )

    def test_compound_similarity(self):
        self.assertGreaterEqual(
            self.get_similar_molecules(
                'COc1ccc2[C@@H]3[C@H](COc2c1)C(C)(C)OC4=C3C(=O)C(=O)C5=C4OC(C)(C)[C@@H]6COc7cc(OC)ccc7[C@H]56', 70
            )['page_meta']['total_count'], 800
        )
        self.assertGreaterEqual(
            self.get_similar_molecules(
                'C\C(=C/C=C/C(=C/C(=O)O)/C)\C=C\C1=C(C)CCCC1(C)C', 70
            )['page_meta']['total_count'], 200
        )

    def test_compound_substructure(self):
        self.assertGreaterEqual(
            self.get_substructure_molecules(
                'c1ccnc2c1nccn2'
            )['page_meta']['total_count'], 600
        )

        self.assertGreaterEqual(
            self.get_substructure_molecules(
                'C\C(=C/C=C/C(=C/C(=O)O)/C)\C=C\C1=C(C)CCCC1(C)C'
            )['page_meta']['total_count'], 100
        )

    def test_bioactivities(self):
        self.assertGreaterEqual(
            self.get_resource_list('activity', {'molecule_chembl_id__exact': 'CHEMBL1'})
            ['page_meta']['total_count'], 10
        )

    def test_molecule_form(self):
        molecule_forms = self.get_resource_list('molecule_form/CHEMBL169')
        self.assertEqual(
            molecule_forms['page_meta']['total_count'] , 4
        )
        self.assertEqual(set(map(lambda x: x['molecule_chembl_id'], molecule_forms['molecule_forms'])),
                         {'CHEMBL169', 'CHEMBL520029', 'CHEMBL1783810', 'CHEMBL1783814'})

        molecule_forms = self.get_resource_list('molecule_form/CHEMBL1078826')
        self.assertEqual(
            molecule_forms['page_meta']['total_count'] , 20
        )

        # TODO: FIX WS IS FAILING THIS TEST
        # molecule_forms = self.get_resource_list('molecule_form/CHEMBL415863')
        # self.assertEqual(
        #     molecule_forms['page_meta']['total_count'] , 2
        # )
        # self.assertEqual(set(map(lambda x: x['molecule_chembl_id'], molecule_forms['molecule_forms'])),
        #                  {'CHEMBL415863', 'CHEMBL1207563'})
        #
        # molecule_forms = self.get_resource_list('molecule_form/CHEMBL1207563')
        # self.assertEqual(
        #     molecule_forms['page_meta']['total_count'] , 2
        # )
        # self.assertEqual(set(map(lambda x: x['molecule_chembl_id'], molecule_forms['molecule_forms'])),
        #                  {'CHEMBL415863', 'CHEMBL1207563'})

    def test_molecule_form(self):
        req = self.get_resource_list(
            'mechanism',
            {
                'molecule_chembl_id__exact':
                'CHEMBL1642'
            }
        )
        self.assertGreaterEqual(
            req['page_meta']['total_count'], 3
        )

        mechanisms_names = {mec_i['mechanism_of_action'] for mec_i in req['mechanisms']}
        expected_mechanisms_names = {
            'Tyrosine-protein kinase ABL inhibitor',
            'Platelet-derived growth factor receptor beta inhibitor',
            'Stem cell growth factor receptor inhibitor',
        }
        self.assertEqual(mechanisms_names, expected_mechanisms_names)
