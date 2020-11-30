import unittest
from textbook import Textbook

class TestTextbook(unittest.TestCase):

    def test_search_by_id(self):

        result = Textbook.search_by_id(1)

        self.assertIsNotNone(result)

    def test_search_by_book_name(self):
        
        book_name = 'Abnormal Psychology'
        result = Textbook.search_by_book_name(book_name)

        self.assertIsNone(result)

    def test_get_title(self):

        result = Textbook.get_title('True')
        self.assertIsNotNone(result)

        result = Textbook.get_title('False')
        self.assertIsNotNone(result)

    def test_search_by_course_name(self):

        course_name = 'Algorithms'

        result = Textbook.search_by_course_name(course_name)
        self.assertIsNotNone(result)

    def test_search_by_subject(self):

        subject = '(MATH-SHU)'

        result = Textbook.search_by_subject(subject)
        self.assertIsNotNone(result)

