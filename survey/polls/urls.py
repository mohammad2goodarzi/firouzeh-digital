from django.urls import path, include

urlpatterns = [
    path("api/v1/", include('polls.api.v1.urls', namespace='v1')),
]
