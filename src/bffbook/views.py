from django.shortcuts import render
from django.http import HttpResponse


def home_view(request):
    user = request.user
    hello = 'Hello World'
    context = {
        'user':user,
        'hello':hello
    }
    return render(request,'main/home.html',context)
    # return HttpResponse('Hello World!!')
