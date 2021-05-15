from django.urls import path
from . import views

app_name = "myapp"

urlpatterns = [
    path('', views.index.as_view(), name='index'),
    path('upload/', views.upload.as_view(), name='upload'),
    path('search/', views.search.as_view(), name='search'),
    path('register/', views.register.as_view(), name='register'),
    path('observation/<int:encounter_id>', views.display_observation, name='observation')
]
