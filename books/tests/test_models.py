from django.test import TestCase
from books.models import Book

class BookModelTest(TestCase):

    def test_get_book_name_method(self):
        """
        Method must return book name
        """
        book = Book.objects.create(name="River Between", pages=200)
        self.assertEqual(book.get_book_name(), "River Between")

    def test_book_string_magic_method(self):
        """
        Method must return book string representation
        """
        book = Book.objects.create(name="River Between", pages=200)
        self.assertEqual(str(book), "River Between")


