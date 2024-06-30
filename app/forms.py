from django.core.files.storage import default_storage
from django_select2.forms import ModelSelect2MultipleWidget
from django import forms
from .models import *

class AuthorForm(forms.ModelForm):
    pen_names = forms.ModelMultipleChoiceField(
        queryset=PenName.objects.all(),
        widget=ModelSelect2MultipleWidget(
            model=PenName,
            search_fields=['name__icontains'],
            attrs={'data-placeholder': 'Search Pen Names', 'style': 'width: 100%;'}
        ),
        required=False
    )
    new_picture = forms.ImageField(label='Choose New Profile Picture', required=False)
    clear_picture = forms.BooleanField(label='Clear Current Picture', required=False)
    date_of_birth = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d'), input_formats=['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y', '%Y/%m/%d'])

    class Meta:
        model = Author
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['pen_names'].initial = self.instance.pen_names.all()

    def clean(self):
        cleaned_data = super().clean()
        new_picture = cleaned_data.get('new_picture')
        clear_picture = cleaned_data.get('clear_picture')

        if new_picture and clear_picture:
            raise forms.ValidationError("Cannot choose both 'New Profile Picture' and 'Clear Current Picture'. Choose one.")

        return cleaned_data

    def save(self, commit=True):
        author = super().save(commit=False)

        if self.cleaned_data.get('clear_picture'):
            # Delete the previous profile picture if clear_picture is checked
            if author.picture:
                default_storage.delete(author.picture.name)
            author.picture = None
        else:
            # If clear_picture is not checked, update the picture only if a new one is provided
            new_picture = self.cleaned_data.get('new_picture')
            if new_picture:
                # If a new picture is provided, delete the old one if it exists
                if author.picture:
                    default_storage.delete(author.picture.name)
                author.picture = new_picture
        
        if commit:
            author.save()
            self.save_m2m()  # Save many-to-many relationships

        return author
    
class ImprintForm(forms.ModelForm):
    class Meta:
        model = Imprint
        fields = '__all__'

class EditionForm(forms.ModelForm):
    class Meta:
        model = Edition
        fields = ['name']
    

class PublisherForm(forms.ModelForm):
    clear_logo = forms.BooleanField(required=False, label="Clear current logo")

    class Meta:
        model = Publisher
        fields = ['name', 'country', 'contact_email', 'contact_phone', 'address', 'website', 'description', 'founding_date', 'status', 'logo', 'clear_logo']

    def save(self, commit=True):
        publisher = super().save(commit=False)
        
        # Handle logo updates
        new_logo = self.cleaned_data.get('logo')
        if self.cleaned_data.get('clear_logo') and publisher.logo:
            publisher.logo.delete(save=False)
            publisher.logo = None
        elif new_logo:
            publisher.logo = new_logo
        
        if commit:
            publisher.save()
        
        return publisher



class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = '__all__'

class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ['name']


class BookForm(forms.ModelForm):
    ebook_file = forms.FileField(required=False, label="Ebook File")
    audiobook_file = forms.FileField(required=False, label="Audiobook File")
    audiobook_duration = forms.DurationField(required=False, label="Audiobook Duration")
    book_cover_image = forms.ImageField(required=False, label="Book Cover Image")
    series_cover_image = forms.ImageField(required=False, label="Series Cover Image")
    clear_book_cover_image = forms.BooleanField(required=False, label="Clear current book cover image")
    clear_series_cover_image = forms.BooleanField(required=False, label="Clear current series cover image")

    class Meta:
        model = Book
        fields = [
            'title', 'series', 'publication_date', 'volume', 'isbn', 'description', 
            'edition', 'language', 'collaborating_publishers', 'authors', 'genres', 
            'book_cover_image', 'series_cover_image', 'clear_book_cover_image', 'clear_series_cover_image'
        ]
    
    def save(self, commit=True):
        book = super().save(commit=False)
        
        if commit:
            book.save()
            self.save_m2m()
            
            ebook_file = self.cleaned_data.get('ebook_file')
            audiobook_file = self.cleaned_data.get('audiobook_file')
            audiobook_duration = self.cleaned_data.get('audiobook_duration')
            book_cover_image = self.cleaned_data.get('book_cover_image')
            series_cover_image = self.cleaned_data.get('series_cover_image')

            # Handling ebook file
            if ebook_file:
                ebook, created = Ebook.objects.get_or_create(book=book)
                ebook.ebook_file = ebook_file
                ebook.save()
            
            # Handling audiobook file and duration
            if audiobook_file:
                audiobook, created = Audiobook.objects.get_or_create(book=book)
                audiobook.audiobook_file = audiobook_file
                audiobook.duration = audiobook_duration
                audiobook.save()

            # Handling book cover image
            if self.cleaned_data.get('clear_book_cover_image'):
                book.book_cover_image.delete(save=False)
                book.book_cover_image = None
            elif book_cover_image:
                book.book_cover_image = book_cover_image
            
            # Handling series cover image
            if self.cleaned_data.get('clear_series_cover_image'):
                book.series_cover_image.delete(save=False)
                book.series_cover_image = None
            elif series_cover_image:
                book.series_cover_image = series_cover_image

            book.save()  # Save the book to store the image changes
        
        return book
