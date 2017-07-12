from django.conf.urls import url, include
from onisite.plugins.featured_content import views

urlpatterns = [
  url('', views.featured, name="featured_home")
]
