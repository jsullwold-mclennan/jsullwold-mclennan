from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # account urls
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),

    # general website urls
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('response_example/', views.status_code_example, name="status-code"),
    path('book_list/', views.book_list, name="book-list"),
    path('books/checkout/<int:book_id>/', views.checkout_book, name='checkout_book'),
    path('books/checkin/<int:book_id>/', views.checkin_book, name='checkin_book'),
    path('add_book/', views.add_book, name="add-book"),
]