
from django.shortcuts import render
from rest_framework.response import Response

from .serializers import LocationSerializer, JobSerializer, WorkerSerializer,\
    FeedbackSerializer,WorkerSearchSeraializer,HireWorkersSerializer,CommentSerializer
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework import mixins
from .models import *
from rest_framework.parsers import FormParser,MultiPartParser,JSONParser,FileUploadParser
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.authentication import TokenAuthentication
from django.core.mail import send_mail
from django.conf import settings
from twilio.rest import Client

from django.utils.decorators import method_decorator

# LOCATION SECTION



class LocationView(generics.GenericAPIView, mixins.ListModelMixin):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
class LocationCreate(generics.GenericAPIView, mixins.CreateModelMixin):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class ViewALocation(generics.GenericAPIView,mixins.RetrieveModelMixin):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

class ChangeALocation(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# LOCATION SECTION END

# JOB SECTION
class JobView(generics.GenericAPIView, mixins.ListModelMixin):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class JobCreate(generics.GenericAPIView,mixins.CreateModelMixin):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
class ViewAJob(generics.GenericAPIView, mixins.RetrieveModelMixin):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

class ChangeAJob(generics.GenericAPIView, mixins.UpdateModelMixin,mixins.DestroyModelMixin):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    queryset = Job.objects.all()
    serializer_class = JobSerializer


    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# JOB SECTION END

# WORKERS SECTION

class WorkerCreate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,)
    def get(self, request):
        worker = Worker.objects.all()
        serializer = WorkerSerializer(worker, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WorkerSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            gender = serializer.validated_data.get('gender')
            age = serializer.validated_data.get('age')
            job = serializer.validated_data.get('job')
            parent_job = Job.objects.get(job_name=job)
            location = serializer.validated_data.get('location')
            parent_location = Location.objects.get(dist=location)
            phone = serializer.validated_data.get('phone')
            email = serializer.validated_data.get('email')
            address = serializer.validated_data.get('address')
            adhar_card = serializer.validated_data.get('adhar_card')
            driving_licence = serializer.validated_data.get('driving_licence')
            photo = serializer.validated_data.get('photo')
            description = serializer.validated_data.get('description')
            current_status = serializer.validated_data.get('current_status')
            comments = serializer.validated_data.get('comments')
            serializer.save()
            return Response(serializer.data)
        return Response('failed')



class WorkerDetails(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request,id):
        worker=Worker.objects.get(id=id)
        serializer=WorkerSerializer(worker)
        return Response(serializer.data)

    def put(self,request,id):
        worker=Worker.objects.get(id=id)
        serializer=WorkerSerializer(worker,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=204)
        return Response(serializer.errors,status=401)

    def delete(self,request,id):
        worker=Worker.objects.get(id=id)
        worker.delete()
        return Response('deleted',status=status.HTTP_200_OK)

# END WORKER SECTION

# SEARCH SECTION

class WorkerSearch(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request,desig_location_available):
        emp=Worker.objects.filter(Q(job__job_name=desig_location_available) |Q(location__dist=desig_location_available)|Q(current_status=desig_location_available))
        serializer=WorkerSearchSeraializer(emp,many=True)
        return Response(serializer.data)

class FeedbackView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    def get(self,request):
        feedbck=Feedback.objects.all()
        serializer=FeedbackSerializer(feedbck,many=True)
        return Response(serializer.data)

class FeedbackCreate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        serializer=FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            customer_name=serializer.validated_data.get('customer_name')
            parent_customer=User.objects.get(username=customer_name)
            worker_name=serializer.validated_data.get('worker_name')
            parent_worker=Worker.objects.get(name=worker_name)
            feedback=serializer.validated_data.get('feedback')
            content=serializer.validated_data.get('content')
            feed=Feedback(customer_name=parent_customer,worker_name=parent_worker,feedback=feedback,content=content)
            feed.save()
            return Response('sucess')
        return Response('failed')

class HireWorkerView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        hirework=HireWorkers.objects.all()
        serializer=HireWorkersSerializer(hirework,many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer=HireWorkersSerializer(data=request.data)
        if serializer.is_valid():
            worker= serializer.validated_data.get('worker')
            parent_worker=Worker.objects.get(name=worker)
            address=serializer.validated_data.get('address')
            location=serializer.validated_data.get('location')
            parent_location=Location.objects.get(dist=location)
            customer=serializer.validated_data.get('customer')
            parent_customer=User.objects.get(username=customer)
            hire=serializer.validated_data.get('hire')
            days=serializer.validated_data.get('days')
            customer_phone=serializer.validated_data.get('customer_phone')
            emails=parent_worker.email
            worker_phone=parent_worker.phone
            print(emails)
            hireworker=HireWorkers(worker=parent_worker,address=address,location=parent_location,
                                   customer=parent_customer,customer_phone=customer_phone,hire=hire,days=days)
            hireworker.save()
            msg = f'you have a {days} day invitation for job.' \
                  f'custormer address:{customer}, {address}, ' \
                  f'phone:{customer_phone}'

            send_mail('WorkerFindgingApp', msg, settings.EMAIL_HOST_USER, [emails], fail_silently=False)
            # return Response({"Hello user": str(amount) + ' has been debited and available balance:' + str(acc.balance)})

            # send sms to worker phone number
            account_sid = 'AC17948d4503e49067e302cd12f0ea34ce'
            auth_token = '78f7ce4ab44156220b43b866da026173'
            client = Client(account_sid, auth_token)

            message = client.messages.create(
                body=f'you have a {days} day invitation for job.' \
                  f'custormer address:{customer}, {address}, ' \
                  f'phone:{customer_phone}',
                from_='(608) 728-7240',
                to=f'{worker_phone}'
            )

            print(message.sid)
            return Response({"send sms to": str(worker_phone) + ' and email to:  ' + str(emails)})


class CommentCreate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        comments=Comment.objects.all()
        serializer=CommentSerializer(comments,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer=CommentSerializer(data=request.data)
        if serializer.is_valid():
            worker=serializer.validated_data.get('worker')
            user=serializer.validated_data.get('user')
            content=serializer.validated_data.get('content')
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)