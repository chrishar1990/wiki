from django import forms
from django.http import HttpResponse
from django.shortcuts import render

from . import util

#tasks_list  = []

class NewTaskForm(forms.Form):
    task = forms.CharField(label="Title")
    content_text_area = forms.CharField(
        label="Content", 
        widget=forms.Textarea(attrs={'rows': 10, 'cols': 10
        ,'class': 'my-textarea' }),)
    

def index(request):
    
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

tasks_list = []



def create_page(request):
    print("View function is running!")  # Debugging: Confirm the view is being called
    allEntries = util.list_entries()
    entryExist = False
    for entry in allEntries:
        print(entry.upper())
    


    if request.method == "POST":
        
        print("Form submitted!")  # Debugging: Confirm the form is being submitted
        form = NewTaskForm(request.POST)
        
        #entryExist = False

        if form.is_valid():
            
            print("Form is valid!")  # Debugging: Confirm the form is valid
            task_title = form.cleaned_data["task"]
            task_content = form.cleaned_data["content_text_area"]
            tasks_list.append({"title": task_title, "content": task_content})
            print(f"Task added: {task_title}  \n Content added:  {task_content}")  # Debugging: Confirm the task is added
            # Redirect or perform some other action
            for entry in allEntries:
                if task_title.upper() == entry.upper():
                    entryExist = True
                    
            
            if(entryExist == False):
                util.save_entry(task_title, task_content)
            else:
                print("Entry already EXIST!!!")
            
        else:
            print("Form is invalid!")  # Debugging: Confirm the form is invalid
            return render(request, "encyclopedia/create_page.html", {
                "form": form
            })
    
    return render(request, "encyclopedia/create_page.html", {
        "form": NewTaskForm(),
        "entry": util.list_entries(),
        "entryExist": entryExist
        
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
    #title = request.POST['searched']
    title = request.POST.get('searched', '').strip()

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
            "results" : results
            })
    else:
        
        print("we got there!!!!")
        return render(request, "encyclopedia/search_entries.html", {
            
            
            })
        

def error(request, title):
    return render(request, "encyclopedia/error.html", {
        "title": title,
        
        
    })


    