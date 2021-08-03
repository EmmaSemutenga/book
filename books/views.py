
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator

from books.models import Book


user_must_be_logged_out_to_access = user_passes_test(lambda user: not user.is_authenticated, login_url='/', redirect_field_name=None)

# def user_must_be_logged_out_to_access(user):
#     return not user.is_authenticated

# @user_passes_test(user_must_be_logged_out_to_access, login_url='/', redirect_field_name=None)
@user_must_be_logged_out_to_access
def register_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        if not username:
            return render(request, 'register_user.html')

        email = request.POST["email"]
        if not email:
            return render(request, 'register_user.html')

        password = request.POST["password"]
        if not password:
            return render(request, 'register_user.html')
            
        user = User.objects.create_user(username, email, password)
        return redirect("login_user")

    return render(request, 'register_user.html')

# @user_passes_test(user_must_be_logged_out_to_access, login_url='/', redirect_field_name=None)
@user_must_be_logged_out_to_access
def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password = password)
        if user is None:
            # send a message to one tryng to login
            return render(request, 'login_user.html')
        login(request, user)
        return redirect("book_list")
    return render(request, 'login_user.html')

@login_required
def logout_user(request):
    logout(request)
    return redirect("login_user")

def home(request):
    return render(request, "index.html")

class BookList(LoginRequiredMixin, ListView):
    model = Book
    template_name = "book_list.html"
    context_object_name = "book_list"
    queryset = Book.objects.order_by('name')


# @method_decorator(user_must_be_logged_out_to_access, name="dispatch")
class BookView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = "book_detail.html"
    context_object_name = "book"

class BookCreate(LoginRequiredMixin, CreateView):
    model = Book
    fields = ['name', 'pages']
    success_url = reverse_lazy('book_list')
    template_name = "book_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["custom_heading"] = "Create Book"
        return context

    # @method_decorator()
    # def dispatch(self, *args, **kwargs):
    #     return super().dispatch(*args, **kwargs)

class BookUpdate(LoginRequiredMixin, UpdateView):
    model = Book
    fields = ['name', 'pages']
    success_url = reverse_lazy('book_list')
    template_name = "book_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["custom_heading"] = "Edit Book"
        return context

class BookDelete(LoginRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('book_list')
    template_name = "book_comfirm_delete.html"
