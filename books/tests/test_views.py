from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Book, ReadingList
from .serializers import BookSerializer, ReadingListSerializer

class AddBookViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='password123')

    def test_add_book(self):
        self.client.force_authenticate(user=self.user)

        data = {
            'user': self.user.id,
            'title': 'Test Book',
            'authors': 'Test Author',
            'genre': 'Test Genre',
            'publication_date': '2022-01-01',
            'description': 'Test Description'
        }

        response = self.client.post(reverse('add-book'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(Book.objects.get().title, 'Test Book')

class RetrieveBooksTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='password123')
        self.book = Book.objects.create(
            user=self.user,
            title='Test Book',
            authors='Test Author',
            genre='Test Genre',
            publication_date='2022-01-01',
            description='Test Description'
        )

    def test_retrieve_books(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(reverse('retrieve-books'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Book')

class ReadingListAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='password123')
        self.reading_list = ReadingList.objects.create(user=self.user, name='Test Reading List')

    def test_add_reading_list(self):
        self.client.force_authenticate(user=self.user)

        data = {'user': self.user.id, 'name': 'New Reading List'}
        response = self.client.post(reverse('reading-list'), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ReadingList.objects.count(), 2)
        self.assertEqual(ReadingList.objects.last().name, 'New Reading List')

    def test_get_reading_lists(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(reverse('reading-list'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['reading_lists']), 1)
        self.assertEqual(response.data['reading_lists'][0]['name'], 'Test Reading List')

    def test_update_reading_list(self):
        self.client.force_authenticate(user=self.user)

        data = {'name': 'Updated Reading List'}
        response = self.client.put(reverse('reading-list-detail', kwargs={'pk': self.reading_list.id}), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ReadingList.objects.get(id=self.reading_list.id).name, 'Updated Reading List')

    def test_delete_reading_list(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(reverse('reading-list-detail', kwargs={'pk': self.reading_list.id}), format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ReadingList.objects.count(), 0)
