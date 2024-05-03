from rest_framework import serializers
from .models import Book, ReadingList, BookReadingList
from django.contrib.auth import get_user_model


User = get_user_model()

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'authors', 'genre', 'publication_date', 'description']
    
    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return Book.objects.create(**validated_data)



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class BookRetrieveSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Book
        fields = ['title', 'authors', 'genre', 'publication_date', 'description', 'user']



class ReadingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingList
        fields = ['id', 'name']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return ReadingList.objects.create(**validated_data)
    


class BookReadingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingList
        fields = "__all__"



class BookReadingListViewSerializer(serializers.ModelSerializer):
    reading_list = ReadingListSerializer()
    book = BookSerializer()
    class Meta:
        model = ReadingList
        fields = ["reading_list", "book", "order"]
