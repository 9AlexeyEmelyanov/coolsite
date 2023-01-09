from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404

from .models import *

menu = [
    {
        'title': 'О сайте',
        'url_name': 'about'
    },
    {
        'title': 'Добавить статью',
        'url_name': 'add_page'
    },
    {
        'title': 'Обратная связь',
        'url_name': 'contact'
    },
    {
        'title': 'Войти',
        'url_name': 'login'
    },
]


def index(request):
    post = Women.objects.all()
    cats = Category.objects.all()

    if len(post) == 0:
        raise Http404()

    context = {
        'post': post,
        'cats': cats, 
        'menu': menu, 
        'title': 'Главная страница',
        'cat_selected': 0,
    }
    return render(request, 'women/index.html', context=context)


def about(request):
    return render(request, 'women/about.html', {
        'menu': menu,
        'title': 'О сайте'
    })


def addpage(request):
    return render(request, 'women/addpage.html', {
        'menu': menu,
        'title': 'Добавление статьи'
    })


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


def show_post(request, post_slug):
    post = get_object_or_404(Women, slug=post_slug)
    context = {
        'post': post,
        'menu': menu,
        'title': post.title,
        'cat_selected': post.slug,
    }
    return render(request, 'women/post.html', context=context)


def show_category(request, cat_id):
    post = Women.objects.filter(category_id=cat_id)
    cats = Category.objects.all()
    
    if len(post) == 0:
        raise Http404()

    context = {
        'post': post,
        'cats': cats,
        'menu': menu,
        'title': 'Отображение по рубрикам',
        'cat_selected': cat_id,
    }

    return render(request, 'women/index.html', context=context)


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
