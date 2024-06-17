from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def home(request):
    book = Book.objects.all()
    return render(request, 'site/home.html', {'books': book})

def index(request):
    book = Book.objects.all()
    return render(request, 'site/index.html', {'books': book})

@login_required
def comment_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        Comment.objects.create(user=request.user, book=book, content=content)
    return redirect('detail_book', book_id=book_id)

@login_required
def detail_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    comments = Comment.objects.filter(book=book)
    liked = False
    if request.user.is_authenticated:
        liked = Like.objects.filter(user=request.user, book=book).exists()
    return render(request, 'site/detail_book.html', {'book': book, 'comments': comments, 'liked': liked})

@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Roupa cadastrada com sucesso!')
            return redirect('home')
    else:
        form = BookForm()
    return render(request, 'site/add_book.html', {'form': form})

@login_required
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Roupa editada com sucesso!')
            return redirect('home')
    else:
        form = BookForm(instance=book)
    return render(request, 'site/edit_book.html', {'form': form})

@login_required
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Roupa deletada com sucesso!')
        return redirect('home')
    return render(request, 'site/delete_book.html', {'book': book})

@login_required
def like_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    like, created = Like.objects.get_or_create(user=request.user, book=book)
    if not created:
        like.delete()
    return redirect('detail_book', book_id=book_id)

