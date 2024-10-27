from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from .models import *
from .forms import BookForm

# Create your views here.
def home(request):
    # return HttpResponse("Welcome to the Book Management App!")
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def status_code_example(request):
    print(f"Received a request to: {request.path}")
    print(f"Response status code is: 200 OK")

    # return HttpResponse(status=200)
    # return HttpResponseRedirect(reverse('home'))
    return redirect('home')

@login_required
def book_list(request):
    available_books = Book.objects.exclude(checked_out=True)
    checked_out_books = Book.objects.filter(checked_out=True, checked_out_by=request.user)
    unavailable_books = Book.objects.filter(checked_out=True).exclude(checked_out_by=request.user)

    context = {
        'available_books': available_books,
        'checked_out_books': checked_out_books,
        'unavailable_books': unavailable_books
    }

    return render(request, 'book_list.html', context)

@login_required
def add_book(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to add books.")
    
    if request.method == 'POST':
        form = BookForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('book-list')
    else:
        form = BookForm()

    return render(request, 'add_book.html', {'form': form})

@login_required
def checkout_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if not book.checked_out:
        book.checked_out = True
        book.checked_out_by = request.user
        book.save()
    return redirect('book-list')

@login_required
def checkin_book(request, book_id):
    book = get_object_or_404(Book, id=book_id, checked_out_by=request.user)
    book.check_in()
    
    return redirect('book-list')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('book-list')
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})
