
from django.urls import path,include
from django.contrib import admin
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/workers/v1/',include('accounts.urls')),
    path('api/workers/v1/',include('workers.urls'))
]
