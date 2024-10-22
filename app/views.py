from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponse
from datetime import datetime

from .models import Book, Author, Publisher


# Create your views here.
def hello(request):
    return HttpResponse("Hello World!")

def home(request):
    tparams = {
        'title': 'Home Page',
        'year': datetime.now().year,
    }
    return render(request, 'index.html', tparams)


def contact(request):
    tparams = {
        'title': 'Contact',
        'message': 'Your contact page.',
        'year': datetime.now().year,
    }
    return render(request, 'contact.html', tparams)


def about(request):
    tparams = {
        'title': 'About',
        'message': 'Your application description page.',
        'year': datetime.now().year,
    }
    return render(request, 'about.html', tparams)

def books(request):
    all_books = Book.objects.all()

    tparams = {
        'title': 'Book library',
        'message': 'Welcome.',
        'year': datetime.now().year,
        'allTitles': all_books,
    }
    return render(request, 'books.html', tparams)


from django.shortcuts import get_object_or_404

def book_detail(request, book_id):
    # Tenta procurar pelo livro pelo ID ou retorna 404
    book = get_object_or_404(Book, pk=book_id)

    tparams = {
        'title': book.title,
        'book': book,
        'year': datetime.now().year,
    }

    return render(request, 'book_detail.html', tparams)

def authors(request):
    all_authors = Author.objects.all()

    tparams = {
        'title': 'Author library',
        'message': 'Welcome.',
        'year': datetime.now().year,
        'allTitles': all_authors,
    }
    return render(request, 'authors.html', tparams)

def author_detail(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    # Filtra os livros relacionados ao autor

    tparams = {
        'title': 'Author Details',
        'author': author,  # Passa o objeto 'author' para o template
        'year': datetime.now().year,
    }

    return render(request, 'author_detail.html', tparams)

def author_books(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    author_books = Book.objects.filter(authors=author)

    tparams = {
        'title': 'Author Books',
        'author': author,
        'allBooks': author_books,
        'year': datetime.now().year,
    }

    return render(request, 'author_books.html', tparams)

def publishers(request):
    all_publishers = Publisher.objects.all()

    tparams = {
        'title': 'Publisher library',
        'message': 'Welcome.',
        'year': datetime.now().year,
        'allPublishers': all_publishers,
    }

    return render(request, 'publishers.html', tparams)

def publisher_detail(request, publisher_id):
    publisher = get_object_or_404(Publisher, pk=publisher_id)
    tparams = {
        'title': 'Publisher Details',
        'publisher': publisher,
        'year': datetime.now().year,
    }

    return render(request, 'publisher_detail.html', tparams)


def publisher_authors(request, publisher_id):
    publisher = get_object_or_404(Publisher, pk=publisher_id)
    publisher_books = Book.objects.filter(publisher=publisher)

    authors_set = set()
    for book in publisher_books:
        for author in book.authors.all():
            authors_set.add(author)

    tparams = {
        'title': 'Publisher Authors',
        'publisher': publisher,
        'allAuthors': list(authors_set),  # Convertemos para lista para passar para o template
        'year': datetime.now().year,
    }

    return render(request, 'publisher_authors.html', tparams)

from django.db.models import Q
from .forms import BookSearchForm
def booksearch(request):
    if request.method == 'POST':
        form = BookSearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            books = Book.objects.filter(
                Q(title__icontains=query) |
                Q(authors__name__icontains=query) |
                Q(publisher__name__icontains=query)
            ).distinct()
            return render(request, 'booklist.html', {'books': books, 'query': query, 'form': form})
        else:
            return render(request, 'booksearch.html', {'form': form, 'error': True})
    else:
        form = BookSearchForm()
        return render(request, 'booksearch.html', {'form': form})
def authorsearch(request):
    if 'query' in request.POST:
        query = request.POST['query']

        if query:
            authors = Author.objects.filter(name__icontains=query)
            return render(request, 'authorlist.html', {'authors': authors, 'query': query})
        else:
            return render(request, 'authorsearch.html', {'error': True})
    else:
        return render(request, 'authorsearch.html', {'error': False})

from .forms import AuthorForm, PublisherForm, BookForm


def add_author(request):
    # Verifica se o usuário está autenticado, redirecionando para a página de login se não estiver
    if not request.user.is_authenticated:
        return redirect('/login')

    # Verifica se a requisição é POST para processar o formulário
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            # Obtém os dados limpos do formulário
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']

            # Cria e salva uma nova instância de Author
            a = Author(name=name, email=email)
            a.save()

            # Retorna uma resposta simples indicando que o autor foi adicionado
            return HttpResponse('<h1>Author added</h1>')
    else:
        # Instancia um formulário vazio para requisições GET
        form = AuthorForm()

    # Renderiza o template com o formulário
    return render(request, 'authorins.html', {"form": form})

def add_publisher(request):
    if request.method == 'POST':
        form = PublisherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('publishers')
    else:
        form = PublisherForm()
    return render(request, 'add_publisher.html', {'form': form})

def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('books')
    else:
        form = BookForm()
    return render(request, 'add_book.html', {'form': form})


def edit_author(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    if request.method == 'POST':
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            return redirect('authors')
    else:
        form = AuthorForm(instance=author)

    return render(request, 'author_edit.html', {'form': form, 'author': author})


def edit_publisher(request, publisher_id):
    publisher = get_object_or_404(Publisher, pk=publisher_id)
    if request.method == 'POST':
        form = PublisherForm(request.POST, instance=publisher)
        if form.is_valid():
            form.save()
            return redirect('publishers')
    else:
        form = PublisherForm(instance=publisher)

    return render(request, 'publisher_edit.html', {'form': form, 'publisher': publisher})


def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    authors = Author.objects.all()  # Fetch all authors
    publishers = Publisher.objects.all()  # Fetch all publishers

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('books')
    else:
        form = BookForm(instance=book)

    context = {
        'book': book,
        'authors': authors,
        'publishers': publishers,
    }
    return render(request, 'book_edit.html', context)

from django.http import HttpResponseRedirect

def buy_book(request, book_id):
    if not request.user.is_authenticated:
        return redirect('/login')
    book = get_object_or_404(Book, id=book_id)

    # Retrieve the session dictionary for purchased books or create a new one if it doesn't exist
    purchased_books = request.session.get('purchased_books', {})

    # Increase the count for the book ID or add it if it's not already in the dictionary
    if str(book_id) in purchased_books:
        purchased_books[str(book_id)] += 1
    else:
        purchased_books[str(book_id)] = 1

    # Save the updated dictionary back to the session
    request.session['purchased_books'] = purchased_books

    # Redirect back to the books page
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/books'))


def purchased_books(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    # Retrieve the session data, convert to dictionary if it's still a list
    purchased_books_data = request.session.get('purchased_books', {})

    # Check if `purchased_books_data` is a list (old format) and convert to dictionary
    if isinstance(purchased_books_data, list):
        # Convert the list into a dictionary with count = 1 for each book ID
        purchased_books_data = {str(book_id): 1 for book_id in purchased_books_data}
        # Save back to the session to ensure future consistency
        request.session['purchased_books'] = purchased_books_data

    # Fetch book objects and count from the session data
    purchased_books = []
    for book_id, count in purchased_books_data.items():
        try:
            book = Book.objects.get(id=book_id)
            purchased_books.append({
                'book': book,
                'count': count
            })
        except Book.DoesNotExist:
            continue

    tparams = {
        'title': 'Purchased Books',
        'purchasedBooks': purchased_books,
        'year': datetime.now().year,
    }

    return render(request, 'purchased_books.html', tparams)


def remove_purchased_book(request, book_id):
    # Retrieve the session dictionary for purchased books
    purchased_books = request.session.get('purchased_books', {})

    # Decrease the count for the book ID or remove it if the count is 1
    if str(book_id) in purchased_books:
        if purchased_books[str(book_id)] > 1:
            purchased_books[str(book_id)] -= 1
        else:
            del purchased_books[str(book_id)]

    # Save the updated dictionary back to the session
    request.session['purchased_books'] = purchased_books

    # Redirect back to the purchased books page
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/purchased_books'))
