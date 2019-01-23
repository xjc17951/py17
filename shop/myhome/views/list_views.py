from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def myhome_list(request):
    return render(request,'myhome/list.html')