from django.shortcuts import redirect, render
from django.contrib import messages
import bcrypt
from .models import User, Book

def index(request):
    return render(request,'index.html')

def success(request):
    if 'user_id' not in request.session:
        return redirect('/')


    user = User.objects.get(id=request.session['user_id'])
    fav_book_ids = []
    for book in user.liked_books.all():
        fav_book_ids.append(book.id)

    context = {
        'user': user,
        'all_books': Book.objects.all(),
        'favorite_book_ids': fav_book_ids,
    }

    return render(request, 'success.html', context)

def register(request):
    errors = User.objects.registration_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        password = request.POST['password']
        hash_browns = bcrypt.hashpw(
            password.encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = hash_browns,
        )     
        request.session['user_id'] = user.id
        return redirect('/books')


def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user_to_login = User.objects.get(email=request.POST['login_email'])
        request.session['user_id'] = user_to_login.id 
        return redirect('/books')

def logout(request):
    request.session.flush()
    return redirect('/')

def create_books(request):
    errors = Book.objects.book_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
    else:
       
        user = User.objects.get(id=request.session['user_id'])

        book = Book.objects.create(
            title = request.POST['title'],
            desc = request.POST['desc'],
            uploaded_by = user
        )

        book.users_who_like.add(user)
        
    return redirect('/books')


def detail(request, book_id):
    book = Book.objects.get(id=book_id)
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'book': book,
        'user': user,
        
    }
    return render(request, 'detail.html', context)

def update(request, book_id):
    errors = Book.objects.book_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
    else:
        book_to_update = Book.objects.get(id=book_id)
        book_to_update.title = request.POST['title']
        book_to_update.desc = request.POST['desc']
        book_to_update.save() 
    return redirect('/books/{}'.format(book_id))


def delete(request, book_id):
    book = Book.objects.get(id=book_id)
    print('Book to delete: {}'.format(book))
    book.delete()
    return redirect('/books')

def add_favorite(request, book_id):
    book = Book.objects.get(id=book_id)
    user = User.objects.get(id=request.session['user_id'])
    user.liked_books.add(book)  
    return redirect('/books')

def unfavorite(request,book_id):
    book = Book.objects.get(id=book_id)
    user = User.objects.get(id=request.session['user_id'])
    user.liked_books.remove(book)
    return redirect('/books/{}'.format(book_id))






