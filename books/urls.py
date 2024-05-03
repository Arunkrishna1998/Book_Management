from django.urls import path
from .views import AddBookView, RetrieveBooks, ReadingListAPI, ReadingListManageAPI, RetrieveReadingList


urlpatterns = [
    path('add-book/', AddBookView.as_view(), name="add-book"),
    path('retrieve-books/', RetrieveBooks.as_view(), name="retrieve-books"),

    path('readinglist/', ReadingListAPI.as_view(), name="readinglist"),
    path('readinglist/<int:pk>/', ReadingListAPI.as_view(), name="readinglist"),

    path('createreadinglist/<int:pk>/', ReadingListManageAPI.as_view(), name="createreadinglist"),
    path('retrievereadinglist/<int:pk>/', RetrieveReadingList.as_view(), name="retrievereadinglist"),

   
]
