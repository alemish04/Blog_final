from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, \
    CreateView  # НЕ используем(пока что), может быть будем позже

from .forms import AuthUserForm, RegisterUserForm
# from .models import Post, Category, Profile
from .models import Post, Category
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.views.generic.edit import CreateView, UpdateView

from django.views.generic.edit import CreateView


def post_list(request):  # отображение списка постов
    # поиск, проверка, был лы запрос с ключом search, сбор и фильтрация постов
    # на этом основании

    search_query = request.GET.get("search", '')
    if search_query:
        posts = Post.objects.filter(Q(title__icontains=search_query) | Q(body__icontains=search_query))
    else:
        posts = Post.objects.all()

    # отображение нужного кол-ва постов на странице и пагинаторов
    paginator = Paginator(posts, 3)
    page_number = request.GET.get("page", 1)
    page = paginator.get_page(page_number)
    is_paginated = page.has_other_pages()
    if page.has_previous():
        prev_url = "?page={}".format(page.previous_page_number())
    else:
        prev_url = ""

    if page.has_next():
        next_url = "?page={}".format(page.next_page_number())
    else:
        next_url = ""
    # отображение нужного кол-ва постов на странице и пагинаторов
    categories = Category.objects.all()
    context = {
        "posts": page,
        "is_paginated": is_paginated,  # собираем словарь свойств, которые передаём на рендер
        "next_url": next_url,
        "prev_url": prev_url,
        "categories": categories,
        # 'profile': profile,
        # 'user': user
    }
    return render(request, "index.html", context=context)


def post_detail(request, id):
    post = Post.objects.get(id__iexact=id)
    return render(request, 'post_detail.html', context={'post': post})


def category_list(request):
    categories = Category.objects.all()
    return render(request, "categories_list.html", context={"categories": categories})


def category_detail(request, id):
    category = Category.objects.get(id__iexact=id)
    categories = Category.objects.all()
    return render(request, "category_detail.html", context={"category": category, "categories": categories})


def about_project(request):
    categories = Category.objects.all()
    return render(request, "about.html", context={"categories": categories})


class MyprojectLoginView(LoginView):
    template_name = 'login.html'
    form_class = AuthUserForm
    success_url = reverse_lazy('posts_list_url')

    def get_success_url(self):
        return self.success_url


class RegisterUserView(CreateView):
    model = User
    template_name = 'register_page.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('posts_list_url')
    success_msg = 'Пользователь успешно создан'

    def form_valid(self, form):
        form_valid = super().form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        aut_user = authenticate(username=username, password=password)
        login(self.request, aut_user)
        return form_valid


class MyProjectLogout(LogoutView):
    next_page = reverse_lazy('posts_list_url')


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import User, Profile


# ...

@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    return render(request, 'profile.html', {'profile': profile, 'user': user})
