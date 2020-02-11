from chembl_webservices.tests import BaseWebServiceTestCase


class ImagesTestCase(BaseWebServiceTestCase):

    def test_compound_structural_alert(self):
        self.get_resource_by_id('compound_structural_alert', 30843761, custom_format='png',
                                               expected_code=400)
        self.get_resource_by_id('compound_structural_alert', 32589079, custom_format='png',
                                               expected_code=400)

        image_binary = self.get_resource_by_id('compound_structural_alert', 30843761, custom_format='svg')
        print(image_binary)
        self.assertTrue(image_binary.startswith("<?xml version='1.0' encoding='iso-8859-1'?>\n<svg version='1.1'"))
        image_binary = self.get_resource_by_id('compound_structural_alert', 32589079, custom_format='svg')
        self.assertTrue(image_binary.startswith("<?xml version='1.0' encoding='iso-8859-1'?>\n<svg version='1.1'"))

    def test_molecule(self):
        self.get_resource_by_id('molecule', 'CHEMBL1', custom_format='png', expected_code=400)
        self.get_resource_by_id('molecule', 'CHEMBL450200', custom_format='png', expected_code=400)
        self.get_resource_by_id('molecule', 'CHEMBL1', custom_format='json', expected_code=400)
        self.get_resource_by_id('molecule', 'CHEMBL450200', custom_format='json', expected_code=400)

        image_binary = self.get_resource_by_id('molecule', 'CHEMBL1', custom_format='svg')
        self.assertTrue(image_binary.startswith("<?xml version='1.0' encoding='iso-8859-1'?>\n<svg:svg version='1.1'"))
        image_binary = self.get_resource_by_id('molecule', 'CHEMBL450200', custom_format='svg')
        self.assertTrue(image_binary.startswith("<?xml version='1.0' encoding='iso-8859-1'?>\n<svg:svg version='1.1'"))
