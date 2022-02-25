import unittest

# from unittest import mock

from app import get_doc_owner_name, remove_doc_from_shelf, add_new_doc


class TestApp(unittest.TestCase):

    def test_get_doc_owner_name(self):
        mock_user_doc_number = '10006'
        result = get_doc_owner_name(mock_user_doc_number)
        self.assertEqual(result, 'Аристарх Павлов')

    def test_remove_doc_from_shelf(self):
        pass

    def test_add_new_doc(self):
        pass


if __name__ == '__main__':
    unittest.main()
