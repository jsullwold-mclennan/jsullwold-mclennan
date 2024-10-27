from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'publisher', 'publication_date', 'isbn', 'pages'] # '__all__'
        
        widgets = {
            'publication_date': forms.DateInput(attrs={'type': 'date'}),
        }