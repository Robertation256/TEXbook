#This test_listing unittest is complete
import unittest
from listing_service import ListingService

class TestListing(unittest.TestCase):

    def test_add(self):

        """
        This function tests the listing insertion class method
        """

        #dummy data points to test class method
        data = {'textbook_id' :101, 'purchase_option': 'rent',
        'offered_price': 500, 'condition': 'used', 'defect': 'loose binding'}
        user_id = 101

        result = ListingService.add(user_id, data)

        self.assertEqual(result, {"status":True,"msg":None})

    def test_get_listing_by_id(self):

        """
        This function tests the get listing by id class method
        """

        result = ListingService.get_listing_by_id(101)
        self.assertIsNotNone(result)

    



