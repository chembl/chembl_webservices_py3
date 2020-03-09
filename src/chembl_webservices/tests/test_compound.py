from requests.exceptions import RetryError

from chembl_webservices.tests import BaseWebServiceTestCase


class CompoundTestCase(BaseWebServiceTestCase):

    resource = 'molecule'
    id_property = 'molecule_chembl_id'
    resource_expected_count = 1950765
    sorting_test_props = ['pref_name']
    mandatory_properties = [
        'atc_classifications',
        'availability_type',
        'biotherapeutic',
        'black_box_warning',
        'chebi_par_id',
        'chirality',
        'dosed_ingredient',
        'first_approval',
        'first_in_class',
        'helm_notation',
        'indication_class',
        'inorganic_flag',
        'max_phase',
        'molecule_chembl_id',
        'molecule_hierarchy',
        'molecule_properties',
        'molecule_structures',
        'molecule_type',
        'natural_product',
        'oral',
        'parenteral',
        'polymer_flag',
        'pref_name',
        'prodrug',
        'structure_type',
        'therapeutic_flag',
        'topical',
        'usan_stem',
        'usan_stem_definition',
        'usan_substem',
        'usan_year',
        'withdrawn_flag',
        'withdrawn_year',
        'withdrawn_country',
        'withdrawn_reason',
        'molecule_properties.cx_most_apka',
        'molecule_properties.cx_most_bpka',
        'molecule_properties.cx_logp',
        'molecule_properties.cx_logd',
        'molecule_properties.hba_lipinski',
        'molecule_properties.hbd_lipinski',
        'molecule_properties.num_lipinski_ro5_violations',
    ]

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
        self.assertEqual(set([x['molecule_chembl_id'] for x in molecule_forms['molecule_forms']]),
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

    def test_filtered_lists(self):
        comp_list_req = self.get_current_resource_list({
            'molecule_properties__cx_logp__gte': 1.9,
            'molecule_properties__aromatic_rings__lte': 3,
            'chirality': -1,
        })
        self.assertGreaterEqual(comp_list_req['page_meta']['total_count'], 1077174)

        comp_list_req = self.get_current_resource_list({
            'molecule_properties__full_mwt__range': '200,201',
        })
        self.assertGreaterEqual(comp_list_req['page_meta']['total_count'], 865)

        comp_list_req = self.get_current_resource_list({
            'molecule_structures__canonical_smiles':
                'COc1ccc2[C@@H]3[C@H](COc2c1)C(C)(C)OC4=C3C(=O)C(=O)C5=C4OC(C)(C)[C@H]6COc7cc(OC)ccc7[C@@H]56',
        })
        self.assertEqual(comp_list_req['page_meta']['total_count'], 1)
        self.assertEqual(comp_list_req[self.get_current_plural()][0]['molecule_chembl_id'], 'CHEMBL446858')

    def test_sdf_and_inchi(self):
        molecules_to_test = ['CHEMBL25', 'CHEMBL2260549', 'CHEMBL458500', 'CHEMBL457234',
            'CHEMBL1161014', 'CHEMBL458299', 'CHEMBL163612', 'CHEMBL499817',
            'CHEMBL455843', 'CHEMBL506341', 'CHEMBL1494499', 'CHEMBL454433',
            'CHEMBL2103782', 'CHEMBL441043']

        for molecule_i in molecules_to_test:
            mol_data = self.get_current_resource_by_id(molecule_i)
            sdf_file = self.get_current_resource_by_id(molecule_i, custom_format='sdf')
            mol_file = self.get_current_resource_by_id(molecule_i, custom_format='mol')
            self.assertTrue(sdf_file.startswith(mol_file), 'SDF file should start with the MOL file.')
            inchi_from_ctab = self.ctab2inchi(sdf_file)
            self.assertEqual(inchi_from_ctab, mol_data['molecule_structures']['standard_inchi'])


    def test_no_structure(self):
        no_structure_doc = self.get_current_resource_by_id('CHEMBL6961')
        self.assertIsNone(no_structure_doc['molecule_structures'])
        req_return =  self.get_current_resource_by_id('CHEMBL6961', custom_format='mol', expected_code=404)
        self.assertIsNone(req_return)

        no_structure_doc = self.get_current_resource_by_id('CHEMBL6963')
        self.assertIsNone(no_structure_doc['molecule_structures'])
        req_return = self.get_current_resource_by_id('CHEMBL6963', custom_format='mol', expected_code=404)
        self.assertIsNone(req_return)


    def test_filtered_lists(self):
        comp_list_req_1 = self.get_current_resource_list({
            'molecule_chembl_id__contains': 'L25'
        })

        comp_list_req_2 = self.get_current_resource_list({
            'molecule_chembl_id__contains': 'CHEMBL25'
        })
        self.assertEqual(comp_list_req_1['page_meta']['total_count'], comp_list_req_2['page_meta']['total_count'])

    def get_chembl_ids_set_from_ids_list(self, ids_list):
        id_set_individual = set()
        id_set_group_request = set()
        for id_i in ids_list:
            mol_by_id_i = self.get_current_resource_by_id(id_i)
            id_set_individual.add(mol_by_id_i['molecule_chembl_id'])

        group_request_molecules = self.get_current_resource_list_by_ids(ids_list)
        for mol_i in group_request_molecules:
            id_set_group_request.add(mol_i['molecule_chembl_id'])

        self.assertEqual(id_set_individual, id_set_group_request)
        return id_set_individual


    def test_get_by_unique_identifier(self):
        chembl_ids = ['CHEMBL6498', 'CHEMBL6499', 'CHEMBL6505']
        inchi_keys = ['XSQLHVPPXBBUPP-UHFFFAOYSA-N', 'JXHVRXRRSSBGPY-UHFFFAOYSA-N', 'TUHYVXGNMOGVMR-GASGPIRDSA-N']
        smiles_ids = ['C#CCN(Cc1ccc2nc(C)nc(O)c2c1)c1ccc(C(=O)NC)cc1',
            'Cc1cc2c(cc1/N=C(\\S)Nc1ccc(S(N)(=O)=O)cc1)C(C)(C)CC(C)(C)S2',
            'CC(C)C[C@H](NC(=O)[C@@H](NC(=O)[C@H](Cc1c[nH]c2ccccc12)NC(=O)'
            '[C@H]1CCCN1C(=O)C(CCCCN)CCCCN)C(C)(C)C)C(=O)O']

        comp_list_req_by_inchi = self.get_current_resource_list({
            'molecule_structures__standard_inchi_key__in': ','.join(inchi_keys)
        })
        set_by_inchi_filter = set(
            [mol['molecule_chembl_id'] for mol in comp_list_req_by_inchi[self.get_current_plural()]]
        )

        comp_list_req_by_smiles = self.get_current_resource_list({
            'molecule_structures__canonical_smiles__in': ','.join(smiles_ids)
        })
        set_by_smiles_filter = set(
            [mol['molecule_chembl_id'] for mol in comp_list_req_by_smiles[self.get_current_plural()]]
        )

        set_by_chembl_ids = self.get_chembl_ids_set_from_ids_list(chembl_ids)
        set_by_inchi_keys = self.get_chembl_ids_set_from_ids_list(inchi_keys)
        set_by_smiles = self.get_chembl_ids_set_from_ids_list(smiles_ids)

        self.assertEqual(set_by_chembl_ids, set_by_inchi_keys)
        self.assertEqual(set_by_chembl_ids, set_by_smiles)
        self.assertEqual(set_by_chembl_ids, set_by_inchi_filter)
        self.assertEqual(set_by_chembl_ids, set_by_smiles_filter)

    def test_get_by_unique_identifier_2(self):
        chembl_125_smiles = 'CCCCCCCCCCCCCCCCOP(=O)([O-])OCC[N+](C)(C)C'
        doc_1 = self.get_current_resource_by_id('CHEMBL125')
        doc_2 = self.get_current_resource_by_id(chembl_125_smiles)
        self.assertEqual(doc_1, doc_2)

    def test_biotherapeutic(self):
        biotherapeutic_chembl_id = 'CHEMBL1743070'
        with_components = self.get_current_resource_by_id(biotherapeutic_chembl_id)
        self.assertIsNotNone(with_components)
        therapeutic = with_components['biotherapeutic']
        self.assertIn("molecule_chembl_id", therapeutic)
        self.assertIn("helm_notation", therapeutic)
        self.assertIn("description", therapeutic)
        self.assertIn("biocomponents", therapeutic)
        self.assertTrue(len(therapeutic['biocomponents']))
        component = therapeutic['biocomponents'][0]
        self.assertIn("sequence", component)
        self.assertIn("tax_id", component)
        self.assertIn("organism", component)
        self.assertIn("description", component)
        self.assertIn("component_type", component)
        self.assertIn("component_id", component)

    def test_atc_class(self):
        atc_chembl_id = 'CHEMBL1475'
        with_multiple_atc = self.get_current_resource_by_id(atc_chembl_id)
        self.assertEqual(len(with_multiple_atc['atc_classifications']), 2)

        comp_list_req = self.get_current_resource_list({
            'atc_classifications__level5': 'C07AB01'
        })
        self.assertGreater(comp_list_req['page_meta']['total_count'], 0)


    def test_atc_class(self):
        with_x_refs_chembl_id = 'CHEMBL25'
        with_x_refs = self.get_current_resource_by_id(with_x_refs_chembl_id)

        self.assertIn('cross_references', with_x_refs, 'No cross references')
        x_refs = with_x_refs['cross_references']
        self.assertTrue(len(x_refs))
        single_ref = x_refs[0]
        self.assertIn('xref_id', single_ref, 'No xref_id in cross reference')
        self.assertIn('xref_name', single_ref, 'No xref_name in cross reference')
        self.assertIn('xref_src', single_ref, 'No xref_src in cross reference')

    def test_ctab_2_inchi(self):
        chembl_id = 'CHEMBL25'
        molstring = self.get_current_resource_by_id(chembl_id, custom_format='sdf')
        inchi_from_molstring = self.ctab2inchi(molstring)
        inchi_from_chembl = self.get_current_resource_by_id(chembl_id)['molecule_structures']['standard_inchi']
        self.assertEqual(inchi_from_molstring, inchi_from_chembl)

    def test_traversing(self):
        comp_list_req = self.get_current_resource_list({
            'atc_classifications__level5__startswith': 'A10'
        })
        self.assertGreater(comp_list_req['page_meta']['total_count'], 0)
        molecule_ids = [molecule['molecule_chembl_id'] for molecule in comp_list_req[self.get_current_plural()]]

        act_list_req = self.get_resource_list('activity', {
            'molecule_chembl_id__in': ','.join(molecule_ids)
        })
        self.assertGreater(act_list_req['page_meta']['total_count'], 0)

    def test_chembl_id_filtering(self):
        self.assertGreaterEqual(
            self.get_current_resource_list({'molecule_chembl_id__icontains': '25'})
            ['page_meta']['total_count'], 90000
        )

    def test_nested_property_filtering(self):
        self.assertGreaterEqual(
            self.get_current_resource_list({'molecule_synonyms__molecule_synonym__icontains': 'bayer'})
            ['page_meta']['total_count'], 15
        )
