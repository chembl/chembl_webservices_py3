
from chembl_webservices.tests import BaseWebServiceTestCase


class BaseSearchTestCase(BaseWebServiceTestCase):

    def test_search_endpoint(self, query):
        pass


class ActivitySearchTestCase(BaseSearchTestCase):

    pass


class AssaySearchTestCase(BaseSearchTestCase):

    pass


class ChemblIdLookupSearchTestCase(BaseSearchTestCase):

    pass


class DocumentSearchTestCase(BaseSearchTestCase):

    pass


class MoleculeSearchTestCase(BaseSearchTestCase):

    pass


class ProteinClassSearchTestCase(BaseSearchTestCase):

    pass


class TargetSearchTestCase(BaseSearchTestCase):

    pass


#
#
#
#     def test_document_search(self):
#         document = new_client.document
#         document.set_format('json')
#         count = len(document.all())
#         res = document.search('cytokine')
#         self.assertTrue(len(res) > 300)
#         self.assertTrue(len(res) < count)
#         self.assertTrue('cytokine' in res[0]['abstract'])
#         res = document.search('activators')
#         self.assertTrue('activity' in res[0]['abstract'])
#         self.assertTrue('activators' not in res[0]['abstract'])
#         act_count = len(res)
#         self.assertTrue(act_count > 38000)
#         self.assertTrue(act_count < count)
#         res = document.filter(abstract__icontains="activators")
#         self.assertTrue('activators' in res[0]['abstract'])
#         act_count_1 = len(res)
#         self.assertTrue(act_count_1 < act_count)
#         self.assertTrue(act_count_1 > 300)


#
#
#     def test_molecule_search(self):
#         molecule = new_client.molecule
#         molecule.set_format('json')
#         res = molecule.search('aspirin')
#         self.assertEqual(len(res), 44)
#         self.assertEqual(res[0]['molecule_chembl_id'], 'CHEMBL25')
#         self.assertEqual(res[0]['pref_name'], 'ASPIRIN')
#         self.assertEqual(res[1]['molecule_chembl_id'], 'CHEMBL2260549')
#         self.assertEqual(res[1]['pref_name'], 'ASPIRIN EUGENOL ESTER')
#         typo = molecule.search('Caffeicæacidæphenethylester')
#         self.assertEqual(len(typo), 0)
#         typo1 = molecule.search('3,5-dihydroxy-4Í-ethyl-trans-stilbene')
#         self.assertEqual(len(typo1), 0)

#
#
#     def test_protein_class_search(self):
#         protein_class = new_client.protein_class
#         protein_class.set_format('json')
#         reader = protein_class.search('reader')
#         self.assertEqual(len(reader), 10, len(reader))
#         self.assertEqual(reader[0]['l2'], 'Reader', reader)
#         self.assertEqual(reader[0]['l1'], 'Epigenetic regulator', reader[0]['l1'])
#         bromodomain = protein_class.search('bromodomain')
#         self.assertEqual(len(bromodomain), 1, len(bromodomain))
#         self.assertEqual(bromodomain[0]['l3'], 'Bromodomain', bromodomain[0]['l3'])
#         self.assertEqual(bromodomain[0]['l2'], 'Reader', bromodomain[0]['l2'])
#         self.assertEqual(bromodomain[0]['l1'], 'Epigenetic regulator', bromodomain[0]['l1'])

#
#     def test_target_search(self):
#         target = new_client.target
#         target.set_format('json')
#         res = target.search('lipoxygenase')
#         self.assertEqual(len(res), 23)
#         self.assertEqual(res[0]['pref_name'], 'Lipoxygenase')
#         bromodomains = target.search('BRD4')
#         self.assertTrue(len(bromodomains) >= 2)
#         self.assertTrue('Bromodomain' in bromodomains[0]['pref_name'])
#         alz = target.search('"Alzheimer"')
#         self.assertTrue(len(alz) >= 3)
#


#
#     def test_chembl_id_lookup_search(self):
#         chembl_id_lookup = new_client.chembl_id_lookup
#         chembl_id_lookup.set_format('json')
#         res = chembl_id_lookup.search('morphine')
#         self.assertTrue(800 < len(res) < 1200, 'len(res) is actually {0}'.format(len(res)))
#         by_score = sorted([x for x in res], key=lambda x: x['score'], reverse=True)
#         self.assertEqual(by_score[0]['chembl_id'], 'CHEMBL70')
#         self.assertEqual(by_score[0]['entity_type'], 'COMPOUND')


#     def test_assay_search(self):
#         assay = new_client.assay
#         assay.set_format('json')
#         count = len(assay.all())
#         res = assay.search('inhibitor')
#         self.assertTrue(len(res) > 6000)
#         self.assertTrue(len(res) < count)
#         self.assertTrue('inhibitor' in res[0]['description'])
#         res = assay.search('inhibitor').filter(assay_type='A')
#         self.assertTrue('inhibitor' in res[0]['description'])
#         self.assertEqual(res[0]['assay_type'], 'A')
#         self.assertTrue(1000 < len(res) < 1300, len(res))