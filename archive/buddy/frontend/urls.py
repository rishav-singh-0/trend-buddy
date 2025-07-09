from django.urls import path, include
from .views import index

urlpatterns = [
    path('/', include('api.data.urls')),
    # path("", index, name="index"),

]