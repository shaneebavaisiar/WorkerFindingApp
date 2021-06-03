from django.contrib import admin

from .models import Worker,HireWorkers,Job,Location,Feedback,Comment
admin.site.register(Worker)
admin.site.register(HireWorkers)
admin.site.register(Job)
admin.site.register(Location)
admin.site.register(Feedback)
admin.site.register(Comment)

