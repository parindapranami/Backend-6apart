from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(NewUserModel)
admin.site.register(Questionnaire)
admin.site.register(Question)
admin.site.register(QuestionOption)
admin.site.register(StudentAnswer)
admin.site.register(Mark)


admin.site.register(SocialDistantVideo)
