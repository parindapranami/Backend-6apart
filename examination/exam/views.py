from django.shortcuts import render, redirect
from django.contrib.auth.models import auth

#REST Auth
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.http import HttpResponse

#serializers
from .serializers import *
import numpy as np
import cv2
import imutils
import os
import time

def index(request):
    return render(request, 'index.html')




from rest_framework.authentication import TokenAuthentication

# class LoginView(APIView):
#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data["user"]
#         auth.login(request,user)
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({
#             'token': token.key,
#         }, status=200)


class LoginNewUserView(APIView):
    def post(self, request):
        serializer = LoginNewUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        auth.login(request,user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
        }, status=200)

class RegisterNewUserView(APIView):
    def post(self, request):
        serializer = RegisterNewUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        user.save()
        return Response({
            'mssg': " registered",
        }, status=200)

class LogOutView(APIView):
    authentication_classes=(TokenAuthentication,)

    def post(self,request):
        auth.logout(request)
        return Response(status=204)
    
# class RegisterTeacherView(APIView):
#     def post(self, request):
#         serializer = RegisterTeacherSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data["user"]
#         user.save()
#         return Response({
#             'mssg': " registered",
#         }, status=200)

# class RegisterStudentView(APIView):
#     def post(self, request):
#         serializer = RegisterStudentSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data["user"]
#         user.save()
#         return Response({
#             'mssg': " registered",
#         }, status=200)



from rest_framework import generics

#Questionnaire

class QuestionnaireCreateGeneric(generics.ListCreateAPIView):
    queryset = Questionnaire.objects.all()
    serializer_class = QuestionnaireSerializer


class QuestionnaireGeneric(generics.RetrieveUpdateDestroyAPIView):
    queryset = Questionnaire.objects.all()
    serializer_class = QuestionnaireSerializer

#Question

class QuestionCreateGeneric(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class QuestionGeneric(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

#Question Options

class QuestionOptionCreateGeneric(generics.ListCreateAPIView):
    queryset = QuestionOption.objects.all()
    serializer_class = QuestionOptionSerializer


class QuestionOptionGeneric(generics.RetrieveUpdateDestroyAPIView):
    queryset = QuestionOption.objects.all()
    serializer_class = QuestionOptionSerializer

#Student Answer

class StudentAnswerCreateGeneric(generics.ListCreateAPIView):
    queryset = StudentAnswer.objects.all()
    serializer_class = StudentAnswerSerializer


class StudentAnswerGeneric(generics.RetrieveUpdateDestroyAPIView):
    queryset = StudentAnswer.objects.all()
    serializer_class = StudentAnswerSerializer

#Marks

class MarksCreateGeneric(generics.ListCreateAPIView):
    queryset = Mark.objects.all()
    serializer_class = MarkSerializer


class MarksGeneric(generics.RetrieveUpdateDestroyAPIView):
    queryset = Mark.objects.all()
    serializer_class = MarkSerializer





import numpy as np
import cv2
import imutils
import os
import time


def Check(a,  b):
    dist = ((a[0] - b[0]) ** 2 + 550 / ((a[1] + b[1]) / 2) * (a[1] - b[1]) ** 2) ** 0.5
    calibration = (a[1] + b[1]) / 2       
    if 0 < dist < 0.25 * calibration:
        return True
    else:
        return False

def Setup(yolo):
    global net, ln, LABELS
    weights = os.path.sep.join([yolo, "yolov3.weights"])
    config = os.path.sep.join([yolo, "yolov3.cfg"])
    labelsPath = os.path.sep.join([yolo, "coco.names"])
    LABELS = open(labelsPath).read().strip().split("\n")  
    net = cv2.dnn.readNetFromDarknet(config, weights)
    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

def ImageProcess(image):
    global processedImg
    (H, W) = (None, None)
    frame = image.copy()
    if W is None or H is None:
        (H, W) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    starttime = time.time()
    layerOutputs = net.forward(ln)
    stoptime = time.time()
    print("Video is Getting Processed at {:.4f} seconds per frame".format((stoptime-starttime))) 
    confidences = []
    outline = []
    
    for output in layerOutputs:
        for detection in output:
            scores = detection[5:]
            maxi_class = np.argmax(scores)
            confidence = scores[maxi_class]
            if LABELS[maxi_class] == "person":
                if confidence > 0.5:
                    box = detection[0:4] * np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype("int")
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))
                    outline.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))

    box_line = cv2.dnn.NMSBoxes(outline, confidences, 0.5, 0.3)

    if len(box_line) > 0:
        flat_box = box_line.flatten()
        pairs = []
        center = []
        status = [] 
        for i in flat_box:
            (x, y) = (outline[i][0], outline[i][1])
            (w, h) = (outline[i][2], outline[i][3])
            center.append([int(x + w / 2), int(y + h / 2)])
            status.append(False)

        for i in range(len(center)):
            for j in range(len(center)):
                close = Check(center[i], center[j])

                if close:
                    pairs.append([center[i], center[j]])
                    status[i] = True
                    status[j] = True
        index = 0

        for i in flat_box:
            (x, y) = (outline[i][0], outline[i][1])
            (w, h) = (outline[i][2], outline[i][3])
            if status[index] == True:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 150), 2)
            elif status[index] == False:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            index += 1
        for h in pairs:
            cv2.line(frame, tuple(h[0]), tuple(h[1]), (0, 0, 255), 2)
    processedImg = frame.copy()

def driverFunction(pic):     
    create = None
    frameno = 0
    filename = pic
    yolo = "models/yolo-coco/"
    opname = filename[:-4] + "-output" + '.mp4'
    cap = cv2.VideoCapture(filename)
    

    time1 = time.time()
    while(True):

        ret, frame = cap.read()
        
        if not ret:
            break
        current_img = frame.copy()
        current_img = imutils.resize(current_img, width=480)
        video = current_img.shape
        frameno += 1

        if(frameno%2 == 0 or frameno == 1):
            Setup(yolo)
            ImageProcess(current_img)
            Frame = processedImg

            if create is None:
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                create = cv2.VideoWriter(opname, -1, 30, (Frame.shape[1], Frame.shape[0]), True)
        create.write(Frame)
        cv2.imshow('Ouput',Frame)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            break
    time2 = time.time()
    print("Completed. Total Time Taken: {} minutes".format((time2-time1)/60))
    
    cap.release()
    cv2.destroyAllWindows()
    
    return create
    
#driverFunction("input.mp4")

class SocialDistantView(APIView):
    def post(self, request):
        import base64
        serializer = SocialDistantVideoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        vid = SocialDistantVideo.objects.latest('id')
        
        print(vid.video.url)
        #vid_url = vid.video.url.lstrip()
        driverFunction("." + vid.video.url)
        file_path = '.' + vid.video.url[:-4] + "-output" + '.mp4'
        FilePointer = open(file_path,"rb")
        report_encoded = base64.b64encode(FilePointer.read())
        # response = Response(FilePointer.read(),content_type='video/mp4',status=200)
        # response['Content-Disposition'] = 'attachment; filename=' + file_path.split('/')[-1]
        # return response
        return Response({
            'message':'File upload success',
            'media_url':'.' + vid.video.url[:-4] + "-output" + '.mp4',
            'resp':report_encoded
        },status=200)


    
    

