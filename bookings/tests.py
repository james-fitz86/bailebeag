
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from bookings.models import Booking, Pitch

User = get_user_model()

# Create your tests here.
class BookingFormTests(TestCase):
    def setUp(self):
        """Set up users and pitches for the tests"""
        self.coach = User.objects.create_user(username='coach', password='pass1234', role='coach')
        self.manager = User.objects.create_user(username='manager', password='pass1234', role='manager')
        self.chairman = User.objects.create_user(username='chairman', password='pass1234', role='chairman')
        self.secretary = User.objects.create_user(username='secretary', password='pass1234', role='secretary')
        self.pitch_main = Pitch.objects.create(name='Main Pitch')
        self.pitch_astro = Pitch.objects.create(name='Astro Pitch')

    def test_anonymous_user_form_fields(self):
        """Test public user booking shows the correct fields"""
        self.client.logout()
        response = self.client.get(reverse('create_booking'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="name"')
        self.assertContains(response, 'Astro Pitch')
        self.assertNotContains(response, 'Main Pitch')

    def test_authenticated_coach_method_hidden(self):
        """Test logged-in coach sees both pitch options and a hidden method field"""
        self.client.login(username='coach', password='pass1234')
        response = self.client.get(reverse('create_booking'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<input type="hidden" name="method"', html=False)
        self.assertContains(response, 'Main Pitch')
        self.assertContains(response, 'Astro Pitch')

    def test_manager_sees_method_choices(self):
        """Test logged-in manager sees both pitches sees both method options """
        self.client.login(username='manager', password='pass1234')
        response = self.client.get(reverse('create_booking'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="method"')
        self.assertContains(response, '<option value="phone">Phone</option>')
        self.assertContains(response, '<option value="email">Email</option>')
        self.assertContains(response, 'Main Pitch')
        self.assertContains(response, 'Astro Pitch')

    def test_chairman_method_hidden_and_all_pitches_visible(self):
        """Test logged-in chairman sees both pitch options and a hidden method field"""
        self.client.login(username='chairman', password='pass1234')
        response = self.client.get(reverse('create_booking'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<input type="hidden" name="method"', html=False)
        self.assertContains(response, 'Main Pitch')
        self.assertContains(response, 'Astro Pitch')

    def test_secretary_method_hidden_and_all_pitches_visible(self):
        """Test logged-in secretary sees both pitch options and a hidden method field"""
        self.client.login(username='secretary', password='pass1234')
        response = self.client.get(reverse('create_booking'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<input type="hidden" name="method"', html=False)
        self.assertContains(response, 'Main Pitch')
        self.assertContains(response, 'Astro Pitch')

    def test_public_user_pitch_queryset_limited_to_astro(self):
        """Tets public user does not see Main Pitch option"""
        self.client.logout()
        response = self.client.get(reverse('create_booking'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Astro Pitch')
        self.assertNotContains(response, 'Main Pitch')


class BookingCreateViewTests(TestCase):
    def setUp(self):
        """Set up a user and pitch for the tests"""
        self.manager = User.objects.create_user(username='manager', password='pass1234', role='manager')
        self.coach = User.objects.create_user(username='coach', password='pass1234', role='coach')
        self.chairman = User.objects.create_user(username='chairman', password='pass1234', role='chairman')
        self.secretary = User.objects.create_user(username='secretary', password='pass1234', role='secretary')
        self.main_pitch = Pitch.objects.create(name='Main Pitch')
        self.astro_pitch = Pitch.objects.create(name='Astro Pitch')

    def test_manager_main_pitch_no_conflict_approved(self):
        """Test booking for manager is status approved if no conflict"""
        self.client.login(username='manager', password='pass1234')
        start = timezone.now() + timezone.timedelta(days=1)
        end = start + timezone.timedelta(hours=1)
        data = {
            'pitch': self.main_pitch.id,
            'name': 'Manager',
            'email': 'manager@example.com',
            'start_time': start.isoformat(),
            'end_time': end.isoformat(),
            'method': 'email'
        }
        response = self.client.post(reverse('create_booking'), data)
        self.assertEqual(response.status_code, 302)
        booking = Booking.objects.last()
        self.assertEqual(booking.status, 'approved')

    def test_manager_main_pitch_with_conflict_sets_conflicting_status(self):
        """Test booking for manager is status conflicting if conflict"""
        Booking.objects.create(
            pitch=self.main_pitch,
            name='Existing',
            email='existing@example.com',
            start_time=timezone.now() + timezone.timedelta(days=1, hours=10),
            end_time=timezone.now() + timezone.timedelta(days=1, hours=11),
            status='approved'
        )
        self.client.login(username='manager', password='pass1234')
        start = timezone.now() + timezone.timedelta(days=1, hours=10, minutes=30)
        end = start + timezone.timedelta(hours=1)
        data = {
            'pitch': self.main_pitch.id,
            'name': 'Manager',
            'email': 'manager@example.com',
            'start_time': start.isoformat(),
            'end_time': end.isoformat(),
            'method': 'email'
        }
        response = self.client.post(reverse('create_booking'), data)
        self.assertEqual(response.status_code, 302)
        booking = Booking.objects.last()
        self.assertEqual(booking.status, 'conflicting')

    def test_coach_main_pitch_no_conflict_sets_approved(self):
        """Test booking for coach is status approved if no conflict"""
        self.client.login(username='coach', password='pass1234')
        start = timezone.now() + timezone.timedelta(days=2)
        end = start + timezone.timedelta(hours=1)
        data = {
            'pitch': self.main_pitch.id,
            'name': 'Coach',
            'email': 'coach@example.com',
            'start_time': start.isoformat(),
            'end_time': end.isoformat(),
            'method': 'web'
        }
        response = self.client.post(reverse('create_booking'), data)
        self.assertEqual(response.status_code, 302)
        booking = Booking.objects.last()
        self.assertEqual(booking.status, 'approved')

    def test_coach_main_pitch_with_conflict_sets_conflicting(self):
        """Test booking for coach is status conflicting if conflict"""
        Booking.objects.create(
            pitch=self.main_pitch,
            name='Existing',
            email='existing@example.com',
            start_time=timezone.now() + timezone.timedelta(days=3, hours=17),
            end_time=timezone.now() + timezone.timedelta(days=3, hours=18),
            status='approved'
        )
        self.client.login(username='coach', password='pass1234')
        start = timezone.now() + timezone.timedelta(days=3, hours=17, minutes=30)
        end = start + timezone.timedelta(hours=1)
        data = {
            'pitch': self.main_pitch.id,
            'name': 'Coach',
            'email': 'coach@example.com',
            'start_time': start.isoformat(),
            'end_time': end.isoformat(),
            'method': 'web'
        }
        response = self.client.post(reverse('create_booking'), data)
        self.assertEqual(response.status_code, 302)
        booking = Booking.objects.last()
        self.assertEqual(booking.status, 'conflicting')

    def test_chairman_main_pitch_auto_approved(self):
        """Test chairman is approved regardless of conflict or not"""
        self.client.login(username='chairman', password='pass1234')
        start = timezone.now() + timezone.timedelta(days=4)
        end = start + timezone.timedelta(hours=1)
        data = {
            'pitch': self.main_pitch.id,
            'name': 'Chairman',
            'email': 'chairman@example.com',
            'start_time': start.isoformat(),
            'end_time': end.isoformat(),
            'method': 'web'
        }
        response = self.client.post(reverse('create_booking'), data)
        self.assertEqual(response.status_code, 302)
        booking = Booking.objects.last()
        self.assertEqual(booking.status, 'approved')

    def test_secretary_main_pitch_auto_approved(self):
        """Test secretary is approved regardless of conflict or not"""
        self.client.login(username='secretary', password='pass1234')
        start = timezone.now() + timezone.timedelta(days=4)
        end = start + timezone.timedelta(hours=1)
        data = {
            'pitch': self.main_pitch.id,
            'name': 'Secretary',
            'email': 'secretary@example.com',
            'start_time': start.isoformat(),
            'end_time': end.isoformat(),
            'method': 'web'
        }
        response = self.client.post(reverse('create_booking'), data)
        self.assertEqual(response.status_code, 302)
        booking = Booking.objects.last()
        self.assertEqual(booking.status, 'approved')

    def test_anonymous_user_booking_sets_pending_status(self):
        """Test public user booking status is pending and method is web"""
        start = timezone.now() + timezone.timedelta(days=5)
        end = start + timezone.timedelta(hours=1)
        data = {
            'pitch': self.astro_pitch.id,
            'name': 'Public User',
            'email': 'public@example.com',
            'start_time': start.isoformat(),
            'end_time': end.isoformat(),
            'method': 'web'
        }
        response = self.client.post(reverse('create_booking'), data)
        self.assertEqual(response.status_code, 302)
        booking = Booking.objects.last()
        self.assertEqual(booking.status, 'pending')
        self.assertEqual(booking.method, 'web')
        self.assertIsNone(booking.created_by)

    def test_invalid_form_submission_returns_form_with_errors(self):
        """Test form submission reurns messages in rendered form"""
        self.client.login(username='manager', password='pass1234')
        data = {
            'pitch': '99',
            'name': 'Incomplete',
            'email': '',
            'start_time': '',
            'end_time': '',
            'method': 'email'
        }
        response = self.client.post(reverse('create_booking'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Select a valid choice. That choice is not one of the available choices.')
        self.assertContains(response, 'This field is required.', count=2)



class BookingPermissionTests(TestCase):
    def setUp(self):
        """Set up users, pitch and booking for the tests"""
        self.pitch = Pitch.objects.create(name='Main Pitch')
        self.chairman = User.objects.create_user(username='chair', password='pass1234', role='chairman')
        self.coach = User.objects.create_user(username='coach', password='pass1234', role='coach')
        self.other_coach = User.objects.create_user(username='othercoach', password='pass1234', role='coach')
        self.secretary = User.objects.create_user(username='secretary', password='pass1234', role='secretary')
        self.manager = User.objects.create_user(username='manager', password='pass1234', role='manager')


        self.booking = Booking.objects.create(
            pitch=self.pitch,
            name='Test Booking',
            email='test@example.com',
            start_time=timezone.now() + timezone.timedelta(days=1),
            end_time=timezone.now() + timezone.timedelta(days=1, hours=1),
            created_by=self.coach
        )

    def test_coach_can_update_own_booking(self):
        """Test coach can update own booking"""
        self.client.login(username='coach', password='pass1234')
        response = self.client.get(reverse('booking_update', kwargs={'pk': self.booking.pk}))
        self.assertEqual(response.status_code, 200)

    def test_coach_cannot_update_others_booking(self):
        """Test coach cannot update booking created by others"""
        self.booking.created_by = self.other_coach
        self.booking.save()
        self.client.login(username='coach', password='pass1234')
        response = self.client.get(reverse('booking_update', kwargs={'pk': self.booking.pk}))
        self.assertEqual(response.status_code, 403)

    def test_coach_can_delete_booking(self):
        """Test coach can delete own booking"""
        self.client.login(username='coach', password='pass1234')
        response = self.client.post(reverse('booking_delete', kwargs={'pk': self.booking.pk}))
        self.assertRedirects(response, reverse('booking_list'))
        self.assertFalse(Booking.objects.filter(pk=self.booking.pk).exists())

    def test_coach_cannot_delete_others_booking(self):
        """Test coach cannot delete booking created by others"""
        self.booking.created_by = self.other_coach
        self.booking.save()
        self.client.login(username='coach', password='pass1234')
        response = self.client.post(reverse('booking_delete', kwargs={'pk': self.booking.pk}))
        self.assertEqual(response.status_code, 403)

    def test_chairman_can_update_any_booking(self):
        """Test chariman can update any booking"""
        self.client.login(username='chair', password='pass1234')
        response = self.client.get(reverse('booking_update', kwargs={'pk': self.booking.pk}))
        self.assertEqual(response.status_code, 200)

    def test_chairman_can_delete_any_booking(self):
        """Test chairman can delete any booking"""
        self.client.login(username='chair', password='pass1234')
        response = self.client.post(reverse('booking_delete', kwargs={'pk': self.booking.pk}))
        self.assertRedirects(response, reverse('booking_list'))
        self.assertFalse(Booking.objects.filter(pk=self.booking.pk).exists())

    def test_secretary_can_update_any_booking(self):
        """Test secretary can update any booking"""
        self.client.login(username='secretary', password='pass1234')
        response = self.client.get(reverse('booking_update', kwargs={'pk': self.booking.pk}))
        self.assertEqual(response.status_code, 200)

    def test_secretary_can_delete_any_booking(self):
        """Test secretary can delete any booking"""
        self.client.login(username='secretary', password='pass1234')
        response = self.client.post(reverse('booking_delete', kwargs={'pk': self.booking.pk}))
        self.assertRedirects(response, reverse('booking_list'))
        self.assertFalse(Booking.objects.filter(pk=self.booking.pk).exists())
    
    def test_manager_can_update_any_booking(self):
        """Test manager can update any booking"""
        self.client.login(username='manager', password='pass1234')
        response = self.client.get(reverse('booking_update', kwargs={'pk': self.booking.pk}))
        self.assertEqual(response.status_code, 200)

    def test_manager_can_delete_any_booking(self):
        """Test manager can delete any booking"""
        self.client.login(username='manager', password='pass1234')
        response = self.client.post(reverse('booking_delete', kwargs={'pk': self.booking.pk}))
        self.assertRedirects(response, reverse('booking_list'))
        self.assertFalse(Booking.objects.filter(pk=self.booking.pk).exists())
    
    def test_login_required_to_update_booking(self):
        """Test login required to update booking"""
        response = self.client.get(reverse('booking_update', kwargs={'pk': self.booking.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.url)

    def test_login_required_to_delete_booking(self):
        """Test login required to delete booking"""
        response = self.client.post(reverse('booking_delete', kwargs={'pk': self.booking.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.url)
        self.assertTrue(Booking.objects.filter(pk=self.booking.pk).exists())


class ApproveRejectTests(TestCase):
    def setUp(self):
        """Set up users, pitches, and bookings for all test scenarios"""
        self.astro_pitch = Pitch.objects.create(name='Astro Pitch')
        self.main_pitch = Pitch.objects.create(name='Main Pitch')

        self.manager = User.objects.create_user(username='manager', password='pass1234', role='manager')
        self.chairman = User.objects.create_user(username='chairman', password='pass1234', role='chairman')
        self.secretary = User.objects.create_user(username='secretary', password='pass1234', role='secretary')
        self.coach = User.objects.create_user(username='coach', password='pass1234', role='coach')
        self.public_user = User.objects.create_user(username='public', password='pass1234')  # No role

        self.astro_booking = Booking.objects.create(
            pitch=self.astro_pitch,
            name='Astro Booker',
            email='astro@example.com',
            start_time=timezone.now() + timezone.timedelta(days=1),
            end_time=timezone.now() + timezone.timedelta(days=1, hours=1),
            status='pending'
        )

        self.main_booking = Booking.objects.create(
            pitch=self.main_pitch,
            name='Main Booker',
            email='main@example.com',
            start_time=timezone.now() + timezone.timedelta(days=2),
            end_time=timezone.now() + timezone.timedelta(days=2, hours=1),
            status='pending'
        )

    def test_manager_can_approve_astro_booking(self):
        """Test manager can approve astro booking"""
        self.client.login(username='manager', password='pass1234')
        response = self.client.post(reverse('booking_approve', kwargs={'booking_id': self.astro_booking.id}))
        self.astro_booking.refresh_from_db()
        self.assertEqual(self.astro_booking.status, 'approved')
        self.assertEqual(response.status_code, 302)

    def test_manager_can_reject_astro_booking(self):
        """Test manager can reject astro booking"""
        self.client.login(username='manager', password='pass1234')
        response = self.client.post(reverse('booking_reject', kwargs={'booking_id': self.astro_booking.id}))
        self.astro_booking.refresh_from_db()
        self.assertEqual(self.astro_booking.status, 'rejected')
        self.assertEqual(response.status_code, 302)
    
    def test_manager_cannot_approve_main_booking(self):
        """Test manager cannot approve main booking"""
        self.client.login(username='manager', password='pass1234')
        response = self.client.post(reverse('booking_approve', kwargs={'booking_id': self.main_booking.id}))
        self.main_booking.refresh_from_db()
        self.assertEqual(self.main_booking.status, 'pending')
        self.assertEqual(response.status_code, 403)

    def test_manager_cannot_reject_main_booking(self):
        """Test manager cannot reject main booking"""
        self.client.login(username='manager', password='pass1234')
        response = self.client.post(reverse('booking_reject', kwargs={'booking_id': self.main_booking.id}))
        self.main_booking.refresh_from_db()
        self.assertEqual(self.main_booking.status, 'pending')
        self.assertEqual(response.status_code, 403)

    def test_chairman_can_approve_main_booking(self):
        """Test chairman can approve main booking"""
        self.client.login(username='chairman', password='pass1234')
        response = self.client.post(reverse('booking_approve', kwargs={'booking_id': self.main_booking.id}))
        self.main_booking.refresh_from_db()
        self.assertEqual(self.main_booking.status, 'approved')
        self.assertEqual(response.status_code, 302)

    def test_chairman_can_reject_main_booking(self):
        """Test chairman can reject main booking"""
        self.client.login(username='chairman', password='pass1234')
        response = self.client.post(reverse('booking_reject', kwargs={'booking_id': self.main_booking.id}))
        self.main_booking.refresh_from_db()
        self.assertEqual(self.main_booking.status, 'rejected')
        self.assertEqual(response.status_code, 302)
    
    def test_chairman_cannot_approve_astro_booking(self):
        """Test chairman cannot approve astro booking"""
        self.client.login(username='chairman', password='pass1234')
        response = self.client.post(reverse('booking_approve', kwargs={'booking_id': self.astro_booking.id}))
        self.astro_booking.refresh_from_db()
        self.assertEqual(self.astro_booking.status, 'pending')
        self.assertEqual(response.status_code, 403)

    def test_chairman_cannot_reject_astro_booking(self):
        """Test chairman cannot reject astro booking"""
        self.client.login(username='chairman', password='pass1234')
        response = self.client.post(reverse('booking_reject', kwargs={'booking_id': self.astro_booking.id}))
        self.astro_booking.refresh_from_db()
        self.assertEqual(self.astro_booking.status, 'pending')
        self.assertEqual(response.status_code, 403)
    
    def test_secretary_can_approve_main_booking(self):
        """Test secretary can approve main booking"""
        self.client.login(username='secretary', password='pass1234')
        response = self.client.post(reverse('booking_approve', kwargs={'booking_id': self.main_booking.id}))
        self.main_booking.refresh_from_db()
        self.assertEqual(self.main_booking.status, 'approved')
        self.assertEqual(response.status_code, 302)

    def test_secretary_can_reject_main_booking(self):
        """Test secretary can reject main booking"""
        self.client.login(username='secretary', password='pass1234')
        response = self.client.post(reverse('booking_reject', kwargs={'booking_id': self.main_booking.id}))
        self.main_booking.refresh_from_db()
        self.assertEqual(self.main_booking.status, 'rejected')
        self.assertEqual(response.status_code, 302)
    
    def test_secretary_cannot_approve_astro_booking(self):
        """Test secretary cannot approve astro booking"""
        self.client.login(username='secretary', password='pass1234')
        response = self.client.post(reverse('booking_approve', kwargs={'booking_id': self.astro_booking.id}))
        self.astro_booking.refresh_from_db()
        self.assertEqual(self.astro_booking.status, 'pending')
        self.assertEqual(response.status_code, 403)

    def test_secretary_cannot_reject_astro_booking(self):
        """Test secretary cannot reject astro booking"""
        self.client.login(username='secretary', password='pass1234')
        response = self.client.post(reverse('booking_reject', kwargs={'booking_id': self.astro_booking.id}))
        self.astro_booking.refresh_from_db()
        self.assertEqual(self.astro_booking.status, 'pending')
        self.assertEqual(response.status_code, 403)

    def test_anonymous_user_cannot_approve_astro_booking(self):
        """Test login required to approve Astro booking"""
        response = self.client.post(reverse('booking_approve', kwargs={'booking_id': self.astro_booking.id}))
        self.astro_booking.refresh_from_db()
        self.assertEqual(self.astro_booking.status, 'pending')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_anonymous_user_cannot_reject_astro_booking(self):
        """Test login required to reject Astro booking"""
        response = self.client.post(reverse('booking_reject', kwargs={'booking_id': self.astro_booking.id}))
        self.astro_booking.refresh_from_db()
        self.assertEqual(self.astro_booking.status, 'pending')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_anonymous_user_cannot_approve_main_booking(self):
        """Test login required to approve main booking"""
        response = self.client.post(reverse('booking_approve', kwargs={'booking_id': self.main_booking.id}))
        self.main_booking.refresh_from_db()
        self.assertEqual(self.main_booking.status, 'pending')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_anonymous_user_cannot_reject_main_booking(self):
        """Test login required to reject main booking"""
        response = self.client.post(reverse('booking_reject', kwargs={'booking_id': self.main_booking.id}))
        self.main_booking.refresh_from_db()
        self.assertEqual(self.main_booking.status, 'pending')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)



class PitchListViewTests(TestCase):
    def setUp(self):
        """Setup users and pitch for tests"""
        self.staff_user = User.objects.create_user(username='staff', password='pass1234', is_staff=True)
        self.normal_user = User.objects.create_user(username='normal', password='pass1234')
        self.pitch = Pitch.objects.create(name='Astro Pitch')

    def test_staff_user_sees_pitches(self):
        """Test staff user sees pitches"""
        self.client.login(username='staff', password='pass1234')
        response = self.client.get(reverse('pitch_list'))
        self.assertContains(response, 'Astro Pitch')

    def test_non_staff_user_sees_nothing(self):
        """Test non staff user does not see pitches"""
        self.client.login(username='normal', password='pass1234')
        response = self.client.get(reverse('pitch_list'))
        self.assertNotContains(response, 'Astro Pitch')
