from django.test import TestCase
from django.contrib.auth import get_user_model
User = get_user_model()
from .forms import UserRegisterForm
from django.urls import reverse
from django.conf import settings


# Create your tests here.
class UserRegistrationTests(TestCase):

    def setUp(self):
        """Set up a user for the tests"""
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_valid_registration(self):
        """Test user registration form with valid data"""
        form_data = {
            'username': 'newtestuser',
            'email': 'testuser@example.com',
            'password1': 'StrongPassword123!',
            'password2': 'StrongPassword123!',
        }
        form = UserRegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_mismatched_passwords(self):
        """Test user registration form with mismatched passwords"""
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
        """Test user registration form with missing username"""
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
        """Test user registration form with missing email"""
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
        """Test user registration form with duplicate username"""
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
        """Test user registration form with password that is too short"""
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
        """Test user registration form with password that is too common"""
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
        """Test user registration form with password that is too similar to the username"""
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
        """Set up a user for the tests"""
        self.user = User.objects.create_user(username='testuser', password='StrongPassword123!')

    def test_valid_login(self):
        """Test user login with valid data"""
        login = self.client.login(username='testuser', password='StrongPassword123!')
        self.assertTrue(login)

    def test_invalid_login_incorrect_password(self):
        """Test user login with incorrect password"""
        login = self.client.login(username='testuser', password='strongpassword123!')
        self.assertFalse(login)

    def test_inavlid_login_nonexistent_user(self):
        """Test user login with nonexistent user"""
        login = self.client.login(username='userwho', password='StrongPassword123!')
        self.assertFalse(login)

    def test_login_redirect(self):
        """Test user login redirects to profile page"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'StrongPassword123!',
        })

        self.assertEqual(response.status_code, 302)

        self.assertRedirects(response, reverse('profile'))

    def test_inactive_user_cannot_login(self):
        """Test inactive user cannot login"""
        self.user.is_active = False
        self.user.save()

        login = self.client.login(username='testuser', password='StrongPassword123!')
        self.assertFalse(login)

    def test_login_redirects_back_to_next(self):
        """Test redirect of non logged in user from profile to login and from login back to profile"""
        response = self.client.get('/profile/')
        expected_login_url = f"{settings.LOGIN_URL}?next=/profile/"
        self.assertRedirects(response, expected_login_url)

        login_response = self.client.post(expected_login_url, {
            'username': 'testuser',
            'password': 'StrongPassword123!',
        })

        self.assertRedirects(login_response, '/profile/')

class UserLogoutTests(TestCase):
    def setUp(self):
        """Set up a user for the tests"""
        self.user = User.objects.create_user(username='testuser', password='StrongPassword123!')

    def test_logout(self):
        """Test a user is successfully logged out"""
        login = self.client.login(username='testuser', password='StrongPassword123!')
        self.assertTrue(login)

        self.client.logout()

        self.assertNotIn('_auth_user_id', self.client.session)

    def test_logout_redirect(self):
        """Test user logout redirects to profile page"""
        login = self.client.login(username='testuser', password='StrongPassword123!')
        self.assertTrue(login)

        response = self.client.post(reverse('logout'))

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'users/logout.html')
        self.assertNotIn('_auth_user_id', self.client.session)

class ProfilePageAccessTests(TestCase):
    def setUp(self):
        """Set up a user for the tests"""
        self.user = User.objects.create_user(
            username='testuser', 
            password='StrongPassword123!',
            first_name='Test',
            last_name='User',
        )

    def test_profile_access_logged_in_user(self):
        """Test logged in user can access the profile page"""
        login = self.client.login(username='testuser', password='StrongPassword123!')
        self.assertTrue(login)

        response = self.client.get(reverse('profile'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertContains(response, "Hi Test User")

    def test_profile_access_non_logged_in_user(self):
        """Test non logged in user cannot access the profile page"""
        response = self.client.get(reverse('profile'))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/?next=/profile/')

class AuthenticationPageAccessTests(TestCase):
    def setUp(self):
        """Set up a user for the tests"""
        self.user = User.objects.create_user(username='testuser', password='StrongPassword123!')

    def test_login_page_access(self):
        """Test the login page can be accessed"""
        response = self.client.get(reverse('login'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_registration_page_access(self):
        """Test the registration page can be accessed"""
        response = self.client.get(reverse('register'))

        self.assertEqual(response.status_code, 200)

    def test_logged_in_user_redirected_from_registration_page(self):
        """Test a logged in user is redirected away from the registration page"""
        login = self.client.login(username='testuser', password='StrongPassword123!')
        self.assertTrue(login)

        response = self.client.get(reverse('register'))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/profile/')

    def test_logged_in_user_redirected_from_login_page(self):
        """Test a logged in user is redirected away from the login page"""
        login = self.client.login(username='testuser', password='StrongPassword123!')
        self.assertTrue(login)

        response = self.client.get(reverse('login'))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/profile/')
