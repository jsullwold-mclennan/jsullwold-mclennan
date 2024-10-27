from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

# Create your models here.
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Genre(models.Model):
    GENRE_CHOICES = [
        ('Fiction', 'Fiction'),
        ('Non-fiction', 'Non-fiction'),
        ('Mystery', 'Mystery'),
        ('Sci-Fi', 'Sci-Fi'),
        ('Fantasy', 'Fantasy'),
        ('Romance', 'Romance'),
        ('Horror', 'Horror'),
        ('Biography', 'Biography'),
        ('History', 'History'),
        ('Self-Help', 'Self-Help'),
        ('Children', 'Children'),
    ]

    name = models.CharField(max_length=100, choices=GENRE_CHOICES)

    def __str__(self):
        return self.name
    
class Publisher(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name

class BookManager(models.Manager):
    def checked_out(self):
        return self.filter(checked_out=True)

    def available(self):
        return self.filter(checked_out=False)

class Book(models.Model):
    title = models.CharField(max_length=200)
    # author = models.CharField(max_length=100) # this field is now replaced with the ForeignKey field
    # genre = models.CharField(max_length=100) # this field is now replaced with the ManyToManyField field
    # publisher = models.CharField(max_length=200, blank=True, null=True) # this field is now replaced with the ForeignKey field
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    genre = models.ManyToManyField(Genre, related_name='books')
    publisher = models.ForeignKey(Publisher, null=True, blank=True, on_delete=models.SET_NULL)
    publication_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
    pages = models.PositiveIntegerField()
    checked_out = models.BooleanField(default=False)
    checked_out_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    objects = BookManager()

    def __str__(self):
        return self.title
    
    def check_in(self):
        self.checked_out = False
        self.checked_out_by = None
        self.save()

    class Meta:
        ordering = ['title']

    def clean(self):
        if len(self.isbn) not in [10, 13]:
            raise ValidationError('ISBN must be 10 or 13 characters long.')

        if self.publication_date > timezone.now().date():
            raise ValidationError('Publication date cannot be in the future.')

        if self.checked_out and self.checked_out_by:
            raise ValidationError('This book is already checked out.')

    def save(self, *args, **kwargs):
        # Call the clean method before saving
        self.clean()
        super().save(*args, **kwargs)