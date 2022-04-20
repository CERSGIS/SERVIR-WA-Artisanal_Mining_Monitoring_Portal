from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from djgeojson.views import GeoJSONLayerView
from .models import *
from django.contrib.auth import authenticate
# Create your views here.
# def login_view(request):
# 	request.session["next"] = request.GET.get("next")
# 	if request.method == "POST":
# 		username = request.POST.get("user", "")
# 		password = request.POST.get("pass", "")
# 		user = authenticate(username=username, password=password)
# 		if user:
# 			login(request, user)
# 			if request.session["next"]:
# 				return redirect(request.session["next"])
# 			else:
# 				return redirect("/backend/")
# 	return render(request, "rootApp/login_form.html", locals())

def root_view(request):
	toHTML  = {}
	return render(request, 'rootApp/index.html', toHTML)


def about_view(request):
	toHTML  = {}
	return render(request, 'rootApp/about.html', toHTML)