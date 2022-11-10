
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as logout
from .views import home_page, update_record, list_user, update, delete, my_info_page
from accounts.views import loginpage, registerpage, logout_view
from django.contrib import admin
from django.urls import path

from courses.views import course_details_page, course_people, courses, enroll_course, add_course, unenroll_course, \
    update_course, delete_course, add_lesson, lesson_page, delete_lesson, schedule_student, feedback_page, \
    delete_feedback, add_feedback

urlpatterns = [
    path('', home_page, name='homepage'),
    path('logout/', logout.LogoutView.as_view(template_name="auth/logout.html"),
         name='logoutpage'),
    path('test/', logout_view, name='test-logout'),
    path('login/', loginpage, name='loginpage'),
    path('register/', registerpage, name="registerpage"),
    path('admin/', admin.site.urls),
    path('infopage/', my_info_page, name="myinfopage"),

    path('users/', list_user, name='list_user'),
    path('update/updaterecord/<int:id>', update_record, name='updaterecord'),
    path('update/<int:id>', update, name='update'),
    path('delete/<int:id>', delete, name='delete'),

    path('course/', courses, name="coursepage"),
    path('course/enroll/', enroll_course, name="enrollCourse"),
    path('course/unenroll/<int:id>', unenroll_course, name="unenrollCourse"),
    path('course/<int:id>', course_details_page, name='detailed'),
    path('course/<int:id>/people', course_people, name='people'),
    path('course/<int:id>/feedback', feedback_page, name='feedback'),
    # path('course/<int:id>/activity', activity_page, name='activity'),
    path('course/addfeedback/<int:id>', add_feedback, name="addfeedbackpage"),
    path('deletelessons/<int:id>', delete_feedback, name="deletefeedback"),
    path('course/addlesson/<int:id>', add_lesson, name="addlessonpage"),
    path('addcourse/', add_course, name="addcoursepage"),
    path('editcourse/<int:id>', update_course, name="editcoursepage"),
    path('deletecourse/<int:id>', delete_course, name="deletecourse"),

    path('schedule', schedule_student, name="schedule"),

    path('lessons/<int:id>', lesson_page, name="lessonspage"),
    path('deletelessons/<int:id>', delete_lesson, name="deletelessons"),
]


if settings.DEBUG:
    urlpatterns = urlpatterns + \
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + \
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
