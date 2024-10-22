from django import forms

from .models import Author, Publisher, Book

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'email']

class PublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = ['name', 'city', 'country', 'website']
        widgets = {
            'website': forms.TextInput(attrs={'class': 'form-control'}),
        }

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'date', 'authors', 'publisher']
        widgets = {
            'date': forms.DateInput(format='%m/%d/%Y'),
            'authors': forms.CheckboxSelectMultiple,
        }

class BookSearchForm(forms.Form):
    query = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Search for books...'})
    )