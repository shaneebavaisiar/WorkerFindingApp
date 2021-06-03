from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import LocationCreate,JobCreate,WorkerCreate,\
    WorkerDetails,WorkerSearch,FeedbackCreate,FeedbackView,HireWorkerView,\
    CommentCreate,JobView,LocationView,ViewALocation,ChangeALocation,ViewAJob,ChangeAJob

urlpatterns = [

    path('location_create/',LocationCreate.as_view()),
    path('location_view/',LocationView.as_view()),
    path('view_a_location/<int:pk>',ViewALocation.as_view()),
    path('change_a_location/<int:pk>',ChangeALocation.as_view()),
    path('job_create/',JobCreate.as_view()),
    path('job_view/',JobView.as_view()),
    path('view_a_job/<int:pk>',ViewAJob.as_view()),
    path('change_a_job/<int:pk>',ChangeAJob.as_view()),
    path('worker/',WorkerCreate.as_view()),
    path('worker/<int:id>',WorkerDetails.as_view()),
    path('worker/<str:desig_location_available>/',WorkerSearch.as_view()),
    path('feedback_view/',FeedbackView.as_view()),
    path('feedback_create/',FeedbackCreate.as_view()),
    path('hireworker/',HireWorkerView.as_view()),
    path('comment/',CommentCreate.as_view())


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
