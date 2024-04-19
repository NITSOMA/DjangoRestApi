from rest_framework import serializers
from .models import Book, AppraisalRequest


class BookSerializer(serializers.ModelSerializer):
    evaluation = serializers.SerializerMethodField(method_name='evaluate')
    higher_rated_books = serializers.SerializerMethodField(method_name='higher')

    class Meta:
        model = Book
        fields = ('title', 'author', 'rating', 'total_voters', 'book_id', 'evaluation', 'higher_rated_books')

    @staticmethod
    def evaluate(book):
        if book.rating >= 4:
            return "Reader's favourite (POSITIVE)"
        elif 4 > book.rating >= 3:
            return "Reader's seem to like it (NEUTRAL)"
        else:
            return "Not reader's favourite (NEGATIVE)"

    @staticmethod
    def higher(book):
        higher_rated = []
        books = Book.objects.filter(rating__gt=book.rating)
        for i in books:
            higher_rated.append(f'{i.title} - http://127.0.0.1:8000/api/books/{i.book_id}')
        if len(higher_rated) == 0:
            return 'Highest Rated BOOk'
        return higher_rated


class AppraisalRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppraisalRequest
        fields = ('url', 'status', 'requested_info')
