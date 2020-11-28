from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
# Create your models here.

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, username, first_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, username, first_name, password, **other_fields)

    def create_user(self, email, username, first_name, password, **other_fields):
        other_fields.setdefault('is_active', True)
        if not email:
            raise ValueError('You must provide an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username,
                          first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class NewUserModel(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    about = models.TextField(max_length=500, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name']

    def __str__(self):
        return self.username


class Questionnaire(models.Model):
    exam_topic = models.CharField(max_length=50)
    exam_description = models.CharField(max_length=150)
    total_marks = models.IntegerField()
    created = models.DateTimeField(default=timezone.now)
    questionnaire_owner = models.ForeignKey(NewUserModel, on_delete=models.CASCADE)
    # student_attempt = models.ForeignKey(NewUserModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.exam_topic

class Question(models.Model):
    question = models.CharField(max_length=200)
    marks = models.IntegerField()
    question_questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    # student_attempt_question = models.ForeignKey(NewUserModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.question

class QuestionOption(models.Model):
    option = models.CharField(max_length=200)
    is_correct = models.BooleanField()
    choice_for_question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.option

class StudentAnswer(models.Model):
    is_correct = models.BooleanField()
    solve_for_question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(QuestionOption, on_delete=models.CASCADE)
    student = models.ForeignKey(NewUserModel, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student.first_name

class Mark(models.Model):
    marks = models.IntegerField()
    mark_for_questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    student = models.ForeignKey(NewUserModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.student.first_name + " got " + str(self.marks)

class SocialDistantVideo(models.Model):
    title = models.CharField(max_length=100, blank=True)
    video = models.FileField(upload_to='videos/')

    class Meta:
        verbose_name = 'video'
        verbose_name_plural = 'videos'

    # def __str__(self):
    #     return self.title