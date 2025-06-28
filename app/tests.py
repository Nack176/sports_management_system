from django.test import TestCase, Client
from django.urls import reverse
from app.models import CustomUser, Sport, Session_Year, Student, Staff, Tournament
from django.contrib.auth import get_user_model

class BaseTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_model = get_user_model()
        # Create a Hod user
        self.hod_user = self.user_model.objects.create_user(
            username='hoduser',
            email='hod@example.com',
            password='password123',
            user_type='1'
        )
        # Create a Staff user
        self.staff_user = self.user_model.objects.create_user(
            username='staffuser',
            email='staff@example.com',
            password='password123',
            user_type='2'
        )
        # Create a Student user
        self.student_user = self.user_model.objects.create_user(
            username='studentuser',
            email='student@example.com',
            password='password123',
            user_type='3'
        )
        # Create Sport and Session_Year for testing
        self.sport = Sport.objects.create(name='Football')
        self.session_year = Session_Year.objects.create(session_start='2023-01-01', session_end='2023-12-31')

class AuthenticationTests(BaseTestCase):
    def test_login_logout(self):
        login_url = reverse('doLogin')
        response = self.client.post(login_url, {'email': 'hod@example.com', 'password': 'password123'})
        self.assertEqual(response.status_code, 302)  # Redirect on success
        logout_url = reverse('logout')
        response = self.client.get(logout_url)
        self.assertEqual(response.status_code, 302)  # Redirect on logout

class HodPanelTests(BaseTestCase):
    def test_add_student(self):
        self.client.login(username='hoduser', password='password123')
        add_student_url = reverse('add_student')
        response = self.client.get(add_student_url)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(add_student_url, {
            'first_name': 'Test',
            'last_name': 'Student',
            'email': 'teststudent@example.com',
            'username': 'teststudent',
            'password': 'password123',
            'address': '123 Street',
            'gender': 'Male',
            'sport_id': self.sport.id,
            'session_year_id': self.session_year.id,
        })
        self.assertEqual(response.status_code, 302)  # Redirect after add

    def test_view_student(self):
        self.client.login(username='hoduser', password='password123')
        view_student_url = reverse('view_student')
        response = self.client.get(view_student_url)
        self.assertEqual(response.status_code, 200)

    # Additional tests for edit, update, delete student, staff, sport, tournament, session can be added similarly

class StaffPanelTests(BaseTestCase):
    def test_staff_home(self):
        self.client.login(username='staffuser', password='password123')
        staff_home_url = reverse('staff_home')
        response = self.client.get(staff_home_url)
        self.assertEqual(response.status_code, 200)

    # Additional tests for notifications, leave, feedback, attendance can be added similarly

class StudentPanelTests(BaseTestCase):
    def test_student_home(self):
        self.client.login(username='studentuser', password='password123')
        student_home_url = reverse('student_home')
        response = self.client.get(student_home_url)
        self.assertEqual(response.status_code, 200)

    # Additional tests for notifications, feedback, leave, attendance can be added similarly
