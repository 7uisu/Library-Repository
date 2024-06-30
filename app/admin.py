from django.contrib import admin
from .models import Genre, Publisher, Imprint, Author, PenName, Language, Edition, Book, Ebook, Audiobook

admin.site.register(Genre)
admin.site.register(Publisher)
admin.site.register(Imprint)
admin.site.register(Author)
admin.site.register(PenName)
admin.site.register(Language)
admin.site.register(Edition)
admin.site.register(Book)
admin.site.register(Ebook)
admin.site.register(Audiobook)
