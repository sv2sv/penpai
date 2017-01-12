from django.shortcuts import render
from django.http import HttpResponse
from data_gain import DataGain
# Create your views here.


def categories(request):
    data = DataGain()
    return HttpResponse(data.get_allcategory())


def details(request, link):
    data = DataGain()
    index = request.GET['index']
    return HttpResponse(data.get_datas(link, index))
