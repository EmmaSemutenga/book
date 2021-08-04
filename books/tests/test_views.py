from django.test import TestCase
from django.urls import reverse
from authentication.models import User
from books.models import Book
from io import BytesIO




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
        img = BytesIO(b'images/Screen_Shot_2019-12-24_at_12.33.34.png')
        img.name = "myimage.png"
        url = reverse("register_user")
        response = self.client.post(url, { "username": "janedoe", "email":"janedoe@email.com", "password":"123", "photo": img})
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

    def test_user_registeration_without_email(self):
        """
        Validation fails and registration page is rendered again
        """
        url = reverse("register_user")
        response = self.client.post(url, { "username": "janedoe", "email":"", "password":"123"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register_user.html")

    def test_user_registeration_without_password(self):
        """
        Validation fails and registration page is rendered again
        """
        url = reverse("register_user")
        response = self.client.post(url, { "username": "janedoe", "email":"janedoe@email.com", "password":""})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register_user.html")

    def test_logged_in_user_doesnt_register(self):
        """
        Logged in user is redirected if they try to login
        """
        img = BytesIO(b'images/Screen_Shot_2019-12-24_at_12.33.34.png')
        img.name = "myimage.png"
        user = User.objects.create_user(username="jdoe", email="jdoe@email.com", password="123", photo=img.name)
        self.client.login(username = "jdoe", password="123")
        url = reverse("register_user")
        response = self.client.post(url, { "username": "", "email":"janedoe@email.com", "password":"123", "photo":img.name})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"), 302)

class LoginViewTests(TestCase):

    def test_user_logs_in(self):
        user = User.objects.create_user(username="jdoe", email="jdoe@email.com", password="123")
        url = reverse('login_user')
        response = self.client.post(url, {"username": "jdoe", "password" : "123"})
        self.assertRedirects(response, reverse("book_list"), 302)

    def test_user_logs_in_without_user(self):
        # user = User.objects.create_user(username="jdoe", email="jdoe@email.com", password="123")
        url = reverse('login_user')
        response = self.client.post(url, {"username": "jdoe", "password" : "123"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login_user.html")

class LogoutViewTests(TestCase):

    def test_user_logout(self):
        user = User.objects.create_user(username="jdoe", email="jdoe@email.com", password="123")
        login_url = reverse('login_user')
        self.client.post(login_url, {"username": "jdoe", "password" : "123"})
        response = self.client.get(reverse('logout_user'), {"username": "jdoe", "password" : "123"})
        self.assertRedirects(response, reverse("login_user"), 302)


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

class BookCreateViewTests(TestCase):

    def test_if_custom_heading_context_is_passed(self):
        user = User.objects.create_user(username="jdoe", email="jdoe@email.com", password="123")
        login_url = reverse('login_user')
        self.client.post(login_url, {"username": "jdoe", "password" : "123"})
        url = reverse("book_new")
        response = self.client.get(url)
        self.assertEqual(response.context["custom_heading"], "Create Book")

class BookUpdateViewTests(TestCase):

    def test_if_custom_heading_context_is_passed(self):
        user = User.objects.create_user(username="jdoe", email="jdoe@email.com", password="123")
        login_url = reverse('login_user')
        self.client.post(login_url, {"username": "jdoe", "password" : "123"})
        book = Book.objects.create(name="Tom Sawyer", pages=350)

        url = reverse("book_edit", args=(book.id,))
        response = self.client.get(url)
        self.assertEqual(response.context["custom_heading"], "Edit Book")
        self.assertTemplateUsed(response, "book_form.html")

