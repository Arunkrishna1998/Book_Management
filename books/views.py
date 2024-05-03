from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializers import (BookSerializer, BookRetrieveSerializer, ReadingListSerializer,
                           UserSerializer, BookReadingListSerializer, BookReadingListViewSerializer)
from .models import Book, ReadingList, BookReadingList
from django.shortcuts import get_object_or_404


class AddBookView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        serializer = BookSerializer(data=data, context={'request': request}) 
        if serializer.is_valid():
            serializer.save()  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class RetrieveBooks(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookRetrieveSerializer



class ReadingListAPI(APIView):
    permission_classes = [IsAuthenticated]

    #Add New Reading List
    def post(self, request):
        data = request.data
        serializer = ReadingListSerializer(data=data, context={'request': request}) 
        if serializer.is_valid():
            serializer.save()  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    #Get all the Reading List of Authenticated User
    def get(self, request):
        user = request.user 
        reading_lists = ReadingList.objects.filter(user=user)  
        serializer = ReadingListSerializer(reading_lists, many=True)  
        response_data = {'reading_lists': serializer.data}
        return Response(response_data, status=status.HTTP_200_OK)
    

    #Update Reading List
    def put(self, request, pk):
            user = request.user
            try:
                reading_list = ReadingList.objects.get(pk=pk, user=user)
            except ReadingList.DoesNotExist:
                return Response({"error": "Reading list does not exist."}, status=status.HTTP_404_NOT_FOUND)
            
            data = request.data
            serializer = ReadingListSerializer(instance=reading_list, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    #Delete Reading List
    def delete(self, request, pk):
        user = request.user
        try:
            reading_list = ReadingList.objects.get(pk=pk, user=user)
        except ReadingList.DoesNotExist:
            return Response({"error": "Reading list does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        reading_list.delete()
        return Response({"message": "Reading list deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    


class ReadingListManageAPI(APIView):
    """
    This API is used to Add, Update, Remove Books from Reading List
    """
    permission_classes = [IsAuthenticated]
    def add_book_to_reading_list(self, reading_list, book, order):
        """
        Add a book to a reading list.
        """
        try:
            # Check if the book is already in the reading list
            BookReadingList.objects.get(reading_list=reading_list, book=book)
            return Response({"message": "Book already exists in the reading list.", "action": "remove"}, status=status.HTTP_400_BAD_REQUEST)
        except BookReadingList.DoesNotExist:
            # Create a new entry in the BookReadingList model to add the book to the reading list
            book_reading_list = BookReadingList.objects.create(reading_list=reading_list, book=book, order=order)
            return Response({"message":"Book Added to Reading List"}, status=status.HTTP_201_CREATED)
        

    def remove_book_from_reading_list(self, reading_list, book):
        """
        Remove a book from a reading list.
        """
        try:
            # Check if the book exists in the reading list
            book_entry = BookReadingList.objects.get(reading_list=reading_list, book=book)
        except BookReadingList.DoesNotExist:
            return Response({"error": "Book does not exist in the reading list."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Delete the book entry from the reading list
        book_entry.delete()
        return Response({"message": "Book removed from the reading list successfully."}, status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk):
        # Patch method to add or remove a book from a reading list
        user = request.user
        try:
            # Retrieve the reading list object
            reading_list = get_object_or_404(ReadingList, pk=pk, user=user)
        except ReadingList.DoesNotExist:
            return Response({"error": "Reading list does not exist or you do not have permission to modify it."}, status=status.HTTP_404_NOT_FOUND)
        
        # Retrieve book_id and action from query parameters
        book_id = request.query_params.get('book_id')
        action = request.query_params.get('action')
        order = request.query_params.get('order')

        if order is None:
            order = 0

        if not (book_id and action):
            return Response({"error": "Book ID and action are required in the query parameters."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Retrieve the book object
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return Response({"error": "Book does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if the action is to add or remove the book from the reading list
        if action == "add":
            return self.add_book_to_reading_list(reading_list, book, order)
        elif action == "remove":
            return self.remove_book_from_reading_list(reading_list, book)
        else:
            return Response({"error": "Invalid action. Use 'add' or 'remove'."}, status=status.HTTP_400_BAD_REQUEST)
        


class RetrieveReadingList(APIView):
    permission_classes = [IsAuthenticated]

    def reading_list_exists(self, pk, user):
        try:
            # Check if the reading list exists and belongs to the user
            reading_list = get_object_or_404(ReadingList, pk=pk, user=user)
            return True
        except ReadingList.DoesNotExist:
            return False

    def get(self, request, pk):
        user = request.user
        if self.reading_list_exists(pk, user):
            # Retrieve the reading list
            reading_list = get_object_or_404(ReadingList, pk=pk)
            # Retrieve books associated with the reading list
            books = reading_list.book.all()
            # Serialize the books
            serializer = BookReadingListSerializer(books, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Reading list does not exist or does not belong to the current user."}, status=status.HTTP_404_NOT_FOUND)

