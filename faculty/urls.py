from django.urls import include, path

app_name = 'faculty'

urlpatterns = [
    path('v1/', include('faculty.api.v1.urls', namespace='v1')),
]
