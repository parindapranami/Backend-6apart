from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns =[
    path('', views.index, name='index'),


    # #REST auth
    # path('api-login',views.LoginView.as_view()),
    # path('api-logout',views.LogOutView.as_view()),
    # path('api-teacher-register',views.RegisterTeacherView.as_view()),
    # path('api-student-register',views.RegisterStudentView.as_view()),

    #Exam API

    #questionnaire
    
    path('questionnaire-get-create',views.QuestionnaireCreateGeneric.as_view()),
    path('questionnaire-update/<int:pk>',views.QuestionnaireGeneric.as_view()),
    
    #question

    path('question-get-create',views.QuestionCreateGeneric.as_view()),
    path('question-update/<int:pk>',views.QuestionGeneric.as_view()),
    
    #question options

    path('question-options-get-create',views.QuestionOptionCreateGeneric.as_view()),
    path('question-options-update/<int:pk>',views.QuestionOptionGeneric.as_view()),
    
    #Student Answers

    path('student-answers-get-create',views.StudentAnswerCreateGeneric.as_view()),
    path('student-answers-update/<int:pk>',views.StudentAnswerGeneric.as_view()),
    
    #Marks

    path('marks-get-create',views.MarksCreateGeneric.as_view()),
    path('marks-update/<int:pk>',views.MarksGeneric.as_view()),

    #REST Auth
    path('api-newuser-register',views.RegisterNewUserView.as_view()),
    path('api-newuser-login',views.LoginNewUserView.as_view()),
    path('api-logout',views.LogOutView.as_view()),

    path('video-get-create',views.SocialDistantView.as_view()),
] 

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)