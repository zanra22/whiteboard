from django.test import TestCase

from accounts.models import User


class AccountTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        prof = User.objects.create(
            first_name='Prof', last_name='Prof', email='123@gmail.com', admin=False, student=False, professor=True)
        student = User.objects.create(
            first_name='Student', last_name='Student', email='stud@gmail.com', admin=False, student=True, professor=False)

        return super().setUpTestData()

    def test_admin_default(self):
        user = User.objects.get(id=1)
        default = user._meta.get_field('admin').default
        self.assertEqual(default, False)

    def test_student_default(self):
        user = User.objects.get(id=1)
        default = user._meta.get_field('student').default
        self.assertEqual(default, False)

    def test_professor_default(self):
        user = User.objects.get(id=1)
        default = user._meta.get_field('professor').default
        self.assertEqual(default, False)


class LoginFormTestCase(TestCase):
    def setUp(self):
        prof = User.objects.create(
            first_name='Prof', last_name='Prof', password='123', email='123@gmail.com', admin=False, student=False, professor=True)
        prof.save()

    def test_login_template(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'auth/login.html')


class RegisterFormTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        return super().setUpTestData()

    def test_register_template(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/register.html')


class HomePageTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        return super().setUpTestData()

    def test_unauthenticated_redirect(self):
        response = self.client.get('/')
        self.assertRedirects(response, '/login/')
