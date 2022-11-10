from django.test import TestCase
from accounts.models import User

from courses.models import Course, Lesson


class CoursesTestCases(TestCase):

    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        creator = User.objects.create(
            first_name='Prof', last_name='Prof', email='123@gmail.com', admin=False, student=False, professor=True)
        lesson = Lesson.objects.create(
            title='Graph Theory',
            description='asdfasdfasjdkfgasdfj'
        )
        course = Course.objects.create(
            title='OOP', description='aksjfasdkfjahsdfas', key='asdfasfsdfO23Op', creator=creator)
        course.lessons.add(lesson)

    def test_title_default(self):
        course = Course.objects.get(id=1)
        default = course._meta.get_field('title').default
        self.assertEqual(default, '')

    def test_title_max_length(self):
        course = Course.objects.get(id=1)
        max_length = course._meta.get_field('title').max_length
        self.assertEqual(max_length, 50)

    def test_description_default(self):
        course = Course.objects.get(id=1)
        default = course._meta.get_field('description').default
        self.assertEqual(default, '')

    def test_description_max_length(self):
        course = Course.objects.get(id=1)
        max_length = course._meta.get_field('description').max_length
        self.assertEqual(max_length, 200)

    def test_key_max_length(self):
        course = Course.objects.get(id=1)
        max_length = course._meta.get_field('key').max_length
        self.assertEqual(max_length, 100)

    def test_key_unique(self):
        course = Course.objects.get(id=1)
        unique = course._meta.get_field('key').unique
        self.assertEqual(unique, True)

    def test_lessons_many_to_many_rel(self):
        course = Course.objects.get(id=1)
        many_to_many = course._meta.get_field('lessons').verbose_name
        self.assertEqual(many_to_many, 'lessons')

    def test_students_many_to_many_rel(self):
        course = Course.objects.get(id=1)
        many_to_many = course._meta.get_field('students').verbose_name
        self.assertEqual(many_to_many, 'students')

    def test_course_str_value(self):
        course = Course.objects.get(id=1)
        self.assertEqual(str(course), course.title)

    def test_lesson_title_max_length(self):
        lesson = Lesson.objects.get(id=1)
        max_length = lesson._meta.get_field('title').max_length
        self.assertLess(max_length, 51)

    def test_lesson_description_max_length(self):
        lesson = Lesson.objects.get(id=1)
        max_length = lesson._meta.get_field('description').max_length
        self.assertLess(max_length, 201)

    def test_lesson_str_value(self):
        lesson = Lesson.objects.get(id=1)
        self.assertEqual(str(lesson), lesson.title)
