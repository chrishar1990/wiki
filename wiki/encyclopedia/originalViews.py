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
    print(entry)
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
    

def search_entries(request):
    #print(request.method)
    title = request.POST['searched']
    entries = util.list_entries()
    query = title
    results = [entry for entry in entries if query.lower() in entry.lower()]
    print("It is below:")
    if results != []:
        print(results)
    else:
        print("empty")
    if request.method == "POST":
        
        #print(searched + "\tThe entry below: ")
        entry = util.get_entry(title)
        if entry is not None:
            return render(request, "encyclopedia/entry_page.html",{
             "entry": entry,
              "title": title
            })

        if entry == None:
            entry = util.get_entry(title.upper())
            if entry is not None:
                return render(request, "encyclopedia/entry_page.html",{
                "entry": entry,
                "title": title
                })
            
        if entry == None:
            entry = util.get_entry(title.capitalize())
            #print(title.capitalize())
            #print(entry)
            if entry is not None:
                return render(request, "encyclopedia/entry_page.html",{
                "entry": entry,
                "title": title,
                "results": results,

                })
        return render(request, "encyclopedia/search_entries.html", {
            "title": title,
            
            })
    else:
        
        print("we got there!!!!")
        return render(request, "encyclopedia/search_entries.html", {
            
            
            })
        

def error(request, title):
    return render(request, "encyclopedia/error.html", {
        "title": title,
        
        
    })


    