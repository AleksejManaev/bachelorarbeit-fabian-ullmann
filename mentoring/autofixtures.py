# -*- coding: utf-8 -*-
from datetime import datetime

import autofixture
# from autofixture.autofixtures import UserFixture
from autofixture.generators import StaticGenerator
# from django.contrib.auth.models import User
from autofixture import AutoFixture
from autofixture import generators
from mentoring.models import Student, Course, Tutor, Placement, MentoringUser as User, PlacementSeminar, PlacementSeminarEntry

import string
from django.contrib.auth.hashers import make_password
from django.utils import timezone


class PlacementSeminarFixture(AutoFixture):
    field_values = {
        'placement_year': 2017,
    }


class UserFixture(AutoFixture):
    '''
    :class:`UserFixture` is automatically used by default to create new
    ``User`` instances. It uses the following values to assure that you can
    use the generated instances without any modification:

    * ``username`` only contains chars that are allowed by django's auth forms.
    * ``email`` is unique.
    * ``first_name`` and ``last_name`` are single, random words of the lorem
      ipsum text.
    * ``is_staff`` and ``is_superuser`` are always ``False``.
    * ``is_active`` is always ``True``.
    * ``date_joined`` and ``last_login`` are always in the past and it is
      assured that ``date_joined`` will be lower than ``last_login``.
    '''

    class Values(object):
        username = generators.StringGenerator(
            max_length=30,
            chars=string.ascii_letters + string.digits + '_')
        first_name = generators.LoremWordGenerator(1)
        last_name = generators.LoremWordGenerator(1)
        password = staticmethod(lambda: make_password(None))
        is_active = True
        # don't generate admin users
        is_staff = False
        is_superuser = False
        date_joined = generators.DateTimeGenerator(max_date=timezone.now())
        last_login = generators.DateTimeGenerator(max_date=timezone.now())

    # don't follow permissions and groups
    follow_m2m = False

    def __init__(self, *args, **kwargs):
        '''
        By default the password is set to an unusable value, this makes it
        impossible to login with the generated users. If you want to use for
        example ``autofixture.create_one('auth.User')`` in your unittests to have
        a user instance which you can use to login with the testing client you
        can provide a ``username`` and a ``password`` argument. Then you can do
        something like::

            autofixture.create_one('auth.User', username='foo', password='bar`)
            self.client.login(username='foo', password='bar')
        '''
        self.username = kwargs.pop('username', None)
        self.password = kwargs.pop('password', None)
        super(UserFixture, self).__init__(*args, **kwargs)
        if self.username:
            self.field_values['username'] = generators.StaticGenerator(
                self.username)

    def unique_email(self, model, instance):
        if User.objects.filter(email=instance.email).exists():
            raise autofixture.InvalidConstraint(('email',))

    def prepare_class(self):
        self.add_constraint(self.unique_email)

    def post_process_instance(self, instance, commit):
        # make sure user's last login was not before he joined
        changed = False
        if instance.last_login < instance.date_joined:
            instance.last_login = instance.date_joined
            changed = True
        if self.password:
            instance.set_password(self.password)
            changed = True
        if changed and commit:
            instance.save()
        return instance


class UsernameGenerator(StaticGenerator):
    def __init__(self, value, type, *args, **kwargs):
        self.type = type
        super(UsernameGenerator, self).__init__(value, *args, **kwargs)

    def generate(self):
        post = (len(Student.objects.all()) + 1) if self.type == 'student' else (len(Tutor.objects.all()) + 1)
        return "%s%s" % (super(UsernameGenerator, self).generate(), post)


class EmailGenerator(StaticGenerator):
    def __init__(self, *args, **kwargs):
        pass

    def generate(self):
        return 'test{number}@fh-brandenburg.de'.format(number=(len(User.objects.all()) + 1))


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
        self.field_values['email'] = EmailGenerator()


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
        'placement_year': 2017,
        'matriculation_number': generators.IntegerGenerator(min_value=20110000, max_value=20159999),
    }


class MyTutorFixture(AutoFixture):
    field_values = {
        'user': MyUserFixture(User, username='tutor', password='tutor', type='tutor'),
        'title': 'Prof. Dr.',
        'phone': '03092751522',
        'placement_responsible': True,
    }


class PlacementSeminarEntryFixture(AutoFixture):
    field_values = {
        'date': generators.DateTimeGenerator(min_date=datetime(2017, 1, 1), max_date=datetime(2018, 12, 31)),
    }


autofixture.register(User, UserFixture, fail_silently=True)
autofixture.register(Course, CourseFixture)
autofixture.register(Student, MyStudentFixture)
autofixture.register(Tutor, MyTutorFixture)
autofixture.register(Placement, PlacementFixture)
autofixture.register(PlacementSeminar, PlacementSeminarFixture)
autofixture.register(PlacementSeminarEntry, PlacementSeminarEntryFixture)
