from django.urls import path, include
from .views import *


app_name = 'landingpage'
urlpatterns = [
	path("", indexViews, name="rootView"),

]

