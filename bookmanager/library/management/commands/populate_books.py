import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from faker import Faker
from library.models import Book, Author, Genre, Publisher
from django.contrib.auth.models import User  # For checked_out_by field

class Command(BaseCommand):
    help = 'Populate the database with random books, authors, genres, and publishers'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Step 1: Create some sample genres
        genre_names = [
            'Fiction', 'Non-fiction', 'Mystery', 'Sci-Fi', 'Fantasy', 'Romance', 'Horror', 
            'Biography', 'History', 'Self-Help', 'Children'
        ]
        genres = []
        for genre_name in genre_names:
            genre, created = Genre.objects.get_or_create(name=genre_name)
            genres.append(genre)

        # Step 2: Create some sample publishers
        publisher_names = ['Penguin Random House', 'HarperCollins', 'Simon & Schuster', 'Hachette Livre', 'Macmillan']
        publishers = []
        for publisher_name in publisher_names:
            publisher, created = Publisher.objects.get_or_create(name=publisher_name, address=fake.address())
            publishers.append(publisher)

        # Step 3: Create some sample authors
        authors = []
        for _ in range(10):  # Create 10 authors
            first_name = fake.first_name()
            last_name = fake.last_name()
            birth_date = fake.date_of_birth(tzinfo=None, minimum_age=20, maximum_age=80)
            author, created = Author.objects.get_or_create(
                first_name=first_name,
                last_name=last_name,
                birth_date=birth_date
            )
            authors.append(author)

        users = list(User.objects.all())  # Fetch all users in the system
        if not users:
            self.stdout.write(self.style.WARNING('No users found. Please create some users before running this command.'))
            return

        # Step 4: Create sample books
        def random_date():
            start_date = date(1900, 1, 1)
            end_date = date.today()
            return start_date + timedelta(days=random.randint(0, (end_date - start_date).days))

        for _ in range(25):  # Generate 25 books
            isbn_13 = fake.isbn13()
            cleaned_isbn = ''.join(filter(str.isdigit, isbn_13))  # Remove any non-digit characters

            book = Book(
                title=fake.catch_phrase(),
                author=random.choice(authors),
                publisher=random.choice(publishers),
                publication_date=random_date(),
                isbn=cleaned_isbn,
                pages=random.randint(100, 1000),
                checked_out=bool(random.getrandbits(1)),  # Randomly mark some books as checked out
            )

            # Randomly assign a user if the book is checked out
            if book.checked_out:
                book.checked_out_by = random.choice(users)

            book.save()  # Save the book instance first before adding M2M fields

            # Add genres (assigning up to 3 random genres per book)
            selected_genres = random.sample(genres, k=random.randint(1, 3))
            book.genre.set(selected_genres)

        self.stdout.write(self.style.SUCCESS('25 books, authors, genres, and publishers added successfully!'))
