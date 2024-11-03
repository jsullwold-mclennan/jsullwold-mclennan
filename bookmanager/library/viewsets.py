from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Book
from .serializers import BookSerializer

class BookViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A ViewSet for viewing book information.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def checkout(self, request, pk=None):
        """
        Checkout a book to the current user.
        """
        book = self.get_object()
        
        if book.checked_out:
            return Response({"error": "Book is already checked out"}, status=400)
        
        book.checked_out = True
        book.checked_out_by = request.user
        book.save()
        
        serializer = self.get_serializer(book)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def checkin(self, request, pk=None):
        """
        Return a checked out book.
        """
        book = self.get_object()
        
        if not book.checked_out:
            return Response({"error": "Book is not checked out"}, status=400)
            
        if book.checked_out_by != request.user:
            return Response({"error": "Book was not checked out by you"}, status=403)
        
        book.check_in()  # Using the model's check_in method
        
        serializer = self.get_serializer(book)
        return Response(serializer.data)
