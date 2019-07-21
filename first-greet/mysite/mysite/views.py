from django.shortcuts import render

def index(request):
    username = request.session.get("name", "游客")
    return render(request, "default/index.html",{"username":username})