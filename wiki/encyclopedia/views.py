from django.http import HttpResponse
from django.shortcuts import render

from . import util


def index(request):
    
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_page(request, title):
    print("What I typed: " + title)  
    entry = util.get_entry(title)
    
    if entry == None:
        
        entry = util.get_entry(title.upper())
        if entry == None:
            return error(request, title)
        else:
            return render(request, "encyclopedia/entry_page.html",{
             "entry": entry,
              "title": title
        })
        
       
    else:
        return render(request, "encyclopedia/entry_page.html",{
             "entry": entry,
              "title": title
        })
    

def error(request, title):
    return render(request, "encyclopedia/error.html", {
        "title": title
        
    })