from django.db import models
from isbn_field import ISBNField

class Genre(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"


class Publisher(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    contact_email = models.EmailField(max_length=20, null=True, blank=True)
    contact_phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(max_length=100, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    description = models.TextField(blank=True)
    founding_date = models.DateField(null=True, blank=True)
    date_added = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    logo = models.ImageField(upload_to='publisher_logos', null=True, blank=True)

    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('closed', 'Closed'),
        ('other', 'Other'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Publisher"
        verbose_name_plural = "Publishers"

class Imprint(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    founding_date = models.DateField(null=True, blank=True)
    logo = models.ImageField(upload_to='imprint_logos', null=True, blank=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, related_name='imprints')

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    social_media_twitter = models.URLField(null=True, blank=True)
    social_media_facebook = models.URLField(null=True, blank=True)
    social_media_linkedin = models.URLField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    mailing_address = models.TextField(null=True, blank=True)
    biography = models.TextField(null=True, blank=True)
    awards_recognitions = models.TextField(null=True, blank=True)
    
    current_publisher = models.ForeignKey(Publisher, related_name='current_authors', null=True, blank=True, on_delete=models.SET_NULL)
    past_publishers = models.ManyToManyField(Publisher, related_name='past_authors', blank=True)
    is_deceased = models.BooleanField(default=False)
    picture = models.ImageField(upload_to='author_pictures', null=True, blank=True)
    

    def __str__(self):
        if self.is_deceased:
            return f"{self.first_name} {self.last_name} (Deceased)"
        else:
            return f"{self.first_name} {self.last_name}"
        

class PenName(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='pen_names')
    pen_name = models.CharField(max_length=100)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return self.pen_name

    class Meta:
        verbose_name = "Pen Name"
        verbose_name_plural = "Pen Names"


class Language(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Language"
        verbose_name_plural = "Languages"

class Edition(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Edition"
        verbose_name_plural = "Editions"


class Book(models.Model):
    title = models.CharField(max_length=200)
    series = models.CharField(max_length=100, null=True, blank=True)
    publication_date = models.DateField()
    volume = models.IntegerField()
    isbn = ISBNField(clean_isbn=False)
    description = models.TextField(null=True, blank=True)
    edition = models.ForeignKey(Edition, on_delete=models.CASCADE, null=True, blank=True, related_name='books')
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='books')
    collaborating_publishers = models.ManyToManyField(Publisher, related_name='collaborating_books', blank=True)

    authors = models.ManyToManyField(Author, related_name='books')
    genres = models.ManyToManyField(Genre, related_name='books')
    book_cover_image = models.ImageField(upload_to='book_covers', null=True, blank=True)
    series_cover_image = models.ImageField(upload_to='series_covers', null=True, blank=True)

    def __str__(self):
        return self.title

    @property
    def has_collaboration(self):
        return self.collaborating_publishers.exists()

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"


class Ebook(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE, related_name='ebook')
    ebook_file = models.FileField(upload_to='ebooks/')

    class Meta:
        verbose_name = "Ebook"
        verbose_name_plural = "Ebooks"
        


class Audiobook(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE, related_name='audiobook')
    audiobook_file = models.FileField(upload_to='audiobooks/')
    duration = models.DurationField()

    class Meta:
        verbose_name = "Audiobook"
        verbose_name_plural = "Audiobooks"
                                
