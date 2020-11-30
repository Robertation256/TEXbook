import unittest
from common.models.image import Image

class TestImage(unittest.TestCase):

    @classmethod
    def InsertUser(cls):
        """
        Inserts a dummy user in the database to test class methods
        """
        cls.InsertUser(
            email = 'test123@nyu.edu',
            password = 'unittest123'
        )
        print('Inserts User')

    @classmethod
    def DeleteUser(cls):
        """
        Deletes the dummy user in the database after the class methods have been tested
        """
        cls.DeleteUser(
            email = 'test123@nyu.edu',
            password = 'unittest123'
        )
        print('Deletes User')


    def test_insertion(self):

        """
        This function tests image insertion
        """

        #Test Case: 1
        avatar_id = Image.add(
        user_email='test123@nyu.edu',
        content='In progress: Unit testing',
        type="avatar",
        image_id=None,
        image_format='jpg')

        print('Test running')
        self.assertTrue(isinstance(avatar_id, int))


    def test_get_image(self):

        """
        This function  tests get image class method
        """

        result = Image.get_image(
            image_id:None,
            user_email: str,
            type: str
    )




#Number 1 - Notification to all requested users!
#event handlers
#Contact information 