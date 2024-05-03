from django.test import TestCase
from ..models import Book, ReadingList, BookReadingList
from users.models import User


class ModelTestCase(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='test_user', password='password123')

        # Create books
        self.book1 = Book.objects.create(user=self.user, title='Book 1', authors='Author 1', genre='Genre 1', publication_date='2022-01-01', description='Description 1')
        self.book2 = Book.objects.create(user=self.user, title='Book 2', authors='Author 2', genre='Genre 2', publication_date='2022-02-01', description='Description 2')

        # Create a reading list
        self.reading_list = ReadingList.objects.create(user=self.user, name='Reading List 1')

        # Create book-reading list relationships
        self.book_reading_list1 = BookReadingList.objects.create(reading_list=self.reading_list, book=self.book1, order=1)
        self.book_reading_list2 = BookReadingList.objects.create(reading_list=self.reading_list, book=self.book2, order=2)

    def test_book_creation(self):
        # Test book creation
        self.assertEqual(self.book1.title, 'Book 1')
        self.assertEqual(self.book2.authors, 'Author 2')
        self.assertEqual(self.book1.genre, 'Genre 1')
        self.assertEqual(self.book2.publication_date, '2022-02-01')
        self.assertEqual(self.book1.description, 'Description 1')

    def test_reading_list_creation(self):
        # Test reading list creation
        self.assertEqual(self.reading_list.user, self.user)
        self.assertEqual(self.reading_list.name, 'Reading List 1')

    def test_book_reading_list_creation(self):
        # Test book-reading list relationship creation
        self.assertEqual(self.book_reading_list1.reading_list, self.reading_list)
        self.assertEqual(self.book_reading_list1.book, self.book1)
        self.assertEqual(self.book_reading_list1.order, 1)
        self.assertEqual(self.book_reading_list2.order, 2)
