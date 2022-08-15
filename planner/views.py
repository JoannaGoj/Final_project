from django.shortcuts import render

# Create your views here.


def przyklad(request):
    if request.method == 'GET':
        return render(request, 'przyklad.html')