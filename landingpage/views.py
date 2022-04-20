from django.shortcuts import render

# Create your views here.
def indexViews(request):
	toHTML = {}
	return render(request, 'index.html', toHTML)