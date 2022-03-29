from django.urls import include, path, re_path
from onisite.plugins.featured_content import views

urlpatterns = [
  path('', views.featured, name="featured_home")
]
