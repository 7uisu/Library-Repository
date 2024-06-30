from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.home_page, name='home'),
    path('about/', views.about_page, name='about'),
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('search/', views.search, name='search'),
    path('browse/', views.browse, name='browse'),

    
    path('admin-panel/', views.admin_panel_page, name='admin-panel'),
    
    
    # Author CRUD
    path('author/<int:author_id>/', views.author_profile, name='author-profile'),
    path('authors/add/', views.author_add, name='author-add'),
    path('authors/update/<int:author_id>/', views.author_update, name='author-update'),
    path('authors/delete/<int:author_id>/', views.author_delete, name='author-delete'),
    # path('authors/delete/<int:author_id>/', views.author_delete, name='author_delete'),

    # URL for autocomplete functionality for Pen name in Author CRUD
    path('pen-name-autocomplete/', views.pen_name_autocomplete, name='pen-name-autocomplete'),

    # Publisher CRUD
    path('publishers/', views.publisher_list, name='publisher-list'),
    path('publishers/add/', views.publisher_add, name='publisher-add'),
    path('publishers/update/<int:publisher_id>/', views.publisher_update, name='publisher-update'),
    path('publishers/delete/<int:publisher_id>/', views.publisher_delete, name='publisher-delete'),

    # Genre CRUD
    path('genres/', views.genre_list, name='genre-list'),
    path('genres/add/', views.genre_add, name='genre-add'),
    path('genres/update/<int:genre_id>/', views.genre_update, name='genre-update'),
    path('genres/delete/<int:genre_id>/', views.genre_delete, name='genre-delete'),

    # Book CRUD
    path('books/', views.book_list, name='book-list'),
    path('book/<int:book_id>/', views.book_profile, name='book-profile'),
    path('books/add/', views.book_add, name='book-add'),
    path('books/update/<int:book_id>/', views.book_update, name='book-update'),
    path('books/delete/<int:book_id>/', views.book_delete, name='book-delete'),

    # Edition CRUD
    path('editions/add/', views.edition_add, name='edition-add'),
    path('editions/update/<int:edition_id>/', views.edition_update, name='edition-update'),
    path('editions/delete/<int:edition_id>/', views.edition_delete, name='edition-delete'),

    # Imprint CRUD
    path('imprints/add/', views.imprint_add, name='imprint-add'),
    path('imprints/update/<int:imprint_id>/', views.imprint_update, name='imprint-update'),
    path('imprints/delete/<int:imprint_id>/', views.imprint_delete, name='imprint-delete'),

    # Language CRUD
    path('languages/add/', views.language_add, name='language-add'),
    path('languages/update/<int:language_id>/', views.language_update, name='language-update'),
    path('languages/delete/<int:language_id>/', views.language_delete, name='language-delete'),
]
