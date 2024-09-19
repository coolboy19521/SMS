from django.urls import path
from .views import home, project, us

urlpatterns = [
    path('', view = home, name = 'home'),
    path('project', view = project, name = 'project'),
    path('us', view = us, name = 'us'),
]