from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from teams.models import Team

User = get_user_model()

# Create your tests here.
class TeamFormTests(TestCase):
    def setUp(self):
        """Set up users for team form tests"""
        self.chairman = User.objects.create_user(username='chairman', password='pass1234', role='chairman')
        self.secretary = User.objects.create_user(username='secretary', password='pass1234', role='secretary')
        self.manager = User.objects.create_user(username='manager', password='pass1234', role='manager')
        self.coach = User.objects.create_user(username='coach', password='pass1234', role='coach')
        self.coach1 = User.objects.create_user(username='coach1', password='pass1234', role='coach')
        self.coach2 = User.objects.create_user(username='coach2', password='pass1234', role='coach')


    def _assert_team_form_ok(self):
        """Shared assertions for privileged roles, assert team form has correct form fields and coach select lists only coaches"""
        response = self.client.get(reverse('create_team'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="age_group"')
        self.assertContains(response, 'name="gender"')
        self.assertContains(response, 'name="sport"')
        self.assertContains(response, 'name="coach"')
        self.assertContains(response, 'Under 12')
        self.assertContains(response, 'Boys')
        self.assertContains(response, 'Football')
        self.assertContains(response, f'value="{self.coach.id}"', count=1)
        self.assertContains(response, f'value="{self.coach1.id}"', count=1)
        self.assertContains(response, f'value="{self.coach2.id}"', count=1)
        self.assertNotContains(response, f'value="{self.manager.id}"')
        self.assertNotContains(response, f'value="{self.secretary.id}"')
        self.assertNotContains(response, f'value="{self.chairman.id}"')

    def test_chairman_form(self):
        """Test Chairman can access create_team view and sees correct form/coach options"""
        self.client.login(username='chairman', password='pass1234')
        self._assert_team_form_ok()

    def test_secretary_form(self):
        """Test Secretary can access create_team view and sees correct form/coach options"""
        self.client.login(username='secretary', password='pass1234')
        self._assert_team_form_ok()

class TeamCreateViewTests(TestCase):
    def setUp(self):
        """Set up users for create team tests"""
        self.chairman = User.objects.create_user(username='chairman', password='pass1234', role='chairman')
        self.secretary = User.objects.create_user(username='secretary', password='pass1234', role='secretary')
        self.manager = User.objects.create_user(username='manager', password='pass1234', role='manager')
        self.coach = User.objects.create_user(username='coach', password='pass1234', role='coach')
        self.coach1 = User.objects.create_user(username='coach1', password='pass1234', role='coach')

    def test_anonymous_user_redirects_to_login(self):
        """Test public users are redirected to login"""
        response = self.client.get(reverse('create_team'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.url)

    def test_non_privileged_roles_forbidden(self):
        """Test Manager & Coach cannot access create team"""
        self.client.login(username='manager', password='pass1234')
        resp_manager = self.client.get(reverse('create_team'))
        self.assertEqual(resp_manager.status_code, 403)

        self.client.login(username='coach', password='pass1234')
        resp_coach = self.client.get(reverse('create_team'))
        self.assertEqual(resp_coach.status_code, 403)

    def test_post_valid_with_coach_redirects_and_creates(self):
        """Test valid POST with a coach creates a team and redirects"""
        self.client.login(username='chairman', password='pass1234')
        data = {
            'age_group': 'U12',
            'gender': 'boys',
            'sport': 'football',
            'coach': str(self.coach1.id),
        }
        response = self.client.post(reverse('create_team'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('team_list'))
        self.assertEqual(Team.objects.count(), 1)
        team = Team.objects.first()
        self.assertEqual(team.age_group, 'U12')
        self.assertEqual(team.gender, 'boys')
        self.assertEqual(team.sport, 'football')
        self.assertEqual(team.coach, self.coach1)

    def test_post_valid_without_coach_creates_null_coach(self):
        """ Test valid POST without a coach creates a team and redirects"""
        self.client.login(username='secretary', password='pass1234')
        data = {
            'age_group': 'U14',
            'gender': 'girls',
            'sport': 'camogie',
            'coach': '',
        }
        response = self.client.post(reverse('create_team'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('team_list'))
        self.assertEqual(Team.objects.count(), 1)
        team = Team.objects.first()
        self.assertEqual(team.age_group, 'U14')
        self.assertEqual(team.gender, 'girls')
        self.assertEqual(team.sport, 'camogie')
        self.assertIsNone(team.coach)

    def test_post_with_non_coach_id_is_rejected(self):
        """Test selecting a non‑coach in coach field re-renders with errors"""
        self.client.login(username='chairman', password='pass1234')
        data = {
            'age_group': 'U10',
            'gender': 'boys',
            'sport': 'hurling',
            'coach': str(self.manager.id),
        }
        response = self.client.post(reverse('create_team'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Select a valid choice. That choice is not one of the available choices.')
        self.assertEqual(Team.objects.count(), 0)

    def test_post_with_invalid_choice_values_is_rejected(self):
        """Test bad age_group/gender/sport choices show validation errors"""
        self.client.login(username='secretary', password='pass1234')
        data = {
            'age_group': 'U99',
            'gender': 'robot',
            'sport': 'golf',
            'coach': '',
        }
        response = self.client.post(reverse('create_team'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Select a valid choice', count=3)
        self.assertEqual(Team.objects.count(), 0)

class TeamPermissionTests(TestCase):
    def setUp(self):
        """Set up users and teams for permission tests"""
        self.chairman = User.objects.create_user(username='chair', password='pass1234', role='chairman')
        self.secretary = User.objects.create_user(username='secretary', password='pass1234', role='secretary')
        self.manager = User.objects.create_user(username='manager', password='pass1234', role='manager')
        self.coach = User.objects.create_user(username='coach', password='pass1234', role='coach')

        self.team1 = Team.objects.create(age_group='U12', gender='boys', sport='football')
        self.team2 = Team.objects.create(age_group='U14', gender='girls', sport='camogie')

    def test_login_required_for_detail(self):
        """Test login required to view team detail"""
        response = self.client.get(reverse('team_detail', kwargs={'pk': self.team1.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.url)

    def test_any_authenticated_user_can_view_detail(self):
        """Test any logged-in user can view team detail"""
        self.client.login(username='manager', password='pass1234')
        response = self.client.get(reverse('team_detail', kwargs={'pk': self.team1.pk}))
        self.assertEqual(response.status_code, 200)

    def test_login_required_to_update_team(self):
        """Test login required to update team"""
        response = self.client.get(reverse('team_edit', kwargs={'pk': self.team1.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.url)

    def test_login_required_to_delete_team(self):
        """Test login required to delete team"""
        response = self.client.post(reverse('team_delete', kwargs={'pk': self.team1.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.url)
        self.assertTrue(Team.objects.filter(pk=self.team1.pk).exists())

    def test_chairman_and_secretary_can_update_team(self):
        """Test chairman & secretary can access update form"""
        self.client.login(username='chair', password='pass1234')
        resp_chair = self.client.get(reverse('team_edit', kwargs={'pk': self.team1.pk}))
        self.assertEqual(resp_chair.status_code, 200)

        self.client.login(username='secretary', password='pass1234')
        resp_sec = self.client.get(reverse('team_edit', kwargs={'pk': self.team1.pk}))
        self.assertEqual(resp_sec.status_code, 200)

    def test_manager_and_coach_cannot_update_team(self):
        """Test manager & coach cannot access update form"""
        self.client.login(username='manager', password='pass1234')
        resp_manager = self.client.get(reverse('team_edit', kwargs={'pk': self.team1.pk}))
        self.assertEqual(resp_manager.status_code, 403)

        self.client.login(username='coach', password='pass1234')
        resp_coach = self.client.get(reverse('team_edit', kwargs={'pk': self.team1.pk}))
        self.assertEqual(resp_coach.status_code, 403)

    def test_chairman_and_secretary_can_delete_team(self):
        """Test chairman & secretary can delete teams"""
        self.client.login(username='chair', password='pass1234')
        resp_chair = self.client.post(reverse('team_delete', kwargs={'pk': self.team1.pk}))
        self.assertRedirects(resp_chair, reverse('team_list'))
        self.assertFalse(Team.objects.filter(pk=self.team1.pk).exists())

        self.client.login(username='secretary', password='pass1234')
        resp_sec = self.client.post(reverse('team_delete', kwargs={'pk': self.team2.pk}))
        self.assertRedirects(resp_sec, reverse('team_list'))
        self.assertFalse(Team.objects.filter(pk=self.team2.pk).exists())

    def test_manager_and_coach_cannot_delete_team(self):
        """Test manager & coach cannot delete teams"""
        if not Team.objects.filter(pk=self.team1.pk).exists():
            self.team1 = Team.objects.create(age_group='U12', gender='boys', sport='football')
        if not Team.objects.filter(pk=self.team2.pk).exists():
            self.team2 = Team.objects.create(age_group='U14', gender='girls', sport='camogie')

        self.client.login(username='manager', password='pass1234')
        resp_manager = self.client.post(reverse('team_delete', kwargs={'pk': self.team1.pk}))
        self.assertEqual(resp_manager.status_code, 403)
        self.assertTrue(Team.objects.filter(pk=self.team1.pk).exists())

        self.client.login(username='coach', password='pass1234')
        resp_coach = self.client.post(reverse('team_delete', kwargs={'pk': self.team2.pk}))
        self.assertEqual(resp_coach.status_code, 403)
        self.assertTrue(Team.objects.filter(pk=self.team2.pk).exists())