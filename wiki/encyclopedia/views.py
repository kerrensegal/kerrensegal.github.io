from django.shortcuts import render
from . import util
from django import forms, redirect
from django.contrib import messages
from markdown2 import Markdown
from random import randint


class NewEntryForm(forms.Form):
    title = forms.CharField(label="New Entry")
    textarea = forms.CharField(label="Text")

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

# def search(request):
#     query = request.GET.get("q", "")

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
                return redirect("entry", title)    
        
        # If form is invalid
        else:
            return render(request, "encyclopedia/new.html", {"form": form})

    # Route reached via GET
    return render(request, "encyclopedia/new.html", {"form": NewEntryForm()}) 
    
def edit(request, entry):

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
            util.save_entry(title=title, textarea=textarea)

            # Redirects user to the entry's page
            return redirect("entry", title)
        
    # Route reached via GET
    title = entry
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
    entry = entries[randint(0, len(entries) - 1)]

    # Redirect user to selected random entry's page
    return redirect("entry", entry)