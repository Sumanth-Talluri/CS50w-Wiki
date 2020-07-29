from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
import random
from markdown2 import Markdown
from . import util


markdowner = Markdown()


# to create form in search in layout
class SearchForm(forms.Form):
    query = forms.CharField(max_length=100)


# to create form to create new pages
class CreateForm(forms.Form):
    title = forms.CharField(label="Add Title")
    body = forms.CharField(label="Add Body", widget=forms.Textarea(
        attrs={'rows': 1, 'cols': 10}))


# to create form to edit pages
class EditForm(forms.Form):
    title = forms.CharField(label="Edit Title")
    body = forms.CharField(label="Edit Body", widget=forms.Textarea(
        attrs={'rows': 1, 'cols': 10}))


# default view
def index(request):
    form = SearchForm()
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(), "form": form
    })


# view to show the particular page
def entry(request, title):
    # checking if particular page is present or not
    flag = util.get_entry(title)
    if flag is None:
        form = SearchForm()
        # showing the error page
        content = "The page you requested is not available."
        return render(request, "encyclopedia/error.html", {"form": form, "content": content})
    else:
        form = SearchForm()
        mdcontent = util.get_entry(title)
        # converting the Markdown content into HTML
        htmlcontent = markdowner.convert(mdcontent)
        return render(request, "encyclopedia/entry.html", {
            "title": title, "content": htmlcontent, "form": form
        })


# view to show the page user searches for or the list of results
def search(request):
    # if user is searching for a page
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data.get("query")
            present = False
            for entry in util.list_entries():
                if data == entry:
                    mdcontent = util.get_entry(data)
                    htmlcontent = markdowner.convert(mdcontent)
                    present = True
                    break
            # if the page user searched for is present then that is displayed
            if present:
                return render(request, "encyclopedia/entry.html", {"content": htmlcontent, "form": form, "title": data})
            # if it is not present then the substrings are checked
            else:
                lst = []
                for entry in util.list_entries():
                    if data in entry:
                        lst.append(entry)
                # if there are no pages with that substring then error page is shown
                if len(lst) == 0:
                    form = SearchForm()
                    content = "The page you requested for is not available"
                    return render(request, "encyclopedia/error.html", {'form': form, "content": content})
                # if there are pages with that substring then they are listed
                else:
                    return render(request, "encyclopedia/index.html", {"entries": lst, "form": form})
    # if user searches for this page manually error is shown
    else:
        form = SearchForm()
        content = "Search for some page in order to see the result"
        return render(request, "encyclopedia/error.html", {'form': form, "content": content})


# view to create new pages in the encyclopedia
def create(request):
    if request.method == "POST":
        createform = CreateForm(request.POST)
        if createform.is_valid():
            title = createform.cleaned_data.get("title")
            body = createform.cleaned_data.get("body")
            present = False
            for entry in util.list_entries():
                if title == entry:
                    present = True
                    break
            # checking if the page is already in the encyclopedia or not
            if present:
                content = "This Page is Already Present"
                form = SearchForm()
                return render(request, "encyclopedia/error.html", {'form': form, "content": content})
            # if it is not present then the page is created
            else:
                util.save_entry(title, body)
                form = SearchForm()
                mdcontent = util.get_entry(title)
                htmlcontent = markdowner.convert(mdcontent)
                return render(request, "encyclopedia/entry.html", {
                    "title": title, "content": htmlcontent, "form": form
                })
    # if request medthod is GET
    else:
        form = SearchForm()
        createform = CreateForm()
        return render(request, "encyclopedia/create.html", {"form": form, "createform": createform})


# view to edit the particular page in the encyclopedia
def edit(request, title):
    if request.method == "POST":
        editform = EditForm(request.POST)
        if editform.is_valid():
            title = editform.cleaned_data.get("title")
            body = editform.cleaned_data.get("body")
            # saving the new content
            util.save_entry(title, body)
            form = SearchForm()
            htmlcontent = markdowner.convert(body)
            return render(request, "encyclopedia/entry.html", {
                "title": title, "content": htmlcontent, "form": form
            })
    else:
        form = SearchForm()
        editform = EditForm({"title": title, "body": util.get_entry(title)})
        return render(request, "encyclopedia/edit.html", {"form": form, "editform": editform})


# view to display random page in the encyclopedia
def randoms(request):
    entries = util.list_entries()
    num = len(entries)
    # generating a random number for the entry
    entry = random.randint(0, num-1)
    title = entries[entry]
    mdcontent = util.get_entry(title)
    htmlcontent = markdowner.convert(mdcontent)
    form = SearchForm()
    return render(request, "encyclopedia/randoms.html", {"form": form, "title": title, "content": htmlcontent})
