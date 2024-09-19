from django.urls import path
from .views import home, admin_login, admin_museums, edit_museum, delete_museum, add_museum, logout_view, museums, exhibit, us

urlpatterns = [
    path('', view = home, name = 'home'),
    path('admin_login', view = admin_login),
    path('admin_museums', view = admin_museums, name = 'admin_museums'),
    path('edit_museum', view = edit_museum, name = 'edit_museum'),
    path('delete_museum', view = delete_museum, name = 'delete_museum'),
    path('add_museum', view = add_museum, name = 'add_museum'),
    path('logout_view', view = logout_view, name = 'logout_view'),
    path('museums', view = museums, name = 'museums'),
    path('exhibit/<int:id>', view = exhibit, name = 'exhibit'),
    path('us', view = us, name = 'us')
]