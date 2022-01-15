from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def test(request):
    print(request.POST)
    return HttpResponse(request)