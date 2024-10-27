from django.contrib import admin
from .models import Book, Author, Genre, Publisher

admin.site.site_header = "Library Admin"
admin.site.site_title = "Library Admin Portal"
admin.site.index_title = "Welcome to the Library Admin"

# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'publication_date', 'checked_out', 'checked_out_by')
    search_fields = ('title', 'author')
    list_editable = ('checked_out', 'checked_out_by')

admin.site.register(Book, BookAdmin)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Publisher)