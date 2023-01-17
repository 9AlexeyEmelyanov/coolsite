
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from .forms import AddPostForm, RegisterUserForm, LoginUserForm, ContactForm
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
        return Women.objects.filter(is_published=True).select_related('category')


class WomenCategory(DataMixin, ListView):

    model = Women
    template_name = 'women/index.html'
    context_object_name = 'post'
    allow_empty = False
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(categories.name),
                                        cat_selected=categories.pk)
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Women.objects.filter(category__slug=self.kwargs['cat_slug'], is_published=True).select_related('category')



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
        c_def = self.get_user_context(title='Добавление статьи', )

        return dict(list(context.items()) + list(c_def.items()))
    

class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'women/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = super().get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self) -> str:
        return reverse_lazy('home')

    


class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'women/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация ')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'women/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Обратная связь')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')
    


def logout_user(request):
    logout(request)
    return redirect('login')



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