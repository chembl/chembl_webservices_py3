from chembl_webservices.tests import BaseWebServiceTestCase


class ImagesTestCase(BaseWebServiceTestCase):

    def test_compound_structural_alert(self):
        # TODO : PNG IS NOT WORKING
        # image_binary = self.get_resource_by_id('compound_structural_alert', 1, custom_format='png')
        # print(image_binary)
        # self.assertTrue(image_binary.startswith(b'\x89PNG\r\n'))
        # image_binary = self.get_resource_by_id('compound_structural_alert', 2, custom_format='png')
        # self.assertTrue(image_binary.startswith(b'\x89PNG\r\n'))
        image_binary = self.get_resource_by_id('compound_structural_alert', 1, custom_format='svg')
        self.assertTrue(image_binary.startswith("<?xml version='1.0' encoding='iso-8859-1'?>\n<svg:svg version='1.1'"))
        image_binary = self.get_resource_by_id('compound_structural_alert', 2, custom_format='svg')
        self.assertTrue(image_binary.startswith("<?xml version='1.0' encoding='iso-8859-1'?>\n<svg:svg version='1.1'"))

    def test_molecule(self):
        image_binary = self.get_resource_by_id('molecule', 'CHEMBL1', custom_format='png')
        self.assertTrue(image_binary.startswith(b'\x89PNG\r\n'))
        image_binary = self.get_resource_by_id('molecule', 'CHEMBL450200', custom_format='png')
        self.assertTrue(image_binary.startswith(b'\x89PNG\r\n'))

        image_binary = self.get_resource_by_id('molecule', 'CHEMBL1', custom_format='svg')
        self.assertTrue(image_binary.startswith("<?xml version='1.0' encoding='iso-8859-1'?>\n<svg:svg version='1.1'"))
        image_binary = self.get_resource_by_id('molecule', 'CHEMBL450200', custom_format='svg')
        self.assertTrue(image_binary.startswith("<?xml version='1.0' encoding='iso-8859-1'?>\n<svg:svg version='1.1'"))

    def test_image(self):
        image_binary = self.get_resource_by_id('image', 'CHEMBL1', custom_format='png')
        self.assertTrue(image_binary.startswith(b'\x89PNG\r\n'))
        image_binary = self.get_resource_by_id('image', 'CHEMBL450200', custom_format='png')
        self.assertTrue(image_binary.startswith(b'\x89PNG\r\n'))

        image_binary = self.get_resource_by_id('image', 'CHEMBL1', custom_format='svg')
        self.assertTrue(image_binary.startswith("<?xml version='1.0' encoding='iso-8859-1'?>\n<svg:svg version='1.1'"))
        image_binary = self.get_resource_by_id('image', 'CHEMBL450200', custom_format='svg')
        self.assertTrue(image_binary.startswith("<?xml version='1.0' encoding='iso-8859-1'?>\n<svg:svg version='1.1'"))
