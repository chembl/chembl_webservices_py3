from chembl_webservices.tests import BaseWebServiceTestCase


class GeneralTestCase(BaseWebServiceTestCase):

    def test_status(self):
        status_res = self.request_url(self.WS_URL + '/status.json')
        message = 'Invalid status response!'
        self.assertEqual(status_res['activities'], 15504603, message)
        self.assertEqual(status_res['api_version'], '2.7.9b0', message)
        self.assertEqual(status_res['chembl_db_version'], 'ChEMBL_25', message)
        self.assertEqual(status_res['chembl_release_date'], '2018-12-10', message)
        self.assertEqual(status_res['compound_records'], 2335417, message)
        self.assertEqual(status_res['disinct_compounds'], 1879206, message)
        self.assertEqual(status_res['publications'], 72271, message)
        self.assertEqual(status_res['status'], 'UP', message)
        self.assertEqual(status_res['targets'], 12482, message)
