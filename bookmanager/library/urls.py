from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from django.views.generic.base import TemplateView

from . import views
from . import viewsets

router = DefaultRouter()
router.register(r'books', viewsets.BookViewSet, basename='book')

urlpatterns = [
    # Account URLs
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),

    # General Website URLs
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('response_example/', views.status_code_example, name="status-code"),

    # Books URLs
    path('book_list/', views.book_list, name='list-books'),
    path('books/checkout/<int:book_id>/', views.checkout_book, name='checkout_book'),
    path('books/checkin/<int:book_id>/', views.checkin_book, name='checkin_book'),
    path('add_book/', views.add_book, name="add-book"),

     path('book_list_api/', views.api_book_list, name='api-list-books'),

    # DRF API Related URL
    path('api/', include(router.urls)),
]
