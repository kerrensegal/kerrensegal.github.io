from django.shortcuts import render
from . import util
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from markdown2 import Markdown
from random import randint


class NewEntryForm(forms.Form):
    title = forms.CharField(label="Page Title")
    textarea = forms.CharField(widget=forms.Textarea, label="Page Content")

def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})

def entry(request, title):
    
    # Check if requested entry title exists
    if title not in util.list_entries():
        return render(request, "encyclopedia/error.html")
    
    # Render the entry's page content
    page = util.get_entry(title)
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "page": Markdown().convert(page)
    })

def search(request):
    
    # Gets user's search query
    query = request.GET.get("q", "")

    # Gets list of all existing entries
    entries = util.list_entries()

    # Establish a list for potential matches
    entry_list = []

    # Compares each entry to the search query
    for entry in entries:
        
        # Checks for an exact match
        if query.lower() == entry.lower():
            return HttpResponseRedirect(reverse("entry", args=(entry,)))
        
        # Checks for any matching substrings
        elif query.lower() in entry.lower():
            entry_list.append(entry)

    return render(request, "encyclopedia/search.html", {
        "title": query,
        "entry_list": entry_list
    })

def new(request):
    
    # Route reached via POST
    if request.method == "POST":
        
        # Form to submit a new entry
        form = NewEntryForm(request.POST)

        # Checks if form is valid
        if form.is_valid():
            
            # Form includes a title and text for the new entry
            title = form.cleaned_data["title"]
            textarea = form.cleaned_data["textarea"]

            # Checks whether entry title already exists
            if title.lower() in [entry.lower() for entry in util.list_entries()]:
                messages.add_message(request, messages.WARNING, message=f'"{title}" already exists.')

            else:

                # Creates new file for the submitted entry
                with open(f"entries/{title}.md", "w") as file:
                    file.write(textarea)

                # Redirects user to the new entry's page
                return HttpResponseRedirect(reverse("entry", args=(title,)))
        
        # If form is invalid
        else:
            return render(request, "encyclopedia/new.html", {"form": form})

    # Route reached via GET
    return render(request, "encyclopedia/new.html", {"form": NewEntryForm()})
    
def edit(request, title):

    # Route reached via POST
    if request.method == "POST":

        # Form to submit entry
        form = NewEntryForm(request.POST)

        # Checks if form is valid
        if form.is_valid():

            # Form includes a title and text for the entry
            title = form.cleaned_data["title"]
            textarea = form.cleaned_data["textarea"]

            # Saves entry
            util.save_entry(title=title, content=textarea)

            # Redirects user to the entry's page
            return HttpResponseRedirect(reverse("entry", args=(title,)))
        
    # Route reached via GET
    textarea = util.get_entry(title)
    form = NewEntryForm({"title": title, "textarea": textarea})
    return render(request, "encyclopedia/edit.html", {
        "form": form,
        "title": title
    })

def random(request):
    
    # Get list of all entries
    entries = util.list_entries()

    # Randomly select an entry
    random = randint(0, len(entries) - 1)
    title = entries[random]
    page = util.get_entry(title)

    # Direct user to selected random entry's page
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "page": Markdown().convert(page)
    })