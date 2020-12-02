#The test profile unit test is complete
import unittest
from addons.profile.models.profile import Profile

class TestProfile(unittest.TestCase):

    def test_add(self):

        """
        This function tests the profile insertion class method
        """

        #Define dummy data to test function
        dict = {'first_name': 'Bilal', 'last_name': 'Munawar', 'major': 'Computer Science', 
        'class_year': 'Senior', 'contact_information': 'bilalmunawar', 'avatar_id': 101, 'email': 'bm2515@nyu.edu'}

        result = Profile.add(dict)
        self.assertEqual(result, {"status": True, "message": "Update succeeds"})


    def test_get_profile_by_email(self):

        """
        This function tests get profile by email class method
        """

        user_email = 'bm2515@nyu.edu'
        #Check if a dummy data point insertion is needed
        result = Profile.get_profile_by_email(user_email)

        self.assertIsNotNone(result)