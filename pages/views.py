from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'pages/index.html')

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

def newsletter(request):
    return render(request,'pages/newsletter.html')

def activities(request):
    return render(request,'pages/activities.html')

def schedule(request):
    return render(request,'pages/schedule.html')

def worship(request):
    return render(request,'pages/worship.html') 

def fellowship(request):
    return render(request,'pages/fellowship.html')
