from django.urls import path

from .views import home, services, projects

urlpatterns = [

    path("", home, name="home"),

    path("services/", services, name="services"),

    path("projects/", projects, name="projects"),

]