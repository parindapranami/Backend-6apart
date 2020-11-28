from rest_framework import serializers,exceptions
from .models import *
from django.contrib.auth import models,authenticate

# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField()

#     def validate(self,data):
#         username = data.get("username","")
#         password = data.get("password","")

#         if username and password:
#             user = authenticate(username=username, password=password)
#             if user:
#                 if user.is_active:
#                     data["user"] = user
#                 else:
#                     msg = "User is deactivated"
#                     raise exceptions.ValidationError(msg)
#             else:
#                 msg = "Can't Login"
#                 raise exceptions.ValidationError(msg)
#         else:
#             msg="Must provide username and password both"
#             raise exceptions.ValidationError(msg)
#         return data

# class RegisterTeacherSerializer(serializers.Serializer):
#     fname = serializers.CharField()
#     lname = serializers.CharField()
#     username = serializers.CharField()
#     email = serializers.EmailField()
#     password1 = serializers.CharField()
#     password2 = serializers.CharField()


#     def validate(self,data):
#         fname =  data.get("fname","")
#         lname = data.get("lname","")
#         username =  data.get("username","")
#         email = data.get("email","")
#         password1 =  data.get("password1","")
#         password2 =  data.get("password2","")

#         if password1 == password2:
#             if models.User.objects.filter(username=username).exists():
#                 msg = "Username exists"
#                 raise exceptions.ValidationError(msg)
#             elif models.User.objects.filter(email=email).exists():
#                 msg = "email exists"
#                 raise exceptions.ValidationError(msg)
#             else:
#                 user = models.User.objects.create_user(
#                     username=username, email=email, password=password1, first_name=fname, last_name=lname)
#                 # user.save()
#                 data["user"]=user
#         else:
#             msg = "Passwords didnt match"
#             raise exceptions.ValidationError(msg)
#         return data


# class RegisterStudentSerializer(serializers.Serializer):
#     fname = serializers.CharField()
#     lname = serializers.CharField()
#     username = serializers.CharField()
#     email = serializers.EmailField()
#     password1 = serializers.CharField()
#     password2 = serializers.CharField()
#     rollno = serializers.IntegerField()


#     def validate(self,data):
#         fname =  data.get("fname","")
#         lname = data.get("lname","")
#         username =  data.get("username","")
#         email = data.get("email","")
#         password1 =  data.get("password1","")
#         password2 =  data.get("password2","")
#         rollno =  data.get("rollno","")

#         if password1 == password2:
#             if models.User.objects.filter(username=username).exists():
#                 msg = "Username exists"
#                 raise exceptions.ValidationError(msg)
#             elif models.User.objects.filter(email=email).exists():
#                 msg = "email exists"
#                 raise exceptions.ValidationError(msg)
#             elif models.User.objects.filter(rollno=rollno).exists():
#                 msg = "roll number exists"
#                 raise exceptions.ValidationError(msg)
#             else:
#                 user = models.User.objects.create_user(
#                     username=username, email=email, password=password1, first_name=fname, last_name=lname, rollno=rollno)
#                 # user.save()
#                 data["user"]=user
#         else:
#             msg = "Passwords didnt match"
#             raise exceptions.ValidationError(msg)
#         return data

class LoginNewUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self,data):
        email = data.get("email","")
        password = data.get("password","")

        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                if user.is_active:
                    data["user"] = user
                else:
                    msg = "User is deactivated"
                    raise exceptions.ValidationError(msg)
            else:
                msg = "Can't Login"
                raise exceptions.ValidationError(msg)
        else:
            msg="Must provide username and password both"
            raise exceptions.ValidationError(msg)
        return data

class RegisterNewUserSerializer(serializers.Serializer):
    fname = serializers.CharField()
    username = serializers.CharField()
    email = serializers.EmailField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()


    def validate(self,data):
        fname =  data.get("fname","")
        username =  data.get("username","")
        email = data.get("email","")
        password1 =  data.get("password1","")
        password2 =  data.get("password2","")

        if password1 == password2:
            if NewUserModel.objects.filter(username=username).exists():
                msg = "Username exists"
                raise exceptions.ValidationError(msg)
            elif NewUserModel.objects.filter(email=email).exists():
                msg = "email exists"
                raise exceptions.ValidationError(msg)
            else:
                user = NewUserModel.objects.create_user(
                    username=username, email=email, password=password1, first_name=fname)
                # user.save()
                data["user"]=user
        else:
            msg = "Passwords didnt match"
            raise exceptions.ValidationError(msg)
        return data


class QuestionnaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questionnaire
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class QuestionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionOption
        fields = '__all__'

class StudentAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAnswer
        fields = '__all__'

class MarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mark
        fields = '__all__'

class SocialDistantVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialDistantVideo
        fields = '__all__'