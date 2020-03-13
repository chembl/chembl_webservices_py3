from requests.exceptions import RetryError

from chembl_webservices.tests import BaseWebServiceTestCase


def skip_structure_test():
    """
    Decorator to add tags to a test class or method.
    """
    def skip_func(*args, **kwargs):
        pass

    def decorator(obj):
        if BaseWebServiceTestCase.TEST_STRUCTURES:
            return obj
        return skip_func

    return decorator

class CompoundByStructureTestCase(BaseWebServiceTestCase):

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

    @skip_structure_test()
    def test_compound_flexmatch(self):
        self.assertIn(
            self.get_current_resource_list(
                {
                    'molecule_structures__canonical_smiles__flexmatch':
                    'COc1ccc2[C@@H]3[C@H](COc2c1)C(C)(C)OC4=C3C(=O)C(=O)C5=C4OC(C)(C)[C@@H]6COc7cc(OC)ccc7[C@H]56'
                }
            )['molecules'][0]['molecule_structures']['standard_inchi_key'],
            [
                'GHBOEFUAGSHXPO-UWXQAFAOSA-N',
            ]
        )
        req = self.get_current_resource_list(
            {
                'molecule_structures__canonical_smiles__flexmatch':
                'C\C(=C\C(=O)O)\C=C\C=C(/C)\C=C\C1=C(C)CCCC1(C)C'
            }
        )
        self.assertGreaterEqual(
            req['page_meta']['total_count'], 7
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

    @skip_structure_test()
    def test_compound_similarity(self):
        self.assertGreaterEqual(
            self.get_similar_molecules(
                'COc1ccc2[C@@H]3[C@H](COc2c1)C(C)(C)OC4=C3C(=O)C(=O)C5=C4OC(C)(C)[C@@H]6COc7cc(OC)ccc7[C@H]56', 40
            )['page_meta']['total_count'], 29
        )
        self.assertGreaterEqual(
            self.get_similar_molecules(
                'C\C(=C/C=C/C(=C/C(=O)O)/C)\C=C\C1=C(C)CCCC1(C)C', 40
            )['page_meta']['total_count'], 200
        )
    @skip_structure_test()
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

    @skip_structure_test()
    def test_filtered_lists(self):
        comp_list_req = self.get_current_resource_list({
            'molecule_structures__canonical_smiles__flexmatch':
                'COc1ccc2[C@@H]3[C@H](COc2c1)C(C)(C)OC4=C3C(=O)C(=O)C5=C4OC(C)(C)[C@H]6COc7cc(OC)ccc7[C@@H]56',
        })
        self.assertEqual(comp_list_req['page_meta']['total_count'], 2)
        self.assertIn(comp_list_req[self.get_current_plural()][0]['molecule_chembl_id'], ['CHEMBL446858', 'CHEMBL1'])

    @skip_structure_test()
    def test_flexmatch(self):
        chembl_id = 'CHEMBL25'
        smiles = self.get_current_resource_by_id(chembl_id)['molecule_structures']['canonical_smiles']

        comp_list_req = self.get_current_resource_list({
            'molecule_structures__canonical_smiles__flexmatch': smiles
        })
        found_ids_by_smiles = set()
        for molecule_i in comp_list_req[self.get_current_plural()]:
            found_ids_by_smiles.add(molecule_i['molecule_chembl_id'])

        comp_list_req = self.get_current_resource_list({
            'molecule_structures__canonical_smiles__flexmatch': chembl_id
        })
        found_ids_by_chembl_id = set()
        for molecule_i in comp_list_req[self.get_current_plural()]:
            found_ids_by_chembl_id.add(molecule_i['molecule_chembl_id'])
        self.assertEqual(found_ids_by_smiles, found_ids_by_chembl_id)

    @skip_structure_test()
    def test_no_structure(self):
        no_structure_doc = self.get_current_resource_by_id('CHEMBL6961')
        self.assertIsNone(no_structure_doc['molecule_structures'])
        req_return =  self.get_current_resource_by_id('CHEMBL6961', custom_format='mol', expected_code=404)
        self.assertIsNone(req_return)

        no_structure_doc = self.get_current_resource_by_id('CHEMBL6963')
        self.assertIsNone(no_structure_doc['molecule_structures'])
        req_return = self.get_current_resource_by_id('CHEMBL6963', custom_format='mol', expected_code=404)
        self.assertIsNone(req_return)

    @skip_structure_test()
    def test_longest_smiles(self):
        longest_chembl_smiles = r"CCCCCCCCCC(C(=O)NCCc1ccc(OP(=S)(Oc2ccc(CCNC(=O)C(CCCCCCCCC)P(=O)(O)O)cc2)N(C)/N=C/c" \
                                r"2ccc(OP3(Oc4ccc(/C=N/N(C)P(=S)(Oc5ccc(CCNC(=O)C(CCCCCCCCC)P(=O)(O)O)cc5)Oc5ccc(CCNC" \
                                r"(=O)C(CCCCCCCCC)P(=O)(O)O)cc5)cc4)=NP(Oc4ccc(/C=N/N(C)P(=S)(Oc5ccc(CCNC(=O)C(CCCCCC" \
                                r"CCC)P(=O)(O)O)cc5)Oc5ccc(CCNC(=O)C(CCCCCCCCC)P(=O)(O)O)cc5)cc4)(Oc4ccc(/C=N/N(C)P(=" \
                                r"S)(Oc5ccc(CCNC(=O)C(CCCCCCCCC)P(=O)(O)O)cc5)Oc5ccc(CCNC(=O)C(CCCCCCCCC)P(=O)(O)O)cc" \
                                r"5)cc4)=NP(Oc4ccc(/C=N/N(C)P(=S)(Oc5ccc(CCNC(=O)C(CCCCCCCCC)P(=O)(O)O)cc5)Oc5ccc(CCN" \
                                r"C(=O)C(CCCCCCCCC)P(=O)(O)O)cc5)cc4)(Oc4ccc(/C=N/N(C)P(=S)(Oc5ccc(CCNC(=O)C(CCCCCCCC" \
                                r"C)P(=O)(O)O)cc5)Oc5ccc(CCNC(=O)C(CCCCCCCCC)P(=O)(O)O)cc5)cc4)=N3)cc2)cc1)P(=O)(O)O." \
                                r"CCCCCCCCCCCCCCCCNOC(CO)C(O)C(OC1OC(CO)C(O)C(O)C1O)C(O)CO.CCCCCCCCCCCCCCCCNOC(CO)C(O" \
                                r")C(OC1OC(CO)C(O)C(O)C1O)C(O)CO.CCCCCCCCCCCCCCCCNOC(CO)C(O)C(OC1OC(CO)C(O)C(O)C1O)C(" \
                                r"O)CO.CCCCCCCCCCCCCCCCNOC(CO)C(O)C(OC1OC(CO)C(O)C(O)C1O)C(O)CO.CCCCCCCCCCCCCCCCNOC(C" \
                                r"O)C(O)C(OC1OC(CO)C(O)C(O)C1O)C(O)CO.CCCCCCCCCCCCCCCCNOC(CO)C(O)C(OC1OC(CO)C(O)C(O)C" \
                                r"1O)C(O)CO.CCCCCCCCCCCCCCCCNOC(CO)C(O)C(OC1OC(CO)C(O)C(O)C1O)C(O)CO.CCCCCCCCCCCCCCCC" \
                                r"NOC(CO)C(O)C(OC1OC(CO)C(O)C(O)C1O)C(O)CO.CCCCCCCCCCCCCCCCNOC(CO)C(O)C(OC1OC(CO)C(O)" \
                                r"C(O)C1O)C(O)CO.CCCCCCCCCCCCCCCCNOC(CO)C(O)C(OC1OC(CO)C(O)C(O)C1O)C(O)CO.CCCCCCCCCCC" \
                                r"CCCCCNOC(CO)C(O)C(OC1OC(CO)C(O)C(O)C1O)C(O)CO.CCCCCCCCCCCCCCCCNOC(CO)C(O)C(OC1OC(CO" \
                                r")C(O)C(O)C1O)C(O)CO"
        longest_smiles_chembl_id = 'CHEMBL1628285'
        doc_1 = self.get_current_resource_by_id(longest_chembl_smiles)
        doc_2 = self.get_current_resource_by_id(longest_smiles_chembl_id)
        self.assertEqual(doc_1, doc_2)

        comp_list_req = self.get_current_resource_list({
            'molecule_structures__canonical_smiles': longest_chembl_smiles
        })
        results_list = comp_list_req[self.get_current_plural()]
        self.assertGreater(
            comp_list_req['page_meta']['total_count'], 0, 'Longest smiles not found with filter by canonical smiles.'
        )
        self.assertEqual(doc_1, results_list[0])

        # Test by flexmatch
        comp_list_req = self.get_current_resource_list({
            'molecule_structures__canonical_smiles__flexmatch': longest_chembl_smiles
        })
        results_list = comp_list_req[self.get_current_plural()]
        self.assertGreater(
            comp_list_req['page_meta']['total_count'], 0,
            'Longest smiles not found with filter by canonical smiles by flexmatch.'
        )
        self.assertEqual(doc_1, results_list[0])

        # Test by substructure
        comp_list_req = self.get_substructure_molecules(longest_chembl_smiles)
        self.assertGreater(
            comp_list_req['page_meta']['total_count'], 0,
            'Longest smiles not found with filter by canonical smiles by substructure.'
        )

        # Test by similarity
        comp_list_req = self.get_similar_molecules(longest_chembl_smiles, 100)
        self.assertGreater(
            comp_list_req['page_meta']['total_count'], 0,
            'Longest smiles not found with filter by canonical smiles by substructure.'
        )

# SIMILARITY

#
#     def test_similarity_resource(self):
#         similarity = new_client.similarity
#         res = similarity.filter(smiles="CO[C@@H](CCC#C\C=C/CCCC(C)CCCCC=C)C(=O)[O-]", similarity=70)
#         self.assertTrue(all(Decimal(res[i]['similarity']) >= Decimal(res[i+1]['similarity']) for i in range(len(res)-1)), [Decimal(r['similarity']) for r in res])
#         self.assertTrue(res.exists())
#
#     def test_similarity_resource_a(self):
#         similarity = new_client.similarity
#         res = similarity.filter(smiles='[O--].[Fe++].OCC1OC(OC2C(CO)OC(OC3C(O)C(CO)OC(OCC4OC(OCC5OC(O)C(O)C(OC6OC(CO)C(O)C(OC7OC(COC8OC(COC9OC(CO)C(O)C(O)C9O)C(O)C(O)C8O)C(O)C(OC8OC(CO)C(O)C(OC9OC(CO)C(O)C(OC%10OC(COC%11OC(COC%12OC(COC%13OC(COC%14OC(COC%15OC(CO)C(O)C(O)C%15O)C(O)C(OC%15OC(CO)C(O)C%15O)C%14O)C(O)C(O)C%13O)C(O)C(O)C%12O)C(O)C(O)C%11O)C(O)C(OC%11OC(CO)C(O)C(O)C%11O)C%10O)C9O)C8O)C7O)C6O)C5O)C(O)C(O)C4O)C3O)C2O)C(O)C1O', similarity=70)
#         self.assertTrue(res.exists())
#         self.assertTrue(all(Decimal(res[i]['similarity']) >= Decimal(res[i+1]['similarity']) for i in range(len(res)-1)), [Decimal(r['similarity']) for r in res])
#         self.assertTrue(len(res) > 90, len(res))
#
#     def test_similarity_resource_b(self):
#         similarity = new_client.similarity
#         res = similarity.filter(smiles="CC(C)OC(=O)[C@H](C)N[P@](=O)(OC[C@H]1O[C@@H](N2C=CC(=O)NC2=O)[C@](C)(F)[C@@H]1O)Oc3ccccc3", similarity=70)
#         self.assertTrue(all(Decimal(res[i]['similarity']) >= Decimal(res[i+1]['similarity']) for i in range(len(res)-1)), [Decimal(r['similarity']) for r in res])
#         self.assertTrue(res.exists())
#
#     def test_similarity_resource_c(self):
#         similarity = new_client.similarity
#         res = similarity.filter(smiles="CC(=O)Oc1ccccc1C(=O)O", similarity=70)
#         self.assertTrue(all(Decimal(res[i]['similarity']) >= Decimal(res[i+1]['similarity']) for i in range(len(res)-1)), [Decimal(r['similarity']) for r in res])
#         self.assertTrue(res.exists())
#         _ = len(res)
#         most_similar = res[0]
#         self.assertEqual(Decimal(most_similar['similarity']), Decimal(100.0))
#         self.assertEqual(most_similar['pref_name'], 'ASPIRIN')
#         self.assertTrue('molecule_hierarchy' in res.filter(molecule_properties__acd_logp__gte=3.4).filter(molecule_properties__hbd__lte=5)[0])
#         random_index = 5 #randint(0, count - 1)
#         random_elem = res[random_index]
#         self.assertIsNotNone(random_elem, "Can't get {0} element from the list".format(random_index))
#         self.assertIn('availability_type', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('black_box_warning', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('chebi_par_id', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('chirality', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('dosed_ingredient', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('first_approval', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('first_in_class', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('indication_class', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('inorganic_flag', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('max_phase', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('molecule_chembl_id', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('molecule_hierarchy', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('molecule_properties', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('molecule_structures', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('molecule_type', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('natural_product', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('oral', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('parenteral', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('polymer_flag', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('pref_name', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('prodrug', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('structure_type', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('therapeutic_flag', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('topical', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('usan_stem', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('usan_stem_definition', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('usan_substem', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('usan_year', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('similarity', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         res.set_format('xml')
#         parseString(res[0])
#         res.set_format('json')
#
#     def test_similarity_resource_d(self):
#         similarity = new_client.similarity
#         res = similarity.filter(smiles="CC(=O)Oc1ccccc1C(=O)O", similarity=70).order_by('similarity')
#         less_similar = res[0]
#         self.assertTrue(Decimal(less_similar['similarity']) >= Decimal(70))
#         self.assertTrue(all(Decimal(res[i]['similarity']) <= Decimal(res[i+1]['similarity']) for i in range(len(res)-1)), [Decimal(r['similarity']) for r in res])
#
#     def test_similarity_resource_e(self):
#         similarity = new_client.similarity
#         res = similarity.filter(smiles="COc1ccc2[C@@H]3[C@H](COc2c1)C(C)(C)OC4=C3C(=O)C(=O)C5=C4OC(C)(C)[C@@H]6COc7cc(OC)ccc7[C@H]56", similarity=70)
#         most_similar = res[0]
#         self.assertEqual(Decimal(most_similar['similarity']), Decimal(100.0))
#         self.assertEqual(most_similar['molecule_chembl_id'], 'CHEMBL1')
#         self.assertTrue(len(res) > 1000)
#         self.assertTrue(all(Decimal(res[i]['similarity']) >= Decimal(res[i+1]['similarity']) for i in range(len(res)-1)), [Decimal(r['similarity']) for r in res])
#
#         res1 = similarity.filter(smiles="COc1ccc2[C@@H]3[C@H](COc2c1)C(C)(C)OC4=C3C(=O)C(=O)C5=C4OC(C)(C)[C@@H]6COc7cc(OC)ccc7[C@H]56", similarity=70).only(['molecule_chembl_id', 'similarity'])
#         most_similar = res1[0]
#         self.assertEqual(list(most_similar.keys()), ['molecule_chembl_id', 'similarity'])
#         self.assertEqual(Decimal(most_similar['similarity']), Decimal(100.0))
#         self.assertEqual(most_similar['molecule_chembl_id'], 'CHEMBL1')
#         self.assertTrue(len(res1) > 1000)
#         self.assertTrue(all(Decimal(res1[i]['similarity']) >= Decimal(res1[i+1]['similarity']) for i in range(len(res1)-1)), [Decimal(r['similarity']) for r in res1])
#
#         self.assertEquals(len(res), len(res1))
#
#     def test_similarity_resource_f(self):
#         similarity = new_client.similarity
#         res = similarity.filter(smiles="COc1ccc2[C@@H]3[C@H](COc2c1)C(C)(C)OC4=C3C(=O)C(=O)C5=C4OC(C)(C)[C@@H]6COc7cc(OC)ccc7[C@H]56", similarity=70).order_by('similarity')
#         self.assertTrue(all(Decimal(res[i]['similarity']) <= Decimal(res[i+1]['similarity']) for i in range(len(res)-1)), [Decimal(r['similarity']) for r in res])
#         less_similar = res[0]
#         self.assertTrue(Decimal(less_similar['similarity']) >= Decimal(70))
#
#     def test_similarity_resource_g(self):
#         similarity = new_client.similarity
#         res = similarity.filter(smiles="COc1ccc2[C@@H]3[C@H](COc2c1)C(C)(C)OC4=C3C(=O)C(=O)C5=C4OC(C)(C)[C@@H]6COc7cc(OC)ccc7[C@H]56", similarity=70).filter(molecule_properties__aromatic_rings=2)
#         self.assertTrue(len(res) > 480)
#
#     def test_similarity_resource_h(self):
#         similarity = new_client.similarity
#         res = similarity.filter(chembl_id="CHEMBL25", similarity=100)
#         res.set_format('json')
#         self.assertEqual(len(res), 1)
#         self.assertEqual(res[0]['molecule_chembl_id'], 'CHEMBL25')
#
#     def test_similarity_resource_i(self):
#         similarity = new_client.similarity
#         self.assertRaisesRegex(HttpNotFound, 'No chemical structure defined', len, similarity.filter(chembl_id="CHEMBL1201822", similarity=70))
#         self.assertRaisesRegex(HttpBadRequest, 'not a valid SMILES string', len, similarity.filter(smiles="45Z", similarity=100))
#         self.assertRaisesRegex(HttpBadRequest, 'Error in molecule perception', len, similarity.filter(smiles="C1C[C@H]2C[C@@H]([C@H](C(=O)OC)[C@@H]1N2CCCF)c1ccc(cc1)[123F]", similarity=100))
#
#     def test_similarity_resource_j(self):
#         similarity = new_client.similarity
#         similarity.set_format('sdf')
#         res = similarity.filter(smiles="CO[C@@H](CCC#C\C=C/CCCC(C)CCCCC=C)C(=O)[O-]", similarity=70)
#         self.assertTrue(len(res))
#

#
# SUBSTRUCTURE

#
#
#     def test_substructure_resource_a(self):
#         substructure = new_client.substructure
#         with self.assertRaisesRegex(HttpBadRequest, 'Structure or identifier required'):
#             substructure[0]
#
#
#     def test_substructure_resource_b(self):
#         substructure = new_client.substructure
#         res = substructure.filter(smiles="CCC#C\C=C/CCC")
#         self.assertTrue(res.exists())
#         slice = res[:6]
#         self.assertEqual(len([m for m in slice]), 6)
#         self.assertTrue(len(res) > 10)
#
#
#     def test_substructure_resource_c(self):
#         substructure = new_client.substructure
#         res = substructure.filter(smiles="CN(CCCN)c1cccc2ccccc12")
#         self.assertTrue(res.exists())
#         count = len(res)
#
#         res1 = substructure.filter(smiles="CN(CCCN)c1cccc2ccccc12").only('molecule_chembl_id')
#         self.assertTrue(res1.exists())
#         count1 = len(res1)
#         self.assertEqual(count, count1)
#
#         random_index = 80 #randint(0, count - 1)
#         random_elem = res[random_index]
#         self.assertIsNotNone(random_elem, "Can't get {0} element from the list".format(random_index))
#         self.assertIn('availability_type', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('black_box_warning', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('chebi_par_id', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('chirality', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('dosed_ingredient', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('first_approval', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('first_in_class', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('indication_class', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('inorganic_flag', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('max_phase', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('molecule_chembl_id', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('molecule_hierarchy', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('molecule_properties', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('molecule_structures', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('molecule_type', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('natural_product', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('oral', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('parenteral', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('polymer_flag', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('pref_name', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('prodrug', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('structure_type', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('therapeutic_flag', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('topical', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('usan_stem', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('usan_stem_definition', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('usan_substem', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         self.assertIn('usan_year', random_elem, 'One of required fields not found in resource {0}'.format(random_elem))
#         res.set_format('xml')
#         parseString(res[0])
#
#
#     def test_substructure_resource_d(self):
#         substructure = new_client.substructure
#         res = substructure.filter(chembl_id="CHEMBL25")
#         res.set_format('json')
#         self.assertTrue(len(res) > 300)
#         self.assertEqual(res[0]['molecule_chembl_id'], 'CHEMBL25')
#
#
#     def test_substructure_resource_e(self):
#         substructure = new_client.substructure
#         self.assertRaisesRegex(HttpNotFound, 'No chemical structure defined', len, substructure.filter(chembl_id="CHEMBL1201822"))
#
#
#     def test_substructure_resource_f(self):
#         substructure = new_client.substructure
#         substructure.set_format('sdf')
#         res = substructure.filter(smiles="CN(CCCN)c1cccc2ccccc12")
#         self.assertTrue(len(res))