from .models import Location,Job,Feedback,Worker,User,Comment
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

class LocationSerializer(ModelSerializer):
    class Meta:
        model=Location
        fields='__all__'
class JobSerializer(ModelSerializer):
    class Meta:
        model=Job
        fields="__all__"

class WorkerSerializer(serializers.Serializer):
    id=serializers.CharField(read_only=True)
    name = serializers.CharField()
    gender = serializers.CharField()
    age = serializers.IntegerField()
    job = serializers.CharField()
    location = serializers.CharField()
    phone = serializers.CharField()
    email = serializers.CharField()
    address = serializers.CharField()
    adhar_card = serializers.CharField()
    driving_licence = serializers.CharField()
    photo = serializers.ImageField()
    description = serializers.CharField()
    current_status = serializers.CharField()

    def create(self, validated_data):
        print(validated_data)
        location=validated_data['location']
        location_instance=Location.objects.get(dist=location)
        validated_data['location']=location_instance
        job=validated_data['job']
        job_instance=Job.objects.get(job_name=job)
        validated_data['job']=job_instance

        return Worker.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name=validated_data.get('name')
        instance.gender=validated_data.get('gender')
        instance.age = validated_data.get('age')
        job=validated_data.get('job')
        job_instance=Job.objects.get(job_name=job)
        instance.job=job_instance
        location=validated_data.get('location')
        location_instance= Location.objects.get(dist=location)
        instance.location = location_instance

        instance.phone=validated_data.get('phone')
        instance.email=validated_data.get('email')
        instance.address=validated_data.get('address')
        instance.adhar_card=validated_data.get('adhar_card')
        instance.driving_licence=validated_data.get('driving_licence')
        instance.photo=validated_data.get('photo')
        instance.description=validated_data.get('description')
        instance.current_status=validated_data.get('current_status')
        instance.save()
        return instance



class WorkerSearchSeraializer(serializers.Serializer):
    name = serializers.CharField()

    gender =serializers.CharField()
    age = serializers.IntegerField()
    job = serializers.CharField()
    location = serializers.CharField()
    phone = serializers.CharField()
    email = serializers.CharField()
    photo = serializers.ImageField()
    description = serializers.CharField()

    current_status =serializers.CharField()

class FeedbackSerializer(serializers.Serializer):
    customer_name = serializers.CharField()
    worker_name = serializers.CharField()
    feedback = serializers.CharField()
    content = serializers.CharField()
    # class Meta:
    #     model=Feedback
    #     fields='__all__'

class HireWorkersSerializer(serializers.Serializer):
    worker = serializers.CharField()
    address = serializers.CharField()
    location = serializers.CharField()
    customer = serializers.CharField()
    hire = serializers.CharField()
    days = serializers.IntegerField()
    customer_phone = serializers.CharField()


class CommentSerializer(serializers.Serializer):
    worker = serializers.CharField()
    user = serializers.CharField()
    content = serializers.CharField()

    def create(self, validated_data):
        worker=validated_data['worker']
        worker_instance=Worker.objects.get(name=worker)
        validated_data['worker']=worker_instance
        user=validated_data['user']
        user_instance=User.objects.get(username=user)
        validated_data['user']=user_instance
        return Comment.objects.create(**validated_data)

