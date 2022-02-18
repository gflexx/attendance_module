from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.db import models

from rest_framework.authtoken.models import Token
from neo4j import graph, LecturerNode, StudentNode, CourseNode

from .utils import course_code_extractor

# manager for user methods
class UserManager(BaseUserManager):
    def create_user(self, email, full_name, reg_number=None, staff_id=None, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address.')

        if not full_name:
            raise ValueError("Your full name is required.")

        # create base user
        if not reg_number and not staff_id:
            user = self.model(
                email=self.normalize_email(email),
                full_name=full_name,
            )

        # create student if reg number
        if reg_number:
            user = self.model(
                email=self.normalize_email(email),
                full_name=full_name,
                reg_number=reg_number
            )

        # create lecturer if staff id
        if staff_id:
            user = self.model(
                email=self.normalize_email(email),
                full_name=full_name,
                staff_id=staff_id
            )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None):
        user = self.create_user(
            email,
            full_name=full_name,
            password=password,
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

# user model
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    full_name = models.CharField(max_length=252)
    image = models.ImageField(upload_to='users/%Y/%m', default='users.png')
    staff_id = models.CharField(
        max_length=18, 
        blank=True, 
        null=True,
        unique=True
    )
    reg_number = models.CharField(
        max_length=18, 
        blank=True, 
        null=True,
        unique=True
    )

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    # check if student by checking for reg number
    @property
    def is_student(self):
        if self.reg_number is not None:
            return True

    # check if lecture by checking for staff id
    @property
    def is_lecturer(self):
        if self.staff_id is not None:
            return True

# create token when user is registered
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

# add student or lecturer neo4j node
@receiver(post_save, sender=User)
def create_neo_node(sender, instance=None, created=False, **kwargs):
    if created:
        user = instance

        # create student node
        if user.is_student:
            reg_num = user.reg_number
            stdnt = StudentNode()
            stdnt.full_name = user.full_name
            stdnt.reg_number = reg_num
            graph.create(stdnt)

            # add student to course node
            course_code = course_code_extractor(reg_num)
            course = CourseNode.match(graph, course_code).first()
            course.students.add(stdnt)
            graph.push(course)

            # add course to student
            stdnt.student_of.add(course)
            graph.push(stdnt)

        # create lecturer node
        elif user.is_lecturer:
            full_name = user.full_name
            staff_id = user.staff_id
            lec = LecturerNode()
            lec.full_name = full_name
            lec.staff_id = staff_id
            graph.create(lec)

        else:
            pass
