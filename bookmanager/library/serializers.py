from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'publication_date', 'publisher', 'pages', 'checked_out', 'checked_out_by', 'genre']
        depth = 1  # To include related fields like `author` and `genre`
