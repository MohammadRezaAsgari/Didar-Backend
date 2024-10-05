from django.urls import include, path

app_name = 'schedule'

urlpatterns = [
    path('v1/', include('schedule.api.v1.urls', namespace='v1')),
]
