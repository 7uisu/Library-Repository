from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Q
from .models import *
from .forms import *

def index(request):
    return render(request, 'pages/index.html')

def home_page(request):
    return render(request, 'pages/home.html')

def about_page(request):
    return render(request, 'pages/about.html')

def login_page(request):
    return render(request, 'pages/login.html')

def register_page(request):
    return render(request, 'pages/register.html')

def search(request):
    query = request.GET.get('q')
    if query:
        results = Book.objects.filter(title__icontains=query)  # or other fields to search
    else:
        results = Book.objects.all()

    return render(request, 'pages/browse.html', {'query': query, 'page_obj': results})

def admin_panel_page(request):
    authors = Author.objects.all()
    publishers = Publisher.objects.all()
    genres = Genre.objects.all()
    books = Book.objects.all()
    imprints = Imprint.objects.all()
    pen_names = PenName.objects.all()
    languages = Language.objects.all()
    editions = Edition.objects.all()
    ebooks = Ebook.objects.all()
    audiobooks = Audiobook.objects.all()

    context = {
        'authors': authors,
        'publishers': publishers,
        'genres': genres,
        'books': books,
        'imprints': imprints,
        'pen_names': pen_names,
        'languages': languages,
        'editions': editions,
        'ebooks': ebooks,
        'audiobooks': audiobooks,
        'total_authors': authors.count(),
        'total_publishers': publishers.count(),
        'total_genres': genres.count(),
        'total_books': books.count(),
        'total_imprints': imprints.count(),
        'total_pen_names': pen_names.count(),
        'total_languages': languages.count(),
        'total_editions': editions.count(),
        'total_ebooks': ebooks.count(),
        'total_audiobooks': audiobooks.count(),
    }

    return render(request, 'pages/admin_panel.html', context)


def author_profile(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    books = author.books.all()
    pen_names = author.pen_names.all()
    return render(request, 'pages/author_profile.html', {'author': author, 'books': books, 'pen_names': pen_names})

def author_add(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin-panel')  # Redirect to admin panel or a success page
    else:
        form = AuthorForm()
    return render(request, 'pages/author-crud/author_add.html', {'form': form})

# Author CRUD
def author_update(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    
    if request.method == 'POST':
        form = AuthorForm(request.POST, request.FILES, instance=author)
        if form.is_valid():
            author_instance = form.save(commit=False)
            
            if 'new_picture' in request.FILES:
                author_instance.picture = request.FILES['new_picture']
            
            author_instance.save()
            form.save_m2m()  # Save many-to-many relationships
            
            pen_names = form.cleaned_data.get('pen_names')
            author.pen_names.set(pen_names)
            
            return redirect('admin-panel')
    else:
        form = AuthorForm(instance=author)
    
    return render(request, 'pages/author-crud/author_update.html', {'form': form, 'author': author})

def author_delete(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    if request.method == 'POST':
        author.delete()
        return redirect('admin-panel')
    return render(request, 'pages/author-crud/author_delete.html', {'author': author})

# Pen Name Search Functionality in the Admin-Panel for the Author
def pen_name_autocomplete(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        query = request.GET.get('q')
        pen_names = PenName.objects.filter(pen_name__icontains=query)
        results = [{"id": pen_name.id, "text": pen_name.pen_name} for pen_name in pen_names]
        return JsonResponse({"results": results})
    return JsonResponse({"results": []})



# Publisher CRUD
def publisher_list(request):
    publishers = Publisher.objects.all()
    return render(request, 'pages/publisher-crud/publisher_list.html', {'publishers': publishers})

def publisher_add(request):
    if request.method == 'POST':
        form = PublisherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin-panel')
    else:
        form = PublisherForm()
    return render(request, 'pages/publisher-crud/publisher_add.html', {'form': form})



def publisher_update(request, publisher_id):
    publisher = get_object_or_404(Publisher, id=publisher_id)
    if request.method == 'POST':
        form = PublisherForm(request.POST, request.FILES, instance=publisher)
        if form.is_valid():
            form.save()
            return redirect('admin-panel')
    else:
        form = PublisherForm(instance=publisher)
    return render(request, 'pages/publisher-crud/publisher_update.html', {'form': form, 'publisher': publisher})




def publisher_delete(request, publisher_id):
    publisher = get_object_or_404(Publisher, id=publisher_id)
    if request.method == 'POST':
        publisher.delete()
        return redirect('admin-panel')
    return render(request, 'pages/publisher-crud/publisher_delete.html', {'publisher': publisher})

def imprint_detail(request, imprint_id):
    imprint = get_object_or_404(Imprint, id=imprint_id)
    return render(request, 'pages/imprint_detail.html', {'imprint': imprint})

def imprint_add(request):
    if request.method == 'POST':
        form = ImprintForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin-panel')
    else:
        form = ImprintForm()
    return render(request, 'pages/imprint-crud/imprint_add.html', {'form': form})

def imprint_update(request, imprint_id):
    imprint = get_object_or_404(Imprint, id=imprint_id)
    if request.method == 'POST':
        form = ImprintForm(request.POST, request.FILES, instance=imprint)
        if form.is_valid():
            form.save()
            return redirect('admin-panel')
    else:
        form = ImprintForm(instance=imprint)
    return render(request, 'pages/imprint-crud/imprint_update.html', {'form': form, 'imprint': imprint})

def imprint_delete(request, imprint_id):
    imprint = get_object_or_404(Imprint, id=imprint_id)
    if request.method == 'POST':
        imprint.delete()
        return redirect('admin-panel')
    return render(request, 'pages/imprint-crud/imprint_delete.html', {'imprint': imprint})

# Genre CRUD
def genre_list(request):
    genres = Genre.objects.all()
    return render(request, 'pages/genre-crud/genre_list.html', {'genres': genres})

def genre_add(request):
    if request.method == 'POST':
        form = GenreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('genre_list')
    else:
        form = GenreForm()
    return render(request, 'pages/genre-crud/genre_add.html', {'form': form})

def genre_update(request, genre_id):
    genre = get_object_or_404(Genre, id=genre_id)
    if request.method == 'POST':
        form = GenreForm(request.POST, instance=genre)
        if form.is_valid():
            form.save()
            return redirect('genre_list')
    else:
        form = GenreForm(instance=genre)
    return render(request, 'pages/genre-crud/genre_update.html', {'form': form})

def genre_delete(request, genre_id):
    genre = get_object_or_404(Genre, id=genre_id)
    if request.method == 'POST':
        genre.delete()
        return redirect('admin-panel')
    return render(request, 'pages/genre-crud/genre_delete.html', {'genre': genre})

# Books CRUD
def book_list(request):
    books = Book.objects.all()
    return render(request, 'pages/book-crud/book_list.html', {'books': books})

def book_add(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'pages/book-crud/book_add.html', {'form': form})

def book_update(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('admin-panel')
    else:
        form = BookForm(instance=book)
    return render(request, 'pages/book-crud/book_update.html', {'form': form})

def book_delete(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('admin-panel')
    return render(request, 'pages/book-crud/book_delete.html', {'book': book})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Edition
from .forms import EditionForm

# Edition CRUD
def edition_add(request):
    if request.method == 'POST':
        form = EditionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin-panel')  # Redirect to the edition list or another appropriate page
    else:
        form = EditionForm()
    return render(request, 'pages/edition-crud/edition_add.html', {'form': form})

def edition_update(request, edition_id):
    edition = get_object_or_404(Edition, id=edition_id)
    if request.method == 'POST':
        form = EditionForm(request.POST, instance=edition)
        if form.is_valid():
            form.save()
            return redirect('admin-panelt')  # Redirect to the edition list or another appropriate page
    else:
        form = EditionForm(instance=edition)
    return render(request, 'pages/edition-crud/edition_update.html', {'form': form})

def edition_delete(request, edition_id):
    edition = get_object_or_404(Edition, id=edition_id)
    if request.method == 'POST':
        edition.delete()
        return redirect('admin-panel')  # Redirect to the edition list or another appropriate page
    return render(request, 'pages/edition-crud/edition_delete.html', {'edition': edition})

# Language CRUD
def language_add(request):
    if request.method == 'POST':
        form = LanguageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin-panel')
    else:
        form = LanguageForm()
    return render(request, 'pages/language-crud/language_add.html', {'form': form})

def language_update(request, language_id):
    language = get_object_or_404(Language, id=language_id)
    if request.method == 'POST':
        form = LanguageForm(request.POST, instance=language)
        if form.is_valid():
            form.save()
            return redirect('admin-panel')
    else:
        form = LanguageForm(instance=language)
    return render(request, 'pages/language-crud/language_update.html', {'form': form})

def language_delete(request, language_id):
    language = get_object_or_404(Language, id=language_id)
    if request.method == 'POST':
        language.delete()
        return redirect('admin-panel')
    return render(request, 'pages/language-crud/language_delete.html', {'language': language})


def browse_books(request):
    query = request.GET.get('q')
    if query:
        book_list = Book.objects.filter(title__icontains=query)
    else:
        book_list = Book.objects.all()
    paginator = Paginator(book_list, 20)  # Show 20 books per page.
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'pages/browse_books.html', {'page_obj': page_obj})

def book_profile(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    ebook = book.ebook if hasattr(book, 'ebook') else None
    audiobook = book.audiobook if hasattr(book, 'audiobook') else None
    return render(request, 'pages/book_profile.html', {'book': book, 'ebook': ebook, 'audiobook': audiobook})



def browse(request):
    query = request.GET.get('q')
    if query:
        book_results = Book.objects.filter(Q(title__icontains=query) | Q(authors__first_name__icontains=query) | Q(authors__last_name__icontains=query)).distinct()
    else:
        book_results = Book.objects.all()

    paginator = Paginator(book_results, 20)  # Show 20 books per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'pages/browse.html', {'page_obj': page_obj, 'query': query})

def search(request):
    query = request.GET.get('q')
    if query:
        book_results = Book.objects.filter(Q(title__icontains=query) | Q(authors__first_name__icontains=query) | Q(authors__last_name__icontains=query)).distinct()
    else:
        book_results = Book.objects.all()

    paginator = Paginator(book_results, 20)  # Show 20 books per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'pages/browse.html', {'page_obj': page_obj, 'query': query})
