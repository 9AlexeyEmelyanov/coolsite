
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import AddPostForm
from .models import *
from .utils import *



class WomenHome(DataMixin, ListView):

    model = Women
    template_name = 'women/index.html'
    context_object_name = 'post'
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Women.objects.filter(is_published=True)


class WomenCategory(DataMixin, ListView):

    model = Women
    template_name = 'women/index.html'
    context_object_name = 'post'
    allow_empty = False
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Категория - ' + str(context['post'][0].category),
                                        cat_selected=context['post'][0].category_id)
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Women.objects.filter(category__slug=self.kwargs['cat_slug'], is_published=True)



def about(request):
    return render(request, 'women/about.html', {
        'menu': menu,
        'title': 'O сайте'
    })

class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    #Переопределение функцию в классе Women - get_absolute_url()
    success_url = reverse_lazy('home')
    redirect_field_name = 'redirect_to'
    login_url = '/admin/'
    

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление статьи')
        return dict(list(context.items()) + list(c_def.items()))


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


class ShowPost(DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))



def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

#def show_post(request, post_slug):
#    post = get_object_or_404(Women, slug=post_slug)
#    context = {
#        'post': post,
#        'menu': menu,
#        'title': post.title,
#       'cat_selected': post.slug,
#    }
#   return render(request, 'women/post.html', context=context)


#def show_category(request, cat_id):
#    post = Women.objects.filter(category_id=cat_id)
#    cats = Category.objects.all()
    
#    if len(post) == 0:
#        raise Http404()

#    context = {
#        'post': post,
#        'cats': cats,
 #       'menu': menu,
 #       'title': 'Отображение по рубрикам',
#        'cat_selected': cat_id,
 #   }
#
 #   return render(request, 'women/index.html', context=context)
#def addpage(request):
#    if request.method == 'POST':
#        form = AddPostForm(request.POST, request.FILES)
#        if form.is_valid():
#            form.save()
#            return redirect('home')
#    else:
#        form = AddPostForm()
#    return render(request, 'women/addpage.html', {
#        'form': form,
#        'menu': menu,
#        'title': 'Добавление статьи'
#    })
#def index(request):
    #post = Women.objects.all()
    #cats = Category.objects.all()

    #if len(post) == 0:
       # raise Http404()

    #context = {
    #    'post': post,
    #    'cats': cats, 
    #    'menu': menu, 
    #    'title': 'Главная страница',
    #    'cat_selected': 0,
    #}
   # return render(request, 'women/index.html', context=context)