from django.shortcuts import render

# Create your views here.

def about(request):
    return render(request,'pages/about.html')

def contact(request):
    return render(request,'pages/contact.html')

def faith(request):
    return render(request,'pages/faith.html')

def team(request):
    return render(request,'pages/team.html')

def partners(request):
    return render(request,'pages/partners.html')

def giving(request):
    return render(request,'pages/giving.html')

def schedule(request):
    return render(request,'pages/schedule.html')




