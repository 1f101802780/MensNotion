from django.shortcuts import render

# Create your views here.
def top(request):
    return render(request, 'groomings/top.html')

def login(request):
    return render(request, 'groomings/login.html')
