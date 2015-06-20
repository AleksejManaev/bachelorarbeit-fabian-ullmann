# -*- coding: utf-8 -*-
import autofixture
from autofixture.autofixtures import UserFixture
from autofixture.generators import StaticGenerator
from django.contrib.auth.models import User
from autofixture import AutoFixture
from autofixture import generators
from mentoring.models import Student, Course, Tutor, Placement


class UsernameGenerator(StaticGenerator):
    def __init__(self, value, type, *args, **kwargs):
        self.type = type
        super(UsernameGenerator, self).__init__(value, *args, **kwargs)

    def generate(self):
        post = (len(Student.objects.all()) + 1) if self.type == 'student' else (len(Tutor.objects.all()) + 1)
        return "%s%s" % (super(UsernameGenerator, self).generate(), post)


class CourseFixture(AutoFixture):
    field_values = {
        'editing_time': generators.ChoicesGenerator(choices=Course.TIME_CHOICES)
    }


class MyUserFixture(UserFixture):
    def __init__(self, *args, **kwargs):
        self.type = kwargs.pop('type', 'student')
        self.username = kwargs.pop('username', None)
        self.password = kwargs.pop('password', None)
        super(UserFixture, self).__init__(*args, **kwargs)
        if self.username:
            self.field_values['username'] = UsernameGenerator(
                self.username, type=self.type)


class PlacementFixture(AutoFixture):
    field_values = {
        'report': generators.StaticGenerator('ullmanfa/placement/report/Arbeitszeugnis_Audi.pdf'),
        'presentation': generators.StaticGenerator('ullmanfa/placement/presentation/Arbeitszeugnis_Audi.pdf'),
        'certificate': generators.StaticGenerator('ullmanfa/placement/certificate/Arbeitszeugnis_Audi.pdf'),
    }


class MyStudentFixture(AutoFixture):
    field_values = {
        'user': MyUserFixture(User, type='student', username='student', password='student'),
        'title': '',
        'phone': '03092751522',
        'matriculation_number': generators.IntegerGenerator(min_value=20110000, max_value=20159999),
    }


class MyTutorFixture(AutoFixture):
    field_values = {
        'user': MyUserFixture(User, username='tutor', password='tutor', type='tutor'),
        'title': 'Prof. Dr.',
        'phone': '03092751522',

    }


autofixture.register(Course, CourseFixture)
autofixture.register(Student, MyStudentFixture)
autofixture.register(Tutor, MyTutorFixture)
autofixture.register(Placement, PlacementFixture)
