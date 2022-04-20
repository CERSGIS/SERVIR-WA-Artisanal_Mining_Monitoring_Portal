from django.urls import path, include
from .views import *

urlpatterns = [
	path("", root_view, name="rootView"),
	path("about/", about_view, name="aboutView"),
]


