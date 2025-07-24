from django.test import TestCase
from django.contrib.auth.models import User
from .forms import UserRegisterForm

# Create your tests here.
class UserRegistrationTests(TestCase):

    def setUp(self):
        # Set up a user and profile for the tests
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_valid_registration(self):
        # Test user registration form with valid data
        form_data = {
            'username': 'newtestuser',
            'email': 'testuser@example.com',
            'password1': 'StrongPassword123!',
            'password2': 'StrongPassword123!',
        }
        form = UserRegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_mismatched_passwords(self):
        # Test user registration form with mismatched passwords
        form_data = {
            'username': 'newtestuser',
            'email': 'testuser@example.com',
            'password1': 'StrongPassword124',
            'password2': 'StrongPassword123',
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
        self.assertIn('The two password fields didn’t match.', form.errors['password2'])


    def test_no_username(self):
        # Test user registration form with missing username
        form_data = {
            'username': '',
            'email': 'testuser@example.com',
            'password1': 'StrongPassword123',
            'password2': 'StrongPassword123',
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('This field is required.', form.errors['username'])


    def test_no_email(self):
        # Test user registration form with missing email
        form_data = {
            'username': 'newtestuser',
            'email': '',
            'password1': 'StrongPassword123',
            'password2': 'StrongPassword123',
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertIn('This field is required.', form.errors['email'])


    def test_duplicate_username(self):
        # Test user registration form with duplicate username
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'StrongPassword123!',
            'password2': 'StrongPassword123!',
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('A user with that username already exists.', form.errors['username'])


    def test_short_password(self):
        # Test user registration form with password that is too short
        form_data = {
            'username': 'newtestuser',
            'email': 'testuser@example.com',
            'password1': 'short',
            'password2': 'short',
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
        self.assertIn('This password is too short. It must contain at least 8 characters.', form.errors['password2'])


    def test_common_password(self):
        # Test user registration form with password that is too common
        form_data = {
            'username': 'newtestuser',
            'email': 'testuser@example.com',
            'password1': 'password123',
            'password2': 'password123',
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
        self.assertIn('This password is too common.', form.errors['password2'])

    def test_password_similar_to_username(self):
        # Test user registration form with password that is too similar to the username
        form_data = {
            'username': 'james1986',
            'email': 'james@example.com',
            'password1': 'james86',
            'password2': 'james86',
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
        self.assertIn('The password is too similar to the username.', form.errors['password2'])

class UserLoginTests(TestCase):

    def setUp(self):
        # Set up a user and profile for the tests
        self.user = User.objects.create_user(username='testuser', password='StrongPassword123!')

    def test_valid_login(self):
        # Test user login with valid data
        login = self.client.login(username='testuser', password='StrongPassword123!')
        self.assertTrue(login)

    def test_invalid_login_incorrect_password(self):
        # Test user login with incorrect password
        login = self.client.login(username='testuser', password='strongpassword123!')
        self.assertFalse(login)
