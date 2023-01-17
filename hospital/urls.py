from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index_view, name="index"),
    path('register', views.register_view, name="register"),
    path('login', views.login_view, name="login"),
    path('logout', views.logout_view, name="logout"),
    path('patient/<int:id>', views.patient_homepage_view, name="patient"),
    path('doctor', views.doctor_homepage_view, name="doctor"), 
    path('edit/<int:id>', views.edit_view, name="edit")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)