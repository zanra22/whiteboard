from django.http import HttpResponse
from django.shortcuts import render, redirect
from accounts.models import User

from courses.forms import AddCourseForm, AddLessonForm, EnrollForm, AddFeedbackForm
from courses.models import Course, Lesson, Feedback

import random


def courses(request):
    user = User.objects.get(id=request.user.id)

    if not request.user.is_authenticated:
        return redirect('loginpage')

    if user.is_student:
        return render(request, "courses/student-courses.html", {
            'courses': user.courses.values(),
        })

    if request.GET.get('search'):
        search = request.GET.get('search')
        courses = Course.objects.filter(title__contains=search)
        return render(request, "courses/courses.html", {'courses': courses})

    if request.user.is_admin:
        courses = Course.objects.all()
        return render(request, "courses/courses.html", {'courses': courses})

    if user.is_professor:
        courses = Course.objects.filter(creator=user.id)
        return render(request, "courses/courses.html", {"courses": courses})


def course_people(request, id):
    course = Course.objects.get(id=id)
    context = {
        'course': course,
        'students': course.students.all(),
    }
    return render(request, "courses/people.html", context)


def enroll_course(request):
    if request.method == "POST":
        try:
            form = EnrollForm(request.POST)
            user = User.objects.get(id=request.user.id)
            key = str(request.POST.get('key'))
            new_course = Course.objects.get(key=key)
            user.courses.add(new_course)
            new_course.students.add(user)
            user.save()
            new_course.save()
            return redirect('coursepage')
        except:
            response = HttpResponse(status=302)
            response['Location'] = '/course/enroll/?error=302'
            return response

    if request.GET.get('error'):
        error = int(request.GET.get('error'))
        if error == 302:
            error = 'Incorrect Course Code. Please try again.'
    else:
        error = ''

    form = EnrollForm()
    context = {
        'form': form,
        'error': error,
    }

    return render(request, "courses/enroll-course.html", context)


def unenroll_course(request, id):
    user = User.objects.get(id=request.user.id)
    course = Course.objects.get(id=id)
    user.courses.remove(course)
    user.save()
    return redirect('homepage')


def create_course_key(creator, title, desc, sched):
    string = creator[:5] + title + desc[:5] + sched[:5]
    l_string = list(string)
    random.shuffle(l_string)
    return "".join(l_string)


def add_course(request):
    form = AddCourseForm()
    if request.method == "POST":
        form = AddCourseForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.creator = request.user
            instance.key = create_course_key(
                instance.creator.email,
                instance.title,
                instance.description,
                instance.schedule
            ).strip()
            instance.save()
            return render(request, "courses/successcourse.html", {
                'form1': form,
                'key': instance.key,
            })
    form = AddCourseForm()
    return render(request, "courses/addcourse.html", {'form': form})


def update_course(request, id):
    course = Course.objects.get(id=id)

    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        course.title = title
        course.description = description
        course.save()
        return redirect('detailed', id)

    context = {
        'course': course
    }
    return render(request, 'courses/editcourse.html', context)


def delete_course(request, id):
    course = Course.objects.get(id=id)
    course.delete()
    return redirect("coursepage")


def course_details_page(request, id):
    course = Course.objects.get(id=id)
    context = {
        'course': course,
        'lessons': course.lessons.values(),
    }

    return render(request, "courses/detail.html", context)


def lesson_page(request, id):
    lesson = Lesson.objects.get(id=id)
    if request.user.is_authenticated:
        return render(request, "lessons/lessons.html", {'lesson': lesson})
    else:
        return redirect('loginpage')


def add_lesson(request, id):
    course = Course.objects.get(id=id)
    if request.method == "POST":
        form = AddLessonForm(request.POST)
        new_lesson = Lesson.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            description1=request.POST.get('description1'),
        )
        course.lessons.add(new_lesson)
        if form.is_valid():
            course.save()

        return redirect('homepage')
    form = AddLessonForm()
    context = {
        'form': form,
        'course': course,
    }

    return render(request, "lessons/addlessons.html", context)


def delete_lesson(request, id):
    lesson = Lesson.objects.get(id=id)
    lesson.delete()
    return redirect('coursepage')

def schedule_student(request):

    user = User.objects.get(id=request.user.id)

    if not request.user.is_authenticated:
        return redirect('loginpage')

    if user.is_student:
        return render(request, "schedule/schedule_student.html", {
            'courses': user.courses.values(),
        })

def feedback_page(request, id):
    course = Course.objects.get(id=id)
    context = {
        'course': course,
        'feedback': course.feedbacks.all(),
    }
    return render(request, "feedback/feedback.html", context)

def add_feedback(request, id):
    course = Course.objects.get(id=id)
    if request.method == "POST":
        form = AddLessonForm(request.POST)
        new_feedback = Feedback.objects.create(
            feedback_title=request.POST.get('title'),
            feedback_description=request.POST.get('description'),
            feedback_creator=request.user
        )
        course.feedbacks.add(new_feedback)
        if form.is_valid():
            course.save()

        return redirect('homepage')
    form = AddFeedbackForm()
    context = {
        'form': form,
        'course': course,
    }

    return render(request, "feedback/addfeedback.html", context)

def delete_feedback(request, id):
    feedback = Feedback.objects.get(id=id)
    feedback.delete()
    return redirect('coursepage')

# def activity_page(request, id):
#     course = Course.objects.get(id=id)
#     context = {
#         'course': course,
#         'students': course.students.all(),
#     }
#     return render(request, "activity/activity.html", context)