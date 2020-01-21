from chembl_webservices.tests import BaseWebServiceTestCase


class GeneralTestCase(BaseWebServiceTestCase):

    def test_status(self):
        status_res = self.request_url(self.WS_URL + '/status.json')
        message = 'Invalid status response!'
        self.assertEqual(status_res['activities'], 15996368, message)
        self.assertEqual(status_res['chembl_db_version'], 'ChEMBL_26', message)
        self.assertEqual(status_res['chembl_release_date'], '2020-01-10T00:00:00', message)
        self.assertEqual(status_res['compound_records'], 2425876, message)
        self.assertEqual(status_res['disinct_compounds'], 1950765, message)
        self.assertEqual(status_res['publications'], 76076, message)
        self.assertEqual(status_res['status'], 'UP', message)
        self.assertEqual(status_res['targets'], 13377, message)
