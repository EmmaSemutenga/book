from django.http import response
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from books.models import Book



class UserRegisterViewTests(TestCase):

    def test_register_page_is_rendered(self):
        """
        Register page is rendered on a get request
        """
        url = "/regiter/"
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register_user.html")

    def test_user_get_registered(self):
        """
        User is registered and redirected to login page
        """
        url = reverse("register_user")
        response = self.client.post(url, { "username": "janedoe", "email":"janedoe@email.com", "password":"123"})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login_user"), 302)

    def test_user_registeration_without_username(self):
        """
        Validation fails and registration page is rendered again
        """
        url = reverse("register_user")
        response = self.client.post(url, { "username": "", "email":"janedoe@email.com", "password":"123"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register_user.html")

    def test_logged_in_user_doesnt_register(self):
        """
        Logged in user is redirected if they try to login
        """
        user = User.objects.create_user(username="jdoe", email="jdoe@email.com", password="123")
        self.client.login(username = "jdoe", password="123")
        url = reverse("register_user")
        response = self.client.post(url, { "username": "", "email":"janedoe@email.com", "password":"123"})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"), 302)

class BookListViewTests(TestCase):
    def setUp(self):
        User.objects.create_user(username="jdoe", email="jdoe@email.com", password="123")
    
    def test_books_exist(self):
        """
        should return list of books
        """
        login = self.client.login(username = "jdoe", password="123")
        book = Book.objects.create(name = "Gullivers Travels", pages=400)
        url = reverse("book_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["book_list"], [book])
