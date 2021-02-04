from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django import forms
from django.urls import reverse
from markdown2 import Markdown
import random

from . import util

class NewQueryForm(forms.Form):
    query = forms.CharField(label='query')


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def wiki(request, entry):
    if entry not in util.list_entries():
        return render(request, 
        "encyclopedia/wiki.html", 
        {"title": "Not found", "content": "Requested entry was not found"})
    content = util.get_entry(entry)
    return render(
        request, 
        "encyclopedia/wiki.html", 
        {"title": entry, "content": Markdown().convert(content)})


def search(request):
    query = request.POST['q']
    pages = util.list_entries()
    match = [page for page in pages if query.lower() == page.lower()]
    submatch = [page for page in pages if query.lower() in page.lower()]
    nomatch = "No results"  
    if len(match) == 1:
        return HttpResponseRedirect(reverse('wiki', args=(match[0],))) 
    elif len(submatch) > 0:
        return render(request, "encyclopedia/search.html", {"results": submatch})
    else:
        return render(request, "encyclopedia/search.html", {"title": nomatch}) 
    
def randompage(request):
    random_page = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse('wiki', args=(random_page,))) 

def new_page(request):
    return render(request, "encyclopedia/newpage.html")

def savepage(request):
    title = request.POST.get("title")
    details = request.POST.get("details")
    duplicate = "This entry already exists - new entry not possible but you can edit the existing one"
    if util.get_entry(title):
        return render(request, "encyclopedia/search.html", {"title": duplicate})
    else:
        util.save_entry(title,details)
        return HttpResponseRedirect(reverse('wiki', args=(title,))) 
