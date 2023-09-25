from django.shortcuts import render
from . import util
from django import forms
from markdown2 import Markdown


class NewEntryForm(forms.Form):

def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})

def entry(request, title):
    
    # Check if requested entry title exists
    if title not in util.list_entries():
        return render("error.html")
    
    # Render the entry's page content
    page = util.get_entry(title)
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "page": Markdown().convert(page)
    })

def search(request):
#     query = request.GET.get("q", "")

def new(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html", {"form": NewEntryForm()})
    
    # ******* FINISH WRITING CODE *************
    
def edit(request, title):
    # ******* FINISH WRITING CODE *************

def random(request):
    # ******* FINISH WRITING CODE *************