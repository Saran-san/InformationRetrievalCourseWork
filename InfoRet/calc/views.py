from django.shortcuts import render
from django.http import HttpResponse
from . import Indexer
from . import Scheduler
# Create your views here.

indexer = Indexer.Indexer()
indexer.LoadIndexedState()

#scheduler = Scheduler.Scheduler(indexer)
#scheduler.start()

def home(request):
    return render(request, 'base.html')

def search(request):
    val = request.GET['searchTerms']
    indexer.Search(val)

    return render(request, 'result2.html')